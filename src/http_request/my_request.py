import requests
def main():
    url = "https://api.dify.ai/v1/workflows/run"

    headers = {
        "Authorization": "Bearer app-VVRC9P6v4fGDEwVJsXBQ3MDf",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {},
        "response_mode": "streaming",
        "user": "abc-123"
    }

    response = requests.post(url, headers=headers, json=payload)

    print("状态码:", response.status_code)
    print("响应内容:", response.text)

    # 如果返回是 JSON，可以直接解析
    try:
        print("JSON 响应:", response.json())
    except Exception:
        pass