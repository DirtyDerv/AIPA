# n8n API Documentation

## API Configuration

### Base Information
- **n8n Server**: `http://192.168.0.14:5678`
- **API Base URL**: `http://192.168.0.14:5678/api/v1`
- **API Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o`

### Authentication Header
```
X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o
```

## Python Example

```python
import requests

# Configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

# List all workflows
response = requests.get(f"{N8N_URL}/api/v1/workflows", headers=headers)
workflows = response.json()
```

## cURL Example

```bash
# List workflows
curl -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o" \
  http://192.168.0.14:5678/api/v1/workflows

# Get specific workflow
curl -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o" \
  http://192.168.0.14:5678/api/v1/workflows/{workflow_id}

# Activate a workflow
curl -X PATCH \
  -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o" \
  -H "Content-Type: application/json" \
  -d '{"active": true}' \
  http://192.168.0.14:5678/api/v1/workflows/{workflow_id}
```

## Common API Endpoints

### Workflows
- `GET /api/v1/workflows` - List all workflows
- `GET /api/v1/workflows/{id}` - Get specific workflow
- `POST /api/v1/workflows` - Create new workflow
- `PUT /api/v1/workflows/{id}` - Update workflow
- `PATCH /api/v1/workflows/{id}` - Partially update workflow (e.g., activate/deactivate)
- `DELETE /api/v1/workflows/{id}` - Delete workflow

### Executions
- `GET /api/v1/executions` - List workflow executions
- `GET /api/v1/executions/{id}` - Get specific execution

### Credentials
- `GET /api/v1/credentials` - List credentials
- `GET /api/v1/credentials/{id}` - Get specific credential

## Environment Variables

For scripts and applications, you can use environment variables:

```bash
export N8N_URL="http://192.168.0.14:5678"
export N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"
```

## Notes

- The API key is a JWT token that contains user identification
- Keep this API key secure and never commit it to public repositories
- The API key can be regenerated in the n8n UI under Settings > API
- All API requests require the `X-N8N-API-KEY` header
- API responses are in JSON format

## Troubleshooting

### Unauthorized (401)
- Check that your API key is correct
- Ensure the API key hasn't been regenerated
- Verify you're using the `X-N8N-API-KEY` header (not `Authorization`)

### Connection Refused
- Verify n8n is running: `docker ps` or check service status
- Confirm the server IP address (192.168.0.14) is accessible
- Check port 5678 is open and not blocked by firewall

### Rate Limiting
- Wait a few seconds between API calls
- For bulk operations, add delays (recommended: 5-15 seconds between activations)

## Official Documentation

For complete API documentation, visit your n8n instance:
`http://192.168.0.14:5678/api-docs`
