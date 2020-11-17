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
            messages = "Sau này, chỉ có làm thì mới có ăn. Không làm thì chỉ có check in lúc " + str(vuTime) + " \U0001F606"
        else:
            messages = "Do đề kháng kém nên em không check out lúc " + str(vuTime) + " được \U0001F635"
            
        telegramAPI = "https://api.telegram.org/" + bot + "/sendMessage?chat_id=1336890414&text=" + title + ":\n" + messages
        requests.post(telegramAPI)       
    else:
        pushInfo("\U0000274C Error", req.text)
        messages = "\U0001F62D Phát này lỗi thật, đéo đùa đâu :((. Response đây: \n" + req.text
        telegramAPI = "https://api.telegram.org/" + bot + "/sendMessage?chat_id=1336890414&text=" + title + ":\n" + messages
        pushInfo("\U0001F629 Request type "+ str(checkType), "fail!, exit program...")
        exit()

def getShopeeCoin():
    url = "https://shopee.vn:443/mkt/coins/api/v2/checkin"
    cookies = {"SPC_F": "351564216461632_fab1e307c22cc697_307c22cc697fab1e", "UA": "Shopee%20Android%20Beeshop%20locale%2Fvi%20version%3D413%20appver%3D26210", "SPC_AFTID": "114c5172-b8a3-405f-8289-c21ce735daa1", "shopee_app_version": "26210", "csrftoken": "r7y1Gvhw5xfoOw1ErBtbgmnQ6nkYOtiv", "SPC_CLIENTID": "DYaxnW9OavNiSBrtmgutsgogqjegbwqa", "REC_T_ID": "3926955b-2889-11eb-b707-10c172968115", "SPC_F": "351564216461632_fab1e307c22cc697_307c22cc697fab1e", "SPC_SI": "bffvn.nxdAlqbkNGsDd9rXmqq2Rj4CaTHhB7vo", "shopee_rn_version": "1605150888", "SPC_RNBV": "4037010", "userid": "18714056", "shopee_token": "l2V2S9T4+5GyfKwsx0Jgex4ov7HGRl9gmkkB8rCVqk0=", "username": "fzenix", "SPC_U": "18714056", "REC_MD_45": "1605586227", "REC_MD_41_1000121": "1605585928_0_50_0_44", "SPC_EC": "NLK6nTjccFxbee143RxE/j4NW//cY0oocEtFKl8ftcTo+TH8bdg9QfGzBiJTZYK+lvM4rYHDO89urGf3jH3btuO1PuQFexqg25Yiu5YXARa6mIveT1FIw4nGnvSB8pxJ87cFZpANuKCF5H7BDKCedg==", "SPC_R_T_ID": "qhO0SoR7gmB2mDEc/+i2vjaB+6pwAtU9oqfp5J7mZwMTWRavo7mWVCLUIEP3OzSfbDddQCXGbpp3tHhYLluXrvkfjh9HLC9PY4uA7haEKDA=", "SPC_R_T_IV": "dnSFo8KQnV4t7U6NuDy0+Q==", "_ga": "GA1.2.722922578.1605585657", "_gid": "GA1.2.1436838490.1605585657", "_gat": "1"}
    headers = {"x-csrftoken": "r7y1Gvhw5xfoOw1ErBtbgmnQ6nkYOtiv", "x-api-source": "rn", "x-shopee-language": "vi", "referer": "https://shopee.vn/mkt/coins/api//bridge_cmd?cmd=reactPath%3Ftab%3Dbuy%26path%3Dshopee%252FHOME_PAGE%253Fis_tab%253Dtrue", "accept": "application/json", "content-type": "application/json", "if-none-match-": "55b03-afb69e438c4b48e93e5e3a9f7e6a9111", "Connection": "close", "Accept-Encoding": "gzip, deflate", "User-Agent": "Android app Shopee appver=26210 app_type=1"}
    resp = requests.post(url, headers=headers, cookies=cookies)
    data = json.loads(resp.text)
    try:
        msg = data['msg']
        jData = data['data']
        check_in_day = jData['check_in_day']
        increase_coins = jData['increase_coins']
        if(msg == "success"):
            message = "Got " + str(increase_coins) + " coins today! " + "\nStreak: " + str(check_in_day) + " day(s)"
            pushInfo("\U0001F514 Shopee Coins", message)
        else:
            message = "Something Wrong!"
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
    delay = random.randint(5, 310)
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


