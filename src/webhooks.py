#
# webhooks.py | YDITS for Discord
#
# (c) 2022 よね/Yone
# licensed under the Apache License 2.0
#

import datetime
import json
import os
from time import sleep

import requests

from data import config


# ---------- Main ---------- #

os.system('cls')
print(
    f"webhooks | YDITS for Discord  {config.version}\n"+\
    f"(c) 2022 よね/Yone\n\n"+\
    f"--------------------\n"
)

# ---------- Functions ---------- #
def get_time():
  global DT
  DT = datetime.datetime.now()


def make_getNiedDT():

  if DT.month < 10:
    eew_getTimeMonth = '0' + str(DT.month)
  else:
    eew_getTimeMonth = str(DT.month)
  if DT.day < 10:
    eew_getTimeDay = '0' + str(DT.day)
  else:
    eew_getTimeDay = str(DT.day)
  if DT.hour < 10:
    eew_getTimeHour = '0' + str(DT.hour)
  else:
    eew_getTimeHour = str(DT.hour)
  if DT.minute < 10:
    eew_getTimeMinute = '0' + str(DT.minute)
  else:
    eew_getTimeMinute = str(DT.minute)
  if DT.second < 10:
    eew_getTimeSecond = '0' + str(DT.second)
  else:
    eew_getTimeSecond = str(DT.second-1)

  return str(DT.year) + eew_getTimeMonth + eew_getTimeDay + eew_getTimeHour + eew_getTimeMinute + eew_getTimeSecond


def get_eew():

  global eew_repNum

  #makeUrl
  getNiedDT = make_getNiedDT()
  url = f'https://www.lmoni.bosai.go.jp/monitor/webservice/hypo/eew/{getNiedDT}.json'

  #Get
  try:
    res = requests.get(url, timeout=3.0)   ### get
  except Exception:
    print("Error1")
    return 0x0201, None, None

  #satatus
  if res.status_code == 200:
    try:
      data = json.loads(res.text)
    except Exception:
      pass

  elif res.status_code == 502:
    pass

  elif res.status_code == 404:
    print(f'HTTP 404: The specified server cannot be found.')

  elif res.status_code == 429:
    print(f'HTTP 429: Too many requests.')

  else:
    print(f'HTTP {res.status_code} has occurred.')

  #time
  eew_time = data['origin_time']

  eew_timeYear = eew_time[0:4]
  eew_timeMonth = eew_time[4:6]
  eew_timeDay = eew_time[6:8]
  eew_timeHour = eew_time[8:10]
  eew_timeMinute = eew_time[10:12]
  eew_timeSecond = eew_time[12:14]

  #Report number
  eew_repNum = data['report_num']

  if eew_repNum != '':
    eew_repNum_put = f"第{eew_repNum}報"
  else:
    eew_repNum_put = ""

  #Alert flag
  if eew_repNum != '':
    eew_alertflg = data['alertflg']
  else:
    eew_alertflg = ''

  #Is training
  eew_isTraining = data['is_training']

  #Is final
  eew_isFinal = data['is_final']

  if eew_isFinal:
    eew_repNum_put = "最終報"

  #Region name
  eew_hypoName = data['region_name']

  if eew_hypoName == '':
    eew_hypoName = "不明"

  #Calcintensity
  eew_maxInt = data['calcintensity']

  if eew_maxInt == '':
    eew_maxInt = "不明"

  #Magunitude
  eew_magunitude = data['magunitude']

  if eew_magunitude == '':
    eew_magunitude = "不明"
  else:
    eew_magunitude = f"M{eew_magunitude}"

  #Depth
  eew_depth = data['depth']

  if eew_depth == '':
    eew_depth = "不明"
  else:
    eew_depth = f"約{eew_depth}"

  title = f'緊急地震速報 ({eew_alertflg})  {eew_repNum_put}'
  text = f'{eew_timeDay}日{eew_timeHour}時{eew_timeMinute}分頃\n'+\
        f'{eew_hypoName}で地震が発生しました\n'+\
        f'予想最大震度：{eew_maxInt}\n'+\
        f'　予想規模　：{eew_magunitude}\n'+\
        f'　予想深さ　：{eew_depth}\n\n'+\
          '今後の情報に注意してください'
  return 0x0102, title ,text


