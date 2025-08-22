import logging
import os
import sys

import aiohttp
import requests

from cron_schedular.cron_job import cron_job, scheduler
from wecom_app_svr import WecomAppServer, RspTextMsg, RspImageMsg, RspVideoMsg
from dotenv import load_dotenv

load_dotenv()
dify_url = os.getenv("DIFY_URL")
dify_api_key = os.getenv("DIFY_API_KEY")

def msg_handler(req_msg):
    if req_msg.msg_type == 'text':
        call_dify(user_input=req_msg.content, user="user")
        # 不直接由该服务器直接回复，而是触发Dify流程由流程自动回复
        ret = RspTextMsg()
        ret.content = '请稍后，答案正在生成中...'
        return ret

    if req_msg.msg_type == 'image':
        ret = RspTextMsg()
        ret.msg_type = "text"
        ret.content = "system: 用户发送了图片，系统目前无法处理图片"
        return ret

    if req_msg.msg_type == 'video':
        ret = RspTextMsg()
        ret.msg_type = "text"
        ret.content = "system: 用户发送了图片，系统目前无法处理视频"
        return ret

    # 返回消息类型
    ret = RspTextMsg()
    ret.content = "system: 用户发送了{}类型的消息，该消息类型暂无法处理".format(req_msg.msg_type)

    return ret



def event_handler(req_msg):
    # TODO
    ret = RspTextMsg()
    if req_msg.event_type == 'add_to_chat':  # 入群事件处理
        ret.content = ""
    return ret

@cron_job(hour=9, minute=15)
def daily_dify_call():
    call_dify(user_input="每日开盘前提醒", user="system")

async def call_dify(user_input: str="", user: str="default-user"):
    url = os.getenv("DIFY_URL")

    headers = {
        "Authorization": "Bearer {}".format(os.getenv("DIFY_API_KEY")),
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {
            "content": user_input
        },
        "response_mode": "streaming",
        "user": user
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


def main():
    load_dotenv()
    scheduler.start()

    logging.basicConfig(stream=sys.stdout)
    logging.getLogger().setLevel(logging.INFO)

    token = os.getenv("WECOM_APP_TOKEN")  # 3个x
    aes_key = os.getenv("WECOM_APP_AES_KEY") # 43个x
    corp_id = os.getenv("WEAPP_CROP_ID")
    host = os.getenv("SERVER_HOST")
    port = os.getenv("SERVER_PORT")
    server = WecomAppServer("wecom-app-svr", host, port, path='/wecom_app_cb', token=token, aes_key=aes_key,
                            corp_id=corp_id)

    server.set_message_handler(msg_handler)
    server.set_event_handler(event_handler)
    server.run()


if __name__ == '__main__':
    main()
