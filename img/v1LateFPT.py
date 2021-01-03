import requests
import json
import random
import time
from threading import Thread
import threading
from datetime import datetime

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

AUTHORIZATION_KEY = "Basic dGh1eWhrMkBmcHQuY29tLnZuOjEyMzQ1Ng=="
APP_AUTHORIZATION_KEY = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjIxMjQ3IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6Iktob2FOVjE3QGZwdC5jb20udm4iLCJBc3BOZXQuSWRlbnRpdHkuU2VjdXJpdHlTdGFtcCI6IlVJTklLSEg3M0ZJTUxPNUU2T0M0UVdTT0daRkpDTUM3IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiRW1wbG95ZWUiLCJodHRwOi8vd3d3LmFzcG5ldGJvaWxlcnBsYXRlLmNvbS9pZGVudGl0eS9jbGFpbXMvdGVuYW50SWQiOiIxIiwiRW1wbG95ZWVJZENsYWltIjoiMjEyMjIiLCJzdWIiOiIyMTI0NyIsImp0aSI6ImQwZDk3MzNkLWZmZmQtNDRjYS04MDg1LTM1YmZiYjcwNjE5ZCIsImlhdCI6MTYwNjEwMjYyMywibmJmIjoxNjA2MTAyNjIzLCJleHAiOjE2MTM4Nzg2MjMsImlzcyI6IkhSSVMiLCJhdWQiOiJIUklTIn0.YNBzpYAJIkxwOPu8kVHuSmK8g4mJzrgbd7JOfFLAemE"
CURRENTVERSION = "2.1.1"
#T
def pushInfo(title, messages):
    bot = "bot1263316426"  
    telegramAPI = "https://api.telegram.org/"+ bot +":AAEsMDr5IUbrwRVV2jGgudIwrAuQNiPpy_Q/sendMessage?chat_id=540921490&text=" + title + ":\n" + messages
    print(title + ":\n" + messages + "\n")
    requests.post(telegramAPI)

#Get AuthorizationKey
def get_AuthorizationToken():
    url = "https://sapi.fpt.vn:443/token/GenerateToken"
    headers = {
                "Connection": "close",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "HRISProject/1632 CFNetwork/1197 Darwin/20.0.0",
                "Accept-Language": "en-us",
                "Authorization": AUTHORIZATION_KEY,
                "Accept-Encoding": "gzip, deflate"
                }
    raw_token = requests.get(url, headers=headers)
    token = ""
    if(raw_token.status_code == 200):
        token = "Bearer " + raw_token.text.replace('"','')
        #pushInfo("\U0001F511 Got Authorization Key", token)
        return token
    else:
        pushInfo("\U0001F510 Error Authorization Key", "Something Shitty Happen... Exit Program")
        exit()

#Get Current Time - by python
def getCurrentTime():
    dateTime = datetime.now()
    pushInfo("\U0001F55C Current Time", dateTime.strftime("%c"))
    return dateTime

#Do Check in and Check out. 1 = Checkin, 2 = Checkout
def checkInOut(authorizationToken, appAuthorization_key, checkType):
    url = "https://sapi.fpt.vn:443/hrapi/api/services/app/Checkin/Checkin"
    headers =   {
                "Pragma": "no-cache",
                "Accept": "application/json, text/plain, */*",
                "Authorization": authorizationToken,
                "currentversioncode": "1632",
                "Expires": "0", 
                "currentversion": CURRENTVERSION,
                "Accept-Language": "en-us",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "platform": "ios", "Accept-Encoding": "gzip, deflate",
                "app-authorization": appAuthorization_key,
                "User-Agent": "HRISProject/1632 CFNetwork/1197 Darwin/20.0.0",
                "Connection": "close",
                "Content-Type": "application/json"
                }
    json =      {
                "AccessPointsIPWAN": "U2FsdGVkX1++Du0oN486cfZYRMUMdaEzzGCCUq01M24=",
                "CheckinType": checkType,
                "SmartPhoneDeviceIMEI": "7C448D1A-DFD9-4DAF-A217-AA2B355C6A1A"
                }
    req = requests.post(url, headers=headers, json=json)
    if (req.status_code == 200):
        print("Request OK")
    else:
        pushInfo("\U0000274C Error", req.text)
        pushInfo("\U0001F629 Request type "+ str(checkType), "fail!, exit program...")
        exit()

