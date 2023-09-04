
import asyncio, os, json, os, re, sys, time, requests, traceback, qrcode
from telethon import Button, events
from .. import client, jdbot, chat_id, _JdDir, logger, QR_IMG_FILE, _botset
from ..bot.utils import V4, press_event, row, split_list
from asyncio import exceptions

userfile = f"{_JdDir}/jbot/diy/user.py"

def creat_qr(text):
    """实例化QRCode生成qr对象"""
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.clear()
    # 传入数据
    qr.add_data(text)
    qr.make(fit=True)
    # 生成二维码
    img = qr.make_image()
    # 保存二维码
    img.save(QR_IMG_FILE)

def restart():
    text = "if [ -d '/jd' ]; then cd /jd/jbot; pm2 start ecosystem.config.js; cd /jd; pm2 restart jbot; else " \
           "ps -ef | grep 'python3 -m jbot' | grep -v grep | awk '{print $1}' | xargs kill -9 2>/dev/null; " \
           "nohup python3 -m jbot >/ql/log/bot/bot.log 2>&1 & fi "
    os.system(text)


def start():
    with open(_botset, 'r', encoding='utf-8') as f:
        myset = json.load(f)
    myset['开启user'] = 'True'
    with open(_botset, "w+", encoding="utf-8") as f:
        json.dump(myset, f, indent=2, ensure_ascii=False)
    restart()


def close():
    with open(_botset, 'r', encoding='utf-8') as f:
        myset = json.load(f)
    myset['开启user'] = 'False'
    with open(_botset, "w+", encoding="utf-8") as f:
        json.dump(myset, f, indent=2, ensure_ascii=False)
    restart()


def state():
    with open(_botset, 'r', encoding='utf-8') as f:
        myset = json.load(f)
    if myset['开启user'].lower() == 'true':
        return True
    else:
        return False


def startrx():
    with open(_botset, 'r', encoding='utf-8') as f:
        myset = json.load(f)
    myset['开启人形'] = 'True'
    with open(_botset, "w+", encoding="utf-8") as f:
        json.dump(myset, f, indent=2, ensure_ascii=False)
    restart()


def closerx():
    with open(_botset, 'r', encoding='utf-8') as f:
        myset = json.load(f)
    myset['开启人形'] = 'False'
    with open(_botset, "w+", encoding="utf-8") as f:
        json.dump(myset, f, indent=2, ensure_ascii=False)
    restart()


