# -*- coding:utf-8 -*-
import time
from PIL import Image as IMG
from PIL import ImageDraw, ImageFont
from io import BytesIO
from mirai import Image, Plain
from mirai.models import message
import numpy as np
import base64
import aiohttp
import imageio
import random
import os
import qrcode
import time


async def build_gif_msg(frames, duration):
    '''图片帧转消息链'''
    output = BytesIO()
    imageio.mimsave(output, frames, format="gif", duration=duration)
    byte_data = output.getvalue()
    base64_str = base64.b64encode(byte_data)
    return message.MessageChain([Image(base64=base64_str)])


async def get_head(qq):
    '''获取QQ头像'''
    url = f'http://q1.qlogo.cn/g?b=qq&nk={qq}&s=640'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:
            operator_img = await resp.read()
    return IMG.open(BytesIO(operator_img))


async def kiss_make_frame(operator, target, i):
    operator_x = [92, 135, 84, 80, 155, 60, 50, 98, 35, 38, 70, 84, 75]
    operator_y = [64, 40, 105, 110, 82, 96, 80, 55, 65, 100, 80, 65, 65]
    target_x = [58, 62, 42, 50, 56, 18, 28, 54, 46, 60, 35, 20, 40]
    target_y = [90, 95, 100, 100, 100, 120, 110, 100, 100, 100, 115, 120, 96]
    bg = IMG.open(f"./statics/meme/KissKiss/KissFrames/{i}.png")
    gif_frame = IMG.new('RGB', (200, 200), (255, 255, 255))
    gif_frame.paste(bg, (0, 0))
    gif_frame.paste(target, (target_x[i - 1], target_y[i - 1]), target)
    gif_frame.paste(operator, (operator_x[i - 1], operator_y[i - 1]), operator)
    return gif_frame


async def kiss(operator_id, target_id):
    '''亲亲'''
    operator = await get_head(operator_id)
    operator = operator.resize((40, 40), IMG.ANTIALIAS)
    if operator.mode == 'RGBA':
        imn = IMG.new('RGB', (40, 40), (255, 255, 255))
        imn.paste(operator, (0, 0), operator)
        operator = imn
    size = operator.size
    r2 = min(size[0], size[1])
    circle = IMG.new('L', (r2, r2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, r2, r2), fill=255)
    alpha = IMG.new('L', (r2, r2), 255)
    alpha.paste(circle, (0, 0))
    operator.putalpha(alpha)

    target = await get_head(target_id)
    target = target.resize((50, 50), IMG.ANTIALIAS)
    if target.mode == 'RGBA':
        imn = IMG.new('RGB', (50, 50), (255, 255, 255))
        imn.paste(target, (0, 0), target)
        target = imn
    size = target.size
    r2 = min(size[0], size[1])
    circle = IMG.new('L', (r2, r2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, r2, r2), fill=255)
    alpha = IMG.new('L', (r2, r2), 255)
    alpha.paste(circle, (0, 0))
    target.putalpha(alpha)

    gif_frames = []
    for i in range(1, 14):
        gif_frames.append(await kiss_make_frame(operator, target, i))
    return await build_gif_msg(gif_frames, 0.03)


async def Boxing_make_frame(target, i):
    target_x = [-10, 0, 10, 20, 30, 40, 50, 60, 50, 40, 30, 50, 10, 0]
    target_y = [30, 20, 10, 0, 0, 10, 20, 30, 20, 10, 0, 10, 20, 30]
    bg = IMG.open(f"./statics/meme/Boxing/{i}.png")
    gif_frame = IMG.new('RGB', (260, 230), (255, 255, 255))
    gif_frame.paste(
        target, (target_x[i - 1] - 40, target_y[i - 1] - 60), target)
    gif_frame.paste(bg, (0, -30), bg)
    return gif_frame


