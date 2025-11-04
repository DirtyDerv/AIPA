@echo off
echo 🚀 AIPA n8n Workflow Activation Helper
echo ======================================
echo.
echo This will help you activate the Discord NLP workflow in n8n
echo.
echo STEPS TO COMPLETE:
echo.
echo 1. Open your web browser and go to: http://192.168.0.14:5678
echo 2. Log in to n8n (if required)
echo 3. Click "Workflows" in the left sidebar
echo 4. Click the "+" button to create a new workflow
echo 5. Click "Import from File"
echo 6. Select: n8n-workflows\09-discord-natural-language.json
echo 7. Click the toggle in the top-right to ACTIVATE the workflow
echo 8. The workflow should now show as "Active" (green)
echo.
echo 9. Click on the "Gemini" node in the workflow
echo 10. Make sure the Gemini API credential is selected
echo 11. If no credential exists, create one with your Gemini API key
echo.
echo 12. Save the workflow
echo.
echo Once activated, try your natural language note again in Discord!
echo.
pause