import requests
import json

N8N_URL = 'http://192.168.0.14:5678'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3Yjk0YTFiYi1lMmMyLTQwZjYtOWQyNC1mYTIwYzViYjI0YjgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMTc2OTg5fQ.LPgyCH9sjlzzNN4iiPbKipMMCw3s6e_jCSgrB2Oh5uk'

headers = {
    'X-N8N-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}

workflows_to_delete = [
    '0X7Pg20PAMUIxKkN',
    '2Cv3OB0mWUnAxOlU',
    'Dp8tNzPnjbyV34k1',
    'FKmSWEM4bAuzxzhm',
    'HDKcZ8fEROLeXtEk',
    'RGJxonmQCdvsKSjQ',
    'RMxcBtviEl6rn2aG',
    'RhI5jTRG89fyE1OZ',
    'TSxfN9RUlgdpcaqZ',
    'WvKPDxADQ3yhoknh',
    'agW8NfkEsWybn2Nh',
    'emQRykXTvI6IYU8A',
    'fJB2NokUjyj6Fpbm',
    'gGn2idMwaBQMZePN',
    'i6ABteIz9IgXUDmb',
    'iZY8gr7pmRfgmDGW',
    'mI3KBhtcDBDH3KT2',
    'te4YBSf8SGNzRB0C',
    'xv2cMGb1dmDPLsLO'
]

def delete_workflow(workflow_id):
    response = requests.delete(f'{N8N_URL}/api/v1/workflows/{workflow_id}', headers=headers)
    if response.status_code == 204:
        print(f'Successfully deleted workflow with ID: {workflow_id}')
        return True
    else:
        print(f'Error deleting workflow with ID {workflow_id}: {response.status_code}')
        print(response.text)
        return False

for workflow_id in workflows_to_delete:
    delete_workflow(workflow_id)
