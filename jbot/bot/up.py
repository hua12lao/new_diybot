#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import chat_id, jdbot, logger, _JdDir, _ConfigDir, chname, mybot
from asyncio import exceptions
from telethon import events
from .update import version, botlog
import requests, os, sys


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/upbot$'))
async def myupbot(event):
    try:
        msg = await jdbot.send_message(chat_id, "准备更新bot . . .")
        resp = requests.get('https://raw.githubusercontent.com/Annyoo2021/mybot/main/config/bot.sh').text
        if not resp:
            await jdbot.edit_message(msg, "下载shell文件失败\n请稍后重试，或尝试关闭代理重启!")
            return
        cmdtext = f"bash {_ConfigDir}/bot.sh"
        path = f"{_ConfigDir}/bot.sh"
        with open(path, 'w+', encoding='utf-8') as f:
            f.write(resp)
        await jdbot.edit_message(msg, "更新不会更新user\n若已部署user, 更新会暂时关闭监控\n如需开启, 请更新完成后执行 /user\n更新过程中程序会重启\n请耐心等待 . . .")
        os.system(cmdtext)
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/ver$', incoming=True))
async def bot_ver(event):
    await jdbot.send_message(chat_id, f'当前版本\n{version}\n{botlog}')
