import requests
import json
import random
import time
from threading import Thread
import threading
from datetime import datetime

#Required Cipher
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

#AUTHORIZATION_KEY FOR ALL
AUTHORIZATION_KEY = "Basic dGh1eWhrMkBmcHQuY29tLnZuOjEyMzQ1Ng=="

#VERSION
CURRENTVERSION = "2.2"

#OS
IOS = {
        "User-Agent": "HRISProject/1632 CFNetwork/1197 Darwin/20.0.0",
        "currentversioncode": "1632"
        }
ANDROID = {
            "User-Agent": "okhttp/3.12.1",
            "currentversioncode": "32"
        }

#KHOA - KEY
KHOA = {
    "app-authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjIxMjQ3IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6Iktob2FOVjE3QGZwdC5jb20udm4iLCJBc3BOZXQuSWRlbnRpdHkuU2VjdXJpdHlTdGFtcCI6IlVJTklLSEg3M0ZJTUxPNUU2T0M0UVdTT0daRkpDTUM3IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiRW1wbG95ZWUiLCJodHRwOi8vd3d3LmFzcG5ldGJvaWxlcnBsYXRlLmNvbS9pZGVudGl0eS9jbGFpbXMvdGVuYW50SWQiOiIxIiwiRW1wbG95ZWVJZENsYWltIjoiMjEyMjIiLCJzdWIiOiIyMTI0NyIsImp0aSI6IjE1YWI5ODhlLTFlNmItNDVkNy04YmNhLWNmZTg1ZmYyN2M2MCIsImlhdCI6MTYyNTQ2MjQxNywibmJmIjoxNjI1NDYyNDE3LCJleHAiOjE2MzMyMzg0MTcsImlzcyI6IkhSSVMiLCJhdWQiOiJIUklTIn0.tV21kLaUUkGE3QYXRl8ZmqbajN1KumBqD9QQOBa6vMY",
    "AccessPointsIPWAN": "U2FsdGVkX182wSyRzH+IiJ2jsswaQrjSvtrVyN3toe0=",
    "SmartPhoneDeviceIMEI": "559B0902-E434-4509-8FBB-5D5DCAF2F0E3",
}

#DAT - KEY
DAT = {
    "app-authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJFbXBsb3llZUlkQ2xhaW0iOiIyMTIxOSIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL25hbWVpZGVudGlmaWVyIjoiMjEyNDQiLCJodHRwOi8vd3d3LmFzcG5ldGJvaWxlcnBsYXRlLmNvbS9pZGVudGl0eS9jbGFpbXMvdGVuYW50SWQiOiIxIiwic3ViIjoiMjEyNDQiLCJqdGkiOiJjNGFkMDI0YS1mMTViLTQwNjQtOTA3Mi05ZjY3ZDMzZjU2ZWEiLCJpYXQiOjE2MTYxNDk5MjksIm5iZiI6MTYxNjE0OTkyOSwiZXhwIjoxNjIzOTI1OTI5LCJpc3MiOiJIUklTIiwiYXVkIjoiSFJJUyJ9.s1ffhF5EDI8ZC0vYsx3VosV4sWtcZhwA8uKZR_8ElLM",
    "AccessPointsIPWAN": "U2FsdGVkX1+P/JXtxxsuXgn+L5Hq/M8JxMChpMQaGek=",
    "SmartPhoneDeviceIMEI": "2A7ACC22-1402-4C84-AB66-B238FC8E37B9",
}

#NHUNG - KEY
NHUNG = {
    "app-authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjIxMjQzIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6Ik5odW5nTFRIMzRAZnB0LmNvbS52biIsIkFzcE5ldC5JZGVudGl0eS5TZWN1cml0eVN0YW1wIjoiM1hZNkFKU0w2M0FRQ0dUUVBYWlZBTlJGV1ZQQUdGWDUiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJFbXBsb3llZSIsImh0dHA6Ly93d3cuYXNwbmV0Ym9pbGVycGxhdGUuY29tL2lkZW50aXR5L2NsYWltcy90ZW5hbnRJZCI6IjEiLCJFbXBsb3llZUlkQ2xhaW0iOiIyMTIxOCIsInN1YiI6IjIxMjQzIiwianRpIjoiMjU5MmJhNTMtOTI2Zi00NjE1LWI4YjEtNzYzZTg0NTYwNTliIiwiaWF0IjoxNjI1NTY3Mzc2LCJuYmYiOjE2MjU1NjczNzYsImV4cCI6MTYzMzM0MzM3NiwiaXNzIjoiSFJJUyIsImF1ZCI6IkhSSVMifQ.XZ7d_wh49NRoeEvGO9AEzXAiL6ls4UAc6NbPhnLgm8w",
    "AccessPointsIPWAN": "U2FsdGVkX1/ImVTUz1pROB6qOKzzF21xv7iKWySQFvg=",
    "SmartPhoneDeviceIMEI": "3BF00794-5150-470E-83ED-54BBD3A18C8E",
}