def getCheckinStatus(authorizationToken, appAuthorization_key):
    url = "https://sapi.fpt.vn:443/hrapi/api/services/app/Checkin/GetCheckinStatus"
    headers = {
            "Pragma": "no-cache",
            "Accept": "application/json, text/plain, */*",
            "Authorization": authorizationToken,
            "currentversioncode": "1632", "Expires": "0",
            "currentversion": CURRENTVERSION,
            "Accept-Language": "en-us",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "platform": "ios",
            "Accept-Encoding": "gzip, deflate",
            "app-authorization": appAuthorization_key,
            "User-Agent": "HRISProject/1632 CFNetwork/1197 Darwin/20.0.0",
            "Connection": "close",
            "Content-Type": "application/json"}
    jsonData = {
            "SmartPhoneDeviceIMEI": "7C448D1A-DFD9-4DAF-A217-AA2B355C6A1A"
            }
    req = requests.post(url, headers=headers, json=jsonData)
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

def vuCheck(checkType):
    def get_VuAuthorizationToken():
        url = "https://sapi.fpt.vn:443/token/GenerateToken"
        headers = {
                    "Connection": "close",
                    "Accept": "application/json, text/plain, */*",
                    "User-Agent": "okhttp/3.12.1",
                    "Accept-Language": "en-us",
                    "Authorization": AUTHORIZATION_KEY,
                    "Accept-Encoding": "gzip, deflate"
                    }
        raw_token = requests.get(url, headers=headers)
        token = "Bearer " + raw_token.text.replace('"','')
        return token

    authorizationToken = get_VuAuthorizationToken()
    appAuthorization_key = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjIxMjQ2IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6IlZ1VkhIMkBmcHQuY29tLnZuIiwiQXNwTmV0LklkZW50aXR5LlNlY3VyaXR5U3RhbXAiOiJaT0ZVSE1UU0lDWURXTklWQkE0TkdRNVc0UUlRUlVQWSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkVtcGxveWVlIiwiaHR0cDovL3d3dy5hc3BuZXRib2lsZXJwbGF0ZS5jb20vaWRlbnRpdHkvY2xhaW1zL3RlbmFudElkIjoiMSIsIkVtcGxveWVlSWRDbGFpbSI6IjIxMjIxIiwic3ViIjoiMjEyNDYiLCJqdGkiOiJhMWFjY2NmYi1kMzc4LTQ0ZjktYTFiNy1kZTIxYWRiNjIxNDIiLCJpYXQiOjE2MDQ5NzkyOTgsIm5iZiI6MTYwNDk3OTI5OCwiZXhwIjoxNjEyNzU1Mjk4LCJpc3MiOiJIUklTIiwiYXVkIjoiSFJJUyJ9.2On5dhG0P4AWqVAhCBtQ5m2NAliZMSfBKoLZXcBCLpY"
    url = "https://sapi.fpt.vn:443/hrapi/api/services/app/Checkin/Checkin"
    headers = {
                "accept": "application/json, text/plain, */*",
                "app-authorization": appAuthorization_key,
                "authorization": authorizationToken,
                "platform": "android",
                "currentversioncode": "32",
                "currentversion": CURRENTVERSION,
                "cache-control": "no-cache, no-store, must-revalidate",
                "pragma": "no-cache", "expires": "0", "Content-Type": "application/json", "Connection": "close",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "okhttp/3.12.1"
                }
    json =      {
                "AccessPointsIPWAN": "U2FsdGVkX19UuLpcx3VkUTxmNvXBu1759LPVyNH43As=",
                "CheckinType": checkType,
                "SmartPhoneDeviceIMEI": "ec22dd1c85f4bc01"
                }
    req = requests.post(url, headers=headers, json=json)
    
    bot = "bot1321871145:AAHHCaUVoJZPQepX3j_1_3ss1lEnXG5vExY"
    title = "\U0001F9D9 Bụt hiện lên và nói:"
    if (req.status_code == 200):
        time = datetime.now()
        vuTime = time.strftime("%X")
        if (checkType == 1):
            messages = "Checkin: " + str(vuTime)
        else:
            messages = "Checkout: " + str(vuTime)           
        telegramAPI = "https://api.telegram.org/" + bot + "/sendMessage?chat_id=1336890414&text=" + title + ":\n" + messages
        requests.post(telegramAPI)
        pushInfo("\U0001F44C Vu Request type " + str(checkType), "OK")
    else:
        pushInfo("\U0000274C Vu Error", req.text)
        messages = "\U0001F62D Error: \n" + req.text
        telegramAPI = "https://api.telegram.org/" + bot + "/sendMessage?chat_id=1336890414&text=" + title + ":\n" + messages
        requests.post(telegramAPI)
        exit()

