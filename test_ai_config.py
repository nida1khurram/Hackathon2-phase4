# Test script to verify the AI configuration is working properly
import os
import sys
sys.path.insert(0, './backend/src')

from config.ai_config import AIConfig

print("AI Configuration Test:")
print("="*50)

# Check what API keys are available in the environment
openai_key = os.environ.get("OPENAI_API_KEY")
openrouter_key = os.environ.get("OPENROUTER_API_KEY")

print(f"OPENAI_API_KEY in environment: {'Yes' if openai_key else 'No'}")
print(f"OPENROUTER_API_KEY in environment: {'Yes' if openrouter_key else 'No'}")

try:
    model = AIConfig.get_default_model()
    print(f"Default model: {model}")
    
    print("\nConfiguration is set up correctly!")
    print("However, you'll need to provide an API key to use the chatbot functionality.")
    print("\nTo use the chatbot, you need to set one of these environment variables:")
    print("- OPENAI_API_KEY for OpenAI API")
    print("- OPENROUTER_API_KEY for OpenRouter API (recommended)")
    
except ValueError as e:
    print(f"Configuration error: {e}")
    print("You need to set an API key to use the chatbot functionality.")