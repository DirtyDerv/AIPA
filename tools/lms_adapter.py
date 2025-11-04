#!/usr/bin/env python3
import json, os, sys, urllib.request
from urllib.parse import urljoin

# --- Configuration ---
# Read from environment variables with fallback to detected values
LMS_HOST = os.environ.get('LMS_HOST', '127.0.0.1:1234')
LMS_API_KEY = os.environ.get('LMS_API_KEY', 'dummy-key') # LM Studio ignores this by default

BASE = f'http://{LMS_HOST}'
ENDPOINT = urljoin(BASE, '/v1/chat/completions')
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LMS_API_KEY}"
}

def generate(prompt, max_tokens=512, stream=False):
    """
    Generate text from the local LLM.

    Args:
        prompt (str): The user prompt.
        max_tokens (int): The maximum number of tokens to generate.
        stream (bool): Whether to stream the response.

    Returns:
        If stream=False, returns the complete generated text as a string.
        If stream=True, returns a generator that yields text chunks.
    """
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "stream": stream
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(ENDPOINT, data=data, headers=HEADERS, method='POST')

    try:
        resp = urllib.request.urlopen(req, timeout=180) # Increased timeout to 3 minutes
    except Exception as e:
        print(f"ERROR: Could not connect to LM Studio at {ENDPOINT}", file=sys.stderr)
        print(f"Please ensure LM Studio is running and the server is started.", file=sys.stderr)
        print(f"You can configure the host via the LMS_HOST environment variable.", file=sys.stderr)
        print(f"Error details: {e}", file=sys.stderr)
        return "" # Return empty string on error

    if not stream:
        body = resp.read().decode(errors='replace')
        try:
            data = json.loads(body)
            return data['choices'][0]['message']['content'].strip()
        except (json.JSONDecodeError, KeyError, IndexError):
            return f"Error: Could not parse response: {body}"
    else:
        # Return a generator for streaming
        return _stream_response(resp)

def _stream_response(resp):
    """Helper to parse and yield content from a streaming SSE response."""
    for line_bytes in resp:
        line = line_bytes.decode(errors='replace').strip()
        if line.startswith('data: '):
            data_str = line[len('data: '):]
            if data_str == '[DONE]':
                break
            try:
                chunk = json.loads(data_str)
                delta = chunk.get('choices', [{}])[0].get('delta', {})
                content = delta.get('content')
                if content:
                    yield content
            except (json.JSONDecodeError, KeyError, IndexError):
                continue # Ignore malformed lines

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--stream':
        print("--- Streaming response ---")
        # The generator will yield chunks as they arrive
        full_response = ""
        for chunk in generate('Tell me a short story about a robot who discovers music.', stream=True):
            print(chunk, end='', flush=True)
            full_response += chunk
        print("\n\n--- End of stream ---")
    else:
        print("--- Non-streaming response ---")
        response = generate('Tell me a short story about a robot who discovers music.')
        print(response)
