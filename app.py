from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- 1. FULL APP TEMPLATE (आपकी CSS और मोबाइल ढांचे के साथ) ---
APP_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ICDS App - Rudra Tech</title>
    <!-- FontAwesome Buttons & Logos -->
    <link rel="stylesheet" href="https://cloudflare.com">
    
    <style>
        /* मोबाइल का मुख्य ढांचा और कॉमन सेटिंग्स जो आपने दी हैं */
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .mobile-app-container {
            width: 360px;
            height: 740px;
            background: #fff;
            border-radius: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
            position: relative;
            display: flex;
            flex-direction: column;
        }
        .app-page {
            display: none; /* डिफ़ॉल्ट रूप से छुपे रहेंगे */
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            margin-bottom: 65px;
        }
        .app-page.active {
            display: block; /* जो एक्टिव होगा सिर्फ वही दिखेगा */
        }

        /* होम पेज और लॉगिन स्क्रीन का सुंदर ग्रेडिएंट स्टाइल */
        #home {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            height: 100%;
            box-sizing: border-box;
        }
        .hero-section {
            margin-top: 30%;
        }
        .hero-section h1 {
            font-size: 26px;
            margin-bottom: 10px;
        }
        .cta-btn {
            background: #fff;
            color: #764ba2;
            border: none;
            padding: 12px 35px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 25px;
            cursor: pointer;
            margin-top: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            transition: 0.3s;
        }
        .cta-btn:hover { transform: scale(1.05); }

        /* लॉगिन फॉर्म की नई स्टाइल जो आपने सुझाई */
        .login-container {
            margin-top: 15%;
            text-align: center;
            padding: 0 10px;
        }
        .login-container h2 { font-size: 22px; margin-bottom: 5px; }
        .login-form { margin-top: 20px; }
        
        .input-group {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.4);
            padding: 12px;
            margin-bottom: 15px;
            border-radius: 25px;
            display: flex;
            align-items: center;
        }
        .input-group i { margin-right: 10px; color: #fff; }
        .input-group input {
            background: none;
            border: none;
            outline: none;
            color: white;
            width: 100%;
        }
        .input-group input::placeholder { color: #eee; }
        
        .login-btn {
            background: #fff;
            color: #764ba2;
            border: none;
            width: 100%;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 25px;
            cursor: pointer;
            margin-top: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        /* अन्य पेजों के लिए इनपुट और कार्ड्स की मोबाइल डिज़ाइन */
        .page-title { color: #764ba2; border-bottom: 2px solid #764ba2; padding-bottom: 5px; margin-bottom: 15px; font-size: 20px; }
        .form-card { background: #f8f9fa; border: 1px solid #e2e8f0; border-radius: 15px; padding: 15px; margin-bottom: 20px; }
        .form-card h4 { color: #2d3748; margin-top: 0; font-size: 16px; margin-bottom: 12px; }
        .app-input { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #cbd5e0; border-radius: 8px; box-sizing: border-box; font-size: 14px; }
        .submit-btn { width: 100%; padding: 12px; background: #764ba2; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .notice-box { background: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; border-radius: 4px; font-size: 13px; margin-bottom: 10px; color: #856404; }

        /* नीचे का कॉमन नेविगेशन बार */
        .bottom-nav {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 65px;
            background: #ffffff;
            display: flex;
            justify-content: space-around;
            align-items: center;
            border-top: 1px solid #eee;
            box-sizing: border-box;
        }
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            color: #888;
            cursor: pointer;
            font-size: 11px;
            text-decoration: none;
        }
        .nav-item i { font-size: 20px; margin-bottom: 2px; }
        .nav-item.active { color: #764ba2; font-weight: bold; }
    </style>
</head>
<body>

    <!-- मुख्य मोबाइल कंटेनर (360px x 740px) -->
    <div class="mobile-app-container">
        
        <!-- ================= 1. HOME & LOGIN PAGE ================= -->
        <div id="home" class="app-page active">
            <div class="hero-section">
                <i class="fa-solid fa-calculator" style="font-size: 50px; margin-bottom: 10px;"></i>
                <h1>ICDS बजट प्रबंधन</h1>
                <p style="font-size: 13px; opacity: 0.9;">Rudra Tech Pvt Ltd</p>
            </div>
            
            <div class="login-container">
                <h2>क्विक लॉगिन</h2>
                <div class="login-form">
                    <div class="input-group">
                        <i class="fa-solid fa-user"></i>
                        <input type="text" placeholder="यूजरनेम दर्ज करें">
                    </div>
                    <div class="input-group">
                        <i class="fa-solid fa-lock"></i>
                        <input type="password" placeholder="पासवर्ड दर्ज करें">
                    </div>
                    <button class="login-btn" onclick="switchPage('service')">लॉगिन करें</button>
                </div>
            </div>
        </div>

        <!-- ================= 2. NOTICE PAGE ================= -->
        <div id="notice" class="app-page">
            <h3 class="page-title"><i class="fa-solid fa-bullhorn me-2"></i>सूचना पट्ट</h3>
            <div class="notice-box">
                <strong>महत्वपूर्ण:</strong> वित्तीय वर्ष हेतु सभी यूनिट हेड का व्यय प्रतिवेदन समय पर देना अनिवार्य है।
            </div>
            <div class="notice-box" style="background:#e1f5fe; border-left-color:#0288d1; color:#01579b;">
                <strong>नया आवंटन:</strong> निदेशालय से मद 2235 में राशि ट्रांसफर कर दी गई है।
            </div>
        </div>

        <!-- ================= 3. SERVICE PAGE ================= -->
        <div id="service" class="app-page">
            <h3 class="page-title"><i class="fa-solid fa-gears me-2"></i>सेवाएं एवं एंट्री</h3>
            
            <!-- Allotment Entry Form -->
            <div class="form-card">
                <h4><i class="fa-solid fa-circle-plus" style="color: green;"></i> 1. Allotment Entry</h4>
                <form action="/submit" method="POST">
                    <input type="hidden" name="type" value="Allotment">
                    <input type="text" name="source" placeholder="Source (स्रोत)" class="app-input" required>
                    <input type="text" name="order_no" placeholder="Order No." class="app-input" required>
                    <input type="text" name="budget_head" placeholder="Budget Head" class="app-input" required>
                    <input type="text" name="unit_code" placeholder="Unit Code" class="app-input" required>
                    <input type="number" name="amount" placeholder="Amount (राशि ₹)" class="app-input" required>
                    <input type="text" name="remark" placeholder="Remark" class="app-input">
                    <button type="submit" class="submit-btn" style="background: green;">आवंटन डेटा सेव करें</button>
                </form>
            </div>

            <!-- Expenditure Entry Form -->
            <div class="form-card">
                <h4><i class="fa-solid fa-file-invoice-dollar" style="color: red;"></i> 2. Expenditure Entry</h4>
                <form action="/submit" method="POST">
                    <input type="hidden" name="type" value="Expenditure">
                    <input type="text" name="order_no" placeholder="Order No." class="app-input" required>
                    <input type="date" name="date" class="app-input" required>
                    <input type="text" name="budget_head" placeholder="Budget Head" class="app-input" required>
                    <input type="text" name="unit_head" placeholder="Unit Head" class="app-input" required>
                    <input type="number" name="amount" placeholder="Amount (व्यय राशि ₹)" class="app-input" required>
                    <button type="submit" class="submit-btn" style="background: red;">व्यय डेटा सेव करें</button>
                </form>
            </div>
        </div>

        <!-- ================= 4. ABOUT ME PAGE ================= -->
        <div id="about" class="app-page" style="text-align: center;">
            <h3 class="page-title">About Me</h3>
            <h4 style="color:#764ba2; margin-bottom: 5px;">Rudra Tech Pvt Ltd</h4>
हम सरकारी कार्यालयों के लिए आधुनिक सॉफ्टवेयर का निर्माण करते हैं।

WhatsApp Chat
Contact Us





डायरेक्ट मैसेज भेजें

Home
Notice
Service
About
Contact
function switchPage(pageId) {
// 1. सभी पेजों से active क्लास हटाओ
document.querySelectorAll('.app-page').forEach(page => {
page.classList.remove('active');
});
// 2. सिलेक्टेड पेज को दिखाओ
document.getElementById(pageId).classList.add('active');
// 3. नेविगेशन बटन्स के रंग बदलो
document.querySelectorAll('.nav-item').forEach(item => {
item.classList.remove('active');
});
// नीचे के मेनू बार को इंडेक्स के हिसाब से एक्टिव करना
const pages = ['home', 'notice', 'service', 'about', 'contact'];
const index = pages.indexOf(pageId);
if(index !== -1) {
document.querySelectorAll('.nav-item')[index].classList.add('active');
}
}



"""
@app.route('/')
def main_app():
# अब सिर्फ एक ही बेस टेम्पलेट लोड होगा और पूरा ऐप उसी में चलेगा
return render_template_string(APP_TEMPLATE)
@app.route('/submit', methods=['POST'])
def submit():
form_type = request.form.get('type')
return f"""



सफलतापूर्वक सेव हुआ!
आपका {form_type} डेटा प्राप्त हो गया है।
ऐप पर वापस जाएं


"""
if name == 'main':
app.run(debug=True)
