# -*- coding:utf-8 -*-
import re
import aiohttp
from mirai import Mirai, WebSocketAdapter, GroupMessage, At, Plain, Image
from mirai.models import NudgeEvent, MemberMuteEvent, MemberUnmuteEvent, message
from mirai.models import MemberJoinEvent, MemberLeaveEventQuit, MemberLeaveEventKick
import requests
from plugins import plugin, meme, gamble, qa
import json
import random

bot_qq = 251744845 # 修改bot的QQ
bot = Mirai(qq=bot_qq, adapter=WebSocketAdapter(verify_key='QQWWEERRTTYY', host='localhost', port=8081))
admin = [1071779170] # 修改管理员的QQ
last_bvid = {}


@bot.on(GroupMessage)
async def full_plugin(event: GroupMessage):
    user = event.sender.id
    group = event.group.id
    user_name = event.sender.member_name
    group_name = event.group.name
    msg_chain = event.message_chain
    ask = str(event.message_chain)
    answer = None
    print(f'[鱼子酱]{user_name}@{group_name}\n内容:{ask}')

    if msg_chain.has(At):
        AtQQ = event.message_chain.get_first(At).target
        if '逮捕' in ask:
            answer = await meme.make_meme(AtQQ, [140, 140, 71, 88], 'dai')
        elif '吃掉' in ask:
            answer = await meme.make_meme(AtQQ, [160, 160, 92, 350], 'eat')
        elif '举起' in ask:
            answer = await meme.make_meme(AtQQ, [245, 245, 75, 2], 'ju')
        elif '啊打' in ask:
            answer = await meme.make_meme(AtQQ, [520,520,870,470], 'ada')
        elif '结婚' in ask:
            answer = await meme.make_meme(AtQQ, [640, 640, 0, 0], 'merry')
        elif '离婚' in ask:
            answer = await meme.make_meme(AtQQ, [1080,1080, 0, 0], 'lihun')
        elif '哈哈' in ask:
            answer = await meme.make_meme(AtQQ, [390,390, 400, 400], 'hahan')
        elif '摸摸' in ask:
            answer = await meme.petpet(AtQQ)
        elif '爱你' in ask:
            answer = await meme.love_you(AtQQ)
        elif '亲亲' in ask:
            answer = await meme.kiss(user, AtQQ)
        elif '丢丢' in ask:
            answer = await meme.diudiu(AtQQ)
        elif '拳拳' in ask:
            answer = await meme.boxing(AtQQ)
        elif '小可爱' in ask:
            at_id = msg_chain.get_first(At).target
            if at_id == bot_qq:
                answer = await meme.lovely('本酱', bot_qq)
            else:
                target = await bot.get_group_member(group, at_id)
                name = random.choice(target.member_name) * 2
                answer = await meme.lovely(name, AtQQ)     
        elif '击杀' in ask:
            target = await bot.get_group_member(group, msg_chain.get_first(At).target)
            if target is None:
                answer = await meme.jisha(user_name, '鱼子酱')
            else:
                answer = await meme.jisha(user_name, target.member_name)
        elif '黑名单' in ask:
            if user in admin:
                target = await bot.get_group_member(group, msg_chain.get_first(At).target)
                answer = f'已将{target.member_name}拉入黑名单,鱼子酱最讨厌这个人了'
        else:
            return

    else:
        if ask == '本周日历':
            return
            answer = await plugin.live_calendar()
        elif ask == '/list':
            answer = await plugin.list(group)
        elif ask == '占卜':
            answer = await gamble.tarot(user)
        elif ask == '抽卡':
            answer = await gamble.ssr(user)
        elif ask == '重开':
            answer = await gamble.restart(user)
        elif '变身' in ask:
            answer = await gamble.remake(ask, user_name)
        elif ask == '鱼子酱小故事':
            answer = await plugin.story()
        elif ask == '我是小可爱':
            name = random.choice(user_name) * 2
            answer = await meme.lovely(name, user)
        elif ask == '鱼鱼':
            answer = await meme.lovely('鱼鱼', 1071779170)

        elif re.findall('^[dD]{2}[bB][oO][tT]$', ask.strip()) != []:
            answer = "DDBOT项目地址\nhttps://github.com/Sora233/DDBOT\n部署指南\nhttps://github.com/Sora233/DDBOT/blob/master/INSTALL.md\n模板指南\nhttps://github.com/Sora233/DDBOT/blob/master/TEMPLATE.md\n指令示例\nhttps://github.com/Sora233/DDBOT/blob/master/EXAMPLE.md\nFAQ\nhttps://github.com/Sora233/DDBOT/blob/master/FAQ.md\ngitee镜像地址\nhttps://gitee.com/sora233/DDBOT\nDDBOT-您的QQ群单推小助手\nhttps://b23.tv/kabe7Ot\n群主手把手教程\nhttps://b23.tv/k9mmZU1"

        elif '举牌' == ask[0:2]:
            text = ask[2:58].strip()
            answer = await meme.jupai(text)

        elif '鱼子酱' in ask and '好不好' in ask:
            answer = await plugin.haobuhao(user)

        elif ask[0:4] == '呼叫鱼鱼':
            msg = f'收到反馈:\n{group_name}\n{user_name}\n\n{msg_chain}'
            await bot.send_friend_message(admin[0], msg)
            answer = '鱼子酱已经把内容转告鱼鱼了'

        elif '鱼子酱' in ask:
            answer = await qa.talk(user, user_name, ask)

        else:
            if user in admin:
                answer = await plugin.fuduji(0.01, msg_chain)
            else:
                answer = await plugin.fuduji(0.001, msg_chain)

    if answer:
        await bot.send(event, answer)


