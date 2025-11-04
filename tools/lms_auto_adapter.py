#!/usr/bin/env python3
"""Auto-detect LM Studio HTTP request shape and provide a tiny wrapper.

Usage:
  python tools/lms_auto_adapter.py --host 127.0.0.1:1234

The script will try multiple endpoints and payload shapes and print any successful combination.
If successful, it will write `tools/lms_adapter.py` with a small `generate()` helper.
"""
import argparse, json, urllib.request, urllib.error, sys, os
from urllib.parse import urljoin

DEFAULT_HOST = "127.0.0.1:1234"
ENDPOINTS = [
    '/api/generate','/generate','/api/textgen','/textgen','/v1/llm/completions',
    '/v1/engines/generate','/v1/engines/text/completions','/v1/complete','/v1/generate',
    '/v1/chat/completions','/v1/completions','/api/v1/generate','/api/generate_stream'
]

PAYLOADS = [
    {"prompt": "{prompt}"},
    {"input": "{prompt}"},
    {"text": "{prompt}"},
    {"instruction": "{prompt}"},
    {"messages": [{"role": "user", "content": "{prompt}"}]},
    {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": "{prompt}"}]},
    {"prompt": "{prompt}", "max_tokens": 128},
]

HEADERS_LIST = [
    {"Content-Type": "application/json"},
]

TIMEOUT = 4


def try_post(url, data_bytes, headers):
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode(errors='replace')
            return resp.getcode(), body
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode(errors='replace')
        except Exception:
            body = ''
        return e.code, body
    except Exception as e:
        return None, str(e)


def looks_like_success(body):
    # Stronger heuristics: must contain one of expected generation keys
    # and must NOT look like an error message from LM Studio
    if not body:
        return False
    low = body.lower()
    # early reject if the server returned a clear error message
    error_markers = ['"error"', 'unexpected endpoint', 'method not allowed', 'cannot get', 'not found']
    for e in error_markers:
        if e in low:
            return False

    success_indicators = ['generated_text', 'generation', 'choices', 'output', 'content', 'text', 'result', 'completion']
    for k in success_indicators:
        if k in low:
            return True
    # fallback: if body is long and doesn't include error markers, consider manual review
    if len(body) > 200:
        return True
    return False


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--host', default=DEFAULT_HOST)
    p.add_argument('--prompt', default='Hello from adapter')
    args = p.parse_args()
    host = args.host
    prompt = args.prompt
    base = f'http://{host}'
    print('Probing', base)

    found = []
    def fill(item):
        # recursively replace {prompt} in strings within dict/list/str
        if isinstance(item, str):
            return item.format(prompt=prompt)
        if isinstance(item, dict):
            return {k: fill(v) for k, v in item.items()}
        if isinstance(item, list):
            return [fill(x) for x in item]
        return item

    for ep in ENDPOINTS:
        url = urljoin(base, ep)
        for payload_t in PAYLOADS:
            try:
                filled = fill(payload_t)
                payload = json.dumps(filled).encode('utf-8')
            except Exception as e:
                print('Error formatting payload', payload_t, e)
                continue
            for headers in HEADERS_LIST:
                code, body = try_post(url, payload, headers)
                print(f'TRY POST {url} with {list(payload_t.keys())} ->', code)
                if code and code < 500 and looks_like_success(body):
                    print('  SUCCESS candidate:', url, payload_t, 'code', code)
                    found.append({'url': url, 'payload': payload_t, 'headers': headers, 'code':code, 'body': body})
                    # stop early on first success for this endpoint
                    break
            if found:
                break
        if found:
            break

    if not found:
        print('\nNo clear success detected. Server responded but did not return an obvious generation body.\n')
        sys.exit(2)

    # Use first found candidate
    candidate = found[0]
    print('\nDetected working endpoint:')
    print('URL:', candidate['url'])
    print('Payload template keys:', list(candidate['payload'].keys()))
    print('Example response snippet:\n', candidate['body'][:1000])

    # write an adapter file
    adapter_code = f"""#!/usr/bin/env python3
import json, urllib.request
from urllib.parse import urljoin

BASE = '{base}'
ENDPOINT = '{candidate['url']}'
HEADERS = {json.dumps(candidate['headers'])}

def generate(prompt, max_tokens=256):
    payload = {json.dumps({k:('"'+v.replace('{prompt}','{prompt}')+'"' if isinstance(v,str) else v) for k,v in candidate['payload'].items()})}
    # replace placeholders
    for k in list(payload.keys()):
        if isinstance(payload[k], str) and '{prompt}' in payload[k]:
            payload[k] = payload[k].replace('{prompt}', prompt)
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(ENDPOINT, data=data, headers=HEADERS, method='POST')
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode(errors='replace')

if __name__ == '__main__':
    print(generate('Hello from lms_adapter'))
"""
    path = os.path.join(os.path.dirname(__file__), 'lms_adapter.py')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(adapter_code)
    print('\nWrote adapter to', path)
    print('You can import tools.lms_adapter.generate(prompt) from your scripts now.')

if __name__ == '__main__':
    main()
