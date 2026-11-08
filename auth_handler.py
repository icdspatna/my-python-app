import random
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth_bp', __name__)

# 1. 10 प्री-रजिस्टर्ड यूजर्स का डेटाबेस (Hardcoded for security)
REGISTERED_USERS = {
    "user1": {"password": "passUser1", "mobile": "9876543210", "name": "अमित कुमार"},
    "user2": {"password": "passUser2", "mobile": "9876543211", "name": "राहुल सिंह"},
    "user3": {"password": "passUser3", "mobile": "9876543212", "name": "प्रिया शर्मा"},
    "user4": {"password": "passUser4", "mobile": "9876543213", "name": "मनोज तिवारी"},
    "user5": {"password": "passUser5", "mobile": "9876543214", "name": "दीपक वर्मा"},
    "user6": {"password": "passUser6", "mobile": "9876543215", "name": "सुनीता देवी"},
    "user7": {"password": "passUser7", "mobile": "9876543216", "name": "राजेश यादव"},
    "user8": {"password": "passUser8", "mobile": "9876543217", "name": "अनिल मिश्रा"},
    "user9": {"password": "passUser9", "mobile": "9876543218", "name": "विक्रम सिंह"},
    "user10": {"password": "passUser10", "mobile": "9876543219", "name": "पूजा कुमारी"}
}

# 2. लाइव जेनरेटेड OTP को अस्थायी रूप से स्टोर करने के लिए (Production में Redis या Session का उपयोग करें)
OTP_STORE = {}

# API 1: यूजरनाम और पासवर्ड चेक करके OTP भेजना
@auth_bp.route('/api/auth/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    
    # यूजरनाम और पासवर्ड का सत्यापन
    if username in REGISTERED_USERS and REGISTERED_USERS[username]["password"] == password:
        user_info = REGISTERED_USERS[username]
        
        # 4 डिजिट का रैंडम OTP जेनरेट करना
        generated_otp = str(random.randint(1000, 9999))
        
        # OTP को इस यूजर के मोबाइल नंबर के साथ मैप करके सेव करना
        OTP_STORE[username] = generated_otp
        
        # नोट: यहाँ आप अपना वास्तविक SMS API (जैसे Twilio या Fast2SMS) लगा सकते हैं
        # अभी परीक्षण के लिए हम इसे कंसोल/रिस्पांस में प्रिंट कर रहे हैं
        print(f"[SMS SIMULATION] Sending OTP {generated_otp} to {user_info['mobile']}")
        
        return jsonify({
            "status": "success", 
            "message": "ओटीपी आपके रजिस्टर्ड मोबाइल नंबर पर भेज दिया गया है।",
            "masked_mobile": f"******{user_info['mobile'][-4:]}" # सुरक्षा के लिए सिर्फ आखिरी 4 अंक दिखाएं
        }), 200
    else:
        return jsonify({"status": "error", "message": "गलत यूजरनेम या पासवर्ड।"}), 401

# API 2: यूजर द्वारा डाले गए OTP का सत्यापन करना और लॉगिन पूरा करना
@auth_bp.route('/api/auth/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json() or {}
    username = data.get("username")
    user_otp = data.get("otp")
    
    if username in OTP_STORE and OTP_STORE[username] == str(user_otp):
        # सत्यापन सफल होने पर OTP को स्टोर से हटा दें (सुरक्षा के लिए)
        del OTP_STORE[username]
        
        user_info = REGISTERED_USERS[username]
        return jsonify({
            "status": "success", 
            "message": "लॉगिन सफल रहा।", 
            "user": {"name": user_info["name"], "username": username}
        }), 200
    else:
        return jsonify({"status": "error", "message": "अमान्य या एक्सपायर्ड ओटीपी।"}), 400

