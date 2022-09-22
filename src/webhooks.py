#
# main.py / YDITS for Discord  ver 1.0.1 / yone1130
#
import os
from time import sleep
import pprint
import datetime
import requests
import json

##### Functions #####
def put_logo():
  sleep(0.5)
  print('                                ')
  print(' ------------------------------ ')
  print('                                ')
  print('  YDITS for Discord  Ver 1.0.1  ')
  print('                                ')
  print(' ------------------------------ ')
  print('                                ')
  sleep(0.5)

def selectMode():
  print('Enter a number to select mode\n')
  print('1: "P2P earthquake information" only')
  print('2: "P2P earthquake information" and "EEW from NIED"')

  while True:
    print('>', end='')
    val = input()

    if val == '1':
      return 1
      break

    if val == '2':
      return 2
      break

    else: print('There is not that number.')

def getTime():
  global DT
  DT = datetime.datetime.now()

class Point:
  def __init__(self, scale, name):
      self.scale = scale
      self.name  = name

def getData(firstFlag, getType):
  getTime()

  if firstFlag == True:
    global latestState_NIED
    global latestState_p2p
    latestState_NIED = 1
    latestState_p2p  = 1
    print(' <Connect>')

  ##### NIED EEW
  global _report_num
  _report_num = ''
  global report_num
  report_num = ''

  if getType == 0 or getType == 1:
    if firstFlag == True: print('NIED      ：', end='')

    global timeMonth
    if DT.month < 10: timeMonth = '0' + str(DT.month)
    else: timeMonth = str(DT.month)
    global timeDay
    if DT.day < 10: timeDay = '0' + str(DT.day)
    else: timeDay = str(DT.day)
    global timeHour
    if DT.hour < 10: timeHour = '0' + str(DT.hour)
    else: timeHour = str(DT.hour)
    global timeMinute
    if DT.minute < 10: timeMinute = '0' + str(DT.minute)
    else: timeMinute = str(DT.minute)
    global timeSecond
    if DT.second < 10: timeSecond = '0' + str(DT.second)
    else: timeSecond = str(DT.second)

    NIED_DT = str(DT.year) + timeMonth + timeDay + timeHour + timeMinute + timeSecond

    url = f'https://www.lmoni.bosai.go.jp/monitor/webservice/hypo/eew/{NIED_DT}.json'

    global res_NIED
    try:
      res_NIED = requests.get(url, timeout=1.0)   ### get
      if latestState_NIED != 1:
        print('Connection restored at ' + str(DT))
        latestState_NIED = 1
    except Exception:
      if latestState_NIED != 0:
        print('Connection error at ' + str(DT))
        latestState_NIED = 0

    global data_NIED
    if res_NIED.status_code == 200:
      if firstFlag == True: print('OK')
      try:
        data_NIED = json.loads(res_NIED.text)
      except Exception:
        pass

    elif res_NIED.status_code == 502:
      pass

    elif res_NIED.status_code == 404:
      print(f'Error HTTP {res_NIED.status_code} ：The specified server cannot be found.')

    elif res_NIED.status_code == 429:
      print(f'Error HTTP {res_NIED.status_code} :Too many requests.')

    else:
      print(f'Error HTTP {res_NIED.status_code} has occurred.')

    #Message
    global message
    message = data_NIED['result']['message']

    #Origin time
    global OriginTime
    OriginTime = data_NIED['origin_time']

    global eewYear
    eewYear = OriginTime[0:4]
    global eewMonth
    eewMonth = OriginTime[4:6]
    global eewDay
    eewDay = OriginTime[6:8]
    global eewHour
    eewHour = OriginTime[8:10]
    global eewMinute
    eewMinute = OriginTime[10:12]
    global eewSecond
    eewSecond = OriginTime[12:14]

    #Report number
    _report_num = data_NIED['report_num']

    if _report_num != '':
      report_num = '第' + _report_num + '報'
    else:
      report_num = ''

    #Alert flag
    global alertflg
    if _report_num != '':
      alertflg = data_NIED['alertflg']
    else:
      alertflg = ''

    #Is training
    global is_training
    is_training = data_NIED['is_training']

    #Is final
    global is_final
    is_final = data_NIED['is_final']

    if is_final:
      report_num = '最終報'

    #Region name
    global region_name
    region_name = data_NIED['region_name']

    if region_name == '':
      region_name = '不明'

    #Calcintensity
    global calcintensity
    calcintensity = data_NIED['calcintensity']

    if calcintensity == '':
      calcintensity = '不明'

    #Magunitude
    global magunitude_NIED
    magunitude_NIED = data_NIED['magunitude']

    if magunitude_NIED == '':
      magunitude_NIED = '不明'
    else:
      magunitude_NIED = 'M' + magunitude_NIED

    #Depth
    global depth_NIED
    depth_NIED = data_NIED['depth']

    if depth_NIED == '':
      depth_NIED = '不明'
    else:
      depth_NIED = '約'+ depth_NIED

    #Is cancel
    global is_cancel
    is_cancel = data_NIED['is_cancel']

    if is_cancel:
      alertflg = '取消'

  ##### P2P Infomation
  global point
  point = {}

  if getType == 0 or getType == 2:
    if firstFlag == True: print('P2P Quakes：', end='')

    url = 'https://api.p2pquake.net/v2/history/'

    params = {
      'zipcode': '',
      'codes': '551',
      'limit': '1'
    }

    global res_p2p
    try:
      res_p2p = requests.get(url, params=params, timeout=1.0)   ### get
      if latestState_p2p != 1:
        print('Connection restored at ' + str(DT))
        latestState_p2p = 1
    except Exception:
      if latestState_p2p != 0:
        print('Connection error at ' + str(DT))
        latestState_p2p = 0

    global data_p2p
    if res_p2p.status_code == 200:
      if firstFlag == True: print('OK\n')
      try:
        data_p2p = json.loads(res_p2p.text)
      except Exception:
        pass
    
    elif res_p2p.status_code == 404:
      print(f'Error HTTP {res_p2p.status_code} ：The specified server cannot be found.')
    
    elif res_p2p.status_code == 429:
      print(f'Error HTTP {res_p2p.status_code} :Too many requests.')
    
    else:
      print(f'Error HTTP {res_p2p.status_code} has occurred.')

    #id
    global id
    id = data_p2p[0]['id']

    #Time of Occurrence
    global jmaDatetime
    jmaDatetime = data_p2p[0]['earthquake']['time']

    #Type
    global _jmaType
    _jmaType = data_p2p[0]['issue']['type']

    global jmaType
    jmaTypes = {
      'ScalePrompt': '震度速報',
      'Destination': '震源情報',
      'ScaleAndDestination': '震源・震度情報',
      'DetailScale': '地震情報',
      'Other': '地震情報'
    }

    if _jmaType in jmaTypes:
      jmaType = jmaTypes[_jmaType]

    #Hypocenter
    global hypocenter
    hypocenter = data_p2p[0]['earthquake']['hypocenter']['name']

    if hypocenter == '':
      hypocenter = '調査中'

    #Max scale
    global _maxScale
    _maxScale = data_p2p[0]['earthquake']['maxScale']

    global maxScale
    Scales = {-1: '調査中', 10: '1', 20: '2', 30: '3', 40: '4', 45: '5弱', 50: '5強', 55: '6弱', 60: '6強', 70: '7'}
    if _maxScale in Scales:
      maxScale = Scales[_maxScale]

    #Magnitude
    global magnitude_p2p
    magnitude_p2p = data_p2p[0]['earthquake']['hypocenter']['magnitude']

    if magnitude_p2p == -1:
      magnitude_p2p = '調査中'
    else:
      magnitude_p2p = 'M' + str(magnitude_p2p)

    #Depth
    global depth_p2p
    depth_p2p = data_p2p[0]['earthquake']['hypocenter']['depth']

    if depth_p2p == -1:
      depth_p2p = '調査中'
    elif depth_p2p == 0:
      depth_p2p = 'ごく浅い'
    else:
      depth_p2p = '約' + str(depth_p2p) + 'km'

    #Tsunami
    global _domesticTsunami
    _domesticTsunami = data_p2p[0]['earthquake']['domesticTsunami']

    global domesticTsunami
    tsunamiLevels = {
      'None': 'この地震による津波の心配はありません。',
      'Unknown': '津波の影響は不明です。',
      'Checking': '津波の影響を現在調査中です。',
      'NonEffective': '若干の海面変動が予想されますが、被害の心配はありません。',
      'Watch': 'この地震で津波注意報が発表されています。',
      'Warning': 'この地震で津波警報等（大津波警報・津波警報あるいは津波注意報）が発表されています。'
    }

    if _domesticTsunami in tsunamiLevels:
      domesticTsunami = tsunamiLevels[_domesticTsunami]

    #Quake report
    global quake
    if _maxScale < 30:
      quake = ''
    if _maxScale == 30: 
      quake = 'この地震による揺れを感じました。\n\n'
    if _maxScale == 40:
      quake = 'この地震によるやや強い揺れを感じました。\n\n'
    if _maxScale >= 50:
      quake = 'この地震による非常に強い揺れを感じました。\n\n'

    global jmaYear
    jmaYear = jmaDatetime[0:4]
    global jmaMonth
    jmaMonth = jmaDatetime[5:7]
    global jmaDay
    jmaDay = jmaDatetime[8:10]
    global jmaHour
    jmaHour = jmaDatetime[11:13]
    global jmaMinute
    jmaMinute = jmaDatetime[14:16]
    global jmaSecond
    jmaSecond = jmaDatetime[17:19]

    # points = data_p2p[0]['points']
    # for temp[0] in range(len(points)):
    #   temp[1] = int(points[temp[0]]['scale'])
    #   temp[2] = points[temp[0]]['addr']
    #   point[len(point)] = Point(temp[1], temp[2])

