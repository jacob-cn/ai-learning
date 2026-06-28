import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"

# ─────────────────────────────────────────
# 1. DEFINE THE ACTUAL FUNCTIONS
#    These do the real work on your system
# ─────────────────────────────────────────

def read_file(path: str) -> str:
    """Read and return the contents of a file."""
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File '{path}' not found."
    except Exception as e:
        return f"Error reading file: {str(e)}"

def list_files(directory: str) -> str:
    """List all files in a directory."""
    try:
        files = []
        for root, dirs, filenames in os.walk(directory):
            # Skip hidden folders like .git, venv
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            for filename in filenames:
                files.append(os.path.join(root, filename))
        if not files:
            return f"No files found in '{directory}'."
        return "\n".join(files)
    except FileNotFoundError:
        return f"Error: Directory '{directory}' not found."

def search_in_files(directory: str, keyword: str) -> str:
    """Search for a keyword across all files in a directory."""
    try:
        results = []
        for root, dirs, filenames in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            for filename in filenames:
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r") as f:
                        for line_num, line in enumerate(f, 1):
                            if keyword.lower() in line.lower():
                                results.append(f"{filepath}:{line_num}: {line.rstrip()}")
                except Exception:
                    pass  # skip binary files
        if not results:
            return f"No matches found for '{keyword}'."
        return "\n".join(results)
    except FileNotFoundError:
        return f"Error: Directory '{directory}' not found."

# ─────────────────────────────────────────
# 2. TELL THE MODEL WHAT TOOLS EXIST
#    Just a description — name, what it does,
#    and its parameter schema. No code here.
# ─────────────────────────────────────────

TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file at a given path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The file path to read, e.g. './main.py'"}
            },
            "required": ["path"],
        },
    },
    {
        "name": "list_files",
        "description": "List all files in a directory recursively.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "The directory path to list, e.g. './my_project'"}
            },
            "required": ["directory"],
        },
    },
    {
        "name": "search_in_files",
        "description": "Search for a keyword across all files in a directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "The directory to search in"},
                "keyword": {"type": "string", "description": "The keyword to search for"},
            },
            "required": ["directory", "keyword"],
        },
    },
]

# Wrap the declarations once — this is the "menu" handed to the model each request.
tools_config = types.Tool(function_declarations=[types.FunctionDeclaration(**t) for t in TOOLS])

# ─────────────────────────────────────────
# 3. THE TOOL EXECUTION ROUTER
#    Maps tool name → actual function call
# ─────────────────────────────────────────

def execute_tool(tool_name: str, tool_args: dict) -> str:
    """Execute the requested tool and return the result."""
    print(f"\n  🔧 Executing tool: {tool_name}({tool_args})")

    if tool_name == "read_file":
        return read_file(**tool_args)
    elif tool_name == "list_files":
        return list_files(**tool_args)
    elif tool_name == "search_in_files":
        return search_in_files(**tool_args)
    else:
        return f"Unknown tool: {tool_name}"

# ─────────────────────────────────────────
# 4. THE AGENT LOOP
#    Keeps calling the model until it stops
#    requesting tools and gives a final answer
# ─────────────────────────────────────────

SYSTEM_PROMPT = """You are a helpful AI dev assistant.
You have tools to read files, list directories, and search code.
Use them whenever the user asks about files or code on their system."""

def chat_with_tools(user_message: str) -> str:
    """Send a message and handle any tool calls in a loop."""

    contents = [types.Content(role="user", parts=[types.Part(text=user_message)])]

    while True:
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[tools_config],
            ),
        )

        candidate = response.candidates[0]

        # Split the reply into tool calls vs. plain text
        function_calls = []
        text_parts = []
        for part in candidate.content.parts:
            if part.function_call:
                function_calls.append(part.function_call)
            elif part.text:
                text_parts.append(part.text)

        # No tool calls = final answer, we're done
        if not function_calls:
            return "\n".join(text_parts)

        # Add the model's turn (the tool requests) to history
        contents.append(candidate.content)

        # Execute each tool and feed the structured results back
        tool_response_parts = []
        for fc in function_calls:
            result = execute_tool(fc.name, dict(fc.args))
            tool_response_parts.append(
                types.Part(
                    function_response=types.FunctionResponse(
                        name=fc.name, response={"result": result}
                    )
                )
            )

        contents.append(types.Content(role="user", parts=tool_response_parts))

# ─────────────────────────────────────────
# 5. MAIN CHAT LOOP
# ─────────────────────────────────────────

def main():
    print("🤖 AI Dev Assistant (with tools!)")
    print("Try: 'list files in .' or 'read the file dev_assistant.py'")
    print("Type 'quit' to exit\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        if not user_input:
            continue

        print("\n⏳ Thinking...\n")
        response = chat_with_tools(user_input)
        print(f"Assistant: {response}\n")

if __name__ == "__main__":
    main()
