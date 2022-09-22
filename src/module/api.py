#
# module\api.py | YDITS for Discord
#
# (c) 2022 よね/Yone
# licensed under the Apache License 2.0
#

import json
import requests


# ---------- Functions ---------- #
async def get_p2p():

    url = 'https://api.p2pquake.net/v2/history/'

    params = {
      'zipcode': '',
      'codes': '551',
      'limit': '1'
    }

    #取得
    try:
        res = requests.get(url, params=params, timeout=3.0)

    #取得失敗時
    except Exception as e:
        return 0x0301, e


    # --- ステータス処理 --- #

    #200
    if res.status_code == 200:
        #デシリアライズ
        try:
            data = json.loads(res.text)
        
        #デシリアライズ失敗時
        except Exception:
            return 0x0302, None

    #429
    elif res.status_code == 429:
        return 0x0303, None

    #Other
    else:
        return 0x0304, res.status_code


    # --- アクセス --- #

    try:
        #time
        eq_time = data[0]['issue']['time']

        eq_timeYear   = eq_time[0:4]
        eq_timeMonth  = eq_time[5:7]
        eq_timeDay    = eq_time[8:10]
        eq_timeHour   = eq_time[11:13]
        eq_timeMinute = eq_time[14:16]
        eq_timeSecond = eq_time[17:19]

        #type
        eq_type = data[0]['issue']['type']

        eq_types = {
            'ScalePrompt': "震度速報",
            'Destination': "震源情報",
            'ScaleAndDestination': "震源・震度情報",
            'DetailScale': "各地の震度情報",
            'Foreign': "遠地地震情報",
            'Other': "地震情報"
        }

        if eq_type in eq_types:
            eq_type = eq_types[eq_type]

        #hypocenter
        eq_hypo = data[0]['earthquake']['hypocenter']['name']

        if eq_hypo == '':
            if eq_type == "震源情報" or "遠地地震情報":
                eq_hypo = "情報なし"
            else:
                eq_hypo = "調査中"

        #maxScale
        eq_maxScale = data[0]['earthquake']['maxScale']

        Scales = {
            -1: '調査中',
            10: '1',
            20: '2',
            30: '3',
            40: '4',
            45: '5弱',
            50: '5強',
            55: '6弱',
            60: '6強',
            70: '7'
        }

        if eq_maxScale in Scales:
            eq_maxScale = Scales[eq_maxScale]

        #magnitude
        eq_magnitude = data[0]['earthquake']['hypocenter']['magnitude']

        if eq_magnitude == -1:
            eq_magnitude = '調査中'
        else:
            eq_magnitude = 'M' + str(eq_magnitude)

        #depth
        eq_depth = data[0]['earthquake']['hypocenter']['depth']

        if eq_depth == -1:
            eq_depth = '調査中'
        elif eq_depth == 0:
            eq_depth = 'ごく浅い'
        else:
            eq_depth = '約' + str(eq_depth) + 'km'

        #Tsunami
        eq_tsunami = data[0]['earthquake']['domesticTsunami']

        tsunamiLevels = {
            'None': 'この地震による津波の心配はありません。',
            'Unknown': '津波の影響は不明です。',
            'Checking': '津波の影響を現在調査中です。',
            'NonEffective': '若干の海面変動が予想されますが、被害の心配はありません。',
            'Watch': 'この地震で津波注意報が発表されています。',
            'Warning': 'この地震で津波警報等（大津波警報・津波警報あるいは津波注意報）が発表されています。'
        }

        if eq_tsunami in tsunamiLevels:
            eq_tsunami = tsunamiLevels[eq_tsunami]

        #colors
        colors = {
            '1': 0xc0c0c0,
            '2': 0x2020c0,
            '3': 0x20c020,
            '4': 0xc0c020,
            '5弱': 0xc0a020,
            '5強': 0xc07f20,
            '6弱': 0xe02020,
            '6強': 0xa02020,
            '7': 0x7f207f
        }

        if eq_maxScale in colors:
            color = colors[eq_maxScale]
        else:
            color = 0x7f7fc0


    #JSONアクセス失敗時
    except Exception as e:
        return 0x0305, e

    #生成
    data=f'発生日時：{eq_timeDay}日{eq_timeHour}時{eq_timeMinute}分頃\n'+\
         f'　震源　：{eq_hypo}\n'+\
         f'最大震度：{eq_maxScale}\n'+\
         f'　規模　：{eq_magnitude}\n'+\
         f'　深さ　：{eq_depth}\n'+\
         f'{eq_tsunami}'

    return 0x0101, [eq_type, color, data]