def put_waiting():
  if Mode == 1: print('Waiting for earthquake information.\n')
  if Mode == 2: print('Waiting for EEW and earthquake information.\n')

def put_data():
  pprint.pprint(data_p2p)

def gotNewdata(Type):
  print('Earthquake information was retrieved.\n')
  print('At time：' + str(DT) + '\n')

  if Type == 1:
    return _report_num
  elif Type == 2:
    return id

def uploadTwitter(uploadType):


  if uploadType == 1:
    url = ''
    params = {
        'embeds': [
          {
            'title': f'緊急地震速報 ({alertflg})  {report_num}',
            'description': 
              f'{eewDay}日{eewHour}時{eewMinute}分頃\n'+
              f'{region_name}で地震が発生しました\n'+
              f'予想最大震度：{calcintensity}\n'+
              f'　予想規模　：{magunitude_NIED}\n'+
              f'　予想深さ　：{depth_NIED}\n\n'+
              f'今後の情報に注意してください'
          }
        ]

    }

  if uploadType == 2:
    url = ''
    params = {
      'embeds': [
        {
          'title': f'{jmaType}',
          'description': 
            f'{jmaDay}日{jmaHour}時{jmaMinute}分頃\n'+
            f'{hypocenter}を震源とする、最大震度{maxScale}の地震がありました。\n'+
            f'地震の規模は{magnitude_p2p}、震源の深さは{depth_p2p}と推定されます。\n'+
            f'{domesticTsunami}'
        }
      ]
    }

  headers = {'Content-Type': 'application/json'}

  res = requests.post(url, json.dumps(params), headers=headers)

  if res.status_code == 204:
    print('Successfully distributed.\n')
  else:
    print(f'Could not be distributed. Error Code：{res.status_code}\n')

### debug ###
def debug():
  print('------------------------------------------------------------------------------------------')
  print('')

###### Setup #####

os.system('cls')
put_logo()

Mode = selectMode()

os.system('cls')
put_logo()

temp = {}

if   Mode == 1: getType = 2
elif Mode == 2: getType = 0
getData(1, getType)

latestId = id
latest_report_num = _report_num

cnt_NIED = 0; cnt_p2p = 0

#put_data()
debug()
put_waiting()

##### Main #####
while True:
  sleep(1)
  cnt_NIED += 1
  cnt_p2p  += 1

  if   Mode == 2:
    if cnt_NIED >= 2:
      cnt_NIED = 0
      getData(0, 1)

  if cnt_p2p >= 12:
    cnt_p2p = 0
    getData(0, 2)

  if Mode == 2:
    if latest_report_num != _report_num and _report_num != '':
      getTime()
      latest_report_num = gotNewdata(1)
      debug()
      uploadTwitter(1)
      put_waiting()

  if latestId != id:
    getTime()
    latestId = gotNewdata(2)
    debug()
    uploadTwitter(2)
    put_waiting()