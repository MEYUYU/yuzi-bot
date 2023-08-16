# -*- coding:utf-8 -*-
from mirai import Image, Plain, At, Face
from mirai.models import message
from PIL import Image as IMG
from PIL import ImageDraw, ImageFont
from linecache import getline
from io import BytesIO
import datetime
import random
import json
import os
import base64
import math


async def live_calendar():
    '''本周日历'''
    week = {0: '星期一', 1: '星期二', 2: '星期三', 3: '疯狂星期四', 4: '星期五', 5: '星期六', 6: '星期日'}
    text = f'今天是{week[datetime.datetime.now().weekday()]}'
    return message.MessageChain([Plain(text=text), Image(path=str('./temp/日历.png'))])


async def list(group):
    '''/list响应'''
    if group in [692222134, 1048144311]:
        imgs = random.choice(os.listdir('./statics/face'))
        path = f'./statics/face/{imgs}'
        text='暂无订阅，可以使用/watch命令订阅'
        return message.MessageChain([Plain(text=text)]) 
    else:
        return


async def story():
    '''鱼子酱小故事'''
    num = random.randint(1, 352)
    story = getline('./statics/story.txt', num).replace("\\n", "\n")
    return (f"{story}小朋友们，你学会了吗？")

def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0,len(obj),sec)]

async def talk(user, name, ask):
    '''聊天'''
    ban_word = ['小故事', '变身']
    vip = {1071779170: ['小可爱', '鱼鱼', 'darling'], 2380542703: ['路路', '妈妈'], 2897652833: ['老爷'], 184467050: ['碘酒', '殿九', '哥哥'], 120201995: [
        "爸爸"], 108720516: ['哥哥', 'giegie'], 3211713368: ['suo酱'], 824713628: ['厨子', '宝贝'], 1196839699: ['老婆'], 2702099379: ['大可爱', '思思妈妈']}
    for i in ban_word:
        if i in ask:
            return
    answer = ''
    if user in vip.keys():
        target_name = random.choice(vip[user])
    else:
        target_name = random.choice([name, '', ''])
    if ask == '鱼子酱':
        answer = random.choice(['**叫我干嘛呀~', '我在呢**', '什么事呀**'])
    else:
        path = f'./statics/anime.json'
        with open(path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        for i in data:
            if i in ask:
                repo = data.get(i, str())
                answer = random.choice(repo)
    if answer == '':
        answer = random.choice(
            ['鱼子酱还会其他的技能哦\n**可以使用指令\n<鱼子酱让我看看>查看', '', '', '', '', '', '', '', '', '', ''])
    answer = answer.replace('**', target_name)
    imgs = random.choice(os.listdir('./statics/face'))
    path = f'./statics/face/{imgs}'
    if answer == '':
        return message.MessageChain([Image(path=path)])
    else:
        '''font_size = 70
        border = 0
        font = ImageFont.truetype('./statics/font/shs_and_emoji.ttf', font_size)
        if '\n' in answer:
            answer_list = answer.split('\n')
        else:
            ii = 1
            while len(answer) / ii > 12:
                ii += 1
            numm = math.ceil(len(answer) / ii)
            answer_list = cut(answer, numm)
        x = 0
        for i in answer_list:
            w, h = font.getsize(i)
            if x <= w:
                x = w
        face = IMG.open(path)
        y = int(x * face.size[1] / face.size[0])
        face = face.resize((x, y), IMG.ANTIALIAS)
        img = IMG.new('RGB', (x + border *2, y + font_size * len(answer_list) + border), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        img.paste(face, (border, len(answer_list)*font_size+border))
        line = 0
        for i in answer_list:
            draw.text((border, line * font_size + border), i, font=font, fill=(0, 0, 0))
            line += 1
        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)
        return message.MessageChain([Image(base64=base64_str)])'''
        return message.MessageChain([Plain(text=answer), Image(path=path)])



async def fuduji(chance, msg_chain):
    '''复读机'''
    if len(msg_chain) == 1:
        return
    for i in msg_chain:
        if i.type not in ['Plain', 'Face', 'Source']:
            return
    ban_word = ['网易云音乐', 'QQ音乐', '体验新功能', '暂不支持', '暂无订阅']
    for i in ban_word:
        if i in str(msg_chain):
            return
    if random.random() < chance:
        return msg_chain


async def haobuhao(user):
    hao = random.randint(0, 100)
    buhao = random.randint(0, 100)
    text =  f'\n好的概率是:{hao}%\n不好的概率:{buhao}%\n'
    if hao > buhao:
        text += '鱼子酱觉得好'    
    elif hao< buhao:
        text += '鱼子酱觉得不好'
    else:
        text += '鱼子酱觉得你可以再问一次'
    return message.MessageChain([At(user), Plain(text=text)])