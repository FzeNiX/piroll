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
        #It's OK
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

def vuCheck(checkType):
    authorizationToken = get_AuthorizationToken(AUTHORIZATION_KEY)
    appAuthorization_key = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjIxMjQ2IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvbmFtZSI6IlZ1VkhIMkBmcHQuY29tLnZuIiwiQXNwTmV0LklkZW50aXR5LlNlY3VyaXR5U3RhbXAiOiJaT0ZVSE1UU0lDWURXTklWQkE0TkdRNVc0UUlRUlVQWSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IkVtcGxveWVlIiwiaHR0cDovL3d3dy5hc3BuZXRib2lsZXJwbGF0ZS5jb20vaWRlbnRpdHkvY2xhaW1zL3RlbmFudElkIjoiMSIsIkVtcGxveWVlSWRDbGFpbSI6IjIxMjIxIiwic3ViIjoiMjEyNDYiLCJqdGkiOiJhMWFjY2NmYi1kMzc4LTQ0ZjktYTFiNy1kZTIxYWRiNjIxNDIiLCJpYXQiOjE2MDQ5NzkyOTgsIm5iZiI6MTYwNDk3OTI5OCwiZXhwIjoxNjEyNzU1Mjk4LCJpc3MiOiJIUklTIiwiYXVkIjoiSFJJUyJ9.2On5dhG0P4AWqVAhCBtQ5m2NAliZMSfBKoLZXcBCLpY"
    
    url = "https://sapi.fpt.vn:443/hrapi/api/services/app/Checkin/Checkin"
    headers = {
                "accept": "application/json, text/plain, */*",
                "app-authorization": appAuthorization_key,
                "authorization": authorizationToken,
                "platform": "android",
                "currentversioncode": "28",
                "currentversion": "2.0.4",
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
    if (req.status_code == 200):
        bot = "bot1321871145:AAHHCaUVoJZPQepX3j_1_3ss1lEnXG5vExY"
        title = "\U0001F618 Anh Vũ Ơi!"
        time = datetime.now()
        vuTime = time.strftime("%X")
        if (checkType == 1):
            messages = "Em đang đi WC không bấm checkin được lúc " + str(vuTime) + " \U0001F60C"
        else:
            messages = "Em out lúc " + str(vuTime) + " rồi \U0001F4A6"
            
        telegramAPI = "https://api.telegram.org/" + bot + "/sendMessage?chat_id=1336890414&text=" + title + ":\n" + messages
        requests.post(telegramAPI)       
    else:
        pushInfo("\U0000274C Error", req.text)
        messages = "\U0001F62D Phát này lỗi thật, đéo đùa đâu :((. Response đây: \n" + req.text
        telegramAPI = "https://api.telegram.org/" + bot + "/sendMessage?chat_id=1336890414&text=" + title + ":\n" + messages
        pushInfo("\U0001F629 Request type "+ str(checkType), "fail!, exit program...")
        exit()

def getShopeeCoin():
    url = "https://shopee.vn:443/mkt/coins/api/v1/checkin_v2/"
    cookies = {"SPC_F": "qWb3oHnlIUuCpoYXqcuQjz3fDxfzKiTn", "REC_T_ID": "40be385a-e218-11ea-9c99-3c15fb7e99d8", "G_ENABLED_IDPS": "google", "SPC_CLIENTID": "qWb3oHnlIUuCpoYXckmidbnfqyrzenfy", "_gcl_au": "1.1.1908891617.1599114002", "_fbp": "fb.1.1599114002859.1144863651", "_ga": "GA1.2.1891969140.1599114004", "_hjid": "7a066d7e-2e09-47bf-a016-a5b6f5cb43fa", "_gcl_aw": "GCL.1603251586.CjwKCAjwlbr8BRA0EiwAnt4MTvSc1bNQJRSB-rTTE499IC-RB86ktKesPBqTMs4L8Fz0GCzyuatAJxoC3cwQAvD_BwE", "_gac_UA-61914164-6": "1.1603251588.CjwKCAjwlbr8BRA0EiwAnt4MTvSc1bNQJRSB-rTTE499IC-RB86ktKesPBqTMs4L8Fz0GCzyuatAJxoC3cwQAvD_BwE", "_med": "affiliates", "_fbc": "fb.1.1604754233867.IwAR05i7DgZKAYoBGaMcZ9lWB2lHZzcqbjJdJdpwuYiec61WMdw_L4cgj9ymQ", "csrftoken": "ZElH45ven16McXZrQsjCneMNVaLxUf6H", "SPC_SI": "bffsg3.2QtX6zBS5S4Wi2bJElKEjRthKZPYkFvV", "welcomePkgShown": "true", "_gid": "GA1.2.1036316801.1604897797", "_hjAbsoluteSessionInProgress": "0", "SPC_U": "18714056", "SPC_EC": "Ogo/LgnNg+wBnyyjpp4YLWCRUiIsXnX7OM395VqivxIDqZVbeQ6tBTzDJl/PSNywPIwazk3lkFk981UJpyS7FQ5ZqPkgTAr8DvH7zqnb4o822ATviea2eM2swsN3UrcERM2NQjGiBQhVMOq288KqWA==", "SPC_IA": "1", "SPC_R_T_ID": "\"VluuRQVnaAZP1oQSIjinYzsfwssPgCadGuQtTvFuUam3Z1qtc1Ms5p24Tu0kAXhU0WAcUPMQzydEUqXgegTkmSErVVxnotlPReQ5+xSMhHQ=\"", "SPC_T_IV": "\"lK/lNCTFIP+B1nVsFe1jhw==\"", "SPC_R_T_IV": "\"lK/lNCTFIP+B1nVsFe1jhw==\"", "SPC_T_ID": "\"VluuRQVnaAZP1oQSIjinYzsfwssPgCadGuQtTvFuUam3Z1qtc1Ms5p24Tu0kAXhU0WAcUPMQzydEUqXgegTkmSErVVxnotlPReQ5+xSMhHQ=\""}
    headers = {"Connection": "close", "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7"}
    resp = requests.post(url, headers=headers, cookies=cookies)
    data = json.loads(resp.text)
    try:
        coin = data['increase_coins']
        message = "Get " + coin + " shopee coins today!"
        pushInfo("\U0001F514 Shopee Coins", message)
    except:
        message = "Shopee cookie may expired"
        pushInfo("\U000026A0 Shopee Coins", message)

dateTime = getCurrentTime()
day = dateTime.strftime("%a")

if (day != "Sat" and day != "Sun"):  
    AuthorizationToken = get_AuthorizationToken(AUTHORIZATION_KEY)
    status = getCheckinStatus(AuthorizationToken, APP_AUTHORIZATION_KEY)

    #Random Delay
    delay = random.randint(20, 310)
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
        # Vu~
        time.sleep(random.randint(1, 25))
        vuCheck(1)

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
        # Vu~
        time.sleep(random.randint(1, 20))   
        vuCheck(2)
    else:      
        pushInfo("\U0001F4A1 Status",
                    "Date: " + status['date'] + "\n" +
                    "Check In: " + status['checkinTime'] + "\n" +
                    "Check Out: " + status['checkoutTime'])
        pushInfo("\U0001F4A1 Info", "Nothing to do now, gotta work \U0001F4AA")
else:
    pushInfo("\U0001F4A1 Info", "Enjoy The Weekend! \U0001F604")

#Another Job. LOL
if (dateTime.hour < 10):
    getShopeeCoin()