def datCheck(checkType):
    def get_datAuthorizationToken():
        url = "https://sapi.fpt.vn:443/token/GenerateToken"
        headers = {
                    "Connection": "close",
                    "Accept": "application/json, text/plain, */*",
                    "User-Agent": "okhttp/3.12.1",
                    "Accept-Language": "en-us",
                    "Authorization": AUTHORIZATION_KEY,
                    "Accept-Encoding": "gzip, deflate"
                    }
        raw_token = requests.get(url, headers=headers)
        token = "Bearer " + raw_token.text.replace('"','')
        return token

    authorizationToken = get_datAuthorizationToken()
    appAuthorization_key = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjIxMjQ0IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6IkRhdE5UMTQwQGZwdC5jb20udm4iLCJBc3BOZXQuSWRlbnRpdHkuU2VjdXJpdHlTdGFtcCI6IlZXRE9NR0c2VlpPR1JERllKM1pXRFpDUjZHU0tUWEJFIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiRW1wbG95ZWUiLCJodHRwOi8vd3d3LmFzcG5ldGJvaWxlcnBsYXRlLmNvbS9pZGVudGl0eS9jbGFpbXMvdGVuYW50SWQiOiIxIiwiRW1wbG95ZWVJZENsYWltIjoiMjEyMTkiLCJzdWIiOiIyMTI0NCIsImp0aSI6ImEyYzA4ODUzLTJmZjUtNDQxNi1hMWM3LTE5OTcwNTIyYmQ5OSIsImlhdCI6MTYwODI3NTQ3NSwibmJmIjoxNjA4Mjc1NDc1LCJleHAiOjE2MTYwNTE0NzUsImlzcyI6IkhSSVMiLCJhdWQiOiJIUklTIn0.hBbrhLr8ysqiFeGKB0pRvoCK3yRFgOuUagRS1-E5z28"
    url = "https://sapi.fpt.vn:443/hrapi/api/services/app/Checkin/Checkin"
    headers =   {
                "Pragma": "no-cache",
                "Accept": "application/json, text/plain, */*",
                "Authorization": authorizationToken,
                "currentversioncode": "1632",
                "Expires": "0", 
                "currentversion": CURRENTVERSION,
                "Accept-Language": "en-us",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "platform": "ios", "Accept-Encoding": "gzip, deflate",
                "app-authorization": appAuthorization_key,
                "User-Agent": "HRISProject/1632 CFNetwork/1197 Darwin/20.0.0",
                "Connection": "close",
                "Content-Type": "application/json"
                }
    json =      {
                "AccessPointsIPWAN": "U2FsdGVkX1+vqUCIQ89ZPkKn3vrEKmg4LplSAFg6Hbs=",
                "CheckinType": checkType,
                "SmartPhoneDeviceIMEI": "2A7ACC22-1402-4C84-AB66-B238FC8E37B9"
                }
    req = requests.post(url, headers=headers, json=json)
    if (req.status_code == 200):
        pushInfo("\U0001F44C Dat Request type " + str(checkType), "OK")
    else:
        pushInfo("\U0000274C Dat Error", req.text)
        exit()        

