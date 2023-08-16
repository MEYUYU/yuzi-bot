# -*- coding:utf-8 -*-
from mirai import Image, Plain
from mirai.models import message
import random
import os
import difflib
import json

path = f'./statics/qaall.json'
with open(path, 'r', encoding='utf-8') as json_file:
    bbb = json.load(json_file)

async def talk(user, name, ask):
    '''聊天'''
    ban_word = ['小故事', '变身']
    img_path = './statics/face'
    vip = {1071779170: ['小可爱', '鱼鱼', 'darling'], 2380542703: ['路路', '妈妈'], 2897652833: ['老爷'], 184467050: ['碘酒', '殿九', '哥哥'], 120201995: ["爸爸"], 108720516: ['哥哥', 'giegie'], 3211713368: ['suo酱'], 824713628: ['厨子', '宝贝'], 1196839699: ['老婆'], 2702099379: ['大可爱', '思思妈妈']}
    for i in ban_word:
        if i in ask:
            return
    answer = ''
    if user in vip.keys():
        target_name = random.choice(vip[user])
    else:
        target_name = random.choice([name, '你', '你这家伙'])
    if ask == '鱼子酱':
        answer = random.choice(['{name}叫我干嘛呀~', '我在呢{name}', '什么事呀{name}'])
    else:
        answers = []
        last_score = 0
        for i in bbb:
            text = list(i.keys())[0]
            if text not in ask:
                continue
            score = difflib.SequenceMatcher(None, text, ask.replace("鱼子酱", "")).quick_ratio()
            if score > last_score:
                answers = list(i.values())
                last_score = score
            elif score == last_score and score > 0:
                answers += list(i.values())
        if answers:
            answer = random.choice(answers).replace("{me}", "鱼子酱").replace("{name}", target_name).replace("{segment}", "\n")
            # answer = answer + "\n\n匹配度" + str(last_score) + "\n" + str(len(answers)) + "个匹配结果"
    if ask == '鱼子酱我饿了':
        answer = '吃吧,鱼子酱请你吃'
        img_path = './statics/food'
    if answer == '':
        answer = random.choice(
            ['鱼子酱还会其他的技能哦\n{name}可以使用指令\n<鱼子酱让我看看>查看', '', '', '', '', '', '', '', '', '', ''])
    answer = answer.replace('{name}', target_name)
    imgs = random.choice(os.listdir(img_path))
    path = f'{img_path}/{imgs}'
    if answer == '':
        return message.MessageChain([Image(path=path)])
    else:
        return message.MessageChain([Plain(text=answer), Image(path=path)])

