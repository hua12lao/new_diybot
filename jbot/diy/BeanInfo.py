

from functools import total_ordering
from .. import client, chat_id, jdbot, logger
from ..bot.utils import _ConfigFile, myck
import datetime, time, httpx, re, os, asyncio, traceback, json
from datetime import timedelta, timezone
from random import sample
from telethon import events
async def getRequest(method, url, data=None, headers=None, params=None, json=None, allow_redirects=False, timeout=100):
    try:
        async with httpx.AsyncClient(verify=False, follow_redirects=allow_redirects) as client:
            res = await client.request(method, url=url, data=data, headers=headers, params=params, json=json, timeout=timeout)
    except:
        res = False
    return res

async def getUA():
    """
    随机生成一个UA
    jdapp;iPhone;10.0.4;14.2;9fb54498b32e17dfc5717744b5eaecda8366223c;network/wifi;ADID/2CF597D0-10D8-4DF8-C5A2-61FD79AC8035;model/iPhone11,1;addressid/7785283669;appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1
    :return: ua
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.15(0x18000f29) NetType/WIFI Language/zh_CN'

    """
    uuid = ''.join(sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
    addressid = ''.join(sample('1234567898647', 10))
    iosVer = ''.join(sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
    iosV = iosVer.replace('.', '_')
    iPhone = ''.join(sample(["8", "9", "10", "11", "12", "13"], 1))
    ADID = ''.join(sample('0987654321ABCDEF', 8)) + '-' + ''.join(sample('0987654321ABCDEF', 4)) + '-' + ''.join(sample('0987654321ABCDEF', 4)) + '-' + ''.join(sample('0987654321ABCDEF', 4)) + '-' + ''.join(sample('0987654321ABCDEF', 12))
    return f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};model/iPhone{iPhone},1;addressid/{addressid};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1'




async def checkCookie(cookie):
    islogin = True
    r = await asyncio.gather(
        checkCookie1(cookie),
        checkCookie2(cookie),
    )
    islogin = r[0] if r[0] != "err" else r[1]
    return islogin


async def checkCookie1(cookie):
    islogin = "err"
    try:
        url = "https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
        headers = {
            "Host": "me-api.jd.com",
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "User-Agent": await getUA(),
            "Accept-Language": "zh-cn",
            "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
            "Accept-Encoding": "gzip, deflate, br"
        }
        res = await getRequest("GET", url, headers=headers, allow_redirects=True)
        data = res.json()
        if data['retcode'] == "1001":  # 失效
            islogin = False
        elif data['retcode'] == "0" and data['data']['userInfo']['baseInfo']['curPin'] != "":  # 有效
            beanNum = data['data']['assetInfo']['beanNum']
            islogin = beanNum if (str(beanNum) != "" and str(beanNum) != "0") else True
    except:
        pass
    return islogin


async def checkCookie2(cookie):
    islogin = True
    url = "https://plogin.m.jd.com/cgi-bin/ml/islogin"
    headers = {
        "Cookie": cookie,
        "User-Agent": await getUA(),
    }
    res = await getRequest("GET", url, headers=headers, allow_redirects=True)
    try:
        data = res.json()
        if data['islogin'] == "0":  # 失效
            islogin = False
        elif data['islogin'] == "1":  # 有效
            islogin = True
    except:
        pass
    return islogin


async def getJxbean(cookie):
    info = False
    try:
        headers = {
            "Host": "m.jingxi.com",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": await getUA(),
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Referer": "https://st.jingxi.com/",
            "Cookie": cookie
        }
        url = f"https://m.jingxi.com/activeapi/querybeanamount?_={int(time.time() * 1000)}&sceneval=2&g_login_type=1&g_ty=ls"
        r = await getRequest("GET", url, headers=headers, timeout=10)
        res = json.loads(re.findall(r"QueryBeanAmount\((.*?)\n?\)", str(r.text))[0])
        info = [res['data']['jingbean'], res['data']['xibean']]
    except:
        pass
    return info


async def getJDUserInfo(cookie):
    info = False
    try:
        headers = {
            "Host": "wq.jd.com",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded;",
            "Accept-Encoding": "gzip, deflate, br",
            'Referer': 'https://wqs.jd.com/',
            "User-Agent": await getUA(),
            "Cookie": cookie,
        }
        jurl = "https://wq.jd.com/user/info/QueryJDUserInfo?sceneval=2"
        r = await getRequest("GET", jurl, headers=headers, timeout=10)
        res = r.json()
        plus = 'Plus' if res['isPlusVip'] == True else '会员'
        info = [res['base']['nickname'], res['base']['jdNum'], res['base']['jvalue'], plus]
    except:
        pass
    return info


async def BeanInfo(num, cookie):
    try:
        beans_res, jxBean, UserInfo = await asyncio.gather(
            get_beans_history(cookie),
            getJxbean(cookie),
            getJDUserInfo(cookie),
        )
        if beans_res['code'] != 200:
            return {'code': 400, 'data': f'**账号{num}请求失败、Cookie已失效**'} if '未登录' in str(beans_res['data']) else beans_res
        else:
            date = beans_res['data'][3][0]
            beanall, infolist, detailsList = 0, {}, []
            for i in beans_res['data'][2][date]:
                if not re.search('退还|扣赠', i['eventMassage']):
                    i['eventMassage'] = i['eventMassage'].replace("参加[", "").replace("]-奖励", "").replace("]店铺活动-奖励", "")
                    i['eventMassage'] = i['eventMassage'].replace("京东自营旗舰店", "(自营)").replace("京东自营官方旗舰店", "(自营官方)").replace("京东官方自营旗舰店", "(自营官方)")
                    i['eventMassage'] = i['eventMassage'].replace("（", "(").replace("）", ")").replace("官方自营旗舰店", "(自营官方)")
                    i['eventMassage'] = i['eventMassage'].replace("官方旗舰店", "(官方)").replace("品牌闪购抽盲盒得京豆", "闪购盲盒")
                    i['eventMassage'] = i['eventMassage'].replace("旗舰店", "(旗舰)").replace("专营店", "(专营)").replace("专卖店", "(专卖)")
                    beanall += int(int(i['amount']))
                    detailsList.append(i)
                    if i['eventMassage'] in infolist:
                        infolist[i['eventMassage']] += int(int(i['amount']))
                    else:
                        infolist[i['eventMassage']] = int(int(i['amount']))
            return {'code': 200, 'data': [beanall, infolist, detailsList, jxBean, UserInfo]}
    except Exception as e:
        return {'code': 400, 'data': str(e)}


def gen_body(page):
    SHA_TZ = timezone(timedelta(hours=8), name='Asia/Shanghai')
    body = {
        "beginDate": datetime.datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(SHA_TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "endDate": datetime.datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(SHA_TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "pageNo": page,
        "pageSize": 20,
    }
    return body


def gen_params(page):
    body = gen_body(page)
    params = {
        "functionId": "dailyspec_beanDetails",
        "appid": "swat_miniprogram",
        "client": "tjj_m",
        "sdkName": "orderDetail",
        "sdkVersion": "1.0.0",
        "clientVersion": "3.1.3",
        "timestamp": int(round(time.time() * 1000)),
        "body": json.dumps(body)
    }
    return params


async def get_beans_history(cookie):
    try:
        headers = {
            "User-Agent": await getUA(),
            "Connection": 'keep-alive',
            "Content-Type": "application/x-www-form-urlencoded;",
            "Cookie": cookie,
        }
        url = "https://bean.m.jd.com/beanDetail/detail.json"
        days = [(datetime.date.today() - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, 1)]
        beans_in = {key: 0 for key in days}
        beans_out = {key: 0 for key in days}
        beans_info = {key: [] for key in days}
        page = 0
        loop = True
        while loop:
            page += 1
            params = f'page={page}'
            res = await getRequest("GET", url, params=params, headers=headers, timeout=10)
            resp = res.text
            res = json.loads(resp)
            if str(res['code']) == "0":
                if len(res['jingDetailList']) != 0:
                    for i in res['jingDetailList']:
                        for date in days:
                            if str(date) in i['date'] and int(i['amount']) > 0:
                                beans_in[str(date)] = beans_in[str(date)] + int(i['amount'])
                                beans_info[str(date)].append(i)
                                break
                            elif str(date) in i['date'] and int(i['amount']) < 0:
                                beans_out[str(date)] = beans_out[str(date)] + (-int(i['amount']))
                                break
                        if i['date'].split(' ')[0] not in str(days):
                            loop = False
                else:
                    loop = False
            else:
                return {'code': 400, 'data': res}
        return {'code': 200, 'data': [beans_in, beans_out, beans_info, days]}
    except Exception as e:
        return {'code': 400, 'data': str(e)}


@client.on(events.NewMessage(pattern=r'^(--|—)\d+$', outgoing=True))
async def get_id(event):
    try:
        info, num = "", re.findall(r'\d+', event.message.text)[0]
        cks = myck(_ConfigFile)
        if len(cks) == 0:
            info = "**你还没有cookie哦，请先添加**"
        elif int(num) > len(cks):
            info = f"**查询账号{num}不存在\n共有{len(cks)}个Cookie**"
        else:
            await event.edit("开始查询")
            cookie = cks[int(num) - 1]
            check = await checkCookie(cookie)
            if not check:
                info = f"**账号{num}查询失败、Cookie已失效**"
            else:
                totalBean = check if check != True else ""
                res = await BeanInfo(num, cookie)
                if res['code'] != 200:
                    info = f'{str(res["data"])}'
                else:
                    info += f"【**账号{num}**】\n【**今收入**】**{res['data'][0]}京豆**\n"
                    jxBean, UserInfo = res['data'][3], res['data'][4]
                    totalBean = totalBean if totalBean else (jxBean[0] if jxBean else "")
                    totalBean = totalBean if totalBean else (UserInfo[1] if UserInfo else "")
                    pulsInfo = UserInfo[2] if UserInfo else ""
                    if totalBean:
                        info += f"【**总京豆**】**{totalBean}京豆**\n"
                    if pulsInfo:
                        info += f"【**京享值**】**{pulsInfo}**\n"
                    info += "\n"
                    for i in res['data'][1]:
                        if res['data'][1][i] >= 20:
                            info += f"【{res['data'][1][i]}豆】{i}\n"
                    info += f"\n已隐藏20豆以下收入"

                    if len(res['data'][2]) > 0:
                        info += f"\n\n【**最新收入**】\n"
                        for i in range(len(res['data'][2])):
                            if i >= 3: break
                            t = re.sub(r'\d+-\d+-\d+\s*', '', res['data'][2][i]['date'])

                            time_struct = datetime.datetime.strptime(t, "%H:%M:%S")
                            time_sub = datetime.datetime.now() - datetime.datetime.combine(datetime.date.today(), time_struct.time())
                            m, s = divmod(time_sub.seconds, 60)
                            h, m = divmod(m, 60)
                            elapse = ('%d小时' % h if h else '') + ('%d分' % m if m else '') + ('%d秒' % s if s else '')

                            info += f"【{res['data'][2][i]['amount']}豆】{res['data'][2][i]['eventMassage']} **{t}** ({elapse}前)\n"
                    else:
                        info += "【**暂无最新收入**】"
        await event.edit(info)
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")


