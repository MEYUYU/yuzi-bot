# -*- coding: utf-8 -*-
import httpx
import json
import time
from html2image import Html2Image
from nonebot.plugin import on_startswith
from nonebot.adapters import Bot, Event

vup_num = on_startswith('查成分')


@vup_num.handle()
async def _(bot: Bot, event: Event):
    uid = str(event.message).replace('查成分', '').replace(' ', '').replace('UID:', '')
    if not uid.isdigit():
        resp = httpx.get(f'http://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&keyword={uid}', timeout=10)
        userinfo = resp.json()
        if userinfo['data']['numResults'] == 0:
            return
        else:
            uid = userinfo['data']['result'][0]['mid']
    resp = httpx.get(f'https://account.bilibili.com/api/member/getCardByMid?mid={uid}', timeout=10)
    ret = resp.json()
    if ret['code'] != 0:
        return
    card = ret['card']
    cookies = {"SESSDATA": "请修改", "bili_jct": "请修改"}
    resp = httpx.get(f'https://api.live.bilibili.com/xlive/web-ucenter/user/MedalWall?target_id={uid}', cookies=cookies, timeout=10)
    medal = resp.json()
    medal_list = {}
    if medal['code'] != 0:
        print('检查cookie')
        return
    if medal['data']['count'] > 0:
        for i in medal['data']['list']:
            name = f"{i['target_name']}({i['medal_info']['target_id']})[{i['medal_info']['medal_name']} lv{i['medal_info']['level']}]"
            medal_list[str(i['medal_info']['target_id'])] = name
    vtbs = []
    print(medal_list)
    with open(f'./statics/vtbs.json', 'r', encoding='UTF-8') as f:
        vtbs_data = json.load(f)
    for mid in card['attentions']:
        mid = str(mid)
        if mid in vtbs_data:
            if mid in medal_list:
                vtb = medal_list[mid]
                vtbs.append(vtb)
                continue
            vtb = vtbs_data[mid]
            vtbs.append(f"{vtb['uname']}({mid})")
    count = len(card['attentions'])
    vtb_count = len(vtbs)
    if count == 0:
        percent = '0%'
    else:
        percent = '{:.2%}'.format(vtb_count / count)
    vtb_msg = '<br>'.join(vtbs)
    regtime = card['regtime']
    fans = card['fans']
    follow = card['attention']
    face = card['face']
    name = card['name']
    mid = card['mid']
    timeArray = time.localtime(regtime)
    regtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    msg = f'<!DOCTYPE html><html><head><title>JcMan</title></head><body><p style="width:600px"><img align="left"style="overflow:scroll;margin-top:2px;margin-bottom:0;margin-left:10px;margin-right:20px;width:120px;height:120px;border-radius:60px;object-fit:cover"src="{face}"></p><p style="font-size:30px;margin-top:40px;margin-bottom:0;font-family:sans-serif">{name}<br>UID:{mid}</p><p></p><p style="display: -webkit-box;-webkit-box-orient: vertical;-webkit-line-clamp: 2;word-wrap: break-word;overflow: hidden;font-size:40px;margin-left:40px;margin-right:40px;margin-top:2px;margin-bottom:0;font-family:sans-serif">{percent}({vtb_count}/{count})</p><p style="display: -webkit-box;-webkit-box-orient: vertical;-webkit-line-clamp: 500;word-wrap: break-word;overflow: hidden;font-size:20px;margin-left:40px;margin-right:40px;font-family:sans-serif">注册时间:{regtime}<br>粉丝:{fans} 关注:{follow}<br><br>{vtb_msg}</p></body></html>'
    y = min(int(250 + 26.2 * (vtb_count + 4)), 13400)
    pic_name = f'bili_{uid}.jpg'
    hti = Html2Image(custom_flags=['--hide-scrollbars'], size=(540, y), output_path='C:/temp/DD')
    hti.screenshot(html_str=msg, save_as=pic_name)
    path = f'file:///C:/temp/DD/{pic_name}'
    rely = [{"type": "image", "data": {"file": path}}]
    await vup_num.finish(rely)
