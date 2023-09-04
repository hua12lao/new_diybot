from telethon import events
from .. import client, chat_id, mybot, jdbot, logger
import os, asyncio, traceback

@client.on(events.NewMessage(pattern=r'^-r\s?[0-9]*$', outgoing=True))
async def reply(event):
    try:
        if not event.is_reply or mybot['开启人形'].lower() == 'false':
            return
        num = event.raw_text.replace(' ', '').split('r')
        if len(num) == 2 and num[-1]:
            num = int(num[-1])
        else:
            num = 1
        reply = await event.get_reply_message()
        await event.delete()
        for _ in range(0, num):
            await reply.forward_to(int(event.chat_id))
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")
        