#DUCANH - KEY
DUCANH = {
    "app-authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjIxMjQ1IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6IkFuaE5ENzVAZnB0LmNvbS52biIsIkFzcE5ldC5JZGVudGl0eS5TZWN1cml0eVN0YW1wIjoiTUpOTVFUTklDT1JRTTdHMkZHVEVGN1lWT0tERDZZREEiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJFbXBsb3llZSIsImh0dHA6Ly93d3cuYXNwbmV0Ym9pbGVycGxhdGUuY29tL2lkZW50aXR5L2NsYWltcy90ZW5hbnRJZCI6IjEiLCJFbXBsb3llZUlkQ2xhaW0iOiIyMTIyMCIsInN1YiI6IjIxMjQ1IiwianRpIjoiMTgzZjgzNWQtODk4Ni00NWY4LTg1M2UtODY5NTRiNDg5OGUzIiwiaWF0IjoxNjI1NzI3NTUzLCJuYmYiOjE2MjU3Mjc1NTMsImV4cCI6MTYzMzUwMzU1MywiaXNzIjoiSFJJUyIsImF1ZCI6IkhSSVMifQ.UbmAPpQWF8NPiBrVu81ctbM_4l_Mkc-lzO8-kbPmsMg",
    "AccessPointsIPWAN": "U2FsdGVkX19hdtZWLYs11QntC/Kutn10fp45jFHlsc4=",
    "SmartPhoneDeviceIMEI": "00a6db055e3d520f",
}

#TelegramBot
def pushInfo(title, messages):
    bot = "bot1263316426:"  
    telegramAPI = "https://api.telegram.org/"+ bot +"AAEsMDr5IUbrwRVV2jGgudIwrAuQNiPpy_Q/sendMessage?chat_id=540921490&text=" + title + ":\n" + messages
    print(title + ":\n" + messages + "\n")
    requests.post(telegramAPI)

#Get AuthorizationToken
def get_AuthorizationToken():
    url = "https://sapi.fpt.vn:443/token/GenerateToken"
    headers = {
                "Connection": "close",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": IOS['User-Agent'],
                "Accept-Language": "en-us",
                "Authorization": AUTHORIZATION_KEY,
                "Accept-Encoding": "gzip, deflate"
                }
    raw_token = requests.get(url, headers=headers)
    token = "Bearer " + raw_token.text.replace('"','')
    return token

#Get Current Time
def getCurrentTime():
    dateTime = datetime.now()
    #pushInfo("\U0001F55C Current Time", dateTime.strftime("%c"))
    return dateTime

#Do Check in and Check out. 1 = Checkin, 2 = Checkout
def checkInOut(name, authorizationToken, currentVersionCode, platform, appAuthorization_key, userAgent, ipWAN, checkType, deviceIMEI):
    url = "https://sapi.fpt.vn:443/hrapi/api/services/app/Checkin/Checkin"
    headers =   {
                "Pragma": "no-cache",
                "Accept": "application/json, text/plain, */*",
                "Authorization": authorizationToken,
                "currentversioncode": currentVersionCode,
                "Expires": "0", 
                "currentversion": CURRENTVERSION,
                "Accept-Language": "en-us",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "platform": platform,
                "Accept-Encoding": "gzip, deflate",
                "app-authorization": appAuthorization_key,
                "User-Agent": userAgent,
                "Connection": "close",
                "Content-Type": "application/json"
                }
    json =      {
                "AccessPointsIPWAN": ipWAN,
                "CheckinType": checkType,
                "SmartPhoneDeviceIMEI": deviceIMEI
                }
    checkingType = "in"
    if(checkType == 2):
        checkingType = "out"
    req = requests.post(url, headers=headers, json=json)
    if (req.status_code == 200):
        print(name + " Request OK")
        pushInfo("\U0001F44C " + name + " Check" + checkingType, "OK")
    else:
        pushInfo("\U0000274C " + name + " Error type " + str(checkType), req.text)

