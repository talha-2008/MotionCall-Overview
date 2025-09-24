import reflex as rx
from typing import TypedDict


class TextContent(TypedDict):
    app_name: str
    enter_room: str
    join_button: str
    feature_1_title: str
    feature_1_desc: str
    feature_2_title: str
    feature_2_desc: str
    feature_3_title: str
    feature_3_desc: str
    feature_4_title: str
    feature_4_desc: str
    lobby_title: str
    join_call_button: str
    back_button: str
    mic_on: str
    mic_off: str
    cam_on: str
    cam_off: str
    share_screen: str
    stop_sharing: str
    start_recording: str
    stop_recording: str
    hang_up: str
    chat_title: str
    settings_title: str
    say_hi: str
    send_message_placeholder: str
    dark_mode: str
    light_mode: str
    language: str
    reduced_motion: str
    you: str
    peer: str
    connecting: str
    connected: str
    reconnecting: str
    peer_left: str
    copied_link: str
    recording_stopped: str
    recording_started: str


TEXT_BN: TextContent = {
    "app_name": "মোশনকল",
    "enter_room": "একটি রুমের নাম লিখুন",
    "join_button": "রুমে যোগ দিন",
    "feature_1_title": "HD ভিডিও কল",
    "feature_1_desc": "ကြည်, পরিষ্কার ভিডিও কোয়ালিটি।",
    "feature_2_title": "স্ক্রিন শেয়ার",
    "feature_2_desc": "আপনার স্ক্রিন সহজেই শেয়ার করুন।",
    "feature_3_title": "রিয়েল-টাইম চ্যাট",
    "feature_3_desc": "কলের সময় বার্তা পাঠান।",
    "feature_4_title": "কল রেকর্ডিং",
    "feature_4_desc": "গুরুত্বপূর্ণ মুহূর্তগুলো রেকর্ড করুন।",
    "lobby_title": "লবি: প্রস্তুত হন",
    "join_call_button": "কলে যোগ দিন",
    "back_button": "ফিরে যান",
    "mic_on": "মাইক অন",
    "mic_off": "মাইক অফ",
    "cam_on": "ক্যামেরা অন",
    "cam_off": "ক্যামেরা অফ",
    "share_screen": "স্ক্রিন শেয়ার করুন",
    "stop_sharing": "শেয়ারিং বন্ধ করুন",
    "start_recording": "রেকর্ডিং শুরু করুন",
    "stop_recording": "রেকর্ডিং বন্ধ করুন",
    "hang_up": "কল শেষ করুন",
    "chat_title": "চ্যাট",
    "settings_title": "সেটিংস",
    "say_hi": "এখনো কোনো বার্তা নেই। হাই বলুন!",
    "send_message_placeholder": "একটি বার্তা টাইপ করুন...",
    "dark_mode": "ডার্ক মোড",
    "light_mode": "লাইট মোড",
    "language": "ভাষা",
    "reduced_motion": "রিডিউসড মোশন",
    "you": "আপনি",
    "peer": "সহকর্মী",
    "connecting": "সংযোগ করা হচ্ছে...",
    "connected": "সংযুক্ত",
    "reconnecting": "পুনরায় সংযোগ করা হচ্ছে...",
    "peer_left": "সহকর্মী চলে গেছে",
    "copied_link": "রুমের লিঙ্ক কপি করা হয়েছে!",
    "recording_stopped": "রেকর্ডিং বন্ধ হয়েছে এবং সংরক্ষিত হয়েছে।",
    "recording_started": "রেকর্ডিং শুরু হয়েছে।",
}
TEXT_EN: TextContent = {
    "app_name": "MotionCall",
    "enter_room": "Enter a room name",
    "join_button": "Join Room",
    "feature_1_title": "HD Video Calls",
    "feature_1_desc": "Crystal clear video quality.",
    "feature_2_title": "Screen Sharing",
    "feature_2_desc": "Easily present your screen.",
    "feature_3_title": "Real-time Chat",
    "feature_3_desc": "Send messages during your call.",
    "feature_4_title": "Call Recording",
    "feature_4_desc": "Record your important moments.",
    "lobby_title": "Lobby: Get Ready",
    "join_call_button": "Join Call",
    "back_button": "Go Back",
    "mic_on": "Mic On",
    "mic_off": "Mic Off",
    "cam_on": "Cam On",
    "cam_off": "Cam Off",
    "share_screen": "Share Screen",
    "stop_sharing": "Stop Sharing",
    "start_recording": "Start Recording",
    "stop_recording": "Stop Recording",
    "hang_up": "Hang Up",
    "chat_title": "Chat",
    "settings_title": "Settings",
    "say_hi": "No messages yet. Say hi!",
    "send_message_placeholder": "Type a message...",
    "dark_mode": "Dark Mode",
    "light_mode": "Light Mode",
    "language": "Language",
    "reduced_motion": "Reduced Motion",
    "you": "You",
    "peer": "Peer",
    "connecting": "Connecting...",
    "connected": "Connected",
    "reconnecting": "Reconnecting...",
    "peer_left": "Peer Left",
    "copied_link": "Room link copied to clipboard!",
    "recording_stopped": "Recording stopped and saved.",
    "recording_started": "Recording started.",
}