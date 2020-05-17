import requests
import hashlib
import base64
from pyDes import *
import time
from datetime import datetime
from classes.functions import Functions

class GhoulCatchers:
    def __init__(self, username, password):
        self.s = requests.session()
        self.functions = Functions()
        self.api = 'api.jumpstart.com'
        self.userid = None
        self.apitoken = None
        self.username = username
        self.password = password
        
    def getTicks(self, date):
        return (date - datetime(1, 1, 1)).total_seconds() * 10000000

    def decryptData(self, data):
        decriptionKey = "AFDF51E3-063E-496B-8762-260063880244"
        encodedKey = decriptionKey.encode("utf-16-le")
        decriptionHash = hashlib.md5()
        decriptionHash.update(encodedKey)
        finalKey = decriptionHash.digest()
        tDes = triple_des(finalKey)
        return tDes.decrypt(base64.b64decode(data))

    def encyptData(self, data):
        decriptionKey = "AFDF51E3-063E-496B-8762-260063880244"
        encodedKey = decriptionKey.encode("utf-16-le")
        decriptionHash = hashlib.md5()
        decriptionHash.update(encodedKey)
        finalKey = decriptionHash.digest()
        tDes = triple_des(finalKey)
        enc = tDes.encrypt(data.encode("utf-16-le"), padmode=PAD_PKCS5)
        return enc

    def loginParent(self):
        url = "https://%s/Common/v3/AuthenticationWebService.asmx/LoginParent" % self.api
        encryptedData = self.encyptData('<?xml version="1.0" encoding="utf-16"?><ParentLoginData xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><UserName>' + self.username +'</UserName><Password>' + self.password + '</Password><Locale>en-US</Locale><FacebookAccessToken /><ExternalUserID xsi:nil="true" /><ExternalAuthData xsi:nil="true" /><email xsi:nil="true" /><SubscriptionID>0</SubscriptionID><ReceivesEmail>false</ReceivesEmail><AutoActivate xsi:nil="true" /><SendActivationEmail xsi:nil="true" /><SendWelcomeEmail xsi:nil="true" /><LinkUserToFaceBook xsi:nil="true" /><FavouriteTeamID xsi:nil="true" /><GroupID xsi:nil="true" /><UserPolicy><TermsAndConditions>true</TermsAndConditions><PrivacyPolicy>true</PrivacyPolicy></UserPolicy></ParentLoginData>')
        data = {"apiKey": "4a8b1082-5a88-40fc-a9f0-44ced5699267",
        "parentLoginData": base64.b64encode(encryptedData)}
        resp = self.s.post(url, data=data)
        encryptedData = self.functions.getBetween(resp.text, '<string>', '</string>')
        decryptedData = self.decryptData(encryptedData)
        self.apitoken = self.functions.getBetween(decryptedData.decode("utf-16-le"), '<ApiToken>', '</ApiToken>')
        self.userid = self.functions.getBetween(decryptedData.decode("utf-16-le"), '<UserID>', '</UserID>')
        self.functions.log('Ghoul Catchers: Logged in as %s' % self.username)

    def loginChild(self):
        url = "https://%s/Common/AuthenticationWebService.asmx/LoginChild" % self.api
        _ticks = int(self.getTicks(datetime.utcnow()))
        _childId = self.encyptData(self.userid)
        a, b, c, e, f = str(_ticks), "AFDF51E3-063E-496B-8762-260063880244", self.apitoken, base64.b64encode(_childId).decode(), "en-US"
        _s = a + b + c + e + f
        data = {"apiKey": "4a8b1082-5a88-40fc-a9f0-44ced5699267", "parentApiToken": self.apitoken, "ticks": str(_ticks), "signature": hashlib.md5(_s.encode()).hexdigest(), "childUserID": base64.b64encode(_childId).decode(), "locale": "en-US"}
        resp = self.s.post(url, data=data)
        _apitoken = self.functions.getBetween(resp.text, '<string>', '</string>')
        self.apitoken = self.decryptData(_apitoken).decode("utf-16-le")[:-4]

    def sendScore(self):
        for x in enumerate(range(50), 1):
            url = "https://api.jumpstart.com/Achievement/AchievementWebService.asmx/ApplyPayout"
            _ticks = int(self.getTicks(datetime.utcnow()))
            a, b, c, d, e = str(_ticks), "AFDF51E3-063E-496B-8762-260063880244", self.apitoken, "GCElementMatch", "300"
            _s = a + b + c + d + e
            data = {"apiToken": self.apitoken,
            "apiKey": "4a8b1082-5a88-40fc-a9f0-44ced5699267",
            "ModuleName": "GCElementMatch",
            "points": "300",
            "ticks": str(_ticks),
            "signature": hashlib.md5(_s.encode()).hexdigest()}
            self.s.post(url, data=data)
            self.functions.log('Ghoul Catchers: Score successfully sent (%s/50)' % x[0])
            time.sleep(10)

    def GhoulCatchers(self):
        self.functions.createTaskData('ghoul', self.username)
        if time.time() - float(self.functions.lastRun('ghoul', self.username)) >= 86400:
            self.loginParent()
            self.loginChild()
            self.sendScore()
            self.functions.updateLastRun('ghoul', self.username)
