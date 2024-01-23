"""

YDITS for Discord

Copyright (c) よね/Yone

Licensed under the Apache License 2.0.

"""

import datetime
import json
import urllib.request
import requests
from PIL import Image


# ---------- Functions ---------- #
async def getEew():
    niedDate = make_niedDate()
    url = f"https://www.lmoni.bosai.go.jp/monitor/webservice/hypo/eew/{niedDate}.json"

    try:
        res = requests.get(url, timeout=3.0)
    except Exception:
        print(f"Error. Cannot get nied.")
        return {"status": 0x0301}

    if res.status_code == requests.codes.ok:
        try:
            data = json.loads(res.text)
        except Exception:
            return {"status": 0x0302}
    elif res.status_code == 502:
        return {"status": 0x0306}
    else:
        print(f"Error. Cannot get nied.\nHTTP {res.status_code}\n")
        return {"status": 0x0304}

    try:
        eew_time = data["origin_time"]
        eew_timeYear = eew_time[0:4]
        eew_timeMonth = eew_time[4:6]
        eew_timeDay = eew_time[6:8]
        eew_timeHour = eew_time[8:10]
        eew_timeMinute = eew_time[10:12]
        eew_timeSecond = eew_time[12:14]

        eew_repNum = data["report_num"]

        if eew_repNum != "":
            eew_repNum_put = f"第{eew_repNum}報"
        else:
            eew_repNum_put = ""

        if eew_repNum != "":
            eew_alertflg = data["alertflg"]
        else:
            eew_alertflg = ""

        eew_isTraining = data["is_training"]

        eew_isFinal = data["is_final"]

        if eew_isFinal:
            eew_repNum_put = "最終報"

        eew_hypoName = data["region_name"]

        if eew_hypoName == "":
            eew_hypoName = "不明"

        eew_maxInt = data["calcintensity"]

        if eew_maxInt == "":
            eew_maxInt = "不明"

        eew_magunitude = data["magunitude"]

        if eew_magunitude == "":
            eew_magunitude = "不明"
        else:
            eew_magunitude = f"M{eew_magunitude}"

        eew_depth = data["depth"]

        if eew_depth == "":
            eew_depth = "不明"
        else:
            eew_depth = f"約{eew_depth}"

    except Exception:
        return {"status": 0x0305}

    if eew_alertflg == "警報":
        eew_color = 0xF04040
    elif eew_alertflg == "予報":
        eew_color = 0xF0C040
    else:
        eew_color = 0x40F040

    if eew_repNum != "":
        return {
            "status": 0x0101,
            "data": {
                "repNum": eew_repNum,
                "title": f"≪緊急地震速報 ({eew_alertflg})  {eew_repNum_put}≫",
                "content": f"{eew_timeDay}日{eew_timeHour}時{eew_timeMinute}分頃\n"
                + f"{eew_hypoName}を震源とする地震が発生しました。\n"
                + f"最大震度は{eew_maxInt}程度、地震の規模は{eew_magunitude}程度、\n"
                + f"震源の深さは{eew_depth}と推定されています。\n"
                + "今後の情報に注意してください",
                "color": eew_color,
            },
        }
    else:
        return {
            "status": 0x0101,
            "data": {
                "repNum": eew_repNum,
                "title": "",
                "content": "緊急地震速報は発表されていません",
                "color": eew_color,
            },
        }


