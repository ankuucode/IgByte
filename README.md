# igbyte 🚀

**igbyte** is a lightweight Python package that provides practical Instagram utilities, including:

- Fetching public Instagram user information via user ID  
- Extracting reel metadata (caption, hashtags, video link)  
- Resetting Instagram accounts using Web or Android APIs  
- Downloading Instagram reels effortlessly  

---

## 📦 Installation

Install using pip:

```bash
pip install igbyte
```

---

## 🛠 Features & Usage

### 1️⃣ Fetch Instagram Profile Info

```python
from igbyte import iguid_info

# Replace with a real user ID
user_info = iguid_info("3954561043")
print(user_info)
```

---

### 2️⃣ Reset Instagram Account

#### Available Reset Methods:
1. **Web API → `igresetv1`**  
2. **Android API → `igresetv2`**

```python
from igbyte import igresetv1, igresetv2

# Web API reset
reset_web = igresetv1("ankucode")
print(reset_web)

# Android API reset
reset_android = igresetv2("ankucode")
print(reset_android)
```

---

### 3️⃣ Download Instagram Reels

```python
from igbyte import download_reel

reel_data = download_reel("https://www.instagram.com/reel/")
print(reel_data)
```

---

## 📧 Contact & Author

**Author:** AnkuCode  
**Email:** ankucode@gmail.com  
**Telegram:** [@ankucode](https://t.me/ankucode)
