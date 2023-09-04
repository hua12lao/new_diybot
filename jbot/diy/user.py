#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import chat_id, jdbot, client, logger, api_id, api_hash, proxystart, proxy, _ConfigDir, _ScriptsDir, _JdbotDir, _JdDir, TOKEN
from ..bot.utils import cmd, backfile, jdcmd, V4, QL, _ConfigFile, myck
from ..diy.utils import getbean, my_chat_id,my_monitor_chatId,read,write
from telethon import events, TelegramClient
import re, asyncio, time, datetime, os, sys, requests, json, traceback

bot_id = int(TOKEN.split(":")[0])

# @client.on(events.NewMessage(from_users=chat_id, pattern=r"^-u$"))
# async def user(event):
#     try:
#         chat = await event.get_chat()
#         await event.delete()
#         # await asyncio.sleep(0.2)
#         msg = await client.send_message(chat.id, "** 监控正常**")
#         await asyncio.sleep(5)
#         await client.delete_messages(chat.id, msg)
#     except Exception as e:
#         title = "★错误★"
#         name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
#         function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
#         details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
#         tip = '建议百度/谷歌进行查询'
#         await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
#         logger.error(f"错误--->{str(e)}")

# @client.on(events.NewMessage(chats=my_monitor_chatId, pattern=r'export\s(jd_zdjr_activity).*=(".*"|\'.*\')'))
# async def activityID(event):
#     try:
#         if event.chat_id == -1001320212725 and "Annyoo" in event.post_author:
#             return
#         text = event.message.text
#         if "2222222222222" in text:
#             name = "开卡有礼"
#         elif "jd_zdjr_activity" in text:
#             name = "组队瓜分"
#         elif "jd_smiek_luckDraw_activityUrl" in text:
#             name = "转盘抽奖"
#         else:
#             return
#         msg = await jdbot.send_message(chat_id, f'【监控】 监测到`{name}` 环境变量！')
#         group = f'[{event.chat.title}](https://t.me/c/{event.chat.id}/{event.message.id})'
#         messages = event.message.text.replace("`","")
#         messages = event.message.text.split("\n")
#         change = ""
#         for message in messages:
#             if "export " not in message:
#                 continue
#             kv = message.replace("export ", "")
#             key = kv.split("=")[0]
#             value = re.findall(r'"([^"]*)"', kv)[0]
#             configs = read("str")
#             if key in configs:
#                 configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
#                 change += f"【替换】{group} `{name}` 环境变量成功\n`{kv}`\n\n"
#                 msg = await jdbot.edit_message(msg, change)
#             else:
#                 configs = read("str")
#                 configs += f'export {key}="{value}"\n'
#                 change += f"【新增】{group} `{name}` 环境变量成功\n`{kv}`\n\n"
#                 msg = await jdbot.edit_message(msg, change)
#             write(configs)
#         if len(change) == 0:
#             await jdbot.edit_message(msg, f"【取消】{group} `{name}` 环境变量无需改动！")
#             return
#         try:
#             if "OPEN_CARD" in event.message.text:
#                 from ..diy.diy import openCard
#                 await openCard()
#             elif "jd_zdjr_activity" in event.message.text:
#                 from ..diy.diy import gua_zdjr_new
#                 await gua_zdjr_new()
#             elif "jd_smiek_luckDraw_activityUrl" in event.message.text:
#                 from ..diy.diy import jd_smiek_luckDraw_activityUrl
#                 await jd_smiek_luckDraw_activityUrl()
#         except ImportError:
#             pass
#     except Exception as e:
#         title = "【💥错误💥】"
#         name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
#         function = "函数名：" + sys._getframe().f_code.co_name
#         tip = '建议百度/谷歌进行查询'
#         await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
#         logger.error(f"错误--->{str(e)}")
