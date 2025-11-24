import requests

def call_tool(tool_name, **params):
    resp = requests.post(
        f"http://agent_server:9000/tools/{tool_name}",
        json=params
    )
    return resp.json()