async def getEqinfo():
    url = "https://api.p2pquake.net/v2/history/"

    params = {"zipcode": "", "codes": "551", "limit": "1"}

    try:
        res = requests.get(url, params=params, timeout=3.0)
    except Exception:
        print("Error. Cannot get P2P.")
        return {"status": 0x0301}

    if res.status_code == requests.codes.ok:
        try:
            data = json.loads(res.text)
        except Exception:
            return {"status": 0x0305}
    else:
        print(f"Error. Cannot get P2P.\nHTTP {res.status_code}\n")
        return {"status": 0x0304}

    eqinfo_id = data[0]["id"]
    eqinfo_time = data[0]["earthquake"]["time"]
    eqinfo_type = data[0]["issue"]["type"]

    eqinfo_types = {
        "ScalePrompt": "震度速報",
        "Destination": "震源情報",
        "ScaleAndDestination": "震源・震度情報",
        "DetailScale": "各地の震度情報",
        "Foreign": "遠地地震情報",
        "Other": "地震情報",
    }

    if eqinfo_type in eqinfo_types:
        eqinfo_type = eqinfo_types[eqinfo_type]

    eqinfo_hypo = data[0]["earthquake"]["hypocenter"]["name"]

    if eqinfo_hypo == "":
        eqinfo_hypo = "調査中"

    eqinfo_maxScale = data[0]["earthquake"]["maxScale"]

    eqinfo_Scales = {
        -1: "調査中",
        10: "1",
        20: "2",
        30: "3",
        40: "4",
        45: "5弱",
        50: "5強",
        55: "6弱",
        60: "6強",
        70: "7",
    }

    if eqinfo_maxScale in eqinfo_Scales:
        eqinfo_maxScale_put = eqinfo_Scales[eqinfo_maxScale]

    eqinfo_magnitude = data[0]["earthquake"]["hypocenter"]["magnitude"]

    if eqinfo_magnitude == -1:
        eqinfo_magnitude = "調査中"
    else:
        eqinfo_magnitude = f"M{str(eqinfo_magnitude)}"

    eqinfo_depth = data[0]["earthquake"]["hypocenter"]["depth"]

    if eqinfo_depth == -1:
        eqinfo_depth = "調査中"
    elif eqinfo_depth == 0:
        eqinfo_depth = "ごく浅い"
    else:
        eqinfo_depth = f"約{str(eqinfo_depth)}km"

    eqinfo_tsunami = data[0]["earthquake"]["domesticTsunami"]

    eqinfo_tsunamiLevels = {
        "None": "この地震による津波の心配はありません。",
        "Unknown": "津波の影響は不明です。",
        "Checking": "津波の影響を現在調査中です。",
        "NonEffective": "若干の海面変動が予想されますが、被害の心配はありません。",
        "Watch": "この地震で津波注意報が発表されています。",
        "Warning": "この地震で津波警報等（大津波警報・津波警報あるいは津波注意報）が発表されています。",
    }

    if eqinfo_tsunami in eqinfo_tsunamiLevels:
        eqinfo_tsunami = eqinfo_tsunamiLevels[eqinfo_tsunami]

    eqinfo_timeYear = eqinfo_time[0:4]
    eqinfo_timeMonth = eqinfo_time[5:7]
    eqinfo_timeDay = eqinfo_time[8:10]
    eqinfo_timeHour = eqinfo_time[11:13]
    eqinfo_timeMinute = eqinfo_time[14:16]
    eqinfo_timeSecond = eqinfo_time[17:19]

    colors = {
        "1": 0xC0C0C0,
        "2": 0x2020C0,
        "3": 0x20C020,
        "4": 0xC0C020,
        "5弱": 0xC0A020,
        "5強": 0xC07F20,
        "6弱": 0xE02020,
        "6強": 0xA02020,
        "7": 0x7F207F,
    }

    if eqinfo_maxScale in colors:
        color = colors[eqinfo_maxScale]
    else:
        color = 0x7F7FC0

    if eqinfo_type == "各地の震度情報":
        pointsText = "\n\n[各地の震度情報]"
        points = [""] * 10
        scales = {-1: 9, 10: 8, 20: 7, 30: 6, 40: 5, 45: 4, 50: 3, 55: 2, 60: 1, 70: 0}
        scalesText = {
            -1: "調査中",
            10: "1",
            20: "2",
            30: "3",
            40: "4",
            45: "5弱",
            50: "5強",
            55: "6弱",
            60: "6強",
            70: "7",
        }
        pointNameList = [[] for i in range(10)]

        for point in data[0]["points"]:
            if point["scale"] in scales:
                scale = scales[point["scale"]]
                pointName = point["pref"]

                if points[scale] == "":
                    points[scale] = (
                        points[scale] + f"\n\n■震度{scalesText[point['scale']]}"
                    )

                if not (pointName in pointNameList[scale]):
                    pointNameList[scale].append(pointName)
                    points[scale] = points[scale] + f"\n\n- {pointName}"

                points[scale] = f"{points[scale]}\n{point['addr']}"

            else:
                continue

        for point in points:
            pointsText = pointsText + point

    return {
        "status": 0x0101,
        "data": {
            "id": eqinfo_id,
            "maxScale": eqinfo_maxScale,
            "title": "【地震情報】",
            "content": f"{eqinfo_timeDay}日{eqinfo_timeHour}時{eqinfo_timeMinute}分頃\n"
            + f"{eqinfo_hypo}を震源とする地震がありました。\n"
            + f"最大震度は{eqinfo_maxScale_put}、地震の規模は{eqinfo_magnitude}、\n"
            + f"震源の深さは{eqinfo_depth}と推定されます。\n"
            + f"{eqinfo_tsunami}"
            + f"{pointsText}",
            "color": color,
        },
    }


