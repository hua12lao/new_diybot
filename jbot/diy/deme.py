from telethon import events
from .. import client, chat_id, jdbot, logger, mybot, _JdDir
import os, asyncio, traceback

@client.on(events.NewMessage(pattern=r'^-d\s?[0-9]*$', outgoing=True))
async def del_msg(event):
    try:
        if mybot['开启人形'].lower() == 'false':
            return
        num = event.raw_text.replace(' ', '').split('d')
        if len(num) == 2 and num[-1]:
            count = int(num[-1])
        else:
            count = 1
        await event.delete()
        count_buffer = 0
        dme_msg = "别搁这防撤回了 . . ."
        target_file = False
        if os.path.exists(f'{_JdDir}/jbot/diy/dme.jpg'):
            target_file = await event.client.upload_file(f'{_JdDir}/jbot/diy/dme.jpg')
        async for message in event.client.iter_messages(event.chat_id, from_user="me"):
            if count_buffer == count:
                break
            if message.forward or message.via_bot or message.sticker or message.contact or message.poll or message.game or message.geo:
                pass
            elif message.text or message.voice:
                if not message.text == dme_msg:
                    try:
                        await message.edit(dme_msg)
                    except:
                        pass
            elif message.document or message.photo or message.file or message.audio or message.video or message.gif:
                if target_file:
                    if not message.text == dme_msg:
                        try:
                            await message.edit(dme_msg, file=target_file)
                        except:
                            pass
                else:
                    if not message.text == dme_msg:
                        try:
                            await message.edit(dme_msg)
                        except:
                            pass
            else:
                pass
            await message.delete()
            count_buffer += 1
        notification = await client.send_message(event.chat_id, f'已删除{count_buffer}/{count}')
        await asyncio.sleep(0.5)
        await notification.delete()
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")
