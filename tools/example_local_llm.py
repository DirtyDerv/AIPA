# Add project root to path to allow imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.lms_adapter import generate

# Simple non-streaming call
print("--- Generating a simple response ---")
response = generate("What are the core principles of good software design?")
print(response)

# Streaming call
print("\n--- Streaming a story ---")
for chunk in generate("Tell me a short story about a curious robot.", stream=True):
    print(chunk, end='', flush=True)
print()
