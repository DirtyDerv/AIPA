# Import Advanced Discord NLP Workflow to n8n
Write-Host "🚀 Importing Advanced Discord NLP Workflow..." -ForegroundColor Cyan

# Read the workflow JSON
$workflowPath = "n8n-workflows/12-discord-nlp-advanced.json"
if (!(Test-Path $workflowPath)) {
    Write-Host "❌ Workflow file not found: $workflowPath" -ForegroundColor Red
    exit 1
}

$workflowJson = Get-Content $workflowPath -Raw -Encoding UTF8
$workflowData = $workflowJson | ConvertFrom-Json

# Import to n8n
$n8nUrl = "http://localhost:5678"
$apiKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"

try {
    $headers = @{
        "X-N8N-API-KEY" = $apiKey
        "Content-Type" = "application/json"
    }

    $response = Invoke-WebRequest -Uri "$n8nUrl/rest/workflows" -Method POST -Headers $headers -Body $workflowJson -UseBasicParsing

    if ($response.StatusCode -eq 200) {
        $result = $response.Content | ConvertFrom-Json
        $workflowId = $result.id
        Write-Host "✅ Advanced NLP workflow imported successfully!" -ForegroundColor Green
        Write-Host "Workflow ID: $workflowId" -ForegroundColor Yellow

        # Try to activate the workflow
        $activateResponse = Invoke-WebRequest -Uri "$n8nUrl/rest/workflows/$workflowId/activate" -Method POST -Headers $headers -UseBasicParsing

        if ($activateResponse.StatusCode -eq 200) {
            Write-Host "✅ Advanced NLP workflow activated!" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Could not activate workflow automatically" -ForegroundColor Yellow
            Write-Host "Please manually activate 'AIPA - Discord NLP Advanced' in n8n web interface" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Failed to import workflow: $($response.StatusCode)" -ForegroundColor Red
        Write-Host $response.Content -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error importing workflow: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Please import manually through n8n web interface at http://localhost:5678" -ForegroundColor Yellow
}