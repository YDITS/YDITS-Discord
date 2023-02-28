#
# module/api.py | YDITS for Discord
#
# (c) 2022-2023 よね/Yone
# licensed under the Apache License 2.0
#
import json
import requests


# ---------- Functions ---------- #
async def get_eqinfo():
    url = 'https://api.p2pquake.net/v2/history/'

    params = {
      'zipcode': '',
      'codes': '551',
      'limit': '1'
    }

    try:
        res = requests.get(url, params=params, timeout=3.0)
    except Exception as e:
        return 0x0301, e

    if res.status_code == 200:
        try:
            data = json.loads(res.text)
        except Exception:
            return 0x0302, None

    elif res.status_code == 429:
        return 0x0303, None

    else:
        return 0x0304, res.status_code

    try:
        #time
        eq_time = data[0]['earthquake']['time']

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

    except Exception as e:
        return 0x0305, e

    data=f'発生日時：{eq_timeDay}日{eq_timeHour}時{eq_timeMinute}分頃\n'+\
         f'　震源　：{eq_hypo}\n'+\
         f'最大震度：{eq_maxScale}\n'+\
         f'　規模　：{eq_magnitude}\n'+\
         f'　深さ　：{eq_depth}\n'+\
         f'{eq_tsunami}'
    return 0x0101, [eq_type, color, data]


async def get_tnmInfo():
    url = 'https://api.p2pquake.net/v2/history/'

    params = {
      'zipcode': '',
      'codes': '552',
      'limit': '1'
    }

    try:
        res = requests.get(url, params=params, timeout=3.0)
    except Exception as e:
        return 0x0301, e

    if res.status_code == 200:
        try:
            data = json.loads(res.text)
        except Exception:
            return 0x0302, None

    elif res.status_code == 429:
        return 0x0303, None

    else:
        return 0x0304, res.status_code

    try:
        #time
        tnmInfo_time = data[0]['time']

        #id
        tnmInfo_id = data[0]['id']

        #cancelled
        tnmInfo_cancelled = data[0]['cancelled']

        #areas
        tnmInfo_areas = data[0]['areas']

        tnmInfo_timeYear   = tnmInfo_time[0:4]
        tnmInfo_timeMonth  = tnmInfo_time[5:7]
        tnmInfo_timeDay    = tnmInfo_time[8:10]
        tnmInfo_timeHour   = tnmInfo_time[11:13]
        tnmInfo_timeMinute = tnmInfo_time[14:16]
        tnmInfo_timeSecond = tnmInfo_time[17:19]

        color = 0x7f7fc0

    except Exception as e:
        return 0x0305, e

    if data[0]['cancelled'] == False:
        #content
        title =  "津波情報"
        data = f"発表日時: {tnmInfo_timeDay}日{tnmInfo_timeHour}時{tnmInfo_timeMinute}分\n\n"+\
                "海岸から離れてください\n"

        #list
        lastGrade = ""

        for area in tnmInfo_areas:

            name  = area['name']
            grade = area['grade']

            if grade != lastGrade:
                if grade == "MajorWarning":
                    data += "\n[大津波警報]\n"
                elif grade == "Warning":
                    data += "\n[津波警報]\n"
                elif grade == "Watch":
                    data += "\n[津波注意報]\n"
                else:
                    data += "\n[不明]\n"
                lastGrade = grade

            data += f"{name}\n"

    elif data[0]['cancelled'] == True:
        title = "津波情報"
        data = "津波警報等は発表されていません。"

    return 0x0101, [title, color, data]
