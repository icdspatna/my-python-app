import random
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth_bp', __name__)

# 1. 10 प्री-रजिस्टर्ड यूजर्स का डेटाबेस (Hardcoded for security)
REGISTERED_USERS = {
    "admin": {"password": "1234",     "mobile": "7870590106", "name": "VIRAJ KUMAR"},
    "user": {"password": "1234", "mobile": "7870590106", "name": "CHANDANI KUMARI"},
    
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
        
        # बदलाव: हम सुरक्षात्मक मास्क के साथ-साथ टेस्टिंग के लिए OTP भी स्क्रीन पर भेज रहे हैं
        return jsonify({
            "status": "success", 
            "message": "ओटीपी सफलतापूर्वक जनरेट हो गया है।",
            "testing_otp": generated_otp,  # यह स्क्रीन पर OTP दिखाएगा
            "masked_mobile": f"******{user_info['mobile'][-4:]}"
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

