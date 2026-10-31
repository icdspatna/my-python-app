from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- 1. APP LAYOUT START ---
LAYOUT_START = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ICDS App - Rudra Tech</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body {
            margin: 0; padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            display: flex; justify-content: center; align-items: center;
            height: 100vh;
        }
        .mobile-app-container {
            width: 360px; height: 740px;
            background: #fff; border-radius: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden; position: relative;
            display: flex; flex-direction: column;
        }
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
    </style>
</head>
<body>
    <div class="mobile-app-container">
"""

# --- 2. INNER PAGES BODY ---
PAGES_BODY = """
        <!-- 1. HOME SCREEN -->
        <div id="home" class="app-page active">
            <div class="hero-section">
                <i class="fa-solid fa-calculator" style="font-size: 50px; margin-bottom: 10px;"></i>
                <h1>ICDS बजट प्रबंधन</h1>
                <p style="font-size: 13px; opacity: 0.9;">Rudra Tech Pvt Ltd</p>
            </div>
            <div class="login-container">
                <h2>Log In</h2>
                <div class="login-form">
                    <div class="input-group"><i class="fa-solid fa-user"></i><input type="text" placeholder="Enter User name"></div>
                    <div class="input-group"><i class="fa-solid fa-lock"></i><input type="password" placeholder="Password"></div>
                    <button class="login-btn" onclick="switchPage('service')">Login</button>
                </div>
            </div>
        </div>

        <!-- 2. NOTICE SCREEN -->
        <div id="notice" class="app-page">
            <h3 class="page-title"><i class="fa-solid fa-bullhorn me-2"></i>Notice Board </h3>
            <div class="notice-box"><strong>महत्वपूर्ण:</strong> व्यय प्रतिवेदन समय पर देना अनिवार्य है।</div>
            <div class="notice-box" style="background:#e1f5fe; border-left-color:#0288d1; color:#01579b;"><strong>New Allotment:</strong> निदेशालय से मद 2235 में राशि ट्रांसफर हुई।</div>
        </div>

        <!-- 3. SERVICE SCREEN (4 Quick Jump Tabs) -->
        <div id="service" class="app-page">
            <h3 class="page-title"><i class="fa-solid fa-gears me-2"></i>Entry Service</h3>
            
            <!-- 4 नैविगेशन बटन्स (Bari bari click karne par niche jump karega) -->
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 20px;">
                <a href="#allotment-section" style="text-decoration:none; padding:10px; background:#e2f0d9; color:#385723; text-align:center; font-size:12px; font-weight:bold; border-radius:8px; border:1px solid #a9d18e;"><i class="fa-solid fa-circle-plus d-block mb-1"></i>Allotment Entry</a>
                <a href="#expenditure-section" style="text-decoration:none; padding:10px; background:#fce4d6; color:#c65911; text-align:center; font-size:12px; font-weight:bold; border-radius:8px; border:1px solid #f8cbad;"><i class="fa-solid fa-file-invoice-dollar d-block mb-1"></i>Expenditure Entry</a>
                <a href="#report-section" style="text-decoration:none; padding:10px; background:#fff2cc; color:#7f6000; text-align:center; font-size:12px; font-weight:bold; border-radius:8px; border:1px solid #ffe599;"><i class="fa-solid fa-chart-line d-block mb-1"></i>Expe Report</a>
                <a href="#balance-section" style="text-decoration:none; padding:10px; background:#e8f4f8; color:#1f4e5b; text-align:center; font-size:12px; font-weight:bold; border-radius:8px; border:1px solid #b4d6e4;"><i class="fa-solid fa-scale-balanced d-block mb-1"></i>Balance Sheet</a>
            </div>

            <!-- TAB 1: Allotment Entry Form -->
            <div id="allotment-section" class="form-card" style="scroll-margin-top: 10px;">
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

            <!-- TAB 2: Expenditure Entry Form -->
            <div id="expenditure-section" class="form-card" style="scroll-margin-top: 10px;">
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

            <!-- TAB 3: Expenditure Report Section (All Bill & Code Wise) -->
            <div id="report-section" class="form-card" style="scroll-margin-top: 10px; background:#fffdf4;">
                <h4><i class="fa-solid fa-chart-line" style="color: #7f6000;"></i> 3. Expenditure Report</h4>
                <div style="padding:10px; background:#fff; border-radius:8px; border:1px solid #ddd; margin-bottom:10px;">
                    <span style="font-size:13px; font-weight:bold; color:#333;">1. Expenditure Report ALL Bill</span>
                    <p style="font-size:11px; color:#666; margin:4px 0 8px 0;">कुल खर्च किए गए सभी बिलों की विस्तृत सूची।</p>
                    <button class="btn-custom" style="padding:4px 10px; font-size:11px; background:#764ba2; color:#fff; border:none; border-radius:4px;">रिपोर्ट देखें</button>
                </div>
                <div style="padding:10px; background:#fff; border-radius:8px; border:1px solid #ddd;">
                    <span style="font-size:13px; font-weight:bold; color:#333;">2. Expenditure Budget Code wise</span>
                    <p style="font-size:11px; color:#666; margin:4px 0 8px 0;">बजट कोड के अनुसार कुल व्यय का विवरण।</p>
                    <button class="btn-custom" style="padding:4px 10px; font-size:11px; background:#764ba2; color:#fff; border:none; border-radius:4px;">विवरण देखें</button>
                </div>
            </div>

            <!-- TAB 4: Balance Sheet Section (Budget code wise & All balance) -->
            <div id="balance-section" class="form-card" style="scroll-margin-top: 10px; background:#f4f9fa;">
                <h4><i class="fa-solid fa-scale-balanced" style="color: #1f4e5b;"></i> 4. Balance Sheet</h4>
                <div style="padding:10px; background:#fff; border-radius:8px; border:1px solid #ddd; margin-bottom:10px;">
                    <span style="font-size:13px; font-weight:bold; color:#333;">1. Total Balance Budget Code wise</span>
                    <p style="font-size:11px; color:#666; margin:4px 0 8px 0;">किस कोड में कितना बैलेंस बचा है (आवंटन - व्यय)।</p>
                    <button class="btn-custom" style="padding:4px 10px; font-size:11px; background:#0288d1; color:#fff; border:none; border-radius:4px;">बैलेंस जांचें</button>
                </div>
                <div style="padding:10px; background:#fff; border-radius:8px; border:1px solid #ddd;">
                    <span style="font-size:13px; font-weight:bold; color:#333;">2. Total Balance ALL</span>
                    <p style="font-size:11px; color:#666; margin:4px 0 8px 0;">कार्यालय का संचित कुल शेष बजट विवरण।</p>
                    <button class="btn-custom" style="padding:4px 10px; font-size:11px; background:#0288d1; color:#fff; border:none; border-radius:4px;">समरी देखें</button>
                </div>
            </div>
        </div>

        <!-- 4. ABOUT SCREEN -->
        <div id="about" class="app-page" style="text-align: center;">
            <h3 class="page-title">About Me</h3>
            <h4 style="color:#764ba2; margin-bottom: 5px;">Rudra Tech Pvt Ltd</h4>
            <p style="font-size: 13px; color:#666;">हम कार्यालयों के लिए आधुनिक सॉफ्टवेयर का निर्माण करते हैं।</p>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            <a href="https://wa.me" target="_blank" class="submit-btn" style="background:#25D366; text-decoration:none; display:block; text-align:center;"><i class="fa-brands fa-whatsapp me-2"></i>WhatsApp Chat</a>
        </div>

        <div id="contact" class="app-page">
            <h3 class="page-title">Contact Us</h3>
            <form action="/submit" method="POST">
                <input type="hidden" name="type" value="Contact">
                <input type="text" name="name" placeholder="आपका नाम" class="app-input" required>
                <input type="text" name="subject" placeholder="विषय (Subject)" class="app-input" required>
                <textarea name="message" placeholder="यहाँ अपना सन्देश लिखें..." class="app-input" rows="4" style="height:auto;" required></textarea>
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
    <script>
        function switchPage(pageId) {
            document.querySelectorAll('.app-page').forEach(page => {
                page.classList.remove('active');
            });
            document.getElementById(pageId).classList.add('active');
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            const pages = ['home', 'notice', 'service', 'about', 'contact'];
            const index = pages.indexOf(pageId);
            if(index !== -1) {
                document.querySelectorAll('.nav-item')[index].classList.add('active');
            }
        }
    </script>
</body>
</html>
"""

# --- 4. FLASK ROUTING ---
@app.route('/')
def main_app():
    full_html = LAYOUT_START + PAGES_BODY + LAYOUT_END
    return render_template_string(full_html)

@app.route('/submit', methods=['POST'])
def submit():
    form_type = request.form.get('type')
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
    app.run(debug=True)
