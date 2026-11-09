import random
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth_bp', __name__)

# सुधार 1: डिक्शनरी के सिंटैक्स को पूरी तरह साफ और क्लोज किया गया ताकि SyntaxError न आए
REGISTERED_USERS = {
    "admin": {"password": "1234", "mobile": "7870590106", "name": "VIRAJ KUMAR"},
    "user": {"password": "1234", "mobile": "7870590106", "name": "CHANDANI KUMARI"}
}

# लाइव जेनरेटेड OTP को अस्थायी रूप से स्टोर करने के लिए
OTP_STORE = {}

# API 1: यूजरनाम और पासवर्ड चेक करके OTP भेजना
@auth_bp.route('/api/auth/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    
    # यूजरनाम और पासवर्ड का सख्त सत्यापन
    if username in REGISTERED_USERS and REGISTERED_USERS[username]["password"] == password:
        user_info = REGISTERED_USERS[username]
        
        # 4 डिजिट का रैंडम OTP जेनरेट करना
        generated_otp = str(random.randint(1000, 9999))
        
        # OTP को इस यूजर के मोबाइल नंबर के साथ मैप करके सेव करना
        OTP_STORE[username] = generated_otp
        
        # टेस्टिंग मोड एक्टिव: सुरक्षात्मक मास्क के साथ टेस्टिंग OTP भी स्क्रीन पर भेजा जा रहा है
        return jsonify({
            "status": "success", 
            "message": "ओटीपी सफलतापूर्वक जनरेट हो गया है।",
            "testing_otp": generated_otp,  
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
    
    # सुधार 2: सख्त नली-चेक (Null-Check) ताकि ब्लैंक या अमान्य इनपुट पर OTP बाईपास न हो सके
    if not username or not user_otp:
        return jsonify({"status": "error", "message": "यूजरनेम और ओटीपी दोनों आवश्यक हैं।"}), 400
        
    if username in OTP_STORE and OTP_STORE[username] == str(user_otp).strip():
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
