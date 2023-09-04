from telethon import events
from .. import client, chat_id, mybot, jdbot, logger
import os, asyncio, traceback

@client.on(events.NewMessage(pattern=r'^-dat$', outgoing=True))
async def datrue(context):
    try:
        if mybot['开启人形'].lower() == 'false':
            return
        input_chat = await context.get_input_chat()
        messages = []
        count = 0
        await context.delete()
        async for message in context.client.iter_messages(input_chat, min_id=1):
            messages.append(message)
            count += 1
            messages.append(1)
            if len(messages) == 100:
                await context.client.delete_messages(input_chat, messages)
                messages = []
            if messages:
                await context.client.delete_messages(input_chat, messages)
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")
