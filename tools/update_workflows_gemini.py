#!/usr/bin/env python3
"""
Update n8n workflows to use Gemini API instead of Claude
"""

import json
from pathlib import Path

GEMINI_API_KEY = "AIzaSyBBo5QRTxtMrxIkMrg4_1ULfKHNIZr3zdE"
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

def convert_claude_to_gemini_node(node):
    """Convert a Claude API node to Gemini API node"""

    if node.get('type') != 'n8n-nodes-base.httpRequest':
        return node

    # Check if this is a Claude API call
    url = node.get('parameters', {}).get('url', '')
    if 'anthropic.com' not in url:
        return node

    print(f"   Converting node: {node.get('name')}")

    # Get the original prompt from Claude format
    body_json = node['parameters'].get('bodyParametersJson', '')

    # Update to Gemini API
    node['parameters']['url'] = f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}"
    node['parameters']['authentication'] = 'none'

    # Remove old auth headers
    if 'headerParametersJson' in node['parameters']:
        node['parameters']['headerParametersJson'] = '={\n  "Content-Type": "application/json"\n}'

    # Update credentials reference
    if 'credentials' in node:
        del node['credentials']

    # Convert body format from Claude to Gemini
    # Claude uses: messages: [{"role": "user", "content": "..."}]
    # Gemini uses: contents: [{"parts": [{"text": "..."}]}]

    if body_json:
        # Replace the body structure to use Gemini format
        new_body = body_json.replace(
            '"messages":',
            '"contents":'
        ).replace(
            '"role": "user",\n      "content":',
            '"parts": [{"text":'
        ).replace(
            '}\n    }\n  ]',
            '}]}\n  ]'
        ).replace(
            'model": "claude-3-5-sonnet-20241022"',
            'generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}'
        ).replace(
            'max_tokens',
            'maxOutputTokens'
        ).replace(
            'temperature',
            'temperature'
        )

        node['parameters']['bodyParametersJson'] = new_body

    # Update node name to reflect Gemini
    node['name'] = node['name'].replace('Claude', 'Gemini').replace('claude', 'gemini')

    return node

def convert_response_parsing(node):
    """Update nodes that parse Claude responses to work with Gemini"""

    if node.get('type') != 'n8n-nodes-base.function' and node.get('type') != 'n8n-nodes-base.code':
        return node

    # Check if this node parses AI responses
    code = ''
    if 'functionCode' in node.get('parameters', {}):
        code = node['parameters']['functionCode']
    elif 'jsCode' in node.get('parameters', {}):
        code = node['parameters']['jsCode']

    if not code:
        return node

    # If it references Claude response structure, update it
    if 'content[0].text' in code or 'response.content' in code:
        print(f"   Updating response parser: {node.get('name')}")

        # Gemini response structure: candidates[0].content.parts[0].text
        code = code.replace(
            'response.content[0].text',
            'response.candidates[0].content.parts[0].text'
        ).replace(
            'items[0].json.content[0].text',
            'items[0].json.candidates[0].content.parts[0].text'
        ).replace(
            '$json.content[0].text',
            '$json.candidates[0].content.parts[0].text'
        )

        if 'functionCode' in node['parameters']:
            node['parameters']['functionCode'] = code
        elif 'jsCode' in node['parameters']:
            node['parameters']['jsCode'] = code

    return node

def update_workflow_file(workflow_file):
    """Update a single workflow file to use Gemini"""
    print(f"\nProcessing: {workflow_file.name}")

    with open(workflow_file, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # Update name
    workflow['name'] = workflow['name'].replace('Claude', 'Gemini')

    # Update each node
    nodes = workflow.get('nodes', [])
    updated_count = 0

    for i, node in enumerate(nodes):
        original_node = json.dumps(node)

        # Convert Claude API calls to Gemini
        node = convert_claude_to_gemini_node(node)

        # Update response parsing
        node = convert_response_parsing(node)

        nodes[i] = node

        if json.dumps(node) != original_node:
            updated_count += 1

    workflow['nodes'] = nodes

    # Save updated workflow
    with open(workflow_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2)

    print(f"   Updated {updated_count} nodes")
    return updated_count > 0

def main():
    print("="*60)
    print("Updating n8n Workflows to use Gemini API")
    print("="*60)

    workflows_dir = Path(__file__).parent / "n8n-workflows"
    workflow_files = sorted(workflows_dir.glob("*.json"))

    if not workflow_files:
        print("\nNo workflow files found!")
        return

    print(f"\nFound {len(workflow_files)} workflow files")

    updated_files = []

    for workflow_file in workflow_files:
        if update_workflow_file(workflow_file):
            updated_files.append(workflow_file.name)

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Workflows updated: {len(updated_files)}")

    if updated_files:
        print("\nUpdated workflows:")
        for name in updated_files:
            print(f"   - {name}")

    print("\n" + "="*60)
    print("Next: Run import_workflows.py to re-import to n8n")
    print("="*60)

if __name__ == "__main__":
    main()
