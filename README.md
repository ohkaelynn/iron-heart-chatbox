# Iron-Heart VRChat OSC Chatbox Proxy

A Python script that **reads heart rate data from Iron-Heart** and **displays it in VRChat's chatbox using OSC**.  

---

## 📌 Features

✅ **Proxy between [nullstalgia/iron-heart](https://github.com/nullstalgia/iron-heart/) and VRChat OSC Chatbox**.  
✅ **Customizable message format**.  
✅ **Trends (🔺/🔻) & contextual messages**.  
✅ **Runs automatically in the background**.  

---

## 🔧 Setup

### 1️⃣ Install Dependencies
```sh
pip install psutil roslibpy
```

### 2️⃣ Run the Script  
```sh
python iron-heart-chat.py
```

### 3️⃣ Launch VRChat & See Your BPM in Chatbox 🎉  

---

## ⚙️ Configuration (`config.json`)  
_Edit this file to customize messages._  

```json
{
    "text_file_path": "C:\\path\\to\\heart_rate.txt",
    "check_interval": 5,
    "keep_chatbox_open": true,
    "chatbox_refresh_time": 10,
    "enable_trend": true,
    "enable_contextual": true,
    "heart_icons": ["❤️", "💖", "💗", "💙", "💚", "💛", "💜"],
    "trend_symbols": {"up": "🔺", "down": "🔻", "steady": "➖"},
    "high_bpm_threshold": 100,
    "low_bpm_threshold": 60,
    "high_bpm_message": "🔥 High BPM!",
    "low_bpm_message": "💤 Low BPM...",
    "normal_bpm_message": "😊 Normal",
    "custom_message_format": "{heart_icon} {bpm} BPM {trend_symbol} | {status}"
}
```

### 📝 Example Output  
```
💖 75 BPM ➖ | 😊 Normal
💙 102 BPM 🔺 | 🔥 High BPM!
💚 58 BPM 🔻 | 💤 Low BPM...
```

---

## 💻 Technologies Used
- **Python 3** – Core scripting language.  
- **psutil** – Detects if **Iron-Heart.exe** is running.  
- **roslibpy** – Sends messages to **VRChat’s chatbox**.  

---

## 📝 Credits  
- 🎯 **[nullstalgia/iron-heart](https://github.com/nullstalgia/iron-heart/)** – Original OSC heart rate monitor.  
- 💬 **[BoiHanny/vrcosc-magicchatbox](https://github.com/BoiHanny/vrcosc-magicchatbox/)** – Trends Logic, Inspiration.  

---

## 💽 License  
📝 **MIT License** – Open-source, free to modify & distribute!  

---
