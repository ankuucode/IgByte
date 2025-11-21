
import requests,json,random,re
from user_agent import generate_user_agent
import hashlib
import uuid

#======================================================================================

def token():
    url=f"https://www.instagram.com/accounts/password/reset/"
    res=requests.get(url)
    tok=res.cookies.get('csrftoken')
    return tok

def igresetv1(user:str):
    url=f'https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/'
    head={
  "accept": "*/*",
  "content-type": "application/x-www-form-urlencoded",
  "x-csrftoken": token(),
  "user-agent": generate_user_agent(),
  "x-ig-www-claim": "0",
  "sec-ch-ua-platform-version": "\"6.0\"",
  "origin": "https://www.instagram.com",
  "sec-fetch-site": "same-origin",
  "sec-fetch-mode": "cors",
  "sec-fetch-dest": "empty",
  "referer": "https://www.instagram.com/accounts/password/reset/",
  "accept-encoding": "gzip, deflate, br, zstd",
  "accept-language": "en-US,en;q=0.9",
  "priority": "u=1, i"
    }
    data={
  "email_or_username": user,
    }
    res=requests.post(url=url,headers=head,data=data)
    if res.status_code==200:
        res_code=res.text
        return res_code

    else:
        return f"Error: status code={res.status_code}"
#======================================================================================

def igresetv2(user:str):
    ua = generate_user_agent()
    dev = 'android-'
    device_id = dev + hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16]
    uui = str(uuid.uuid4())
    headers = {
        'User-Agent': ua,
        'Cookie': 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    data = {
        'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.' + json.dumps({
            '_csrftoken': '9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
            'adid': uui,
            'guid': uui,
            'device_id': device_id,
            'query': user
        }),
        'ig_sig_key_version': '4',
    }
    res= requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', headers=headers, data=data)
    if res.status_code==200:
        res_code=res.text
    else:
        return f"Error: status code={res.status_code}"

#======================================================================================
def iguid_info(uid):
    lsd = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(32))
    url = "https://www.instagram.com/api/graphql"

    headers = {
        "x-fb-lsd": lsd,
    }

    variables = {
        "userID": str(uid),
        "username": "ankucode"
    }

    data = {
        "lsd": lsd,
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "PolarisUserHoverCardContentV2Query",
        "server_timestamps": "true",
        "doc_id": "31530620256583767",
        "variables": json.dumps(variables)
    }

    res = requests.post(url, headers=headers, data=data)

    try:
        r_json = res.json()

        user = r_json.get("data", {}).get("user", {})

        
        selected = {
            "full_name": user.get("full_name"),
            "followers": user.get("follower_count"),
            "following": user.get("following_count"),
            "media_count": user.get("media_count"),
            "uid": user.get("pk"),
            "username": user.get("username"),
            "is_verified": user.get("is_verified"),
            "profile_pic_url": user.get("profile_pic_url"),
            "Developer":"@AnkuCode",
            "Telegram": "@AnkuCode"
        }

        return selected

    except Exception as e:
        print("Error:", e)
        return None
#======================================================================================

def download_reel(insta_url:str):
    url = f'https://saverify.com/api.php?source=instagram&url={insta_url}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        rjson = response.json()

        video_url = rjson.get('videoUrl')
        caption = rjson.get('description', '')

        hashtags = re.findall(r'#\w+', caption)

        result = {
            'reel_download_link': video_url,
            'caption': caption,
            'hashtags': hashtags,
            'developer': 'ankucode',
            'telegram': 'ankucode'
        }
        res=json.dumps(result,indent=2)
        return res

    except Exception as e:
        print("Error:", e)
        return None