def checkrx():
    with open(_botset, 'r', encoding='utf-8') as f:
        myset = json.load(f)
    if myset['开启人形'].lower() == 'true':
        return True
    else:
        return False

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/user$'))
async def user_login(event):
    isconnected = True if client.is_connected() else False
    try:
        if not os.path.exists(userfile):
            await jdbot.send_message(chat_id, f'user.py不存在\n请先执行以下命令\n再执行：/user\n\n```/cmd cd {_JdDir}/jbot/diy && wget https://ghproxy.com/https://raw.githubusercontent.com/Annyoo2021/mybot/main/jbot/diy/user.py```')
            return
        tellogin, qrlogin = False, False
        sender = event.sender_id
        # session = "/jd/config/user.session" if V4 else "/ql/config/user.session"
        async with jdbot.conversation(sender, timeout=120) as conv:
            while True:
                msg = await conv.send_message("请做出你的选择")
                buttons = [
                    Button.inline("重新登录", data="relogin") if isconnected else Button.inline("我要登录", data="login"),
                    Button.inline('关闭user', data='close') if state() else Button.inline('开启user', data='start'),
                    Button.inline('关闭人形', data='closerx') if checkrx() else Button.inline('开启人形', data='startrx')
                ]
                opt_btns = [
                    Button.inline('上级目录', data='upper menu'),
                    Button.inline('取消会话', data='cancel')
                ]
                newbuttons = split_list(buttons, row)
                newbuttons.append([Button.inline('取消会话', data='cancel')])
                text = "请做出你的选择："
                if not state():
                    text = "**若首次部署、切勿开启user**\n请做出你的选择："
                msg = await jdbot.edit_message(msg, f'{text}', buttons=newbuttons)
                convdata = await conv.wait_event(press_event(sender))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    await jdbot.edit_message(msg, '对话已取消')
                    conv.cancel()
                    return False
                elif res == 'close':
                    await jdbot.edit_message(msg, "user关闭成功，准备重启机器人 . . .")
                    close()
                elif res == 'start':
                    await jdbot.edit_message(msg, "user开启成功，准备重启机器人 . . .")
                    start()
                elif res == 'closerx':
                    await jdbot.edit_message(msg, "人形关闭成功，准备重启机器人 . . .")
                    closerx()
                elif res == 'startrx':
                    await jdbot.edit_message(msg, "人形开启成功，准备重启机器人 . . .")
                    startrx()
                else:
                    btns = [
                        Button.inline('手机登录', data='tellogin'),
                        Button.inline('扫码登录', data='qrlogin')
                    ]
                    newbtns = split_list(btns, row)
                    newbtns.append(opt_btns)
                    msg = await jdbot.edit_message(msg, '请做出你的选择：', buttons=newbtns)
                    convdata = await conv.wait_event(press_event(sender))
                    res2 = bytes.decode(convdata.data)
                    if res2 == 'cancel':
                        await jdbot.edit_message(msg, '对话已取消')
                        conv.cancel()
                        return False
                    elif res2 == 'upper menu':
                        await msg.delete()
                        continue
                    elif res2 == 'tellogin':
                        tellogin = True
                        break
                    else:
                        qrlogin = True
                        break
            await msg.delete()
        if tellogin:
            await client.connect()
            async with jdbot.conversation(sender, timeout=100) as conv:
                loop = 3
                info = ''
                while loop:
                    msg = await conv.send_message(f'{info}请输入带区域号手机号：\n例如：+8618888888888\n\n回复 `cancel` 或 `取消` 即可取消登录')
                    phone = await conv.get_response()
                    if phone.raw_text == 'cancel' or phone.raw_text == '取消':
                        await msg.delete()
                        await conv.send_message('取消登录')
                        if not isconnected:
                            await client.disconnect()
                        return
                    elif re.search('^\+\d+$', phone.raw_text):
                        await client.send_code_request(phone.raw_text, force_sms=True)
                        break
                    else:
                        await msg.delete()
                        info = "手机号输入有误\n"
                        loop -= 1
                        continue
                else:
                    await conv.send_message('输入错误3次，取消登录')
                    if not isconnected:
                        await client.disconnect()
                    return
                loop = 3
                info = ''
                while loop:
                    msg = await conv.send_message(f'{info}请按以下格式输入验证码:\n例如：`code12345code`\n**两边的code必须有！**')
                    code = await conv.get_response()
                    check = re.findall('code(\d{5})code', code.raw_text)
                    if len(check) != 0:
                        thecode = check[0]
                        await client.sign_in(phone.raw_text, thecode)
                        break
                    else:
                        await msg.delete()
                        info = "验证码输入有误\n"
                        loop -= 1
                        continue
                else:
                    await conv.send_message('输入错误3次，取消登录\n已关闭user\n如需开启 请重启后重新执行 /user\n开始重启 . . .')
                    close()
                    await client.disconnect()
                    restart()
                    return
                await jdbot.send_message(chat_id, '恭喜您已登录成功！\n自动重启中！')
            start()
        elif qrlogin:
            await client.connect()
            qr_login = await client.qr_login()
            creat_qr(qr_login.url)
            await jdbot.send_message(chat_id, '请使用TG扫描二维码以开启USER', file=QR_IMG_FILE)
            await qr_login.wait(timeout=100)
            await jdbot.send_message(chat_id, '恭喜您已登录成功！\n自动重启中！')
            os.remove(QR_IMG_FILE)
            start()
    except asyncio.exceptions.TimeoutError:
        await jdbot.edit_message(msg, '登录已超时，对话已停止')
    except Exception as e:
        close()
        await client.disconnect()
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")
