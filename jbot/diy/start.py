#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .. import chat_id, jdbot, logger
from ..bot.utils import V4, QL
from telethon import events
from .. import jdbot, chat_id,chname
import sys, os, traceback


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/start$'))
async def my_start(event):
    try:
        if V4:
            msg = '''使用方法如下：
    /help 获取命令，可直接发送至botfather。
    /start 开始使用本程序。
    /restart 重启本程序。
    /upbot 升级机器人。
    /ver 查看程序版本号。
    /user 登录启动TG监控。
    /a 使用你的自定义快捷按钮。
    /addcron 增加cron，例：0 0 * * * jtask xxxxx。
    /clearboard 删除快捷输入按钮。
    /bean 获取京豆变化，默认为总京豆收支。/bean in 京豆进账，/bean out 京豆支出。
    /chart 获取京豆变化数据柱状图和曲线图。例：/chart 1，获取账号1京豆变化。
    /cmd 执行命令，例：/cmd python3 /python/bot.py，则执行python目录下的bot.py。不建议使用BOT使用并发，可能产生不明原因的崩溃。 
    /cron 进行cron管理。
    /dl 下载文件，例：/dl https://raw.githubusercontent.com/SuMaiKaDe/bot/main/requirements.txt
    /edit 从/jd目录选择文件并编辑，需要将编辑好信息全部发给BOT，BOT会根据你发的信息进行替换。建议仅编辑config或crontab.list，其他文件慎用！！！
    /getcookie 扫码获取cookie，30s内可取消，31s~2分钟内不能进行其他交互直到超时或获取到cookie。
    /getfile 获取/jd目录下文件。
    /log 查看脚本执行日志。
    /node 执行js脚本，输入/node xxxxx.js。如执行非scripts目录js，需输入绝对路径执行。node命令会等待脚本执行完，期间不能使用BOT，建议使用snode命令。
    /set 设置。
    /setshort 设置自定义按钮，每次设置会覆盖原设置。
    /setname 设置命令别名。
    /snode 选择脚本执行，只能选择/scripts和/own目录下的脚本，选择完后直接后台运行，不影响BOT响应其他命令。 
    /repo 管理添加的仓库。
    /export 管理添加的环境变量。
    /checkcookie 检测账号过期。
    /blockcookie 屏蔽账号。
    /install 拓展本程序功能。
    /uninstall 删除本程序拓展功能。
    /list 列出本程序拓展的功能。
    
    此外，直接发送文件至BOT，会让您选择保存到目标文件夹，支持保存并运行。发送以 .git 结尾的链接开始添加仓库。发送以 .js .sh .py结尾的已raw链接开始下载文件。发送格式为 key="value" 或者 key='value' 的消息开始添加环境变量。'''
        elif QL:
            msg = '''使用方法如下：
    /help 获取命令，可直接发送至botfather。
    /start 开始使用本程序。
    /restart 重启本程序。
    /up 升级本程序。
    /upbot 升级拓展功能。
    /ver 查看程序版本号。
    /user 登录启动TG监控。
    /a 使用你的自定义快捷按钮。
    /clearboard 删除快捷输入按钮。
    /bean 获取京豆变化，默认为总京豆收支。
    /chart 获取京豆变化数据柱状图和曲线图。例：/chart 1，获取账号1京豆变化。
    /cmd 执行命令，例：/cmd python3 /python/bot.py，则执行python目录下的bot.py。不建议使用BOT使用并发，可能产生不明原因的崩溃。 
    /dl 下载文件。
    /edit 从/jd目录选择文件并编辑，需要将编辑好信息全部发给BOT，BOT会根据你发的信息进行替换。建议仅编辑config或crontab.list，其他文件慎用！！！
    /getcookie 扫码获取cookie，30s内可取消，31s~2分钟内不能进行其他交互直到超时或获取到cookie。
    /getfile 获取/jd目录下文件。
    /log 查看脚本执行日志。
    /node 执行js脚本，输入/node jd_bean_change。如执行非scripts目录js，需输入绝对路径执行。node命令会等待脚本执行完，期间不能使用BOT，建议使用snode命令。
    /set 设置。
    /setshort 设置自定义按钮，每次设置会覆盖原设置。
    /setname 设置命令别名。
    /snode 选择脚本执行，只能选择/scripts和/own目录下的脚本，选择完后直接后台运行，不影响BOT响应其他命令。 
    /repo 管理添加的仓库。
    /export 管理添加的环境变量。
    /install 拓展本程序功能。
    /uninstall 删除本程序拓展功能。
    /list 列出本程序拓展的功能。
    /addenv 青龙新增环境变量。
    /env 青龙管理环境变量。

    此外，直接发送文件至BOT，会让您选择保存到目标文件夹，支持保存并运行。发送以 .git 结尾的链接开始添加仓库。发送以 .js .sh .py结尾的已raw链接开始下载文件。发送格式为 key="value" 或者 key='value' 的消息开始添加环境变量。'''
        await jdbot.send_message(chat_id, msg)
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")
if chname:
    jdbot.add_event_handler(my_start,events.NewMessage(from_users=chat_id, pattern='开始'))