@bot.on(GroupMessage)
# 哔哩哔哩解析
async def bili_resolve(event: GroupMessage):
    global last_bvid
    text = str(event.message_chain.as_mirai_code)
    text = text.replace('\\n', '').replace('\\', '')
    if 'b23.tv/' in text:
        b23_url = re.findall('b23.tv/[A-Za-z0-9]+', text)[0]
        url = f'https://{b23_url}'
        resp = requests.get(url, allow_redirects=False)
        text = resp.text
    if(bv := re.search('[Bb][Vv][A-Za-z0-9]+', text))is not None:
        bvid = bv.group(0)
    elif(av := re.search('/[Aa][Vv]([0-9]+)', text))is not None:
        avid = int(av.group(1))
        table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        s=[11,10,3,8,4,6]
        avid=(avid^177451812)+8728348608
        r=list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]]=table[avid//58**i%58]
        bvid = ''.join(r)
    else:
        return
    if event.group.id in last_bvid.keys():
        last = last_bvid[event.group.id]
        if bvid == last['id'] or bvid in last['desc']:
            return
    bv_url = f'http://api.bilibili.com/x/web-interface/view?bvid={bvid}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=bv_url) as resp:
            data = await resp.json()
    if data['code'] != 0:
        return
    last_bvid[event.group.id] = {'id':bvid,'desc':data['data']['desc']}
    msg = await meme.bili_pic(data, bvid)
    await bot.send(event, msg)


@bot.on(GroupMessage)
async def use(event: GroupMessage):
    '''读取关键词'''
    with open(f'./statics/ask.json', 'r', encoding='UTF-8') as f:
        ask_data = json.load(f)
    for ask in ask_data:
        if str(event.message_chain) == ask:
            if ask_data[ask]["group"] == 0 or ask_data[ask]["group"] == event.group.id:
                msg = ask_data[ask]["answer"]
                if '[图片]' in msg:
                    text = msg.replace('[图片]', '')
                    path = f'./temp/ask/{ask}.jpg'
                    msg = message.MessageChain([Plain(text=text), Image(path=path)])
                await bot.send(event, msg)


@bot.on(GroupMessage)
# 关键词存删
async def add(event: GroupMessage):
    msg = str(event.message_chain)
    if '关键词' in msg and '&' in msg and event.sender.id in admin:
        if msg[0:5] == '添加关键词':
            group = 0
        elif msg[0:7] == '添加本群关键词':
            group = event.group.id
        else:
            return
        with open(f'./statics/ask.json', 'r', encoding='UTF-8') as f:
            ask_data = json.load(f)
        msg = msg.split('&')
        ask = msg[0].replace('添加本群关键词', '').replace('添加关键词', '')
        answer = msg[1]
        ask_data[ask] = {"answer": answer, "group": group}
        if '[图片]' in str(event.message_chain):
            images = event.message_chain[Image]
            filename = f'./temp/ask/{ask}.jpg'
            await images[0].download(filename=filename, determine_type=False)
        with open(f'./statics/ask.json', 'w', encoding='UTF-8') as f:
            json.dump(ask_data, f, ensure_ascii=False)
        await bot.send(event, "添加成功")

    if msg[0:5] == '删除关键词' and event.sender.id in admin:
        with open(f'./statics/ask.json', 'r', encoding='UTF-8') as f:
            ask_data = json.load(f)
        try:
            ask = msg[5:]
            del ask_data[ask]
            with open(f'./statics/ask.json', 'w', encoding='UTF-8') as f:
                json.dump(ask_data, f, ensure_ascii=False)
            await bot.send(event, "删除成功")
        except:
            await bot.send(event, "删除失败")
            return
    if msg == '关键词列表' and event.sender.id in admin:
        with open(f'./statics/ask.json', 'r', encoding='UTF-8') as f:
            ask_data = json.load(f)
        msg = '关键词列表'
        for ask in ask_data:
            useable = '(本群不可用)'
            if ask_data[ask]["group"] == 0 or ask_data[ask]["group"] == event.group.id:
                useable = '(本群可用)'
            msg = msg + '\n' + ask + '   ' + useable
        await bot.send(event, msg)



@bot.on(NudgeEvent)
async def handle_nudge(event: NudgeEvent):
    entity = await bot.get_entity(event.subject)
    AtQQ = event.target
    msg = await meme.petpet(AtQQ)
    await bot.send_group_message(entity.id, msg)

@bot.on(MemberMuteEvent)
async def handle__mute(event: MemberMuteEvent):
    member_name = event.member['memberName']
    group = event.member['group']['id']
    mute_time = event.duration_seconds
    rely = f'{member_name} 喝下了{mute_time}杯红茶'
    await bot.send_group_message(group, rely)

@bot.on(MemberUnmuteEvent)
async def handle__unmute(event: MemberUnmuteEvent):
    member_name = event.member.member_name
    group = event.group.id
    rely = f'{member_name} 发誓改过自新,重新做人'
    await bot.send_group_message(group, rely)

@bot.on(MemberJoinEvent)
async def handle__welcome(event: MemberJoinEvent):
    member_name = event.member.member_name
    group = event.group.id
    group_name = event.group.name
    rely = f'欢迎{member_name}加入{group_name}'
    await bot.send_group_message(group, rely)

@bot.on(MemberLeaveEventQuit)
async def handle_quit(event: MemberLeaveEventQuit):
    member_name = event.member.member_name
    group = event.group.id
    rely = f'o~ya~su~mi~\n{member_name}'
    await bot.send_group_message(group, rely)

@bot.on(MemberLeaveEventKick)
async def handle_kick(event: MemberLeaveEventKick):
    member_name = event.member.member_name
    group = event.group.id
    rely = f'o~ya~su~mi~\n{member_name}\n🕯️'
    await bot.send_group_message(group, rely)


bot.run(host='127.0.0.1', port=8003)
