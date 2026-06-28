import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Confirm this exact string in AI Studio's model picker for your project —
# Flash-Lite variants consistently have the best RPM/RPD on free tier.
MODEL = "gemma-4-31b-it"

MAX_ROUNDS = 5
MIN_SECONDS_BETWEEN_CALLS = 6     # comfortable gap between calls — adjust once you confirm your real RPM
MAX_RESULT_CHARS = 2000           # caps any single tool result so context doesn't grow unbounded (TPM defense)

WORKDIR = Path(__file__).parent
_last_call_time = [0.0]


def _truncate(text: str, limit: int = MAX_RESULT_CHARS) -> str:
    """Caps a tool result so repeated/large outputs don't blow up token usage per round."""
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n... [truncated, {len(text)} total chars]"


def _paced_generate(**kwargs):
    """Wraps every model call with pacing + visible retry-on-429,
    so we don't need to know the exact RPM/TPM number to stay under it."""
    elapsed = time.time() - _last_call_time[0]
    if elapsed < MIN_SECONDS_BETWEEN_CALLS:
        time.sleep(MIN_SECONDS_BETWEEN_CALLS - elapsed)

    for attempt in range(3):
        try:
            print(f"  📡 Calling {MODEL}... (attempt {attempt + 1})", flush=True)
            response = client.models.generate_content(**kwargs)
            _last_call_time[0] = time.time()
            return response
        except Exception as e:
            print(f"  ❌ Exception: {type(e).__name__}: {e}", flush=True)
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait = 15 * (attempt + 1)
                print(f"  ⏳ Rate limited, waiting {wait}s before retry...", flush=True)
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Failed after 3 retries — likely hit RPD (daily) limit, not RPM.")


# ─────────────────────────────────────────
# TOOLS — same shape as Stage 3, nothing new mechanically
# ─────────────────────────────────────────

def read_file(path: str) -> str:
    try:
        return (WORKDIR / path).read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading {path}: {e}"


def write_file(path: str, content: str) -> str:
    try:
        (WORKDIR / path).write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} chars to {path}"
    except Exception as e:
        return f"Error writing {path}: {e}"


def list_files(directory: str = ".") -> str:
    try:
        files = [str(p.relative_to(WORKDIR)) for p in (WORKDIR / directory).rglob("*.py")]
        return "\n".join(files) if files else "No .py files found."
    except Exception as e:
        return f"Error listing {directory}: {e}"


TOOLS = [
    {
        "name": "read_file",
        "description": "Read the full contents of a file by relative path.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"}}, "required": ["path"]}
    },
    {
        "name": "write_file",
        "description": "Overwrite a file with new content. Use this to apply code changes.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"},
            "content": {"type": "string", "description": "The FULL new file content"}},
            "required": ["path", "content"]}
    },
    {
        "name": "list_files",
        "description": "List all .py files in a directory, recursively.",
        "parameters": {"type": "object", "properties": {
            "directory": {"type": "string"}}, "required": []}
    },
]


def execute_tool(name: str, args: dict) -> str:
    print(f"  🔧 {name}({args})")
    if name == "read_file":
        return read_file(**args)
    if name == "write_file":
        return write_file(**args)
    if name == "list_files":
        return list_files(**args)
    return f"Unknown tool: {name}"


# ─────────────────────────────────────────
# THE REACT LOOP — Stage 3's loop + explicit reasoning + loop-guard
# ─────────────────────────────────────────

AGENT_SYSTEM_PROMPT = """You are an autonomous coding agent working in a small Python project.

MISSION: Complete the user's goal by reading and editing files using your tools.
You work without human approval between steps — act decisively.

You are running under a TIGHT rate limit. Be efficient: do not re-read a file
you already have the contents of in this conversation. Aim to finish in as
few tool calls as possible.

PROCESS — before every tool call, briefly state your reasoning (one sentence),
prefixed with "Thought:". This is for the human reading the trace, not for the user.

ALWAYS:
- Read a file before editing it — never guess its contents
- Make the smallest change that satisfies the goal
- When you believe you're done, call no more tools and instead write a FINAL REPORT

NEVER:
- Edit a file you haven't read in this session
- Re-read a file you already read this session
- Call the exact same tool with the exact same arguments twice
- Claim success without having actually called write_file
"""

VERIFIER_SYSTEM_PROMPT = """You are a skeptical code reviewer. You did NOT write this code.
You will be shown a goal and the current file contents.
Your only job: does the file actually satisfy the goal? Be strict — do not give credit
for effort or partial attempts. Respond in this exact format:

VERDICT: PASS or FAIL
REASON: one sentence
"""


def run_agent(goal: str):
    print(f"\n🎯 GOAL: {goal}\n")

    contents = [types.Content(role="user", parts=[types.Part(text=goal)])]
    tools_config = types.Tool(function_declarations=[
        types.FunctionDeclaration(**t) for t in TOOLS
    ])

    touched_files = set()
    seen_calls = set()  # tracks (tool_name, args_json) pairs already tried this run

    for round_num in range(1, MAX_ROUNDS + 1):
        response = _paced_generate(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=AGENT_SYSTEM_PROMPT,
                tools=[tools_config],
            ),
        )

        candidate = response.candidates[0]
        function_calls = []
        text_parts = []

        for part in candidate.content.parts:
            if part.function_call:
                function_calls.append(part.function_call)
            elif part.text:
                text_parts.append(part.text)
                print(part.text.strip())

        if not function_calls:
            print(f"\n✅ Agent finished after {round_num} round(s).\n")
            return touched_files

        contents.append(candidate.content)

        tool_response_parts = []
        for fc in function_calls:
            args = dict(fc.args)
            call_signature = (fc.name, json.dumps(args, sort_keys=True))

            if call_signature in seen_calls:
                # Same tool, same args, again — don't burn tokens repeating it,
                # tell the model directly so it's forced to change approach.
                result = "You already called this exact tool with these exact arguments. Try something different or finish."
                print(f"  🔁 Blocked repeat: {fc.name}({args})")
            else:
                seen_calls.add(call_signature)
                if fc.name == "write_file":
                    touched_files.add(args.get("path"))
                result = execute_tool(fc.name, args)
                result = _truncate(result)

            tool_response_parts.append(types.Part(
                function_response=types.FunctionResponse(name=fc.name, response={"result": result})
            ))

        contents.append(types.Content(role="user", parts=tool_response_parts))

    print(f"\n⚠️  Hit MAX_ROUNDS ({MAX_ROUNDS}) without finishing. Stopping.\n")
    return touched_files


# ─────────────────────────────────────────
# THE VERIFIER — a SEPARATE call, grading the actual file
# (the generator/verifier split, applied at the harness level)
# ─────────────────────────────────────────

def verify(goal: str, touched_files: set):
    if not touched_files:
        print("🔍 VERIFY: no files were changed — nothing to verify.")
        return

    for path in touched_files:
        content = read_file(path)
        content = _truncate(content, limit=4000)  # verifier needs more context than a mid-loop tool result
        prompt = f"GOAL: {goal}\n\nFILE ({path}):\n{content}"

        response = _paced_generate(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=VERIFIER_SYSTEM_PROMPT),
        )
        print(f"\n🔍 VERIFY ({path}):\n{response.text.strip()}\n")


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

if __name__ == "__main__":
    goal = input("What should the agent do?\n> ").strip()
    touched = run_agent(goal)
    verify(goal, touched)