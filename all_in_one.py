# -*- coding: utf-8 -*-
import os
import time
from telethon import TelegramClient, events, sync
import tg_code

api_id = [0123456, 6543210]  # 输入 api_id，一个账号一项
api_hash = ['0123456789abcdef0123456789abcdef', 'abcdef0123456789abcdef0123456789']  # 输入 api_hash，一个账号一项
bots_connands = {
    "@charontv_bot": ["/checkin", "获得"],
    "@JMSIPTV_bot": ["/checkin", "成功"],
    "@blueseamusic_bot": ["/checkin", "成功"],
    "@svipxddosbot": ["签到领积分", "成功"]
}


def check_in_bot(client, bot_id, bot_command, success_message):
    """
    自动签到 Telegram 机器人。

    Args:
        client: TelegramClient 实例。
        bot_id: 机器人 ID。
        bot_command: 签到命令。
        success_message: 签到成功消息。
    """
    client.send_message(bot_id, bot_command)
    time.sleep(2)
    messages = client.get_messages(bot_id)
    if success_message not in messages[0].message:
        if messages[0].buttons:
            # 处理带有按钮的签到
            the_result = bot_inline_with_captcha(client, bot_id, messages)
        else:
            # 处理需要识别验证码的签到
            the_result = bot_pic_with_captcha(client, bot_id, messages)
        if success_message not in the_result:
            print(f"签到失败：{bot_id}")
        else:
            print(f"签到成功：{bot_id}")


def bot_pic_with_captcha(client, bot_id, messages):
    """
    处理需要识别验证码的签到。
    """
    messages[0].download_media(file="1.jpg")
    the_code = tg_code.truecaptcha()
    client.send_message(bot_id, the_code)
    time.sleep(5)
    messages = client.get_messages(bot_id)
    return messages[0].message


def bot_inline_with_captcha(client, bot_id, messages):
    """
    处理带有按钮的签到。
    """
    messages[0].download_media(file="1.jpg")
    the_code = tg_code.truecaptcha()
    try:
        res = messages[0].click(text=the_code)
        if res is None:
            messages[0].click(0)
    except AttributeError:
        print(f"点击按钮失败：{bot_id}")
    time.sleep(5)
    messages = client.get_messages(bot_id)
    return messages[0].message


if __name__ == "__main__":
    session_name = api_id[:]
    for num in range(len(api_id)):
        session_name[num] = "id_" + str(session_name[num])
        client = TelegramClient(session_name[num], api_id[num], api_hash[num])
        client.start()
        for key, value in bots_connands.items():
            check_in_bot(client, key, value[0], value[1])
    os._exit(0)
