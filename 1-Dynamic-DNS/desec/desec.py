import os
import socket
import requests
import logging
import logging.handlers
import json

def getipv6():
  s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
  s.connect(("240e:940:603:a:0:ff:b08d:239d", 80))
  ip_address = s.getsockname()[0]
  print('This PC IPv6: ', ip_address)
  return ip_address


def hitduck(cur_ip6):
  hostname='kofutoku.dedyn.io'
  proxies = {
   "http": "socks5h://127.0.0.1:1080",
   "https": "socks5h://127.0.0.1:1080"
  }
  payload = {}
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept-Encoding': 'application/json',
    'accept': 'application/dns-json',
    'Authorization': 'Token uveSJgCuTpzv7LSVPTWiPrakPUsN'
  }
  url = f"https://update.dedyn.io/?hostname={hostname}&myipv6={cur_ip6}&myipv4"
  
  response = requests.request("GET", url, headers=headers, data=payload, verify=False, proxies=proxies)
  print(response,response.status_code,response.text)
  if (response.status_code==200):
    return True
  else:
    return False

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
logloc = os.path.join(ROOT_DIR,'desec.log')
curip = os.path.join(ROOT_DIR,'curip.json')
BACKUP_COUNT = 7

logging.basicConfig(filename=logloc,
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger("desec_log")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.TimedRotatingFileHandler(
    logloc,
    when='midnight',
    interval=1,
    backupCount=BACKUP_COUNT
)

# Set up formatter and add to handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

cur_ip6 = getipv6()
data = {}
with open(curip, "r") as file:
  #content = file.read()
  #content = content.strip()
  data = json.load(file)
  content = data['ip6']
  print(repr(str(content)),'\n', repr(cur_ip6), '\n', content==cur_ip6)
#  exit()
  

if (content == cur_ip6):
    txt = 'IP still the same: '+ cur_ip6
    logger.info(txt)
    print(txt)
    exit()
else:
    result = hitduck(cur_ip6)
    if (result==True):
      data['ip6'] = cur_ip6
      print('ini data', data)
      with open(curip, "wt") as file:
        json.dump(data, file)
      txt = f'IP changed from {content} to {cur_ip6}'
      logger.info(txt)
      print(txt)
    else:
      txt = f'Failed changing IP from {content} to {cur_ip6}'
      logger.error(txt)
      print(txt)
