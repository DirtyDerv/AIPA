#!/usr/bin/env python3
import urllib.request, urllib.error, json, sys
HOST='http://127.0.0.1:1234'
paths=['/api/generate','/generate','/api/textgen','/textgen','/v1/llm/completions','/v1/engines/generate','/v1/engines/text/completions','/v1/complete','/v1/generate','/api/v1/generate']
headers={'Content-Type':'application/json'}
payload=json.dumps({'prompt':'Hello from post-probe','max_tokens':50}).encode('utf-8')
for p in paths:
    url=HOST+p
    req=urllib.request.Request(url,data=payload,headers=headers,method='POST')
    try:
        with urllib.request.urlopen(req,timeout=5) as r:
            body=r.read().decode(errors='replace')
            print(p,'->',r.status)
            print('resp snippet:',body[:400])
    except urllib.error.HTTPError as e:
        try:
            b=e.read().decode(errors='replace')
        except:
            b=''
        print(p,'-> HTTP',e.code,' snippet:',b[:400])
    except Exception as e:
        print(p,'-> ERROR',e)
