import requests
import json

N8N_URL = 'http://192.168.0.14:5678'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk'

headers = {
    'X-N8N-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}

def list_workflows():
    response = requests.get(f'{N8N_URL}/api/v1/workflows', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        print(f'Error listing workflows: {response.status_code}')
        print(response.text)
        return []

workflows = list_workflows()
for workflow in workflows:
    print(f"- {workflow['name']} (ID: {workflow['id']})")
