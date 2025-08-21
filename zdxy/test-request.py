import aiohttp
import asyncio

async def fire():
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

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.post(url, headers=headers, json=payload) as response:
            print("状态码:", response.status)
            response_text = await response.text()
            print("响应内容:", response_text)

            # 如果返回是 JSON，可以直接解析
            try:
                json_response = await response.json()
                print("JSON 响应:", json_response)
            except Exception:
                pass

async def main():
    request_task = asyncio.create_task(fire())  # 启动，不等待
    print("我不会被阻塞")
    await request_task

if __name__ == '__main__':
    asyncio.run(main())
    print("程序结束")

