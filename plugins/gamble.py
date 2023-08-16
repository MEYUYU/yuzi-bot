# -*- coding:utf-8 -*-
from mirai import Image, Plain, At, Face
from mirai.models import message
import random
from PIL import ImageFont, ImageDraw, Image as IMG
import numpy as np
from io import BytesIO
import base64
import os


async def tarot(user):
    img_path = f'./statics/tarot'
    card = f'tarot{random.randint(1,53)}'
    if card == 'tarot53':
        imgs = [f'{card}.jpg']
        card = f'{card}-'
        for sp in os.listdir(img_path):
            if card in sp:
                imgs.append(sp)
        selected_img = random.sample(imgs, 1)
        path = str(f'./statics/tarot/{selected_img[0]}')
    else:
        path = str(f'./statics/tarot/{card}.jpg')
    return message.MessageChain([At(user), Image(path=path)])


async def ssr(user):
    img = IMG.new('RGB', (475, 570), (255, 255, 255))
    rares = ['R', 'SR', 'SSR']
    chances = [23.0, 65.0, 12.0]
    p = np.array(chances)
    p /= p.sum()
    for num in range(0, 10):
        rare = np.random.choice(rares, p=p.ravel())
        if rare == 'R':
            card = random.choice(['01', '02', '03', '04', '05', '06'])
        elif rare == 'SR':
            card = random.choice(['07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'])
        else:
            card = random.choice(['20', '21', '22', '23', '24', '25', '26', '27'])
        img_path = f'./statics/dona/{card}.png'
        cardimg = IMG.open(img_path)
        img.paste(cardimg, (num % 5 * 95, int(num / 5) * 285))
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return message.MessageChain([At(user), Image(base64=base64_str)])


async def restart(user):
    statics_path = './statics/reborn'
    difficulty = random.choice(['bad','bad','good','good','normal','origin','origin','origin','origin','origin'])
    img_path = f'{statics_path}/{difficulty}'
    score = 100
    img = IMG.new('RGB', (1080, 1480), (230, 220, 210))
    font1 = ImageFont.truetype(f'{statics_path}/xiao.ttf', 30)
    font2 = ImageFont.truetype(f'{statics_path}/xiao.ttf', 100)
    font3 = ImageFont.truetype(f'{statics_path}/xiao.ttf', 60)
    num = 1
    world_path = f'{img_path}/world'
    card_list = []
    for yy in os.listdir(world_path):
        if '001' in yy:
            card_list.append(yy)
    card = random.choice(card_list)
    pic_card = IMG.open(f'{world_path}/{card}')
    img.paste(pic_card, (0, 320))
    score += int(card[3:].replace('.jpg', ''))
    if card == '001+20.jpg':
        last_world_list = ['002', '006', '004', '005']
    else:
        last_world_list = ['002', '003', '004', '005']
    for xx in last_world_list:
        card_list = []
        for yy in os.listdir(world_path):
            if xx in yy:
                card_list.append(yy)
        card = random.choice(card_list)
        pic_card = IMG.open(f'{world_path}/{card}')
        img.paste(pic_card, (num * 180, 320))
        num += 1
        score += int(card[3:].replace('.jpg', ''))
    num = 0
    for self in ['101', '102', '103', '104', '105', '106']:
        card_list = []
        for yy in os.listdir(f'{img_path}/self'):
            if self in yy:
                card_list.append(yy)
        rank = random.choice(card_list)
        pic_self = IMG.open(f'{img_path}/self/{rank}')
        img.paste(pic_self, (num * 180, 740))
        num += 1
        score += int(rank[3:].replace('.jpg', ''))
    attribute_path = f'{img_path}/attribute'
    attributes_num = random.randint(2, 6)
    attributes = random.sample(os.listdir(attribute_path), attributes_num)
    num = 0
    for attribute in attributes:
        pic_attribute = IMG.open(f'{attribute_path}/{attribute}')
        img.paste(pic_attribute, (num * 180, 1160))
        num += 1
        score += int(attribute[3:].replace('.jpg', ''))
    draw = ImageDraw.Draw(img)
    # time2 = str(int(time.time()*1000000))
    draw.text((30, 8), 'No.' + str(user), font=font1, fill=(0, 0, 0))
    # draw.text((30, 8), 'No.' + time2, font=font1, fill=(0, 0, 0))
    draw.text((120, 60), '重开设定(绝密)ver2', font=font2, fill=(0, 0, 0))
    draw.text((400, 10), '难度评分：' + str(score), font=font3, fill=(0, 0, 0))
    draw.text((280, 260), '（种族/性别/局势/审美/开局）', font=font1, fill=(0, 0, 0))
    draw.text((30, 220), '世界设定', font=font3, fill=(0, 0, 0))
    draw.text((280, 680), '（力量/魔力/智力/体质/魅力/运气）', font=font1, fill=(0, 0, 0))
    draw.text((30, 640), '基础能力', font=font3, fill=(0, 0, 0))
    draw.text((30, 1060), '特质', font=font3, fill=(0, 0, 0))
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return message.MessageChain([At((user)), Image(base64=base64_str)])


async def remake(ask, user_name):
    if ask[0:2] == '变身':
        return f'{user_name}变身失败了，大概是因为没有念羞耻的台词吧，试一试使用<羞耻的台词+变身>'
    elif '变身' in ask[-4:]:
        dead_reason = random.choice(['走在马路上被泥头车创了', '被天上飞过的巨龙掉下来砸死', '被青梅竹马用柴刀剁了', '探索太空的时候氧气耗尽', '被黑洞吸入了', '上厕所在马桶上触发了传送', '被智障女神选中', '加班过度，睡了过去', '被原子弹打中了', '改了个名叫龙傲天后第二天', '被自己的手机吸了进去', '用手指测试插座有没有电', '掉进了没有井盖的下水道', '沉迷纸片人，忘了吃饭', '练习混元太极拳走火入魔', '吃瓜的时候被西瓜子呛死', '与罕见对喷被气死', '扭蛋十连金兴奋到昏迷'])
        text = f'{user_name}{dead_reason}，穿越到了异世界，变身成了二次元少女，长这样'
        img_path = f'./statics/remake'
        imgs = random.choice(os.listdir(img_path))
        path = f'./statics/remake/{imgs}'
        return message.MessageChain([Plain(text=text), Image(path=path)])
    else:
        return