def getCheckinStatus(authorizationToken, currentVersionCode, platform, appAuthorization_key, userAgent, deviceIMEI, name):
    url = "https://sapi.fpt.vn:443/hrapi/api/services/app/Checkin/GetCheckinStatus"
    headers = {
            "Pragma": "no-cache",
            "Accept": "application/json, text/plain, */*",
            "Authorization": authorizationToken,
            "currentversioncode": currentVersionCode,
            "Expires": "0",
            "currentversion": CURRENTVERSION,
            "Accept-Language": "en-us",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "platform": platform,
            "Accept-Encoding": "gzip, deflate",
            "app-authorization": appAuthorization_key,
            "User-Agent": userAgent,
            "Connection": "close",
            "Content-Type": "application/json"}
    jsonData = {
            "SmartPhoneDeviceIMEI": deviceIMEI
            }
    req = requests.post(url, headers=headers, json=jsonData)
    if(req.status_code == 401):
        pushInfo("\U000026A0 Warning ", name + " token expired!")
        return 0
    else:
        jsonStatus = json.loads(req.text)
        result = jsonStatus['result']
        status = result['status']
        checkinStatus = {
                        "date": status['date'][:10],
                        "checkinTime": status['checkinTime'],
                        "checkoutTime": status['checkoutTime'],
                        "checkinStatus": status['checkinStatus'],
                        "checkoutStatus": status['checkoutStatus']
                        }
        return checkinStatus

dateTime = getCurrentTime()

def isLateTooMuch(authorizationToken, appAuthorization_key):
    url = "https://sapi.fpt.vn:443/hrapi/api/services/app/Checkin/GetListCheckinLogStatisticInMonth"
    headers = {
            "accept": "application/json, text/plain, */*",
            "app-authorization": appAuthorization_key,
            "authorization": authorizationToken,
            "cache-control": "no-cache, no-store, must-revalidate",
            "pragma": "no-cache",
            "expires": "0", "Content-Type": "application/json",
            "Connection": "close",
            "Accept-Encoding": "gzip, deflate"
            }
    month = dateTime.strftime("%m")
    year = dateTime.strftime("%Y")
    data = {
            "Month": month,
            "Year": year
            }
    resp = requests.post(url, headers=headers, json=data)
    monthStatistic = json.loads(resp.text)
    if (monthStatistic['totalLate'] > 2):
        return True
    else:
        return False

def userCheck(name, platform, appAuthorization_key, ipWAN, deviceIMEI):
    NOT_LATEDELAY = random.randint(110, 465)
    LATEDELAY = random.randint(100, 1000)
    authorizationToken = get_AuthorizationToken()
    if (platform == "ios"):
        currentVersionCode = IOS['currentversioncode']
        userAgent = IOS['User-Agent']
    else:
        currentVersionCode = ANDROID['currentversioncode']
        userAgent = ANDROID['User-Agent']
    status = getCheckinStatus(authorizationToken, currentVersionCode, platform, appAuthorization_key, userAgent, deviceIMEI, name)
    day = dateTime.strftime("%a")
    if (day != "Sat" and day != "Sun"):
        if (status['checkinStatus'] == 1 and dateTime.hour == 7 and dateTime.minute <= 59):
            if (isLateTooMuch(authorizationToken, appAuthorization_key)):
                time.sleep(NOT_LATEDELAY)
            else:
                time.sleep(LATEDELAY)
            checkInOut(name, authorizationToken, currentVersionCode, platform, appAuthorization_key, userAgent, ipWAN, 1, deviceIMEI)
        elif (status['checkoutStatus'] == 1 and dateTime.hour >= 17 and dateTime.minute >= 30):
            #time.sleep(random.randint(5, 250))
            checkInOut(name, authorizationToken, currentVersionCode, platform, appAuthorization_key, userAgent, ipWAN, 2, deviceIMEI)
            if (name == "Khoa"):
                status = getCheckinStatus(authorizationToken, currentVersionCode, platform, appAuthorization_key, userAgent, deviceIMEI, name)
                pushInfo("\U0001F4A1 Status",
                            "Date: " + status['date'] + "\n" +
                            "Check In: " + status['checkinTime'] + "\n" +
                            "Check Out: " + status['checkoutTime'])

t1 = threading.Thread(target=userCheck, args=("Khoa", "ios", KHOA['app-authorization'], KHOA['AccessPointsIPWAN'], KHOA['SmartPhoneDeviceIMEI']))
t3 = threading.Thread(target=userCheck, args=("Dat", "ios", DAT['app-authorization'], DAT['AccessPointsIPWAN'], DAT['SmartPhoneDeviceIMEI']))
t4 = threading.Thread(target=userCheck, args=("Nhung", "ios", NHUNG['app-authorization'], NHUNG['AccessPointsIPWAN'], NHUNG['SmartPhoneDeviceIMEI']))
t5 = threading.Thread(target=userCheck, args=("Duc Anh", "android", DUCANH['app-authorization'], DUCANH['AccessPointsIPWAN'], DUCANH['SmartPhoneDeviceIMEI']))
t1.start()
t4.start()
t5.start()
