#!/usr/bin/env python3
"""Local LLM probe and minimal client for LM Studio-like/OpenAI-compatible local servers.

Usage:
  python tools/local_llm_client.py --probe
  python tools/local_llm_client.py --test "Hello"  # sends a small chat completion test

Behavior:
- Tries a set of common localhost:port combinations and OpenAI-compatible paths
- Prints any endpoints that respond and whether a simple chat completion succeeded

Assumptions:
- The local LLM exposes an OpenAI-compatible REST API (e.g. /v1/models, /v1/chat/completions)
- If not, the probe will still show which host:port responded and the returned content

"""
import argparse
import json
import sys
import urllib.request
import urllib.error
from urllib.parse import urljoin

COMMON_HOSTS = [
    ("127.0.0.1", 11434),  # LM Studio default in many installs
    ("127.0.0.1", 8000),
    ("127.0.0.1", 8080),
    ("127.0.0.1", 5000),
    ("localhost", 11434),
]

PATHS = ["/", "/v1/models", "/v1/chat/completions", "/v1/completions", "/health", "/api/status"]

TIMEOUT = 3


def try_get(url):
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = resp.read().decode(errors="replace")
            return resp.getcode(), data
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode(errors="replace")
        except Exception:
            body = ""
        return e.code, body
    except Exception as e:
        return None, str(e)


def try_post_json(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode(errors="replace")
            return resp.getcode(), body
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode(errors="replace")
        except Exception:
            body = ""
        return e.code, body
    except Exception as e:
        return None, str(e)


def probe_all():
    findings = []
    for host, port in COMMON_HOSTS:
        base = f"http://{host}:{port}"
        for path in PATHS:
            url = urljoin(base, path)
            code, body = try_get(url)
            findings.append({"url": url, "code": code, "body_snippet": body[:800]})
    return findings


def test_chat(url, prompt="Hello from probe", model=None):
    # Try OpenAI-style chat completion first
    payload = {
        "model": model or "gpt-4o-mini" ,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 64
    }
    code, body = try_post_json(url, payload)
    return code, body


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--probe', action='store_true', help='Probe common local endpoints')
    parser.add_argument('--host', type=str, help='Probe a specific host:port, e.g. 127.0.0.1:41343')
    parser.add_argument('--test', type=str, help='Send a small test prompt (chat)')
    parser.add_argument('--endpoint', type=str, help='Explicit endpoint URL to use for test POST (e.g. http://127.0.0.1:11434/v1/chat/completions)')
    parser.add_argument('--model', type=str, help='Model name to include in test payload (optional)')
    args = parser.parse_args()

    if args.probe:
        if args.host:
            # probe a single host:port
            parts = args.host.split(':')
            host = parts[0]
            port = int(parts[1]) if len(parts) > 1 else 11434
            print(f'Probing {host}:{port} (timeout {TIMEOUT}s)')
            results = []
            base = f'http://{host}:{port}'
            for path in PATHS:
                url = urljoin(base, path)
                code, body = try_get(url)
                results.append({"url": url, "code": code, "body_snippet": body[:800]})
        else:
            print('Probing common local endpoints (timeout %ds)...' % TIMEOUT)
            results = probe_all()
        for r in results:
            url = r['url']
            code = r['code']
            snippet = r['body_snippet']
            if code is None:
                print(f"- {url} -> no response ({snippet})")
            else:
                print(f"- {url} -> HTTP {code}")
                if snippet:
                    print('   snippet:', repr(snippet[:200]))
        sys.exit(0)

    if args.test:
        endpoint = args.endpoint or 'http://127.0.0.1:11434/v1/chat/completions'
        print(f'Sending test chat to {endpoint} ...')
        code, body = test_chat(endpoint, prompt=args.test, model=args.model)
        if code is None:
            print('No response:', body)
            sys.exit(2)
        print('HTTP', code)
        try:
            parsed = json.loads(body)
            print(json.dumps(parsed, indent=2)[:4000])
        except Exception:
            print('Body (raw):', body[:2000])
        sys.exit(0)

    parser.print_help()
