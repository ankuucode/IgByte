
import requests,json,random,re
from user_agent import generate_user_agent
import hashlib
import uuid
import time
#======================================================================================

def token():
    url=f"https://www.instagram.com/accounts/password/reset/"
    res=requests.get(url)
    tok=res.cookies.get('csrftoken')
    return tok



def igresetv1(user: str):
    """
    Reset an Instagram account password using the web API.

    Args:
        user (str): Instagram username or email.

    Returns:
        dict: JSON response from Instagram API.

    Example:
        print(igresetv1("username"))
    """

    url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"

    headers = {
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

    data = {
        "email_or_username": user,
    }

    res = requests.post(url=url, headers=headers, data=data)
    return res.json()

#======================================================================================

def igresetv2(user: str):
    """
    Reset an Instagram account password using the **Android private API**.

    This function sends a recovery email or SMS request to Instagram by
    simulating an Android device and signing the request body.

    Args:
        user (str): Instagram username or email.

    Returns:
        str: Response text from Instagram.
            - On success → Instagram recovery message
            - On failure → Error message with server response

    Notes:
        • This method uses Instagram's **private mobile API** (not official).
        • It generates:
            - Random Android User-Agent
            - Random device_id
            - Random UUID for adid and guid
        • The signed_body is required by Instagram to validate the request.

    Example:
        print(igresetv2("instagram_user"))
    """

    ua = generate_user_agent()

    # Generate Android-style device_id
    dev = 'android-'
    device_id = dev + hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16]

    # Generate UUID for guid and adid
    uui = str(uuid.uuid4())

    headers = {
        'User-Agent': ua,
        'Cookie': 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    # Signed body with required API parameters
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

    # Make the request
    res = requests.post(
        'https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/',
        headers=headers,
        data=data
    )

    # Return result
    if res.status_code == 200:
        return res.text
    else:
        return f"Error: {res.text}"

#======================================================================================

def iguid_info(uid):
    """
    Get Instagram account details using the user ID (UID).

    This function fetches basic profile information from Instagram
    for a given user ID by sending a GraphQL query.

    Args:
        uid (str or int): The Instagram user ID.

    Returns:
        dict: A dictionary containing account details:
            - full_name (str): Full name of the user.
            - followers (int): Number of followers.
            - following (int): Number of accounts the user follows.
            - media_count (int): Number of posts/media uploaded.
            - uid (str/int): Instagram user ID.
            - username (str): Instagram username.
            - is_verified (bool): True if the account is verified.
            - profile_pic_url (str): URL of the profile picture.
        None: If an error occurs during the request or parsing.

    Example:
        info = iguid_info("123456789")
        print(info)
    """

    # Generate a random lsd token
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
            "Developer": "@AnkuCode",
            "Telegram": "@AnkuCode"
        }

        return selected

    except Exception as e:
        print("Error:", e)
        return None

#======================================================================================

def download_reel(insta_url:str):
    """
    Download Instagram reel video from a given URL.

    Args:
        insta_url (str): URL of the Instagram reel.
        save_path (str): Optional. Directory to save the video. Defaults to current directory.

    Returns:
        dict: Information about the downloaded reel:
            - file_path (str): Path where video is saved
            - caption (str)
            - hashtags (list)
            - developer (str)
            - telegram (str)
        None: If download fails
    """
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

#======================================================================================

def infoig(user: str):
    """
    Get detailed Instagram profile metadata using the username.

    This function queries Instagram's web API to fetch public profile information
    for a given username. The returned data includes the full profile details,
    along with developer credits.

    Args:
        user (str): Instagram username.

    Returns:
        dict: Dictionary containing the user's profile metadata:
        If an error occurs (e.g., network issue or blocked request), returns:
            {"error": "<error_message>"}

    Example:
        profile_info = infoig("instagram_username")
        print(profile_info)
    """

    headers = {
        'authority': 'www.instagram.com',
        'accept': '*/*',
        'accept-language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': f'https://www.instagram.com/{user}/',
        'user-agent': generate_user_agent(),
        'x-asbd-id': '129477',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': '0',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'username': user,
    }

    try:
        response = requests.get(
            'https://www.instagram.com/api/v1/users/web_profile_info/',
            params=params,
            headers=headers
        ).json()
    except Exception as e:
        return {"error": str(e)}

    info = response.get('data', {}).get('user', {})

    dev = {
        "Developer": "@AnkuCode",
        "TGchannel": "@AnkuCode || @TryByte"
    }

    info.update(dev)
    return info



def gen_igcookie():
    """
    Generate Instagram session cookies.

    This function sends a simple GET request to Instagram's signup page
    in order to obtain:
        - csrftoken  → Required for most Instagram API requests
        - mid        → Machine ID cookie used by Instagram
        - cookies    → Full cookie jar returned by Instagram
    
    Returns:
            print(cookie)
        
            csrftoken (str or None): Instagram CSRF security token
            mid (str or None): Instagram machine ID
            cookies (RequestsCookieJar): All cookies Instagram returned
    """

    # Instagram page used to generate fresh cookies
    url = "https://www.instagram.com/accounts/emailsignup/"

    # User-Agent is required so Instagram doesn't block the request
    headers = {
        'User-Agent': generate_user_agent()
    }

    # Send request
    response = requests.get(url, headers=headers)

    # Extract cookies
    cookies = response.cookies

    # Individually extract useful tokens
    csrf_token = cookies.get("csrftoken")
    mid = cookies.get("mid")
    cooki=f'''
csrf_token= {csrf_token}
mid= {mid}
full_cookies= {cookies}
'''

    return cooki

#======================================================================================

def initiate_signup(userame,email):
    """
    Initiate a web-based signup request.

    This function sends a POST request to a web registration endpoint.
    It prepares required headers, session cookies, and form data needed
    to mimic a standard browser signup attempt.

    Parameters:
        username (str): Desired username for the new account.
        email (str): Email address used during registration.

    Returns:
        str: The raw text response returned by the server.
    """
    url = "https://www.instagram.com/accounts/web_create_ajax/attempt/"
    headers = {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": generate_user_agent(),
        "x-requested-with": "XMLHttpRequest",
        "x-ig-app-id": "936619743392459",
        "x-csrftoken": token(),
        "x-instagram-ajax": "1",
        "origin": "https://www.instagram.com",
        "referer": "https://www.instagram.com/accounts/emailsignup/",
    }
    data ={
  "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:ankucode8596",
  "email": email,
  "failed_birthday_year_count": "{}",
  "first_name": "ankush",
  "username": {userame},
  "opt_into_one_tap": "false",
  "use_new_suggested_user_name": "true",
    }

    res = requests.post(url, headers=headers, data=data)
    return res.text
