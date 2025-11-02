from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

def main():
    # Choose the best model for conversation
    model = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0.7)

    print("Welcome! I am your Gemini AI assistant 🤖")
    print("Ask me anything about technology, science, history, or just chat! (type 'quit' to exit)\n")

    chat_history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            print("Goodbye! 👋")
            break

        # Add user message to chat history
        chat_history.append(HumanMessage(content=user_input))

        try:
            # Send message to Gemini and get a response
            response = model.invoke(chat_history)

            print("Assistant:", response.content, "\n")

            # Add AI response to history for context
            chat_history.append(AIMessage(content=response.content))

        except Exception as e:
            print("⚠️ Error:", e)
            break

if __name__ == "__main__":
    main()