async def get_tnmInfo():
    url = "https://api.p2pquake.net/v2/history/"

    params = {"zipcode": "", "codes": "552", "limit": "1"}

    try:
        res = requests.get(url, params=params, timeout=3.0)
    except Exception as e:
        return {"status": 0x0301}

    if res.status_code == requests.codes.ok:
        try:
            data = json.loads(res.text)
        except Exception:
            return {"status": 0x0302}

    elif res.status_code == 429:
        return {"status": 0x0303}

    else:
        return {"status": 0x0304}

    try:
        tnmInfo_time = data[0]["time"]
        tnmInfo_id = data[0]["id"]
        tnmInfo_cancelled = data[0]["cancelled"]
        tnmInfo_areas = data[0]["areas"]
        tnmInfo_timeYear = tnmInfo_time[0:4]
        tnmInfo_timeMonth = tnmInfo_time[5:7]
        tnmInfo_timeDay = tnmInfo_time[8:10]
        tnmInfo_timeHour = tnmInfo_time[11:13]
        tnmInfo_timeMinute = tnmInfo_time[14:16]
        tnmInfo_timeSecond = tnmInfo_time[17:19]
        color = 0x7F7FC0

    except Exception as e:
        return {"status": 0x0305}

    if data[0]["cancelled"] == False:
        title = "津波情報"
        data = (
            f"発表日時: {tnmInfo_timeDay}日{tnmInfo_timeHour}時{tnmInfo_timeMinute}分\n\n"
            + "海岸から離れてください\n"
        )

        lastGrade = ""

        for area in tnmInfo_areas:
            name = area["name"]
            grade = area["grade"]

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

    elif data[0]["cancelled"] == True:
        title = "津波情報"
        data = "津波警報等は発表されていません。"

    return {
        "status": 0x0101,
        "data": {"title": title, "content": data, "color": 0x40FF40},
    }


def get_kmoni_img():
    niedDate = make_niedDate()

    urllib.request.urlretrieve(
        f"http://www.kmoni.bosai.go.jp/data/map_img/RealTimeImg/jma_s/{niedDate[:8]}/{niedDate}.jma_s.gif",
        "kmoni_points_temp_img.gif",
    )
    kmoni_points = Image.open("kmoni_points_temp_img.gif")
    urllib.request.urlretrieve(
        "http://www.kmoni.bosai.go.jp/data/map_img/CommonImg/base_map_w.gif",
        "kmoni_back_temp_img.gif",
    )
    kmoni_back = Image.open("kmoni_back_temp_img.gif")
    urllib.request.urlretrieve(
        f"http://www.kmoni.bosai.go.jp/data/map_img/PSWaveImg/eew/{niedDate[:8]}/{niedDate}.eew.gif",
        "kmoni_pswave_temp_img.gif",
    )
    kmoni_pswave = Image.open("kmoni_pswave_temp_img.gif")

    kmoni_back = kmoni_back.convert("RGBA")
    kmoni_points = kmoni_points.convert("RGBA")
    kmoni_pswave = kmoni_pswave.convert("RGBA")

    kmoni_points = kmoni_points.resize(kmoni_back.size)
    kmoni_pswave = kmoni_pswave.resize(kmoni_back.size)

    kmoni_data_img = Image.alpha_composite(kmoni_points, kmoni_pswave)
    kmoni_img = Image.alpha_composite(kmoni_back, kmoni_data_img)

    kmoni_img.save("kmoni_temp_img.gif")

    return


def get_eqlv():
    url = f"https://kwatch-24h.net/EQLevel.json"

    try:
        res = requests.get(url, timeout=3.0)
    except Exception:
        print(f"Error. Cannot get EQLevel.")
        return {"status": 0x0301}

    if res.status_code == requests.codes.ok:
        try:
            data = json.loads(res.text)
        except Exception:
            return {"status": 0x0302}
    elif res.status_code == 502:
        return {"status": 0x0306}
    else:
        print(f"Error. Cannot get nied.\nHTTP {res.status_code}\n")
        return {"status": 0x0304}

    try:
        eqlv_l = data["l"]
        eqlv_g = data["g"]
        eqlv_y = data["y"]
        eqlv_r = data["r"]
    except Exception:
        return {"status": 0x0305}

    return {
        "status": 0x0101,
        "data": {
            "content": "■強震観測点情報\n"
            + f"⚪振動Lv: {eqlv_l}\n"
            + f"🔴赤点数: {eqlv_r}\n"
            + f"🟡黄点数: {eqlv_y}\n"
            + f"🟢緑点数: {eqlv_g}\n"
        },
    }


def make_niedDate():
    DT = datetime.datetime.now()
    nideDateYear = str(DT.year)
    nideDateMonth = str(DT.month).zfill(2)
    nideDateDay = str(DT.day).zfill(2)
    nideDateHour = str(DT.hour).zfill(2)
    nideDateMinute = str(DT.minute).zfill(2)
    nideDateSecond = str(DT.second - 2).zfill(2)

    return f"{nideDateYear}{nideDateMonth}{nideDateDay}{nideDateHour}{nideDateMinute}{nideDateSecond}"
