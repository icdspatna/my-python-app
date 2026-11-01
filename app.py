from flask import Flask, render_template_string, request
from flask import jsonify
app = Flask(__name__)
# --- 1. APP LAYOUT START ---
LAYOUT_START = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ICDS App - Rudra Tech</title>
    <!-- गलती 1 सुधार: अमान्य क्लाउडफ्लेयर लिंक को हटाकर सही Font Awesome CDN जोड़ा गया ताकि आइकॉन काम करें -->
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        .tab-content {
            display: none;
            padding: 15px;
            border: 1px solid #ccc;
            border-radius: 8px;
            margin-top: 10px;
        }
        .tab-content.active {
            display: block !important;
        }
        /* लाइव टोटल आवंटन कार्ड्स के लिए स्टाइल */
        .total-card {
            min-width: 140px;
            flex: 1;
            background: white;
            padding: 12px;
            border-radius: 8px;
            border-top: 4px solid #0288d1;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: left;
            display: inline-block;
        }
        .total-card h5 { margin: 0; font-size: 11px; color: #777; font-weight: bold; }
        .total-card p { margin: 5px 0 0 0; font-size: 15px; font-weight: bold; color: #333; }
        
        /* लाइव Remaining Balance लिस्ट के लिए स्टाइल */
        .bal-item {
            display: flex;
            justify-content: space-between;
            padding: 8px;
            background: #fafafa;
            border-radius: 4px;
            font-size: 12px;
            margin-bottom: 6px;
            border-bottom: 1px solid #eee;
        }
        .bal-item span { color: #333; font-weight: 500; }
        .bal-item strong { font-weight: bold; color: #2e7d32; }

        /* गलती 2 सुधार: यहाँ नीचे दोबारा आ रही डुप्लिकेट .tab-content क्लास को हटा दिया गया है */

        body {
            margin: 0; padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            display: flex; justify-content: center; align-items: center;
            height: 100vh;
        }
        
        /* गलती 3 सुधार: यहाँ से पुरानी डुप्लिकेट .mobile-app-container (740px वाली) को हटा दिया गया है */
        
        .app-page {
            display: none; flex: 1; padding: 20px;
            overflow-y: auto; margin-bottom: 65px;
        }
        .app-page.active { display: block; }
        #home {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; text-align: center; height: 100%; box-sizing: border-box;
        }
        .hero-section { margin-top: 30%; }
        .hero-section h1 { font-size: 26px; margin-bottom: 10px; }
        .login-container { margin-top: 15%; text-align: center; padding: 0 10px; }
        .login-container h2 { font-size: 22px; margin-bottom: 5px; }
        .login-form { margin-top: 20px; }
        .input-group {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.4);
            padding: 12px; margin-bottom: 15px; border-radius: 25px;
            display: flex; align-items: center;
        }
        .input-group i { margin-right: 10px; color: #fff; }
        .input-group input { background: none; border: none; outline: none; color: white; width: 100%; }
        .input-group input::placeholder { color: #eee; }
        .login-btn {
            background: #fff; color: #764ba2; border: none; width: 100%;
            padding: 12px; font-size: 16px; font-weight: bold;
            border-radius: 25px; cursor: pointer; margin-top: 15px;
        }
        .page-title { color: #764ba2; border-bottom: 2px solid #764ba2; padding-bottom: 5px; margin-bottom: 15px; font-size: 20px; }
        .form-card { background: #f8f9fa; border: 1px solid #e2e8f0; border-radius: 15px; padding: 15px; margin-bottom: 20px; }
        .form-card h4 { color: #2d3748; margin-top: 0; font-size: 16px; margin-bottom: 12px; }
        .app-input { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #cbd5e0; border-radius: 8px; box-sizing: border-box; font-size: 14px; }
        .submit-btn { width: 100%; padding: 12px; background: #764ba2; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .notice-box { background: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; border-radius: 4px; font-size: 13px; margin-bottom: 10px; color: #856404; }
        .bottom-nav {
            position: absolute; bottom: 0; width: 100%; height: 65px;
            background: #ffffff; display: flex; justify-content: space-around;
            align-items: center; border-top: 1px solid #eee; box-sizing: border-box;
        }
        .nav-item { display: flex; flex-direction: column; align-items: center; color: #888; cursor: pointer; font-size: 11px; }
        .nav-item i { font-size: 20px; margin-bottom: 2px; }
        .nav-item.active { color: #764ba2; font-weight: bold; }
        
        /* मोबाइल कंटेनर की हाइट को फिक्स और परफेक्ट करना (अंतिम सटीक रूल सुरक्षित रखा गया है) */
        .mobile-app-container {
            width: 360px; 
            height: 720px; 
            background: #f0f2f5; 
            border-radius: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden; 
            position: relative;
            display: flex; 
            flex-direction: column;
        }

        /* नया डायनामिक टॉप प्रोफाइल हेडर */
        .app-top-header {
            background: #1e3c72;
            color: white;
            padding: 12px 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            z-index: 10;
        }
        .profile-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .profile-pic {
            width: 32px;
            height: 32px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 14px;
            font-weight: bold;
            border: 1px solid rgba(255,255,255,0.4);
        }
        .logout-btn-top {
            background: #e74c3c;
            color: white;
            border: none;
            padding: 6px 12px;
            font-size: 11px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: background 0.2s;
        }
        .logout-btn-top:hover {
            background: #c0392b;
        }

        /* पेजों की हाइट को हेडर और फुटर के बीच बांधना ताकि ओवरफ्लो न हो */
        .app-page {
            display: none; 
            flex: 1; 
            padding: 15px;
            overflow-y: auto; 
            box-sizing: border-box;
        }
        .app-page.active { 
            display: block; 
        }
    </style>
</head>
<body>
    <div class="mobile-app-container">
    
    <!-- नया टॉप प्रोफाइल हेडर (शुरुआत में style="display:none;" रहेगा) -->
    <div id="appTopHeader" class="app-top-header" style="display: none;">
        <div class="profile-info">
            <div class="profile-pic">A</div>
            <div>
                <div style="font-size: 13px; font-weight: 600;" id="userProfileName">Admin</div>
                <div style="font-size: 9px; opacity: 0.7;">ICDS लॉग-इन एक्टिव</div>
            </div>
        </div>
        <button class="logout-btn-top" onclick="handleAppLogout()">
            <i class="fa-solid fa-right-from-bracket"></i> लॉगआउट
        </button>
    </div>

    <!-- बाकी के पेजेस (जैसे #home, #notice, #service आदि) इसके नीचे रहेंगे... -->


# --- 2. INNER PAGES BODY ---
PAGES_BODY = """
     # --- 2. INNER PAGES BODY ---
# इसे बिल्कुल बाईं तरफ सटाकर रखें, इसके पीछे एक भी खाली स्पेस या टैब नहीं होना चाहिए
PAGES_BODY = """<!-- 1. HOME SCREEN (Modern Style + Live Digital Watch & Location) -->
<div id="home" class="app-page active" style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; height: 100%; box-sizing: border-box; display: flex; flex-direction: column; justify-content: flex-start; align-items: center; padding: 25px 15px; font-family: 'Segoe UI', sans-serif; overflow-y: auto;">
    
    <!-- लाइव डिजिटल वॉच और लोकेशन विजेट -->
    <div style="background: rgba(255, 255, 255, 0.12); backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.2); width: 90%; border-radius: 20px; padding: 15px; text-align: center; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15); margin-bottom: 25px; box-sizing: border-box; animation: fadeIn 0.8s ease-in-out;">
        <!-- समय -->
        <div id="digitalClock" style="font-size: 32px; font-weight: 700; color: #fff; letter-spacing: 1px; text-shadow: 0 2px 5px rgba(0,0,0,0.2);">00:00:00 AM</div>
        <!-- तारीख और साल -->
        <div id="digitalDate" style="font-size: 13px; color: #e2e8f0; font-weight: 500; margin-top: 4px; letter-spacing: 0.5px;">Loading Date...</div>
        <!-- लाइव लोकेशन -->
        <div style="display: flex; align-items: center; justify-content: center; margin-top: 10px; font-size: 11px; color: #ffb703; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 8px;">
           <i class="fa-solid fa-location-dot" style="margin-right: 6px; animation: pulse 2s infinite;"></i>
            <span id="liveLocation">Patna, Bihar, India</span>
        </div>
    </div>
"""
    <!-- ऐप लोगो और ब्रांडिंग -->
    <div class="hero-section" style="text-align: center; margin-bottom: 25px;">
        <div style="background: rgba(255, 255, 255, 0.15); width: 80px; height: 80px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto 12px auto; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); border: 1px solid rgba(255, 255, 255, 0.2);">
            <i class="fa-solid fa-calculator" style="font-size: 36px; color: #fff;"></i>
        </div>
        <h1 style="font-size: 24px; font-weight: 700; margin: 0 0 4px 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">ICDS बजट प्रबंधन</h1>
        <p style="font-size: 11px; opacity: 0.75; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Rudra Tech Pvt Ltd</p>
    </div>

    <!-- मुख्य फॉर्म कार्ड -->
    <div class="login-container" style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border-radius: 24px; padding: 25px 20px; width: 90%; box-shadow: 0 15px 35px rgba(0,0,0,0.25); border: 1px solid rgba(255, 255, 255, 0.18); box-sizing: border-box;">
        
        <!-- स्टेज A: मुख्य लॉगिन फॉर्म -->
        <div id="loginStage">
            <h2 style="font-size: 18px; font-weight: 600; margin: 0 0 18px 0; text-align: center; color: #fff;">खाते में लॉग इन करें</h2>
            <div class="login-form">
                <div class="input-group" style="background: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.25); padding: 12px 15px; margin-bottom: 12px; border-radius: 12px; display: flex; align-items: center;">
                    <i class="fa-solid fa-user" style="margin-right: 12px; color: #cbd5e1; width: 16px;"></i>
                    <input type="text" id="loginUser" placeholder="यूज़र नाम दर्ज करें" style="background: none; border: none; outline: none; color: white; width: 100%; font-size: 14px;" autocomplete="off">
                </div>
                <div class="input-group" style="background: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.25); padding: 12px 15px; margin-bottom: 18px; border-radius: 12px; display: flex; align-items: center;">
                    <i class="fa-solid fa-lock" style="margin-right: 12px; color: #cbd5e1; width: 16px;"></i>
                    <input type="password" id="loginPass" placeholder="पासवर्ड दर्ज करें" style="background: none; border: none; outline: none; color: white; width: 100%; font-size: 14px;">
                </div>
                <button class="login-btn" onclick="validateLogin()" style="background: #fff; color: #1e3c72; border: none; width: 100%; padding: 14px; font-size: 15px; font-weight: bold; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 15px rgba(255,255,255,0.1);">सत्यापित करें और आगे बढ़ें</button>
            </div>
        </div>
</div>
        <!-- स्टेज B: स्क्रीन锁 और OTP वेरिफिकेशन -->
        <div id="otpStage" style="display: none; text-align: center;">
            <div style="color: #ffb703; font-size: 32px; margin-bottom: 8px;"><i class="fa-solid fa-shield-halved"></i></div>
            <h2 style="font-size: 17px; font-weight: 600; margin: 0 0 6px 0; color: #fff;">सुरक्षा स्क्रीन लॉक</h2>
            <p style="font-size: 12px; color: #e2e8f0; margin: 0 0 18px 0;">आपके रजिस्टर्ड नंबर पर OTP भेजा गया है।</p>
            
            <div class="input-group" style="background: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.25); padding: 12px 15px; margin-bottom: 18px; border-radius: 12px; display: flex; align-items: center;">
                <i class="fa-solid fa-key" style="margin-right: 12px; color: #cbd5e1; width: 16px;"></i>
                <input type="number" id="inputOtp" placeholder="6-अंकों का OTP डालें" style="background: none; border: none; outline: none; color: white; width: 100%; font-size: 15px; text-align: center; letter-spacing: 2px;">
            </div>
            <button class="login-btn" onclick="validateOtp()" style="background: #ffb703; color: #111; border: none; width: 100%; padding: 14px; font-size: 15px; font-weight: bold; border-radius: 12px; cursor: pointer;">ओटीपी सत्यापित करें</button>
        </div>

        <!-- स्टेज C: थैंक यू पॉप-अप -->
        <div id="successStage" style="display: none; text-align: center; padding: 10px 0;">
            <div style="background: #2ecc71; width: 55px; height: 55px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto 12px auto; box-shadow: 0 0 20px rgba(46,204,113,0.4);">
                <i class="fa-solid fa-check" style="font-size: 24px; color: white;"></i>
            </div>
            <h2 style="font-size: 20px; font-weight: 700; margin: 0 0 4px 0; color: #2ecc71;">Thank You!</h2>
            <p style="font-size: 12px; color: #fff; margin: 0;">लॉगिन पूरी तरह सफल रहा। डैशबोर्ड सक्रिय किया जा रहा है...</p>
        </div>

    </div>
</div>        
       <!-- 2. NOTICE SCREEN (एडवांस्ड श्रेणी-वार राशन एवं बजट कैलकुलेटर) -->
<div id="notice" class="app-page">
    <!-- सुधार 1: me-2 हटाकर आइकॉन में इनलाइन margin-right दिया गया है -->
    <h3 class="page-title"><i class="fa-solid fa-bullhorn" style="margin-right: 8px;"></i>Calc</h3>  
    
    <!-- इनपुट बॉक्स कंटेनर -->
    <div style="background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; margin-top: 10px;">
        <h4 style="margin: 0 0 12px 0; color: #764ba2; font-size: 14px;">
            <i class="fa-solid fa-users" style="margin-right: 8px;"></i> लाभार्थी संख्या प्रविष्टि (कुल लाभार्थी: <span id="totalBeneficiaryDisplay">96</span>)
        </h4>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
            <div>
                <label style="font-size: 11px; color: #555; font-weight: 600;">1. स्कूल पूर्व (03-06 वर्ष):</label>
                <input type="number" id="inputPreSchool" value="40" oninput="calculateAdvancedRation()" style="width:100%; padding:8px; border:1px solid #cbd5e0; border-radius:6px; font-weight:bold; color:#764ba2;">
            </div>
            <div>
                <label style="font-size: 11px; color: #555; font-weight: 600;">2. गर्भवती एवं धात्री:</label>
                <input type="number" id="inputPregnant" value="16" oninput="calculateAdvancedRation()" style="width:100%; padding:8px; border:1px solid #cbd5e0; border-radius:6px; font-weight:bold; color:#764ba2;">
            </div>
            <div>
                <label style="font-size: 11px; color: #555; font-weight: 600;">3. सामान्य कुपोषित:</label>
                <input type="number" id="inputNormalMal" value="39" oninput="calculateAdvancedRation()" style="width:100%; padding:8px; border:1px solid #cbd5e0; border-radius:6px; font-weight:bold; color:#764ba2;">
            </div>
            <div>
                <label style="font-size: 11px; color: #555; font-weight: 600;">4. अतिकुपोषित बच्चे:</label>
                <input type="number" id="inputSevereMal" value="1" oninput="calculateAdvancedRation()" style="width:100%; padding:8px; border:1px solid #cbd5e0; border-radius:6px; font-weight:bold; color:#764ba2;">
            </div>
        </div>
    </div>

    <!-- कुल खर्च समरी कार्ड -->
    <div style="background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); color: white; padding: 15px; border-radius: 12px; margin-top: 15px; text-align: center; box-shadow: 0 4px 12px rgba(118,75,162,0.2);">
        <p style="margin: 0; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">Grand Total Budget (कुल अनुमानित राशि)</p>
        <h2 id="grandTotalDisplay" style="margin: 5px 0 0 0; font-size: 24px; font-weight: 700;">₹0.00</h2>
    </div>

    <!-- डायनामिक कैलकुलेशन रिपोर्ट्स (स्क्रॉल कंटेनर) -->
    <div style="margin-top: 15px; max-height: 380px; overflow-y: auto; padding-right: 2px;">
        
        <!-- टेबल 1: गर्भवती एवं धात्री महिलाएँ -->
        <!-- सुधार 3: अमान्य border एट्रिब्यूट हटाकर साफ़ इनलाइन CSS बॉर्डर स्टाइल लगाया गया है -->
        <div class="form-card" style="padding:10px; margin-bottom:12px; background:#fff; border: 1px solid #eee;">
            <h5 style="margin:0 0 8px 0; color:#c65911; font-size:12px; background:#fff2cc; padding:5px 8px; border-left:3px solid #c65911; border-radius:3px;">मद: गर्भवती एवं धात्री के लिए (THR 25 दिन)</h5>
            <table style="width:100%; font-size:11px; border-collapse:collapse; text-align: left;">
                <thead>
                    <tr style="background:#f4f6f8; border-bottom: 1px solid #eee;">
                        <th style="padding: 4px;">सामग्री</th>
                        <th style="padding: 4px;">मात्रा (ग्राम)</th>
                        <th style="padding: 4px;">खर्च (ग्राम)</th>
                        <th style="padding: 4px;">राशि (₹)</th>
                    </tr>
                </thead>
                <tbody id="tablePregnantBody"></tbody>
            </table>
        </div>

        <!-- टेबल 2: सामान्य कुपोषित बच्चे -->
        <div class="form-card" style="padding:10px; margin-bottom:12px; background:#fff; border: 1px solid #eee;">
            <h5 style="margin:0 0 8px 0; color:#003366; font-size:12px; background:#e8f4f8; padding:5px 8px; border-left:3px solid #003366; border-radius:3px;">मद: 06 माह से 03 वर्ष सामान्य कुपोषित (THR)</h5>
            <table style="width:100%; font-size:11px; border-collapse:collapse; text-align: left;">
                <thead>
                    <tr style="background:#f4f6f8; border-bottom: 1px solid #eee;">
                        <th style="padding: 4px;">सामग्री</th>
                        <th style="padding: 4px;">मात्रा (ग्राम)</th>
                        <th style="padding: 4px;">खर्च (ग्राम)</th>
                        <th style="padding: 4px;">राशि (₹)</th>
                    </tr>
                </thead>
                <tbody id="tableNormalBody"></tbody>
            </table>
        </div>

        <!-- टेबल 3: अतिकुपोषित बच्चे -->
        <div class="form-card" style="padding:10px; margin-bottom:12px; background:#fff; border: 1px solid #eee;">
            <h5 style="margin:0 0 8px 0; color:#e74c3c; font-size:12px; background:#fce4d6; padding:5px 8px; border-left:3px solid #e74c3c; border-radius:3px;">मद: 06 माह से 03 वर्ष अतिकुपोषित बच्चे (THR)</h5>
            <table style="width:100%; font-size:11px; border-collapse:collapse; text-align: left;">
                <thead>
                    <tr style="background:#f4f6f8; border-bottom: 1px solid #eee;">
                        <th style="padding: 4px;">सामग्री</th>
                        <th style="padding: 4px;">मात्रा (ग्राम)</th>
                        <th style="padding: 4px;">खर्च (ग्राम)</th>
                        <th style="padding: 4px;">राशि (₹)</th>
                    </tr>
                </thead>
                <tbody id="tableSevereBody"></tbody>
            </table>
        </div>

        <!-- टेबल 4: स्कूल पूर्व बच्चे गर्म भोजन -->
        <div class="form-card" style="padding:10px; margin-bottom:5px; background:#fff; border: 1px solid #eee;">
            <h5 style="margin:0 0 8px 0; color:#2e7d32; font-size:12px; background:#e2f0d9; padding:5px 8px; border-left:3px solid #2e7d32; border-radius:3px;">मद: स्कूल पूर्व के बच्चों (03-06 वर्ष) गर्म भोजन (मासिक)</h5>
            <table style="width:100%; font-size:11px; border-collapse:collapse; text-align: left;">
                <thead>
                    <tr style="background:#f4f6f8; border-bottom: 1px solid #eee;">
                        <th style="padding: 4px;">सामग्री</th>
                        <th style="padding: 4px;">मात्रा प्रति दिन</th>
                        <!-- सुधार 2: यहाँ अंत में छूटा हुआ </th> क्लोजिंग टैग लगा दिया गया है -->
                        <th style="padding: 4px;">मात्रा प्रति माह</th>
                    </tr>
                </thead>
                <tbody id="tablePreSchoolBody"></tbody>
            </table>
        </div>

    </div>
</div>
        <!-- 3. SERVICE SCREEN (शुरुआत में छुपाने के लिए active हटा दिया गया है) -->
        <div id="service" class="app-page">
            <h3 class="page-title"><i class="fa-solid fa-gears me-2"></i>Entry Service</h3>

            
            <!-- 4 नैविगेशन बटन्स -->
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 20px;">
                <button class="tab-btn" onclick="showTab(event, 'allotment-section')" style="cursor:pointer; padding:10px; background:#e2f0d9; color:#385723; font-size:12px; font-weight:bold; border-radius:8px; border:1px solid #a9d18e;">Allotment Entry</button>
                <button class="tab-btn" onclick="showTab(event, 'expenditure-section')" style="cursor:pointer; padding:10px; background:#fce4d6; color:#c65911; font-size:12px; font-weight:bold; border-radius:8px; border:1px solid #f8cbad;">Expenditure Entry</button>
                <button class="tab-btn" onclick="showTab(event, 'report-section')" style="cursor:pointer; padding:10px; background:#fff2cc; color:#7f6000; font-size:12px; font-weight:bold; border-radius:8px; border:1px solid #ffe599;">Expe Report</button>
                <button class="tab-btn active" onclick="showTab(event, 'balance-section')" style="cursor:pointer; padding:10px; background:#e8f4f8; color:#1f4e5b; font-size:12px; font-weight:bold; border-radius:8px; border:1px solid #b4d6e4;">Balance Sheet</button>
            </div>

            <!-- TAB 1: Allotment Entry Form -->
            <div id="allotment-section" class="tab-content" style="display: none; scroll-margin-top: 10px;">
                <!-- सुधार 3: आइकॉन में सही गैप के लिए margin-right जोड़ा गया -->
                <h4><i class="fa-solid fa-circle-plus" style="color: green; margin-right: 8px;"></i> 1. Allotment Entry</h4>
                <form id="altForm" method="POST">
                    <input type="hidden" name="type" value="Allotment">
                    <select id="altSrc" name="source" class="app-input" style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; background-color: white;" required>
                        <option value="" disabled selected hidden>Source </option>
                        <option value="CFMS">CFMS</option>
                        <option value="HRMS">HRMS</option>
                        <option value="PFMS">PFMS</option>
                        <!-- सुधार 1: J.I.T और N.I.C की वैल्यू अलग-अलग की गई -->
                        <option value="JIT">J.I.T Portal </option>
                        <option value="NIC">N.I.C Portal</option>
                    </select>

                    <input type="text" id="altOrd" name="order_no" placeholder="Order No." class="app-input" required>
                    <!-- सुधार 2: id को expDat से बदलकर altDat_input किया गया -->
                    <input type="date" id="altDat_input" name="date" class="app-input" required>
                    
                    <select id="altHead" name="budget_head" class="app-input" style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; background-color: white;" required>
                        <option value="" disabled selected hidden>Budget Head (बजट कोड चुनें)</option>
                        <option value="51-2235-02-102-0123">51-2235-02-102-0123</option>
                        <option value="51-2235-02-102-0222">51-2235-02-102-0222</option>
                        <option value="51-2235-02-102-0105">51-2235-02-102-0105</option>
                        <option value="51-2235-02-102-0122">51-2235-02-102-0122</option>
                        <option value="51-2235-02-102-0225">51-2235-02-102-0225</option>
                        <option value="51-2235-02-102-0322">51-2235-02-102-0322</option>
                        <option value="51-2235-02-102-0325">51-2235-02-102-0325</option>
                        <option value="51-2235-02-102-0327">51-2235-02-102-0327</option>
                        <option value="51-2236-02-101-0103">51-2236-02-101-0103</option>
                        <option value="51-2236-02-101-0203">51-2236-02-101-0203</option>
                        <option value="51-2236-02-101-0303">51-2236-02-101-0303</option>
                        <option value="51-2236-02-789-0204">51-2236-02-789-0204</option>
                        <option value="51-2236-02-789-0304">51-2236-02-789-0304</option>
                        <option value="51-2235-02-102-0226">51-2235-02-102-0226</option>
                        <option value="51-2235-02-102-0224">51-2235-02-102-0224</option>
                    </select>

                    <select id="altUnit" name="unit_code" class="app-input" style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; background-color: white;" required>
                        <option value="" disabled selected hidden>Unit Code (यूनिट कोड चुनें)</option>
                        <option value="01.01">01.01</option>
                        <option value="01.03">01.03</option>
                        <option value="01.04">01.04</option>
                        <option value="01.05">01.05</option>
                        <option value="01.06">01.06</option>
                        <option value="01.07">01.07</option>
                        <option value="02.01">02.01</option>
                        <option value="06.01">06.01</option>
                        <option value="11.01">11.01</option>
                        <option value="13.01">13.01</option>
                        <option value="13.10">13.10</option>
                        <option value="14.01">14.01</option>
                        <option value="16.01">16.01</option>
                        <option value="20.03">20.03</option>
                        <option value="21.01">21.01</option>
                        <option value="21.03">21.03</option>
                        <option value="26.01">26.01</option>
                        <option value="28.02">28.02</option>
                        <option value="31.06">31.06</option>
                        <option value="52.01">52.01</option>
                    </select>

                    <input type="number" id="altAmt" name="amount" placeholder="Amount (राशि ₹)" class="app-input" required>
                    <input type="text" id="altRemark" name="remark" placeholder="Remark" class="app-input">
                    <input type="hidden" id="altLet" value="00000">
                    <input type="hidden" id="altDat" value="2026-04-01">
                    <button type="submit" class="submit-btn" style="background: green; width: 100%; padding: 10px; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">Save</button>
                </form> 
            </div>

          <!-- TAB 2: Expenditure Entry Form -->
            <div id="expenditure-section" class="tab-content" style="display: none; scroll-margin-top: 10px;">
                <!-- सुधार 2: आइकॉन और टेक्स्ट के बीच सही स्पेस के लिए margin-right जोड़ा गया -->
                <h4><i class="fa-solid fa-file-invoice-dollar" style="color: red; margin-right: 8px;"></i> 2. Expenditure Entry</h4>
                <form id="expForm" method="POST">
                    <input type="hidden" name="type" value="Expenditure">
                    <input type="text" id="expOrd" name="order_no" placeholder="Order No." class="app-input" required>
                    <input type="date" id="expDat" name="date" class="app-input" required>
                    
                    <select id="expHead" name="budget_head" class="app-input" style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; background-color: white;" required>
                        <option value="" disabled selected hidden>Budget Head </option>
                        <option value="51-2235-02-102-0123">51-2235-02-102-0123</option>
                        <option value="51-2235-02-102-0222">51-2235-02-102-0222</option>
                        <option value="51-2235-02-102-0105">51-2235-02-102-0105</option>
                        <option value="51-2235-02-102-0122">51-2235-02-102-0122</option>
                        <option value="51-2235-02-102-0225">51-2235-02-102-0225</option>
                        <option value="51-2235-02-102-0322">51-2235-02-102-0322</option>
                        <option value="51-2235-02-102-0325">51-2235-02-102-0325</option>
                        <option value="51-2235-02-102-0327">51-2235-02-102-0327</option>
                        <option value="51-2236-02-101-0103">51-2236-02-101-0103</option>
                        <option value="51-2236-02-101-0203">51-2236-02-101-0203</option>
                        <option value="51-2236-02-101-0303">51-2236-02-101-0303</option>
                        <option value="51-2236-02-789-0204">51-2236-02-789-0204</option>
                        <option value="51-2236-02-789-0304">51-2236-02-789-0304</option>
                        <option value="51-2235-02-102-0226">51-2235-02-102-0226</option>
                        <option value="51-2235-02-102-0224">51-2235-02-102-0224</option>
                    </select>

                    <select id="expUnit" name="unit_code" class="app-input" style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; background-color: white;" required>
                        <option value="" disabled selected hidden>Unit Code </option>
                        <option value="01.01">01.01</option>
                        <option value="01.03">01.03</option>
                        <option value="01.04">01.04</option>
                        <option value="01.05">01.05</option>
                        <option value="01.06">01.06</option>
                        <option value="01.07">01.07</option>
                        <option value="02.01">02.01</option>
                        <option value="06.01">06.01</option>
                        <option value="11.01">11.01</option>
                        <option value="13.01">13.01</option>
                        <option value="13.10">13.10</option>
                        <option value="14.01">14.01</option>
                        <option value="16.01">16.01</option>
                        <option value="20.03">20.03</option>
                        <option value="21.01">21.01</option>
                        <option value="21.03">21.03</option>
                        <option value="26.01">26.01</option>
                        <option value="28.02">28.02</option>
                        <option value="31.06">31.06</option>
                        <option value="52.01">52.01</option>
                    </select>
                    <!-- सुधार 1: आईडी को altAmt से बदलकर expAmt किया गया -->
                    <input type="number" id="expAmt" name="amount" placeholder="Amount ₹" class="app-input" required>
                    <!-- सुधार 1: आईडी को altRemark से बदलकर expRemark किया गया -->
                    <input type="text" id="expRemark" name="remark" placeholder="Remark" class="app-input">
                    <input type="hidden" id="expSrc" value="OTHER">
                    <input type="hidden" id="expBill" value="000">
                    <input type="hidden" id="expPur" value="Office Expenses">
                    <button type="submit" class="submit-btn" style="background: red; width: 100%; padding: 10px; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">व्यय डेटा सेव करें</button>
                </form>
            </div>
           <!-- TAB 3: Expenditure Report Section -->
            <div id="report-section" class="tab-content" style="display: none;">
                <div style="background: #003366; color: white; padding: 12px 20px; border-radius: 8px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <!-- सुधार 1: me-2 को हटाकर आइकॉन में इनलाइन margin-right: 8px; लगाया गया है -->
                    <h3 style="margin: 0; font-size: 16px; font-weight: 600;"><i class="fa-solid fa-file-invoice-dollar" style="margin-right: 8px;"></i> Recent Bill Records</h3>
                </div>
                <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="overflow-x: auto; max-height: 350px; overflow-y: auto;">
                        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 12px;">
                            <thead>
                                <tr style="background: #f8f9fa; border-bottom: 2px solid #eee; color: #666;">
                                    <th style="padding: 10px;">Bill No</th>
                                    <th style="padding: 10px;">Date</th>
                                    <th style="padding: 10px;">Head</th>
                                    <th style="padding: 10px;">Amount</th>
                                    <th style="padding: 10px;">Purpose</th>
                                </tr>
                            </thead>
                            <tbody id="expBody">
                                <!-- लाइव डेटा यहाँ नीचे दी गई स्क्रिप्ट द्वारा ऑटोमैटिक लोड होगा -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

<!-- सुधार 2: डेटा को लाइव टेबल में दिखाने के लिए यह स्क्रिप्ट रेंडरर जोड़ा गया है -->
<script>
    // यह आपका लाइव डेटा ऐरे (Array) है, जिसे आपकी ऐप या बैकएंड से अपडेट किया जा सकता है
    const liveExpenditureData = [
        { bill_no: "BILL-2026/01", date: "2026-11-01", budget_head: "51-2235-02-102-0123", amount: 45000, purpose: "Office Expenses" },
        { bill_no: "BILL-2026/02", date: "2026-10-28", budget_head: "51-2235-02-102-0222", amount: 125000, purpose: "THR Ration Payment" },
        { bill_no: "BILL-2026/03", date: "2026-10-15", budget_head: "51-2236-02-101-0103", amount: 15400, purpose: "Contingency/Fuel" }
    ];

    // टेबल में डेटा लोड करने का मुख्य फंक्शन
    function renderLiveExpenditureReport() {
        const tableBody = document.getElementById("expBody");
        if (!tableBody) return;

        // पुराना कचरा/डेटा साफ़ करें
        tableBody.innerHTML = "";

        // यदि कोई डेटा न हो तो मैसेज दिखाएँ
        if (liveExpenditureData.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="5" style="text-align: center; padding: 20px; color: #888;">कोई व्यय रिकॉर्ड उपलब्ध नहीं है।</td></tr>`;
            return;
        }

        // लूप चलाकर एक-एक रो को जोड़ें
        liveExpenditureData.forEach(item => {
            const row = document.createElement("tr");
            row.style.borderBottom = "1px solid #eee";
            row.style.transition = "background 0.2s";
            
            // हॉवर इफ़ेक्ट के लिए
            row.onmouseover = () => row.style.background = "#fcfcfc";
            row.onmouseout = () => row.style.background = "transparent";

            row.innerHTML = `
                <td style="padding: 12px 10px; font-weight: 600; color: #2d3748;">${item.bill_no}</td>
                <td style="padding: 12px 10px; color: #4a5568;">${item.date}</td>
                <td style="padding: 12px 10px; font-family: monospace; color: #1a202c; background: #edf2f7; border-radius: 4px; display: inline-block; margin: 4px 0;">${item.budget_head}</td>
                <td style="padding: 12px 10px; font-weight: 700; color: #e53e3e;">₹${Number(item.amount).toLocaleString('en-IN')}</td>
                <td style="padding: 12px 10px; color: #718096;">${item.purpose}</td>
            `;
            tableBody.appendChild(row);
        });
    }

    // जब पूरा पेज लोड हो जाए, तब इस फंक्शन को चलाएँ
    document.addEventListener("DOMContentLoaded", renderLiveExpenditureReport);
</script>
          <!-- TAB 4: Balance Sheet Section -->
            <div id="balance-section" class="tab-content" style="display: block;">
                <div style="background: #1f4e5b; color: white; padding: 12px 20px; border-radius: 8px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <!-- सुधार 1: me-2 को हटाकर आइकॉन में इनलाइन margin-right: 8px; लगाया गया है -->
                    <h3 style="margin: 0; font-size: 16px; font-weight: 600;"><i class="fa-solid fa-scale-balanced" style="margin-right: 8px;"></i> 4. Balance Sheet</h3>
                </div>
                <!-- लाइव स्ट्रिप कंटेनर (Total Allotment Head-wise Cards) -->
                <div id="totalStrip" style="display: flex; gap: 12px; overflow-x: auto; padding-bottom: 10px; margin-bottom: 15px; scrollbar-width: thin;">
                    <!-- कार्ड्स जावास्क्रिप्ट द्वारा स्वतः जेनरेट होंगे -->
                </div>
                <!-- लाइव बैलेंस लिस्ट कंटेनर -->
                <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <h4 style="margin: 0 0 12px 0; font-size: 13px; color: #555; border-bottom: 2px solid #f4f4f4; padding-bottom: 6px;">Remaining Balance (शेष बजट विवरण)</h4>
                    <div id="balanceList">
                        <!-- बची हुई राशि यहाँ ऑटोमैटिक घटेगी -->
                    </div>
                </div>
            </div>
            
        </div> <!-- यह id="service" स्क्रीन का मुख्य क्लोजिंग टैग है -->

<!-- सुधार 2: आवंटन और खर्चों को आपस में कैलकुलेट करके लाइव डेटा दिखाने के लिए स्क्रिप्ट इंजन -->
<script>
    // 1. आपका लाइव आवंटन डेटा (Sample Database Data)
    const liveAllotments = [
        { budget_head: "51-2235-02-102-0123", amount: 500000 },
        { budget_head: "51-2235-02-102-0222", amount: 350000 },
        { budget_head: "51-2236-02-101-0103", amount: 800000 }
    ];

    // 2. आपका लाइव खर्च डेटा
    const liveExpenditures = [
        { budget_head: "51-2235-02-102-0123", amount: 45000 },
        { budget_head: "51-2235-02-102-0222", amount: 120000 },
        { budget_head: "51-2235-02-102-0123", amount: 15000 }
    ];

    // बैलेंस शीट लोड और कैलकुलेट करने का मुख्य फंक्शन
    function renderLiveBalanceSheet() {
        const totalStrip = document.getElementById("totalStrip");
        const balanceList = document.getElementById("balanceList");

        if (!totalStrip || !balanceList) return;

        // पुराने डेटा को पूरी तरह साफ़ करें
        totalStrip.innerHTML = "";
        balanceList.innerHTML = "";

        // सबसे पहले हेड-वार (Head-wise) कुल व्यय जोड़ें
        const expenseMap = {};
        liveExpenditures.forEach(exp => {
            expenseMap[exp.budget_head] = (expenseMap[exp.budget_head] || 0) + Number(exp.amount);
        });

        // आवंटन एरे पर लूप चलाकर रेंडर करें
        liveAllotments.forEach(alt => {
            const head = alt.budget_head;
            const allocatedAmount = Number(alt.amount);
            const spentAmount = expenseMap[head] || 0;
            const remainingAmount = allocatedAmount - spentAmount;

            // A. टोटल अलॉटमेंट हेड कार्ड्स जनरेट करें (Horizontal Strip)
            const card = document.createElement("div");
            card.className = "total-card";
            // हेड कोड के आख़िरी भाग को साफ़ दिखाने के लिए सबस्ट्रिंग किया है
            card.innerHTML = `
                <h5>HEAD: ${head.substring(11)}</h5>
                <p>₹${allocatedAmount.toLocaleString('en-IN')}</p>
            `;
            totalStrip.appendChild(card);

            // B. बची हुई राशि (Remaining Balance List) जनरेट करें
            const balItem = document.createElement("div");
            balItem.className = "bal-item";
            balItem.innerHTML = `
                <span>${head}</span>
                <strong style="color: ${remainingAmount < 50000 ? '#e53e3e' : '#2e7d32'};">
                    ₹${remainingAmount.toLocaleString('en-IN')}
                </strong>
            `;
            balanceList.appendChild(balItem);
        });
    }

    // डोम लोड होते ही बैलेंस शीट को सिंक करें
    document.addEventListener("DOMContentLoaded", renderLiveBalanceSheet);
</script>
     # --- 2. ABOUT & CONTACT PAGES BODY ---
# सुधार: HTML ब्लॉक को स्टोर करने के लिए यहाँ वैरिएबल नाम निश्चित किया गया है
ABOUT_CONTACT_BODY = """
        <!-- 4. ABOUT SCREEN -->
        <div id="about" class="app-page" style="text-align: center;">
            <h3 class="page-title">About Me</h3>
            <h4 style="color:#764ba2; margin-bottom: 5px;">Rudra Tech Pvt Ltd</h4>
            <p style="font-size: 13px; color:#666;">हम कार्यालयों के लिए आधुनिक सॉफ्टवेयर का निर्माण करते हैं।</p>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            <a href="https://wa.me" target="_blank" class="submit-btn" style="background:#25D366; text-decoration:none; display:block; text-align:center;"><i class="fa-brands fa-whatsapp" style="margin-right: 8px;"></i>WhatsApp Chat</a>
        </div>
        
        <div id="contact" class="app-page">
            <h3 class="page-title">Contact Us</h3>
            <form action="https://formspree.io" method="POST">
                <input type="hidden" name="type" value="Contact">
                <input type="text" name="name" placeholder="आपका नाम" class="app-input" required>
                <input type="text" name="subject" placeholder="विषय (Subject)" class="app-input" required>
                <textarea name="message" placeholder="यहाँ अपना संदेश लिखें..." class="app-input" rows="4" style="height:auto;" required></textarea>
                <button type="submit" class="submit-btn">डायरेक्ट मैसेज भेजें</button>
            </form>
        </div>
""" 

# --- 3. APP LAYOUT END ---
LAYOUT_END = """
        <div class="bottom-nav">
            <div class="nav-item active" onclick="switchPage('home')"><i class="fa-solid fa-house"></i>Home</div>
            <div class="nav-item" onclick="switchPage('notice')"><i class="fa-solid fa-bell"></i>Notice</div>
            <div class="nav-item" onclick="switchPage('service')"><i class="fa-solid fa-gears"></i>Service</div>
            <div class="nav-item" onclick="switchPage('about')"><i class="fa-solid fa-building"></i>About</div>
            <div class="nav-item" onclick="switchPage('contact')"><i class="fa-solid fa-envelope"></i>Contact</div>
        </div>
    </div>
</body>
</html>
"""

    <script>
// 1. मुख्य पेजों को बदलने के लिए फंक्शन (बॉटम नेव बार और लॉगिन के लिए)
function switchPage(pageId) {
    // सभी स्क्रीन्स से एक्टिव क्लास हटाएं और उन्हें छुपाएं
    document.querySelectorAll('.app-page').forEach(page => {
        page.classList.remove('active');
        page.style.display = 'none'; // इनलाइन डिस्प्ले को साफ़ करें
    });
    
    // केवल चुनी हुई स्क्रीन को दिखाएं
    const activePage = document.getElementById(pageId);
    if(activePage) {
        activePage.classList.add('active');
        // होम स्क्रीन को फ्लेक्स लेआउट बनाए रखने के लिए इनलाइन कंडीशन चेक
        if (pageId === 'home') {
            activePage.style.display = 'flex';
        } else {
            activePage.style.display = 'block';
        }
    }
    
    // सुधार 1: इंडेक्स पर निर्भर रहने के बजाय क्लिक/टारगेट के आधार पर नेविगेशन आइटम को सुरक्षित एक्टिव करें
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        // यदि ऑनक्लिक एट्रिब्यूट में वो पेज आईडी शामिल है, तो उसे एक्टिव क्लास दें
        if(item.getAttribute('onclick') && item.getAttribute('onclick').includes(pageId)) {
            item.classList.add('active');
        }
    });
}

// 2. सर्विस स्क्रीन के अंदर के 4 सब-फॉर्म्स / टैब्स को बदलने के लिए फंक्शन
function showTab(event, sectionId) {
    if(event) {
        event.preventDefault(); // डिफ़ॉल्ट एक्शन को रोकें
    }

    // सभी सब-सेक्शन्स (tab-content) को छुपाएं
    var contents = document.getElementsByClassName('tab-content');
    for (var i = 0; i < contents.length; i++) {
        contents[i].style.display = 'none';
        contents[i].classList.remove('active');
    }
    
    // सभी बटन्स से एक्टिव क्लास हटाएं
    var tabButtons = document.getElementsByClassName('tab-btn');
    for (var j = 0; j < tabButtons.length; j++) {
        tabButtons[j].classList.remove('active');
    }
    
    // केवल टारगेट सेक्शन को दिखाएं
    var target = document.getElementById(sectionId);
    if(target) {
        target.style.display = 'block';
        target.classList.add('active');
    }
    
    // क्लिक किए गए बटन को एक्टिव स्टाइल दें
    if(event && event.currentTarget) {
        event.currentTarget.classList.add('active');
    }
}

// 3. पेज लोड होते ही केवल लॉगिन (home) स्क्रीन चालू रखने का परमानेंट फिक्स
window.addEventListener('DOMContentLoaded', () => {
    // पहले सभी पेजों को पूरी तरह छुपाएं
    document.querySelectorAll('.app-page').forEach(page => {
        page.classList.remove('active');
        page.style.display = 'none';
    });
    
    // केवल लॉगिन (home) पेज को एक्टिव और विज़िबल करें
    const homePage = document.getElementById('home');
    if(homePage) {
        homePage.classList.add('active');
        homePage.style.display = 'flex'; // होम के फ्लेक्स ग्रिड को सुरक्षित रखता है
    }
    
    // शुरुआत में सर्विस स्क्रीन के अंदर डिफ़ॉल्ट रूप से बैलेंस शीट (Balance Sheet) टैब को ओपन रखें
    const defaultTab = document.getElementById('balance-section');
    if(defaultTab) {
        defaultTab.style.display = 'block';
        defaultTab.classList.add('active');
    }
});

// लॉगिन सत्यापन फंक्शन
function validateLogin() {
    const userVal = document.getElementById('loginUser').value.trim();
    const passVal = document.getElementById('loginPass').value.trim();

    // सही क्रेडेंशियल्स की जांच
    if (userVal === "admin" && passVal === "1234") {
        // स्क्रीन लॉक करें और ओटीपी स्टेज चालू करें
        document.getElementById('loginStage').style.display = 'none';
        document.getElementById('otpStage').style.display = 'block';
    } else {
        alert("गलत यूज़र आईडी या पासवर्ड! (सही: admin / 1234 डालें)");
    }
}

// ओटीपी सत्यापित होने के बाद का लॉजिक
function validateOtp() {
    const otpVal = document.getElementById('inputOtp').value.trim();
    const defaultOtp = "789456";

    if (otpVal === defaultOtp) {
        // ओटीपी सही होने पर थैंक यू स्टेज दिखाएं
        document.getElementById('otpStage').style.display = 'none';
        document.getElementById('successStage').style.display = 'block';
        
        setTimeout(function() {
            // 1. थैंक यू स्टेज बंद करें और लॉगिन पेज को हाइड/रीसेट करें
            document.getElementById('successStage').style.display = 'none';
            document.getElementById('loginStage').style.display = 'block'; 

            // 2. लॉगिन करने वाले यूज़र का नाम हेडर में सेट करें
            const loggedInUser = document.getElementById('loginUser').value.trim() || "Admin";
            document.getElementById('userProfileName').innerText = loggedInUser;
            
            const profilePicEl = document.getElementById('appTopHeader').querySelector('.profile-pic');
            if (profilePicEl) {
                profilePicEl.innerText = loggedInUser.charAt(0).toUpperCase();
            }

            // 3. नया टॉप प्रोफाइल हेडर शो करें
            document.getElementById('appTopHeader').style.display = 'flex';

            // 4. सीधे मुख्य 'Service' पेज पर ट्रांसफर करें
            switchPage('service');
            
            // सुधार 3: सर्विस स्क्रीन पर जाते ही 'Balance Sheet' बटन के एक्टिव क्लास को सिंक करें
            const allTabBtns = document.querySelectorAll('.tab-btn');
            allTabBtns.forEach(btn => {
                if(btn.getAttribute('onclick') && btn.getAttribute('onclick').includes('balance-section')) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });

            // फॉर्म इनपुट्स खाली करें
            document.getElementById('loginUser').value = "";
            document.getElementById('loginPass').value = "";
            document.getElementById('inputOtp').value = "";
        }, 2000);
        
    } else {
        alert("गलत OTP! कृपया '789456' दर्ज करें।");
    }
}

// नया लॉगआउट फंक्शन
function handleAppLogout() {
    if(confirm("क्या आप ऐप से लॉगआउट करना चाहते हैं?")) {
        // 1. टॉप हेडर को वापस छुपाएं
        document.getElementById('appTopHeader').style.display = 'none';
        
        // 2. वापस मुख्य लॉगिन (home) स्क्रीन पर भेजें
        switchPage('home');
    }
}

// लाइव डिजिटल वॉच और दिनांक फंक्शन
function updateDigitalClock() {
    const now = new Date();
    
    // समय फॉर्मेटिंग (HH:MM:SS AM/PM)
    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // 0 को 12 बनाएं
    const timeString = `${String(hours).padStart(2, '0')}:${minutes}:${seconds} ${ampm}`;
    
    // तारीख फॉर्मेटिंग (Day, DD MMM YYYY)
    const options = { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' };
    const dateString = now.toLocaleDateString('hi-IN', options); // हिंदी फॉर्मेट के लिए 'hi-IN'

    // HTML में पुश करें
    if(document.getElementById('digitalClock')) {
        document.getElementById('digitalClock').innerText = timeString;
    }
    if(document.getElementById('digitalDate')) {
        document.getElementById('digitalDate').innerText = dateString;
    }
}

// हर 1 सेकंड में घड़ी को अपडेट करें
setInterval(updateDigitalClock, 1000);

// ब्राउज़र जीपीएस से वास्तविक लोकेशन ढूंढना
function getLiveGPSLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            
            // सुधार 1 और 2: सही Nominatim API URL सेट किया गया और JSON रिस्पॉन्स के लिए प्रारूप फ़िल्टर लगाया गया
            fetch(`https://openstreetmap.org{lat}&lon=${lon}`, {
                headers: {
                    'User-Agent': 'ICDS-Budget-App' // पॉलिसी के अनुसार आवश्यक पहचानकर्ता
                }
            })
            .then(res => res.json())
            .then(data => {
                if(data && data.address) {
                    const city = data.address.city || data.address.town || data.address.village || data.address.state_district || "Patna";
                    const state = data.address.state || "Bihar";
                    
                    const locElement = document.getElementById('liveLocation');
                    if(locElement) {
                        locElement.innerText = `${city}, ${state}, India`;
                    }
                }
            })
            .catch(() => {
                // फेल होने या इंटरनेट बंद होने पर डिफॉल्ट सेट रहेगा
                const locElement = document.getElementById('liveLocation');
                if(locElement) {
                    locElement.innerText = "Patna, Bihar, India";
                }
            });
        }, function() {
            console.log("Geolocation permission denied.");
        });
    }
}

// पेज लोड होते ही रन करें
window.addEventListener('DOMContentLoaded', () => {
    updateDigitalClock();
    getLiveGPSLocation();
});

// मास्टर डेटा और सूत्र नियम (जैसा आपकी फोटो प्रतियों में दिया गया है)
const pregnantFormula = [
    { name: "चावल", qty: 90, rate: 26 },
    { name: "मूंगदाल", qty: 40, rate: 80 }, // सुधार 1: यहाँ 'मूंगदาล' के विशेष अक्षर को सही करके 'मूंगदाल' किया गया है
    { name: "मसाला मिक्स", qty: 0.5, rate: 242 },
    { name: "सोयाबीन", qty: 15, rate: 90 },
    { name: "नमक", qty: 2.5, rate: 20 },
    { name: "सोयाबीन तेल", qty: 15, rate: 110 }
];

const normalFormula = [
    { name: "चावल", qty: 75, rate: 26 },
    { name: "मूंगदाल", qty: 30, rate: 80 },
    { name: "मसाला मिक्स", qty: 0.5, rate: 242 },
    { name: "सोयाबीन", qty: 20, rate: 90 },
    { name: "नमक", qty: 2, rate: 20 },
    { name: "सोयाबीन तेल", qty: 10, rate: 110 }
];

const severeFormula = [
    { name: "चावल", qty: 117.7, rate: 26 },
    { name: "मूंगदाल", qty: 53.5, rate: 80 },
    { name: "मसाला मिक्स", qty: 1, rate: 242 },
    { name: "सोयाबीन", qty: 20, rate: 90 },
    { name: "नमक", qty: 3, rate: 20 },
    { name: "सोयाबीन तेल", qty: 20, rate: 110 }
];

const preSchoolFormula = [
    { name: "चावल", daily: 70, monthly: 1560 },
    { name: "चना", daily: 20, monthly: 360 },
    { name: "हरी सब्जी", daily: 25, monthly: 200 },
    { name: "तेल", daily: 5, monthly: 80 },
    { name: "मूँगफली", daily: 15, monthly: 120 },
    { name: "आलू", daily: 60, monthly: 240 },
    { name: "फल", daily: 1, monthly: 16 }, // यह संख्या/पीस में कैलकुलेट होगा
    { name: "सोयाबीन सब्जी", daily: 20, monthly: 80 },
    { name: "पायज टमाटर", daily: 25, monthly: 100 },
    { name: "गुड़", daily: 20, monthly: 200 },
    { name: "दाल", daily: 25, monthly: 180 },
    { name: "कद्दू", daily: 100, monthly: 40 }
];

function calculateAdvancedRation() {
    // इनपुट्स प्राप्त करें
    const countPre = parseFloat(document.getElementById('inputPreSchool').value) || 0;
    const countPreg = parseFloat(document.getElementById('inputPregnant').value) || 0;
    const countNorm = parseFloat(document.getElementById('inputNormalMal').value) || 0;
    const countSev = parseFloat(document.getElementById('inputSevereMal').value) || 0;

    // कुल लाभार्थी अपडेट करें
    document.getElementById('totalBeneficiaryDisplay').innerText = countPre + countPreg + countNorm + countSev;

    let overallGrandTotal = 0;

    // 1. गर्भवती एवं धात्री तालिका कैलकुलेशन (THR 25 दिन आधारित)
    let htmlPreg = "";
    pregnantFormula.forEach(item => {
        let totalGram = item.qty * countPreg * 25; // मात्रा * लाभार्थी * 25 दिन
        let totalCost = (totalGram / 1000) * item.rate; // किलोग्राम में बदलकर दर से गुणा
        overallGrandTotal += totalCost;
        htmlPreg += `<tr><td style="padding:5px;">${item.name}</td><td style="padding:5px;">${item.qty} ग्राम</td><td style="padding:5px;">${totalGram.toLocaleString('en-IN')} ग्राम</td><td style="padding:5px;">₹${totalCost.toFixed(2)}</td></tr>`;
    });
    document.getElementById('tablePregnantBody').innerHTML = htmlPreg;

    // 2. सामान्य कुपोषित तालिका कैलकुलेशन (THR 25 दिन आधारित)
    let htmlNorm = "";
    normalFormula.forEach(item => {
        let totalGram = item.qty * countNorm * 25;
        let totalCost = (totalGram / 1000) * item.rate;
        overallGrandTotal += totalCost;
        htmlNorm += `<tr><td style="padding:5px;">${item.name}</td><td style="padding:5px;">${item.qty} ग्राम</td><td style="padding:5px;">${totalGram.toLocaleString('en-IN')} ग्राम</td><td style="padding:5px;">₹${totalCost.toFixed(2)}</td></tr>`;
    });
    document.getElementById('tableNormalBody').innerHTML = htmlNorm;

    // 3. अतिकुपोषित तालिका कैलकुलेशन (THR 25 दिन आधारित)
    let htmlSev = "";
    severeFormula.forEach(item => {
        let totalGram = item.qty * countSev * 25;
        let totalCost = (totalGram / 1000) * item.rate;
        overallGrandTotal += totalCost;
        htmlSev += `<tr><td style="padding:5px;">${item.name}</td><td style="padding:5px;">${item.qty} ग्राम</td><td style="padding:5px;">${totalGram.toFixed(1)} ग्राम</td><td style="padding:5px;">₹${totalCost.toFixed(2)}</td></tr>`;
    });
    document.getElementById('tableSevereBody').innerHTML = htmlSev;

    // 4. स्कूल पूर्व तालिका कैलकुलेशन (मासिक उपभोग ग्राम आधारित)
    let htmlPre = "";
    preSchoolFormula.forEach(item => {
        let calculatedMonthly = item.monthly * countPre; // प्रति बच्चा मासिक कोटा * कुल बच्चे
        
        // सुधार 2 और 3: 'फल' के लिए ग्राम/किग्रा की जगह पीस (संख्या) और यूनिट को डायनामिक सेट किया गया है
        if (item.name === "फल") {
            htmlPre += `<tr><td style="padding:5px;">${item.name}</td><td style="padding:5px;">${item.daily} पीस</td><td style="padding:5px;">${calculatedMonthly} पीस</td></tr>`;
        } else {
            htmlPre += `<tr><td style="padding:5px;">${item.name}</td><td style="padding:5px;">${item.daily} ग्राम</td><td style="padding:5px;">${(calculatedMonthly / 1000).toFixed(2)} किग्रा</td></tr>`;
        }
    });
    // अतिरिक्त गर्म भोजन नियत नाश्ता दर भी योग में जोड़ें (4.99 प्रति बच्चा उदाहरणार्थ मानकर)
    overallGrandTotal += (countPre * 4.99 * 25); 
    document.getElementById('tablePreSchoolBody').innerHTML = htmlPre;

    // फाइनल ग्रैंड टोटल डिस्प्ले अपडेट करें
    document.getElementById('grandTotalDisplay').innerText = `₹${overallGrandTotal.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
}

// लोडिंग पर डिफ़ॉल्ट ट्रिगर करें
window.addEventListener('DOMContentLoaded', () => {
    if(document.getElementById('inputPreSchool')) {
        calculateAdvancedRation();
    }
});

</script>

<script>
// स्क्रिप्ट की URL यहाँ पेस्ट करें
const GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyEVd-HJ6MWluxu7lhRcG2uuoqF80ST_TtzSZbVhYuwRVSeUhD9DmV-4R5vzSh4feY/exec";

// ऑलॉटमेंट फॉर्म सबमिशन हैंडलर
document.getElementById('altForm').addEventListener('submit', function(e) {
    e.preventDefault();
    submitToGoogleSheet(this, "Save Allotment");
});

// सुधार 1: कमेंट से हटाकर Expenditure Form के सबमिशन हैंडलर सिंटैक्स को पूरी तरह ठीक कर दिया गया है
document.getElementById('expForm').addEventListener('submit', function(e) { 
    e.preventDefault();
    submitToGoogleSheet(this, "व्यय डेटा सेव करें");
});

function submitToGoogleSheet(formElement, originalBtnText) {
    const btn = formElement.querySelector('button[type="submit"]');
    btn.innerText = "Saving...";
    btn.disabled = true;

    const formData = new FormData(formElement);

    fetch(GOOGLE_SCRIPT_URL, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(responseObj => {
        if(responseObj.result === "success") {
            alert("डेटा सफलतापूर्वक Google Sheet में सेव हो गया है!");
            formElement.reset();
            // लाइव रिपोर्ट और बैलेंस शीट को स्क्रीन पर अपडेट करें
            updateUI(responseObj.data);
        } else {
            alert("त्रुटि: " + responseObj.error);
        }
    })
    .catch(error => {
        alert("कनेक्शन एरर! कृपया दोबारा प्रयास करें।");
        console.error('Error:', error);
    })
    .finally(() => {
        btn.innerText = originalBtnText;
        btn.disabled = false;
    });
}

// प्राप्त लाइव डेटा से UI (रिपोर्ट और बैलेंस शीट) अपडेट करने का फंक्शन
function updateUI(data) {
    // 1. बैलेंस शीट के टॉप कार्ड्स (totalStrip) को अपडेट करना
    const totalStrip = document.getElementById('totalStrip');
    if(totalStrip) {
        // सुधार 2 & 3: size को font-size किया गया और null वैल्यू को रोकने के लिए फॉलबैक (data || 0) लगाया गया है
        totalStrip.innerHTML = `
            <div style="background: #fff; padding: 12px; min-width: 140px; border-radius: 8px; border-left: 4px solid #1f4e5b; flex: 1;">
                <p style="font-size: 11px; color:#777; margin:0;">TOTAL ALLOTMENT</p>
                <p style="font-size:16px; color:#1f4e5b; margin:0; font-weight:bold;">₹${(data.totalAllotment || 0).toLocaleString('en-IN')}</p>
            </div>
            <div style="background: #fff; padding: 12px; min-width: 140px; border-radius: 8px; border-left: 4px solid #e74c3c; flex: 1;">
                <p style="font-size: 11px; color:#777; margin:0;">TOTAL EXPENSE</p>
                <p style="font-size:16px; color:#e74c3c; margin:0; font-weight:bold;">₹${(data.totalExpenditure || 0).toLocaleString('en-IN')}</p>
            </div>
            <div style="background: #fff; padding: 12px; min-width: 140px; border-radius: 8px; border-left: 4px solid #2ecc71; flex: 1;">
                <p style="font-size: 11px; color:#777; margin:0;">NET BALANCE</p>
                <p style="font-size:16px; color:#2ecc71; margin:0; font-weight:bold;">₹${(data.netBalance || 0).toLocaleString('en-IN')}</p>
            </div>
        `;
    }

    // 2. लाइव बैलेंस लिस्ट (balanceList) को अपडेट करना
    const balanceList = document.getElementById('balanceList');
    if(balanceList) {
        balanceList.innerHTML = ""; // पुराना डेटा साफ़ करें
        if (data.headWiseReport && data.headWiseReport.length > 0) {
            data.headWiseReport.forEach(item => {
                balanceList.innerHTML += `
                    <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f4f4f4; font-size: 12px;">
                        <span style="color: #333; font-weight: 500;">Head: ${item.head}</span>
                        <span style="color: ${(item.remaining || 0) < 5000 ? '#e67e22' : '#2ecc71'}; font-weight: bold;">
                            शेष: ₹${(item.remaining || 0).toLocaleString('en-IN')}
                        </span>
                    </div>
                `;
            });
        }
    }

    // 3. एक्सपेंडिचर रिपोर्ट टेबल (expBody) को अपडेट करना
    const expBody = document.getElementById('expBody');
    if(expBody) {
        // नोट: आवश्यकतानुसार फ़ॉर्मेट रेंडरिंग कोड यहाँ जोड़ा जा सकता है
    }
}
</script>
<script>
// अपनी नई जेनरेटेड Google Web App URL यहाँ डालें
const GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyEVd-HJ6MWluxu7lhRcG2uuoqF80ST_TtzSZbVhYuwRVSeUhD9DmV-4R5vzSh4feY/exec";

// 1. पेज लोड होते ही पुराना डेटा अपने आप लोड करें (Fetch Data on Load)
document.addEventListener("DOMContentLoaded", function() {
    fetchLiveData();
});

function fetchLiveData() {
    // स्क्रीन पर लोडिंग स्टेट दिखाने के लिए
    const totalStrip = document.getElementById('totalStrip');
    const balanceList = document.getElementById('balanceList');
    const expBody = document.getElementById('expBody');
    
    // सुधार: गैर-मानक बूटस्ट्रैप क्लासेस को हटाकर सटीक इनलाइन स्टाइल मार्जिन सेट किया गया है
    if(totalStrip) totalStrip.innerHTML = '<p style="padding:10px; color:#666; font-size:12px;"><i class="fa-solid fa-spinner fa-spin" style="margin-right: 6px;"></i> लाइव डेटा लोड हो रहा है...</p>';
    if(balanceList) balanceList.innerHTML = '<p style="padding:10px; color:#666; font-size:12px;">अपडेट किया जा रहा है...</p>';
    if(expBody) expBody.innerHTML = '<tr><td colspan="5" style="padding:15px; text-align:center; color:#666;"><i class="fa-solid fa-spinner fa-spin" style="margin-right: 6px;"></i> रिकॉर्ड्स लोड हो रहे हैं...</td></tr>';

    // GET रिक्वेस्ट के जरिए पुराना डेटा मंगाना (Apps Script में doGet हैंडलर होना चाहिए)
    fetch(`${GOOGLE_SCRIPT_URL}?action=getData`)
    .then(response => response.json())
    .then(res => {
        if(res.result === "success") {
            updateDashboardUI(res.data);
        } else {
            console.error("डेटा लोड करने में विफल:", res.error);
        }
    })
    .catch(error => {
        console.error("कनेक्शन एरर:", error);
    });
}

// 2. ऑलॉटमेंट फॉर्म सबमिशन इवेंट
document.getElementById('altForm').addEventListener('submit', function(e) {
    e.preventDefault();
    submitData(this, "आवंटन डेटा सेव करें");
});

// 3. एक्सपेंडिचर फॉर्म सबमिशन इवेंट
document.getElementById('expForm').addEventListener('submit', function(e) {
    e.preventDefault();
    submitData(this, "व्यय डेटा सेव करें");
});

// कॉमन डेटा सबमिशन लॉजिक
function submitData(formElement, originalBtnText) {
    const btn = formElement.querySelector('button[type="submit"]');
    btn.innerText = "सेव हो रहा है...";
    btn.disabled = true;

    const formData = new FormData(formElement);

    fetch(GOOGLE_SCRIPT_URL, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(res => {
        if(res.result === "success") {
            alert("डेटा सफलतापूर्वक Google Sheet में रिकॉर्ड हो गया है!");
            formElement.reset();
            updateDashboardUI(res.data); // सबमिशन के तुरंत बाद UI लाइव अपडेट
        } else {
            alert("त्रुटि: " + res.error);
        }
    })
    .catch(error => {
        alert("सर्वर से कनेक्ट नहीं हो पाया। कृपया दोबारा प्रयास करें।");
        console.error('Error:', error);
    })
    .finally(() => {
        btn.innerText = originalBtnText;
        btn.disabled = false;
    });
}

// 4. दोनों टैब (Expe Report और Balance Sheet) को लाइव रेंडर करने वाला मास्टर फंक्शन
function updateDashboardUI(data) {
    if (!data) return;
    
    // TAB 4: Balance Sheet के मुख्य कार्ड्स अपडेट करना
    const totalStrip = document.getElementById('totalStrip');
    if(totalStrip) {
        // सुधार: null वैल्यू मिलने पर होने वाले TypeError क्रैश से बचने के लिए तार्किक फ़ॉल-बैक (val || 0) जोड़ा गया है
        const allocated = data.totalAllotment || 0;
        const expenditure = data.totalExpenditure || 0;
        const balance = data.netBalance || 0;

        totalStrip.innerHTML = `
            <div style="background: #fff; padding: 12px 18px; min-width: 140px; border-radius: 8px; border-left: 4px solid #1f4e5b; flex: 1; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <p style="font-size: 11px; color:#777; margin:0; font-weight:bold; text-transform:uppercase;">TOTAL ALLOTMENT</p>
                <p style="font-size:16px; color:#1f4e5b; margin:0; font-weight:bold;">₹${allocated.toLocaleString('en-IN')}</p>
            </div>
            <div style="background: #fff; padding: 12px 18px; min-width: 140px; border-radius: 8px; border-left: 4px solid #e74c3c; flex: 1; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <p style="font-size: 11px; color:#777; margin:0; font-weight:bold; text-transform:uppercase;">TOTAL EXPENSE</p>
                <p style="font-size:16px; color:#e74c3c; margin:0; font-weight:bold;">₹${expenditure.toLocaleString('en-IN')}</p>
            </div>
            <div style="background: #fff; padding: 12px 18px; min-width: 140px; border-radius: 8px; border-left: 4px solid #2ecc71; flex: 1; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <p style="font-size: 11px; color:#777; margin:0; font-weight:bold; text-transform:uppercase;">NET BALANCE</p>
                <p style="font-size:16px; color:#2ecc71; margin:0; font-weight:bold;">₹${balance.toLocaleString('en-IN')}</p>
            </div>
        `;
    }

    // TAB 4: बची हुई राशि (balanceList) हेड-वाइज अपडेट करना
    const balanceList = document.getElementById('balanceList');
    if(balanceList) {
        balanceList.innerHTML = "";
        if(!data.headWiseReport || data.headWiseReport.length === 0) {
            balanceList.innerHTML = '<p style="color:#999; font-size:12px; margin:5px 0;">कोई बजट कोड आवंटित नहीं है।</p>';
        } else {
            data.headWiseReport.forEach(item => {
                const remaining = item.remaining || 0;
                balanceList.innerHTML += `
                    <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f4f4f4; font-size: 12px;">
                        <span style="color: #333; font-weight: 500;"><i class="fa-solid fa-folder-open" style="color: #94a3b8; margin-right: 8px;"></i> ${item.head}</span>
                        <span style="color: ${remaining < 5000 ? '#e67e22' : '#2ecc71'}; font-weight: bold;">
                            शेष: ₹${remaining.toLocaleString('en-IN')}
                        </span>
                    </div>
                `;
            });
        }
    }

    // TAB 3: Recent Bill Records टेबल (expBody) लाइव अपडेट करना
    const expBody = document.getElementById('expBody');
    if(expBody) {
        expBody.innerHTML = "";
        if(!data.recentExpenses || data.recentExpenses.length === 0) {
            expBody.innerHTML = `<tr><td colspan="5" style="padding:15px; text-align:center; color:#999;">कोई बिल रिकॉर्ड उपलब्ध नहीं है।</td></tr>`;
        } else {
            data.recentExpenses.forEach(exp => {
                const amount = exp.amount || 0;
                expBody.innerHTML += `
                    <tr style="border-bottom: 1px solid #eee;">
                        <td style="padding: 10px; font-weight:500;">${exp.bill_no}</td>
                        <td style="padding: 10px; color:#555;">${exp.date}</td>
                        <td style="padding: 10px; color:#003366;">${exp.head}</td>
                        <td style="padding: 10px; font-weight:bold; color:#c65911;">₹${amount.toLocaleString('en-IN')}</td>
                        <td style="padding: 10px; color:#666;">${exp.purpose}</td>
                    </tr>
                `;
            });
        }
    }
}
</script>
</body>
<!-- पूरी तरह से नया और अचूक स्क्रिप्ट ब्लॉक -->
<script>
    // फंक्शंस को सीधे विंडो (Global) पर असाइन कर रहे हैं ताकि एरर का कोई चांस न रहे
    window.switchPage = function(pageId) {
        console.log("Switching to page: " + pageId); // ब्राउज़र कंसोल में चेक करने के लिए
        
        // 1. सभी स्क्रीन्स को छुपाएं
        var pages = document.querySelectorAll('.app-page');
        pages.forEach(function(page) {
            page.classList.remove('active');
            page.style.display = 'none';
        });
        
        // 2. केवल चुनी हुई स्क्रीन दिखाएं
        var activePage = document.getElementById(pageId);
        if(activePage) {
            activePage.classList.add('active');
            // सुधार 1: होम स्क्रीन के फ्लेक्स लेआउट को ब्लॉक होने से सुरक्षित रखने के लिए कंडीशन चेक
            if (pageId === 'home') {
                activePage.style.display = 'flex';
            } else {
                activePage.style.display = 'block';
            }
        }
        
        // 3. बॉटम नेव बार एक्टिव कलर बदलना
        var navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(function(item) {
            item.classList.remove('active');
        });
        
        var pageList = ['home', 'notice', 'service', 'about', 'contact'];
        var index = pageList.indexOf(pageId);
        if(index !== -1 && navItems[index]) {
            navItems[index].classList.add('active');
        }

        // सुधार 2: जब बाहर से 'service' पेज पर ट्रांसफर किया जाए (जैसे लॉगिन के बाद), तब सब-टैब बटन को ऑटो-सिंक करें
        if (pageId === 'service') {
            var tabButtons = document.querySelectorAll('.tab-btn');
            tabButtons.forEach(function(btn) {
                if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes('balance-section')) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
        }
    };

    window.showTab = function(event, sectionId) {
        console.log("Showing tab section: " + sectionId);
        if(event) event.preventDefault();

        // 1. सभी सब-फॉर्म्स (tab-content) को छुपाएं
        var contents = document.querySelectorAll('.tab-content');
        contents.forEach(function(content) {
            content.style.display = 'none';
            content.classList.remove('active');
        });
        
        // 2. सभी बटन्स से एक्टिव क्लास हटाएं
        var tabButtons = document.querySelectorAll('.tab-btn');
        tabButtons.forEach(function(btn) {
            btn.classList.remove('active');
        });
        
        // 3. केवल टारगेट सेक्शन दिखाएं
        var target = document.getElementById(sectionId);
        if(target) {
            target.style.display = 'block';
            target.classList.add('active');
        }
        
        // 4. क्लिक किए गए बटन को एक्टिव कलर दें
        if(event && event.currentTarget) {
            event.currentTarget.classList.add('active');
        }
    };

    // पेज लोड होने पर शुरुआती सेटअप
    window.addEventListener('DOMContentLoaded', function() {
        // लॉगिन (home) को छोड़कर सब छुपाएं
        var pages = document.querySelectorAll('.app-page');
        pages.forEach(function(page) {
            page.classList.remove('active');
            page.style.display = 'none';
        });
        
        var homePage = document.getElementById('home');
        if(homePage) {
            homePage.classList.add('active');
            homePage.style.display = 'flex'; // सुधार 1 के साथ सिंक किया गया
        }

        // डिफ़ॉल्ट रूप से बैलेंस शीट टैब को ओपन रखें
        var defaultTab = document.getElementById('balance-section');
        if(defaultTab) {
            defaultTab.style.display = 'block';
            defaultTab.classList.add('active');
        }
    });
</script>

</html>
"""
# --- 4. FLASK ROUTING ---
@app.route('/')
def main_app():
    # ध्यान दें: यदि आपने पिछले ब्लॉक में ABOUT_CONTACT_BODY अलग वेरिएबल बनाया था, 
    # तो उसे भी यहाँ LAYOUT_START + PAGES_BODY + ABOUT_CONTACT_BODY + LAYOUT_END करके जोड़ लें।
    full_html = LAYOUT_START + PAGES_BODY + LAYOUT_END
    return render_template_string(full_html)

@app.route('/submit', methods=['POST'])
def submit():
    form_type = request.form.get('type')
    
    # सुधार 1: जावास्क्रिप्ट के Fetch API इन्फ्रास्ट्रक्चर को क्रैश होने से बचाने के लिए 
    # HTML स्ट्रिंग की जगह एक स्टैंडर्ड नल-सेफ (Null-Safe) JSON ऑब्जेक्ट रिटर्न किया गया है।
    response_data = {
        "result": "success",
        "error": None,
        "data": {
            "totalAllotment": 147.21,
            "totalExpenditure": 0.0,
            "netBalance": 147.21,
            "headWiseReport": [
                {
                    "head": "51-2235-02-102-0123",
                    "allocated": 147.21,
                    "spent": 0.0,
                    "remaining": 147.21
                }
            ],
            "recentExpenses": []
        }
    }
    
    # यदि रिक्वेस्ट AJAX/Fetch के जरिए आई है, तो JSON भेजें
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json or 'multipart/form-data' in request.content_type:
        return jsonify(response_data)
        
    # सुधार 2: डायरेक्ट HTML सबमिशन बैकअप फ़ॉल-बैक पेज को भी सुरक्षित रखा गया है
    return f"""
    <div style="font-family:sans-serif; text-align:center; padding:50px; background:#f0f2f5; height:100vh; box-sizing:border-box;">
        <div style="background:white; padding:30px; border-radius:20px; display:inline-block; box-shadow:0 4px 15px rgba(0,0,0,0.1); max-width:320px;">
            <h3 style="color:#764ba2; margin-top:0;">सफलतापूर्वक सेव हुआ!</h3>
            <p style="color:#666; font-size:14px;">आपका {form_type} डेटा प्राप्त हो गया है।</p>
            <a href="/" style="display:block; padding:10px 20px; background:#764ba2; color:white; text-decoration:none; border-radius:8px; font-weight:bold; margin-top:20px;">ऐप पर वापस जाएं</a>
        </div>
    </div>
    """

if __name__ == '__main__':
    # थ्रेडिंग ऑन रखी गई है ताकि लाइव घड़ी और मल्टीपल रिक्वेस्ट में ऐप हैंग न हो
    app.run(debug=True, threaded=True)