async def boxing(target_id):
    '''打拳'''
    target = await get_head(target_id)
    target = target.convert('RGBA')
    target = target.resize((280, 280), IMG.ANTIALIAS)
    gif_frames = []
    for i in range(1, 14):
        gif_frames.append(await Boxing_make_frame(target, i))
    return await build_gif_msg(gif_frames, 0.04)


async def Diu_make_frame(target, i):
    bg = IMG.open(f"./statics/meme/diu.png")
    gif_frame = IMG.new('RGB', (512, 512), (255, 255, 255))
    temp = target.rotate(45 * i)
    gif_frame.paste(temp, (10, 176), temp)
    gif_frame.paste(bg, (0, 0), bg)
    return gif_frame


async def diudiu(target_id):
    '''丢丢'''
    target = await get_head(target_id)
    target = target.convert('RGBA')
    target = target.resize((150, 150), IMG.ANTIALIAS)
    gif_frames = []
    for i in range(0, 8):
        gif_frames.append(await Diu_make_frame(target, i))
    return await build_gif_msg(gif_frames, 0.04)


async def make_pet_frame(avatar, i):
    frame_spec = [[15, 20, 120, 125], [10, 35, 125, 125], [
        5, 50, 130, 125], [10, 35, 125, 125], [15, 20, 120, 125]]
    spec = frame_spec[i]
    hand = IMG.open(f'./statics/meme/PetPet/frame{i}.png')
    avatar = avatar.resize(
        (int((spec[2] - spec[0]) * 1), int((spec[3] - spec[1]) * 1)), IMG.ANTIALIAS)
    gif_frame = IMG.new('RGB', (112, 112), (255, 255, 255))
    gif_frame.paste(avatar, (spec[0], spec[1]), avatar)
    gif_frame.paste(hand, (0, 0), hand)
    return gif_frame


async def petpet(member_id):
    '''摸头'''
    avatar = await get_head(member_id)
    avatar = avatar.convert('RGBA')
    gif_frames = []
    for i in range(5):
        gif_frames.append(await make_pet_frame(avatar, i))
    return await build_gif_msg(gif_frames, 0.04)


async def make_love_frame(avatar, i):
    locs = [(68, 65, 70, 70), (63, 59, 80, 80)]
    x, y, w, h = locs[i]
    heart = IMG.open(f"./statics/meme/love_you/{i}.png")
    heart = heart.convert('RGBA')
    img = avatar.resize((w, h), IMG.ANTIALIAS)
    gif_frame = IMG.new("RGB", (205, 205), (255, 255, 255))
    gif_frame.paste(img, (x, y), img)
    gif_frame.paste(heart, (0, 0), heart)
    return gif_frame


async def love_you(member_id):
    '''永远爱你'''
    avatar = await get_head(member_id)
    avatar = avatar.convert('RGBA')
    gif_frames = []
    for i in range(2):
        gif_frames.append(await make_love_frame(avatar, i))
    return await build_gif_msg(gif_frames, 0.25)


async def make_pound_frame(avatar, i):
    locs = [(135, 240, 138, 47), (135, 240, 138, 47), (150, 190, 105, 95), (150, 190, 105, 95),(148, 188, 106, 98), (146, 196, 110, 88), (145, 223, 112, 61), (145, 223, 112, 61)]
    x, y, w, h = locs[i]
    mask = IMG.open(f"./statics/meme/pound/{i}.png")
    mask = mask.convert('RGBA')
    gif_frame = IMG.new("RGB", (500, 400), (255, 255, 255))
    img = avatar.resize((w, h), IMG.ANTIALIAS)
    gif_frame.paste(img, (x, y), img)
    gif_frame.paste(mask, (0, 0), mask)
    return gif_frame


async def pound(member_id):
    '''捣'''
    avatar = await get_head(member_id)
    avatar = avatar.convert('RGBA')
    gif_frames = []
    for i in range(8):
        gif_frames.append(await make_pound_frame(avatar, i))
    return await build_gif_msg(gif_frames, 0.05)


