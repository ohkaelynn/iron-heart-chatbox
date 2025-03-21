import os
import time
import psutil
import json
import random
import threading
from pythonosc.udp_client import SimpleUDPClient
from PIL import Image, ImageDraw
import pystray

# CONFIGURATION FILE PATH
CONFIG_FILE_PATH = "config.json"

# OSC Connection
VRCHAT_OSC_IP = "127.0.0.1"
VRCHAT_OSC_PORT = 9000
client = SimpleUDPClient(VRCHAT_OSC_IP, VRCHAT_OSC_PORT)

# Load Configurations
def load_config():
    """Loads or creates a default configuration file."""
    default_config = {
        "text_file_path": "C:\\path\\to\\heart_rate.txt",
        "check_interval": 5,
        "keep_chatbox_open": True,
        "chatbox_refresh_time": 10,
        "enable_trend": True,
        "enable_contextual": True,
        "heart_icons": ["❤️", "💖", "💗", "💙", "💚", "💛", "💜"],
        "trend_symbols": {"up": "🔺", "down": "🔻", "steady": "➖"},
        "high_bpm_threshold": 100,
        "low_bpm_threshold": 60,
        "high_bpm_message": "🔥 High BPM!",
        "low_bpm_message": "💤 Low BPM...",
        "normal_bpm_message": "😊 Normal",
        "custom_message_format": "{heart_icon} {bpm} BPM {trend_symbol} | {status}"
    }

    if not os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "w") as config_file:
            json.dump(default_config, config_file, indent=4)
        return default_config
    else:
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config_file:
            return json.load(config_file)

config = load_config()

# Heart Rate History for Trend Detection
hr_history = []
last_sent_message = ""
last_sent_time = time.time()
paused = False

def is_iron_heart_running():
    """Check if iron-heart.exe is running."""
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'].lower() == "iron-heart.exe":
            return True
    return False

def read_heart_rate():
    """Read heart rate from the text file."""
    try:
        with open(config["text_file_path"], "r") as file:
            line = file.readline().strip()
            if line.isdigit():
                return int(line)
    except Exception as e:
        print(f"Error reading heart rate file: {e}")
    return None

def get_heart_icon():
    """Cycle through heart icons for variation."""
    return random.choice(config["heart_icons"])

def detect_trend():
    """Analyze recent heart rate changes and return a trend symbol."""
    if not config["enable_trend"] or len(hr_history) < 3:
        return ""  # Not enough data or disabled

    recent_values = hr_history[-3:]  # Check last 3 values
    if recent_values[0] < recent_values[1] < recent_values[2]:
        return config["trend_symbols"]["up"]
    elif recent_values[0] > recent_values[1] > recent_values[2]:
        return config["trend_symbols"]["down"]
    else:
        return config["trend_symbols"]["steady"]

def get_status_message(bpm):
    """Returns a contextual message based on BPM thresholds."""
    if not config["enable_contextual"]:
        return ""
    if bpm >= config["high_bpm_threshold"]:
        return config["high_bpm_message"]
    elif bpm <= config["low_bpm_threshold"]:
        return config["low_bpm_message"]
    else:
        return config["normal_bpm_message"]

def format_message(bpm):
    """Create a user-defined chatbox message using placeholders."""
    heart_icon = get_heart_icon()
    trend_symbol = detect_trend()
    status_message = get_status_message(bpm)
    
    # If contextual messages are disabled, remove status and extra divider
    if not config["enable_contextual"]:
        return f"{heart_icon} {bpm} BPM {trend_symbol}".strip()
    
    return config["custom_message_format"].format(
        bpm=bpm,
        heart_icon=heart_icon,
        trend_symbol=trend_symbol,
        status=status_message
    ).strip()

def send_to_vrchat(message):
    """Send formatted heart rate message to VRChat OSC Chatbox."""
    global last_sent_message, last_sent_time

    try:
        client.send_message("/chatbox/input", [message, True])  # True keeps the chatbox open
        print(f"Sent to VRChat: {message}")
        last_sent_message = message
        last_sent_time = time.time()
    except Exception as e:
        print(f"Failed to send OSC message: {e}")

def main():
    """Main loop to check heart rate and send to VRChat."""
    global paused
    print("Starting Heart Rate to VRChat OSC Script...")

    while True:
        if not paused:
            if is_iron_heart_running():
                bpm = read_heart_rate()
                if bpm:
                    hr_history.append(bpm)
                    if len(hr_history) > 10:
                        hr_history.pop(0)
                    
                    message = format_message(bpm)
                    
                    if message != last_sent_message:
                        send_to_vrchat(message)
                    
                    if config["keep_chatbox_open"] and (time.time() - last_sent_time) > config["chatbox_refresh_time"]:
                        send_to_vrchat(last_sent_message)
            else:
                print("Iron-Heart.exe not running. Waiting...")
        
        time.sleep(config["check_interval"])

# --- SYSTEM TRAY INTEGRATION ---
def create_icon():
    """Create a simple icon for the system tray."""
    icon_size = (64, 64)
    image = Image.new("RGB", icon_size, (255, 0, 255))
    draw = ImageDraw.Draw(image)
    draw.ellipse((10, 10, 54, 54), fill=(255, 0, 255))
    return image

def toggle_pause(icon, item):
    """Pause/unpause the script when clicked."""
    global paused
    paused = not paused
    print(f"Script {'paused' if paused else 'resumed'}.")

def exit_script(icon, item):
    """Exit the script gracefully."""
    icon.stop()
    os._exit(0)

def tray_app():
    """Run the system tray application."""
    icon = pystray.Icon("heart_monitor", create_icon(), menu=pystray.Menu(
        pystray.MenuItem("Pause/Resume", toggle_pause),
        pystray.MenuItem("Exit", exit_script)
    ))
    icon.run()

# Start the main script in a separate thread
threading.Thread(target=main, daemon=True).start()

# Start the system tray
tray_app()