def get_eqinfo():

  global eqinfo_id

  url = 'https://api.p2pquake.net/v2/history/'

  params = {
    'zipcode': '',
    'codes': '551',
    'limit': '1'
  }

  try:
    res = requests.get(url, params=params, timeout=3.0)   ### get
  except Exception:
    print("Error2")
    return 0x0202, None, None

  if res.status_code == 200:
    try:
      data = json.loads(res.text)
    except Exception:
      pass
  
  elif res.status_code == 404:
    print("HTTP 404: The specified server cannot be found.")
  
  elif res.status_code == 429:
    print("HTTP 429: Too many requests.")
  
  else:
    print(f"Error HTTP {res.status_code} has occurred.")

  #id
  eqinfo_id = data[0]['id']

  #time
  eqinfo_time = data[0]['earthquake']['time']

  #type
  eqinfo_type = data[0]['issue']['type']

  eqinfo_types = {
      'ScalePrompt': "震度速報",
      'Destination': "震源情報",
      'ScaleAndDestination': "震源・震度情報",
      'DetailScale': "各地の震度情報",
      'Foreign': "遠地地震情報",
      'Other': "地震情報"
  }

  if eqinfo_type in eqinfo_types:
    eqinfo_type = eqinfo_types[eqinfo_type]

  #hypocenter
  eqinfo_hypo = data[0]['earthquake']['hypocenter']['name']

  if eqinfo_hypo == '':
    eqinfo_hypo = '調査中'

  #maxScale
  eqinfo_maxScale = data[0]['earthquake']['maxScale']

  eqinfo_Scales = {
    -1: '調査中',
    10: '1',
    20: '2',
    30: '3',
    40: '4',
    45: '5弱',
    50: '5強',
    55: '6弱',
    60: '6強',
    70:'7'
  }

  if eqinfo_maxScale in eqinfo_Scales:
    eqinfo_maxScale_put = eqinfo_Scales[eqinfo_maxScale]

  #magnitude
  eqinfo_magnitude = data[0]['earthquake']['hypocenter']['magnitude']

  if eqinfo_magnitude == -1:
    eqinfo_magnitude = '調査中'
  else:
    eqinfo_magnitude = f"M{str(eqinfo_magnitude)}"

  #depth
  eqinfo_depth = data[0]['earthquake']['hypocenter']['depth']

  if eqinfo_depth == -1:
    eqinfo_depth = '調査中'
  elif eqinfo_depth == 0:
    eqinfo_depth = 'ごく浅い'
  else:
    eqinfo_depth = f"約{str(eqinfo_depth)}km"

  #tsunami
  eqinfo_tsunami = data[0]['earthquake']['domesticTsunami']

  eqinfo_tsunamiLevels = {
    'None': 'この地震による津波の心配はありません。',
    'Unknown': '津波の影響は不明です。',
    'Checking': '津波の影響を現在調査中です。',
    'NonEffective': '若干の海面変動が予想されますが、被害の心配はありません。',
    'Watch': 'この地震で津波注意報が発表されています。',
    'Warning': 'この地震で津波警報等（大津波警報・津波警報あるいは津波注意報）が発表されています。'
  }

  if eqinfo_tsunami in eqinfo_tsunamiLevels:
    eqinfo_tsunami = eqinfo_tsunamiLevels[eqinfo_tsunami]

  eqinfo_timeYear   = eqinfo_time[0:4]
  eqinfo_timeMonth  = eqinfo_time[5:7]
  eqinfo_timeDay    = eqinfo_time[8:10]
  eqinfo_timeHour   = eqinfo_time[11:13]
  eqinfo_timeMinute = eqinfo_time[14:16]
  eqinfo_timeSecond = eqinfo_time[17:19]

  title = f'{eqinfo_type}'
  text = f'{eqinfo_timeDay}日{eqinfo_timeHour}時{eqinfo_timeMinute}分頃\n'+\
         f'{eqinfo_hypo}を震源とする、最大震度{eqinfo_maxScale_put}の地震がありました。\n'+\
         f'地震の規模は{eqinfo_magnitude}、震源の深さは{eqinfo_depth}と推定されます。\n'+\
         f'{eqinfo_tsunami}'

  return 0x0101, title ,text


def put_waiting():
  print('>Waiting for EEW and earthquake information.\n')


def gotNewdata():
  print('>Earthquake information was retrieved.')
  print('At time：' + str(DT) + '\n')
  print('------------------------------------------------------------------------------------------\n')


def upload(type, title, text):

  if type == 1:
    url = ''
    params = {
        'embeds': [
          {
            'title': title,
            'description': text
          }
        ]
    }

  if type == 2:
    url = ''
    params = {
      'embeds': [
        {
          'title': title,
          'description': text
        }
      ]
    }

  headers = {'Content-Type': 'application/json'}

  res = requests.post(url, json.dumps(params), headers=headers)

  if res.status_code == 204:
    print('Successfully distributed.\n')
  else:
    print(f'Could not be distributed. Error Code：{res.status_code}\n')


# ---------- Init ---------- #

eew_repNum_last = -1
eqinfo_id_last  = -1

cnt_getEew    = 0
cnt_getEqinfo = 0

put_waiting()

# ---------- Mainloop ---------- #
while True:

  get_time()

  #eew
  if cnt_getEew >= 1:

    cnt_getEew = 0
    eew_code, eew_title, eew_text = get_eew()

    if eew_repNum_last != eew_repNum and eew_repNum != '':
      eew_repNum_last = eew_repNum
      gotNewdata()
      upload(1, eew_title, eew_text)
      put_waiting()

  #eqinfo
  if cnt_getEqinfo >= 10:

    cnt_getEqinfo = 0
    eqinfo_code, eqinfo_title, eqinfo_text = get_eqinfo()

    if eqinfo_id_last != eqinfo_id:
      if eqinfo_id_last != -1:
        gotNewdata()
        upload(2, eqinfo_title, eqinfo_text)
        put_waiting()
      eqinfo_id_last = eqinfo_id

  #Update
  cnt_getEew += 1
  cnt_getEqinfo  += 1

  sleep(1)
