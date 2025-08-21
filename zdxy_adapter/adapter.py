import logging
import os
import sys

import requests

from cron_schedular.cron_job import cron_job, scheduler
from wecom_app_svr import WecomAppServer, RspTextMsg, RspImageMsg, RspVideoMsg
from dotenv import load_dotenv

load_dotenv()
dify_url = os.getenv("DIFY_URL")
dify_api_key = os.getenv("DIFY_API_KEY")


def msg_handler(req_msg):
    if req_msg.msg_type == 'text' and req_msg.content.strip() == 'help':
        ret = RspTextMsg()
        ret.content = f'msg_type: {req_msg.msg_type}, content: {req_msg.content}'
        return ret
    if req_msg.msg_type == 'image':
        ret = RspImageMsg(req_msg.to_user, req_msg.from_user, req_msg.media_id)
        return ret
    if req_msg.msg_type == 'video':
        ret = RspVideoMsg(req_msg.to_user, req_msg.from_user, req_msg.media_id, "视频标题", "视频描述")
        return ret

    # 返回消息类型
    ret = RspTextMsg()
    ret.content = f'msg_type: {req_msg.msg_type}, content: {req_msg.content}'

    return ret


def event_handler(req_msg):
    # TODO
    ret = RspTextMsg()
    if req_msg.event_type == 'add_to_chat':  # 入群事件处理
        ret.content = f'msg_type: {req_msg.msg_type}\n群会话ID: {req_msg.chat_id}\n查询用法请回复: help'
    return ret

@cron_job(hour=19, minute=2)
def call_dify(user: str = "abc-123", content: str = "你好"):

    headers = {
        "Authorization": "Bearer {}".format(dify_api_key),
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {"content": content},
        "response_mode": "blocking",
        "user": user
    }

    response = requests.post(dify_url, headers=headers, json=payload)

    if response.status_code != 200:
        logging.error("call dify failed \n {}".format(response.json()))
    else:
        logging.info("call dify success \n {}".format(response.json()))


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
