import requests
import json
import time

# n8n API configuration
N8N_URL = "http://192.168.0.14:5678"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGEyYTE3NC1kMzU5LTRhZTQtYTFhZS1iNDI1YzczMjk3NTkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDk1NzI0fQ.O2U8Ix7OLoXP7bQW-tyM9g2BssUP4YA5Ko5uJ4Um_5o"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def add_delays_to_workflow(workflow_id, workflow_name):
    """Add Wait nodes between consecutive Telegram nodes"""

    print(f"\nProcessing: {workflow_name}")
    print("-" * 80)

    # Get workflow
    response = requests.get(f"{N8N_URL}/api/v1/workflows/{workflow_id}", headers=headers)

    if response.status_code != 200:
        print(f"  [FAIL] Could not get workflow: {response.status_code}")
        return False

    workflow = response.json()
    nodes = workflow['nodes']
    connections = workflow.get('connections', {})

    # Find all Telegram send nodes
    telegram_nodes = []
    for node in nodes:
        if node['type'] == 'n8n-nodes-base.telegram':
            telegram_nodes.append(node['name'])

    if not telegram_nodes:
        print(f"  [SKIP] No Telegram nodes found")
        return False

    print(f"  Found {len(telegram_nodes)} Telegram nodes")

    # Find consecutive Telegram nodes
    delays_needed = []

    for source_node_name, targets in connections.items():
        source_node = next((n for n in nodes if n['name'] == source_node_name), None)

        if source_node and source_node['type'] == 'n8n-nodes-base.telegram':
            # This is a Telegram node, check what it connects to
            for output_connections in targets.get('main', []):
                for conn in output_connections:
                    target_name = conn['node']
                    target_node = next((n for n in nodes if n['name'] == target_name), None)

                    if target_node and target_node['type'] == 'n8n-nodes-base.telegram':
                        # Two consecutive Telegram nodes!
                        delays_needed.append({
                            'source': source_node_name,
                            'target': target_name,
                            'connection_index': targets['main'].index(output_connections)
                        })

    if not delays_needed:
        print(f"  [OK] No consecutive Telegram nodes found - already optimized!")
        return False

    print(f"  [INFO] Found {len(delays_needed)} places needing delays")

    # Add Wait nodes
    new_nodes = []
    new_connections = {}
    wait_node_counter = 1

    for delay in delays_needed:
        # Create a Wait node
        wait_node_id = f"rate-limit-wait-{wait_node_counter}"
        wait_node = {
            "parameters": {
                "amount": 1.5,
                "unit": "seconds"
            },
            "id": wait_node_id,
            "name": f"Rate Limit Delay {wait_node_counter}",
            "type": "n8n-nodes-base.wait",
            "typeVersion": 1,
            "position": [0, 0]  # Will be calculated
        }

        new_nodes.append(wait_node)

        # Update connections: Source -> Wait -> Target
        source = delay['source']
        target = delay['target']
        wait_name = wait_node['name']

        # Connect source to wait
        if source not in new_connections:
            new_connections[source] = connections.get(source, {'main': [[]]})

        # Replace target with wait in source connections
        for output_list in new_connections[source]['main']:
            for conn in output_list:
                if conn['node'] == target:
                    conn['node'] = wait_name

        # Connect wait to target
        new_connections[wait_name] = {
            'main': [[{'node': target, 'type': 'main', 'index': 0}]]
        }

        print(f"    Added: {source} -> {wait_name} -> {target}")
        wait_node_counter += 1

    # Merge new nodes and connections
    workflow['nodes'].extend(new_nodes)
    workflow['connections'].update(new_connections)

    # Update workflow
    update_data = {
        'name': workflow['name'],
        'nodes': workflow['nodes'],
        'connections': workflow['connections'],
        'settings': workflow.get('settings', {}),
        'staticData': workflow.get('staticData')
    }

    update_response = requests.put(
        f"{N8N_URL}/api/v1/workflows/{workflow_id}",
        headers=headers,
        json=update_data
    )

    if update_response.status_code == 200:
        print(f"  [OK] Successfully added {len(new_nodes)} delay nodes!")
        return True
    else:
        print(f"  [FAIL] Failed to update: {update_response.status_code}")
        return False


# Main execution
print("=" * 80)
print("TELEGRAM RATE LIMIT FIX - Adding Delays Between Messages")
print("=" * 80)

workflows = [
    ("DRuQZOp9tM79Sf6D", "Telegram Main Interface"),
    ("JG4cI6JJErOgPenc", "Calendar Management"),
    ("dsYFoJPM2wUqZaK3", "Email Processing"),
    ("l4fNYmAfBcN2t4YQ", "Business Intelligence & Reports"),
    ("udPdDxTRVWWP67Tx", "BMF Work Logging"),
    ("s0dI6JlJ1iNRMxSu", "DJ Booking"),
    ("dXRNts8WNKGOaXRW", "Woody's Creations"),
    ("e5sxJhHN1p8I4aUX", "Marketing Campaigns")
]

updated_count = 0

for wf_id, wf_name in workflows:
    if add_delays_to_workflow(wf_id, wf_name):
        updated_count += 1
    time.sleep(2)  # Avoid API rate limiting

print("\n" + "=" * 80)
print(f"Summary: Updated {updated_count}/{len(workflows)} workflows")
print("\nRate limit delays added! Wait 60 seconds before testing.")
print("=" * 80)