dateTime = getCurrentTime()

def myCheckin():
    day = dateTime.strftime("%a")

    if (day != "Sat" and day != "Sun"):        
        AuthorizationToken = get_AuthorizationToken()
        time.sleep(random.randint(1, 5))
        status = getCheckinStatus(AuthorizationToken, APP_AUTHORIZATION_KEY)
        #Random Delay
        delay = random.randint(50, 365)
        if (status['checkinStatus'] == 1 and dateTime.hour == 7 and dateTime.minute <= 59):
            pushInfo("\U000023F3 Delay Action", str(delay) + " seconds")
            #Check In
            time.sleep(delay)
            checkInOut(AuthorizationToken, APP_AUTHORIZATION_KEY, 1)
            time.sleep(1)
            status = getCheckinStatus(AuthorizationToken, APP_AUTHORIZATION_KEY)
            pushInfo("\U0001F44C Check in", "Complete")
            pushInfo("\U0001F4A1 Status",
                        "Date: " + status['date'] + "\n" +
                        "Check In: " + status['checkinTime'] + "\n" +
                        "Check Out: " + status['checkoutTime'])

        elif (status['checkoutStatus'] == 1 and dateTime.hour >= 17 and dateTime.minute >= 30):
            pushInfo("\U000023F3 Delay Action", str(delay) + " seconds")
            #Check Out
            time.sleep(delay)
            checkInOut(AuthorizationToken, APP_AUTHORIZATION_KEY, 2)
            time.sleep(1)
            status = getCheckinStatus(AuthorizationToken, APP_AUTHORIZATION_KEY)
            pushInfo("\U0001F44C Check out", "Complete!")
            pushInfo("\U0001F4A1 Status",
                        "Date: " + status['date'] + "\n" +
                        "Check In: " + status['checkinTime'] + "\n" +
                        "Check Out: " + status['checkoutTime'])
        else:      
            pushInfo("\U0001F4A1 Status",
                        "Date: " + status['date'] + "\n" +
                        "Check In: " + status['checkinTime'] + "\n" +
                        "Check Out: " + status['checkoutTime'])
            pushInfo("\U0001F4A1 Info", "Nothing to do now, gotta work \U0001F4AA")
    else:
        pushInfo("\U0001F4A1 Info", "Enjoy The Weekend! \U0001F604")

def vuCheckin():
    day = dateTime.strftime("%a")
    if (day != "Sat" and day != "Sun"):
        if (dateTime.hour == 7 and dateTime.minute <= 59):
            time.sleep(random.randint(5, 300))
            vuCheck(1)
        elif (dateTime.hour >= 17 and dateTime.minute >= 30):
            time.sleep(random.randint(3, 250))
            vuCheck(2)

def datCheckin():
    day = dateTime.strftime("%a")
    if (day != "Sat" and day != "Sun"):
        if (dateTime.hour == 7 and dateTime.minute <= 59):
            time.sleep(random.randint(5, 300))
            datCheck(1)
        elif (dateTime.hour >= 17 and dateTime.minute >= 30):
            time.sleep(random.randint(5, 250))
            datCheck(2)

t1 = threading.Thread(target=myCheckin)
t2 = threading.Thread(target=vuCheckin)
t3 = threading.Thread(target=datCheckin)
t1.start()
t2.start()
t3.start()
