import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"
SYSTEM_PROMPT = "You are a helpful assistant for a developer learning AI development."

# The model API is stateless. This list is our transcript memory.
# On turn 1, everything sent is new. On turn 2+, older messages are re-sent
# so the model can keep conversational context.
history: list[types.Content] = []


def print_history():
    """Show exactly what gets sent each turn (new + previously sent messages)."""
    print("\n--- full conversation sent each turn (turn 2+ includes re-sent history) ---")
    for i, msg in enumerate(history, 1):
        print(f"  {i}. [{msg.role}] {msg.parts[0].text}")
    print("--- end (all of the above goes in the next request) ---\n")


def main():
    print("🤖 Multi-turn chatbot — the model has no memory; this script does.")
    print("Type 'history' to see everything sent each turn, 'quit' to exit.\n")

    turn = 0
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if not user_input:
            continue
        if user_input.lower() == "history":
            print_history()
            continue

        turn += 1

        # 1. add your message to the running history
        history.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
        messages_sent_this_turn = len(history)
        previously_sent_messages = max(messages_sent_this_turn - 1, 0)

        # 2. send the ENTIRE history every call.
        #    On turn 1 this is all new; on later turns, prior messages are re-sent.
        response = client.models.generate_content(
            model=MODEL,
            contents=history,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )

        # 3. append the reply so the next turn remembers it too
        history.append(types.Content(role="model", parts=[types.Part(text=response.text)]))

        # show the multi-turn mechanics: re-sent context grows every turn
        usage = response.usage_metadata
        print(f"\nGemini: {response.text}")
        print(
            f"  ↳ turn {turn}: sent {messages_sent_this_turn} message(s) "
            f"(1 new, {previously_sent_messages} previously sent) = "
            f"{usage.prompt_token_count} tokens of context in, "
            f"{usage.candidates_token_count} tokens out\n"
        )


if __name__ == "__main__":
    main()