async def make_meme(AtQQ, paste_info, back_path):
    '''静态表情包制作并生成消息链'''
    path = f'./statics/meme/{back_path}.png'
    avatar = await get_head(AtQQ)
    avatar = avatar.convert('RGBA')
    avatar = avatar.resize((paste_info[0], paste_info[1]), IMG.ANTIALIAS)
    back_pic = IMG.open(path)
    img = IMG.new('RGB', (back_pic.size[0], back_pic.size[1]), (255, 255, 255))
    img.paste(avatar, (paste_info[2], paste_info[3]), avatar)
    img.paste(back_pic, (0, 0), back_pic)
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return message.MessageChain([Image(base64=base64_str)])


async def jisha(user, target):
    '''击杀图片生成消息链'''
    gun_file = random.choice(['ak47', 'awp', 'bizon', 'knife'])
    gun = f'./statics/meme/cs/{gun_file}.jpg'
    font = ImageFont.truetype('./statics/font/out.ttf', 30)
    width, height = font.getsize(user)
    width2, height2 = font.getsize(target)
    img_gun = IMG.open(gun)
    width3, height3 = img_gun.size
    x = width + width2 + width3 + 30
    img = IMG.new('RGB', (x, 50), (255, 0, 0))
    img_bg = IMG.new('RGB', (x - 8, 42), (71, 71, 71))
    img.paste(img_bg, (4, 4))
    img.paste(img_gun, (width + 10, 9))
    draw = ImageDraw.Draw(img)
    draw.text((4, 8), user, font=font, fill=(255, 255, 255))
    draw.text((width + width3 + 24, 8), target,
              font=font, fill=(255, 255, 255))
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return message.MessageChain([Image(base64=base64_str)])


def find_coeffs(pa, pb):
    '''图片扭曲变形'''
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -
                      p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -
                      p2[1] * p1[0], -p2[1] * p1[1]])
    A = np.matrix(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)
    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)


async def bian(user):
    '''看扁了'''
    avatar = await get_head(user)
    avatar = avatar.convert('RGBA')
    avatar = avatar.resize((200, 200), IMG.ANTIALIAS)
    p = random.randint(0, 100)
    coeffs = find_coeffs([(0, 0), (200, 0), (200, 200), (0, 200)], [(0, 0), (200, 0), (200 - p, 200), (p, 200)])
    avatar = avatar.transform((200, 200), IMG.PERSPECTIVE, coeffs, IMG.BICUBIC)
    output_buffer = BytesIO()
    avatar.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return message.MessageChain([Plain(text=f'你被看扁了{p}%'), Image(base64=base64_str)])



async def jupai(text):
    '''举牌'''
    if text == '':
        return
    font = ImageFont.truetype('./statics/font/shs_and_emoji.ttf', 40)
    pic_list = []
    for i in text:
        width, height = font.getsize(i)
        back = random.choice(os.listdir('./statics/meme/jupai'))
        path = f'./statics/meme/jupai/{back}'
        img = IMG.open(path)
        word = IMG.new('RGBA', (63, 42), (255, 255, 255, 1))
        draw = ImageDraw.Draw(word)
        draw.text((20 - width / 2, 20 - height / 2),
                  i, font=font, fill=(0, 0, 0))
        coeffs = find_coeffs([(29, 0), (63, 14), (34, 42), (0, 28)], [
                             (0, 0), (63, 0), (63, 42), (0, 42)])
        word = word.transform((63, 42), IMG.PERSPECTIVE, coeffs, IMG.BICUBIC)
        img.paste(word, (14, 9), word)
        pic_list.append(img)
    text_num = len(pic_list) - 1
    lines = int(text_num / 8)
    last = text_num % 8
    if lines == 0:
        x = last * 55 + 80
        y = last * 21 + 165
    else:
        x = lines * 45 + 465
        y = max(lines * 45 + last * 21 + 165, (lines - 1) * 45 + 312)
    out = IMG.new('RGBA', (x, y), (255, 255, 255, 1))
    k = 0
    for i in pic_list:
        no_x = k % 8
        no_y = int(k / 8)
        out.paste(i, (no_x * 55 + (lines - no_y)
                  * 45, no_y * 45 + no_x * 21), i)
        k += 1
    output_buffer = BytesIO()
    out.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return message.MessageChain([Image(base64=base64_str)])

