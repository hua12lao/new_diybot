from telethon import events
from .. import client, chat_id, mybot, jdbot, logger
import os, asyncio, traceback

@client.on(events.NewMessage(pattern=r'^-i$', outgoing=True))
async def check_id(event):
    try:
        if event.is_private or not event.is_reply or mybot['开启人形'].lower() == 'false':
            return
        message = await event.get_reply_message()
        text = f"此消息ID：`{str(event.message.id)}`\n\n"
        text += f"**群组信息**\nid：`{str(event.chat_id)}\n`" if event.is_group else f"**频道信息**\nid：`{str(event.chat_id)}\n`"
        msg_from = event.chat if event.chat else (await event.get_chat())
        title = f"群组名称：`{msg_from.title}`\n" if event.is_group else f"频道名称：`{msg_from.title}`\n"
        text += title
        try:
            if msg_from.username:
                text += f"群组用户名：`@{msg_from.username}`\n"
        except AttributeError:
            return
        if message:
            text += f"\n**查询的消息**：\n消息id：`{str(message.id)}`\n用户id：`{str(message.sender_id)}`"
            try:
                if message.sender.bot:
                    text += f"\n机器人：`是`"
                if message.sender.last_name:
                    text += f"\n姓：`{message.sender.last_name}`"
                try:
                    text += f"\n名：`{message.sender.first_name}`"
                except TypeError:
                    pass
                if message.sender.username:
                    text += f"\n用户名：@{message.sender.username}"
            except AttributeError:
                pass
            await event.edit(text)
        else:
            await event.delete()
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(pattern=r'^-i$', outgoing=True))
async def get_id(event):
    try:
        if event.is_reply or mybot['开启人形'].lower() == 'false':
            return
        chat = await event.get_chat()
        title = chat.title if event.is_group or event.is_channel else ""
        if event.is_group:
            await event.edit(f'**群组名：**`{title}`\n**群组ID：**`-100{chat.id}`')
        elif event.is_channel:
            await event.edit(f'**频道名：**`{title}`\n**频道ID：**`-100{chat.id}`')
        elif event.is_private:
            await event.edit(f'**姓：**`{chat.last_name}`\n**名：**`{chat.first_name}`\n**用户id：**`{str(chat.id)}`\n**用户名：**@{chat.username}')
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")

