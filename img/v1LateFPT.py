import requests
import json
import random
import time
from datetime import datetime

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

AUTHORIZATION_KEY = "Basic dGh1eWhrMkBmcHQuY29tLnZuOjEyMzQ1Ng=="
APP_AUTHORIZATION_KEY = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjIxMjQ3IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6Iktob2FOVjE3QGZwdC5jb20udm4iLCJBc3BOZXQuSWRlbnRpdHkuU2VjdXJpdHlTdGFtcCI6IlVJTklLSEg3M0ZJTUxPNUU2T0M0UVdTT0daRkpDTUM3IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiRW1wbG95ZWUiLCJodHRwOi8vd3d3LmFzcG5ldGJvaWxlcnBsYXRlLmNvbS9pZGVudGl0eS9jbGFpbXMvdGVuYW50SWQiOiIxIiwiRW1wbG95ZWVJZENsYWltIjoiMjEyMjIiLCJzdWIiOiIyMTI0NyIsImp0aSI6IjdkZTJkM2U5LWFiYTItNGQxNC04NTgxLWU5YmE1YmViNDEzMiIsImlhdCI6MTYwNDQ2NjY4NCwibmJmIjoxNjA0NDY2Njg0LCJleHAiOjE2MTIyNDI2ODQsImlzcyI6IkhSSVMiLCJhdWQiOiJIUklTIn0.N8HQCtkSKj6YZWUJxIkvyI6ixn3NcOF99Ei4FC97ByA"

ALERT = 0
def pushInfo(title, messages):
    bot = "bot1263316426"
    ##REMOVE NOFITY SUPPORT, LESS NOISE, ALL GO TELEGRAM
    # global ALERT
    # try:
    #     import androidhelper
    #     droid = androidhelper.Android()
    #     droid.notify(title, messages)
    # except:
    #     if(ALERT == 0):
    #         ALERT+=1
    #         print("Info: No Android Helper Support")     
    telegramAPI = "https://api.telegram.org/"+ bot +":AAEsMDr5IUbrwRVV2jGgudIwrAuQNiPpy_Q/sendMessage?chat_id=540921490&text=" + title + ":\n" + messages
    print(title + ":\n" + messages + "\n")
    requests.post(telegramAPI)

#Get AuthorizationKey
def get_AuthorizationToken(authorization_key):
    url = "https://sapi.fpt.vn:443/token/GenerateToken"
    headers = {
                "Connection": "close",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "HRISProject/1611 CFNetwork/1197 Darwin/20.0.0",
                "Accept-Language": "en-us",
                "Authorization": authorization_key,
                "Accept-Encoding": "gzip, deflate"
                }
    raw_token = requests.get(url, headers=headers)
    token = ""
    if(raw_token.status_code == 200):
        token = "Bearer " + raw_token.text.replace('"','')
        pushInfo("\U0001F511 Got Authorization Key", token)
        return token
    else:
        pushInfo("\U0001F510 Error Authorization Key", "Something Shitty Happen... Exit Program")
        exit()

# #Get Current Time - by python
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
                "currentversioncode": "1611",
                "Expires": "0", "currentversion": "2.0.3",
                "Accept-Language": "en-us",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "platform": "ios", "Accept-Encoding": "gzip, deflate",
                "app-authorization": appAuthorization_key,
                "User-Agent": "HRISProject/1611 CFNetwork/1197 Darwin/20.0.0",
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
        pushInfo("\U0001F44C Request type "+ str(checkType), "complete!")
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
            "currentversioncode": "1611", "Expires": "0", "currentversion": "2.0.3", "Accept-Language": "en-us",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "platform": "ios",
            "Accept-Encoding": "gzip, deflate",
            "app-authorization": appAuthorization_key,
            "User-Agent": "HRISProject/1611 CFNetwork/1197 Darwin/20.0.0",
            "Connection": "close",
            "Content-Type": "application/json"}
    jsonData={
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

# dateTime = getCurrentTime()
dateTime = datetime(2020, 9, 9, 7, 45)
day = dateTime.strftime("%a")

if (day != "Sat" and day != "Sun"):  
    AuthorizationToken = get_AuthorizationToken(AUTHORIZATION_KEY)
    status = getCheckinStatus(AuthorizationToken, APP_AUTHORIZATION_KEY)
    
    #Random Delay
    delay = random.randint(10, 321)
    if (dateTime.hour == 7 and dateTime.minute <= 59):
    # if (status['checkinStatus'] == 1 and dateTime.hour == 7 and dateTime.minute <= 59):
        pushInfo("\U000023F3 Delay Action", str(delay) + " seconds")
        #Check In
        time.sleep(delay)
        # checkInOut(AuthorizationToken, APP_AUTHORIZATION_KEY, 1)
        pushInfo("\U0001F44C Check in", "Complete")
        pushInfo("\U0001F4A1 Status",
                    "Date: " + status['date'] + "\n" +
                    "Check In: " + status['checkinTime'] + "\n" +
                    "Check Out: " + status['checkoutTime'])
    elif (status['checkoutStatus'] == 1 and dateTime.hour >= 17 and dateTime.minute >= 30):
        pushInfo("\U000023F3 Delay Action", str(delay) + " seconds")
        #Check Out
        time.sleep(delay)
        # checkInOut(AuthorizationToken, APP_AUTHORIZATION_KEY, 2)
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