async def bili_pic(data, bvid):
    bili_url = f'https://www.bilibili.com/video/{bvid}'
    qr = qrcode.QRCode(box_size=3, border=2)
    qr.add_data(bili_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#000000")
    pubtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['data']['pubdate']))
    head_url = data['data']['owner']['face']
    title = data['data']['title']
    up = f"{data['data']['owner']['name']}(UID:{data['data']['owner']['mid']})"
    view = f"{data['data']['stat']['view']}次观看  发布时间:{pubtime}"
    img_url = data['data']['pic']
    async with aiohttp.ClientSession() as session:
        async with session.get(url=img_url) as resp:
            img_content = await resp.read()
    pic = IMG.open(BytesIO(img_content))
    async with aiohttp.ClientSession() as session:
        async with session.get(url=head_url) as resp:
            img_content = await resp.read()
    head = IMG.open(BytesIO(img_content))
    height = int(1920 * pic.size[1] / pic.size[0])
    width = int(200 * head.size[0] / head.size[1])
    pic = pic.resize((1920, height),IMG.ANTIALIAS)
    head = head.resize((width, 200),IMG.ANTIALIAS)
    img = IMG.new('RGB',(1920,height+200),(255,255,255))
    img.paste(pic,(0,200))
    img.paste(head)
    draw = ImageDraw.Draw(img)
    font0 = ImageFont.truetype('./statics/font/shs_and_emoji.ttf', 50)
    draw.text((width + 20,15),title,font=font0, fill=(0, 0, 0))
    draw.text((width + 20,75),up,font=font0, fill=(0, 0, 0))
    draw.text((width + 20,135),view,font=font0, fill=(0, 0, 0))
    qr_width = qr_img.pixel_size
    img.paste(qr_img, (1920 - qr_width, 200 - qr_width))
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return message.MessageChain([Plain(text=bvid), Image(base64=base64_str)])


async def lovely(name, user):
    '''小天使图片'''
    img = IMG.new('RGB', (768, 950), (255, 255, 255))
    avatar = await get_head(user)
    avatar = avatar.convert('RGBA')
    avatar = avatar.resize((640, 640), IMG.ANTIALIAS)
    img.paste(avatar,(64, 140),avatar)
    draw = ImageDraw.Draw(img)
    font0 = ImageFont.truetype('./statics/font/shs_and_emoji.ttf', 70)
    text0 = f"请问你们看到{name}了吗?"
    text_w, _ = font0.getsize(text0)
    draw.text((384 - text_w / 2, 40), text0, font=font0, fill=(0, 0, 0))
    font1 = ImageFont.truetype('./statics/font/shs_and_emoji.ttf', 60)
    draw.text((24, 811), "非常可爱！简直就是小天使", font=font1, fill=(0, 0, 0))
    font2 = ImageFont.truetype('./statics/font/shs_and_emoji.ttf', 33)
    draw.text((31, 880), "她没失踪也没怎么样  我只是觉得你们都该看一下", font=font2, fill=(0, 0, 0))
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return message.MessageChain([Image(base64=base64_str)])


async def food():
    '''随机食物'''
    path = './statics/food'
    food_num = random.randint(1, 4)
    food_list = random.sample(os.listdir(path), food_num)
    img = IMG.open(f'./statics/food_zn.jpg')
    x = 0
    y = 0
    for i in food_list:
        food_path = f'{path}/{i}'
        food_img = IMG.open(food_path)
        img.paste(food_img, (x, y), food_img)
        x += 100
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return message.MessageChain([Image(base64=base64_str)])

