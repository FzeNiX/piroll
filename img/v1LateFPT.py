import requests
import json
import random
import time
from datetime import datetime

import androidhelper
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

AUTHORIZATION_KEY = "Basic dGh1eWhrMkBmcHQuY29tLnZuOjEyMzQ1Ng=="
APP_AUTHORIZATION_KEY = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjIxMjQ3IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6Iktob2FOVjE3QGZwdC5jb20udm4iLCJBc3BOZXQuSWRlbnRpdHkuU2VjdXJpdHlTdGFtcCI6IlVJTklLSEg3M0ZJTUxPNUU2T0M0UVdTT0daRkpDTUM3IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiRW1wbG95ZWUiLCJodHRwOi8vd3d3LmFzcG5ldGJvaWxlcnBsYXRlLmNvbS9pZGVudGl0eS9jbGFpbXMvdGVuYW50SWQiOiIxIiwiRW1wbG95ZWVJZENsYWltIjoiMjEyMjIiLCJzdWIiOiIyMTI0NyIsImp0aSI6IjdkZTJkM2U5LWFiYTItNGQxNC04NTgxLWU5YmE1YmViNDEzMiIsImlhdCI6MTYwNDQ2NjY4NCwibmJmIjoxNjA0NDY2Njg0LCJleHAiOjE2MTIyNDI2ODQsImlzcyI6IkhSSVMiLCJhdWQiOiJIUklTIn0.N8HQCtkSKj6YZWUJxIkvyI6ixn3NcOF99Ei4FC97ByA"

droid = androidhelper.Android()

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
    print("[-] Getting Authorization Token from server...")
    raw_token = requests.get(url, headers=headers)
    token = ""
    if(raw_token.status_code == 200):
        print("[+] Got the token :)")
        token = "Bearer " + raw_token.text.replace('"','')
        droid.notify("Got Authorization Key", token)
        print("\t" + token)
        return token
    else:
        droid.notify("Error Authorization Key", "Something Shitty Happen... Exit Program")
        print("Something Shitty Happened... Exit Program")
        exit()

# #Get Current Time - by python
def getCurrentTime():
    dateTime = datetime.now()
    print("[-] Current Time is: " + dateTime.strftime("%c"))
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
        print("[+] Request type "+ str(checkType) + " complete!")
    else:
        print("[X] Error Response:" + req.text)
        droid.notify("Error", req.text)
        print("[+] Request type "+ str(checkType) + " fail!, exit program...")
        droid.notify("Error", "Request type "+ str(checkType) + " fail!, exit program...")
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

dateTime = getCurrentTime()
day = dateTime.strftime("%a")

if (day != "Sat" and day != "Sun"):  
    AuthorizationToken = get_AuthorizationToken(AUTHORIZATION_KEY)
    status = getCheckinStatus(AuthorizationToken, APP_AUTHORIZATION_KEY)
    
    #Random Delay
    delay = random.randint(10, 321)
    if (status['checkinStatus'] == 1 and dateTime.hour == 7 and dateTime.minute <= 59):
        print("[+] Delay action in: " + str(delay) + " seconds")
        droid.notify("Delay Action", "[+] Delay action in: " + str(delay) + " seconds")
        #Check In
        time.sleep(delay)
        checkInOut(AuthorizationToken, APP_AUTHORIZATION_KEY, 1)
        print("\n[+] Check In Done")
        droid.notify("Check in Status", "Check In Complete")
        droid.notify("Status", status['date'] + "\n" +
                    "Check In: " + status['checkinTime'] + "\n" +
                    "Check Out: " + status['checkoutTime'])
    elif (status['checkoutStatus'] == 1 and dateTime.hour >= 17 and dateTime.minute >= 30):
        print("[+] Delay action in: " + str(delay) + " seconds")
        droid.notify("Delay Action", "[+] Delay action in: " + str(delay) + " seconds")
        #Check Out
        time.sleep(delay)
        checkInOut(AuthorizationToken, APP_AUTHORIZATION_KEY, 2)
        print("\n[+] Check Out Done")
        droid.notify("Check out Status", "Check Out Complete")
        droid.notify("Status", status['date'] + "\n" +
                    "Check In: " + status['checkinTime'] + "\n" +
                    "Check Out: " + status['checkoutTime'])
    else:      
        print("Date: " + status['date'])
        print("Check In: " + status['checkinTime'])
        print("Check Out: " + status['checkoutTime'])
        print("\n[+] Nothing to do now, gotta work :D")
        droid.notify("Status", status['date'] + "\n" +
                    "Check In: " + status['checkinTime'] + "\n" +
                    "Check Out: " + status['checkoutTime'])
        droid.notify("Nothing to do", "Nothing to do now, gotta work :D")
else:
    print("Enjoy the rest day, no check to do :D")
    droid.notify("Nothing to do", "Enjoy the rest day, no check to do :D")
