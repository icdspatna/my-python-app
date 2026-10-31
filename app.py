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
    .tab-content {
    display: none; /* डिफ़ॉल्ट रूप से सब छुप जाएगा */
    padding: 15px;
    border: 1px solid #ccc;
    border-radius: 8px;
    margin-top: 10px;
            }

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
        <div id="service" class="app-page active">
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
                <h4><i class="fa-solid fa-circle-plus" style="color: green;"></i> 1. Allotment Entry</h4>
                <form id="altForm" method="POST">
                    <input type="hidden" name="type" value="Allotment">
                    <select id="altSrc" name="source" class="app-input" style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; background-color: white;" required>
                        <option value="" disabled selected hidden>Source (स्रोत चुनें)</option>
                        <option value="CFMS">CFMS</option>
                        <option value="HRMS">HRMS</option>
                        <option value="PFMS">PFMS</option>
                        <option value="OTHER">Other (अन्य)</option>
                    </select>

                    <input type="text" id="altOrd" name="order_no" placeholder="Order No." class="app-input" required>
                    
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
                    <button type="submit" class="submit-btn" style="background: green; width: 100%; padding: 10px; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">आवंटन डेटा सेव करें</button>
                </form> 
            </div>

            <!-- TAB 2: Expenditure Entry Form -->
            <div id="expenditure-section" class="tab-content" style="display: none; scroll-margin-top: 10px;">
                <h4><i class="fa-solid fa-file-invoice-dollar" style="color: red;"></i> 2. Expenditure Entry</h4>
                <form id="expForm" method="POST">
                    <input type="hidden" name="type" value="Expenditure">
                    <input type="text" id="expOrd" name="order_no" placeholder="Order No." class="app-input" required>
                    <input type="date" id="expDat" name="date" class="app-input" required>
                    
                    <select id="expHead" name="budget_head" class="app-input" style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; background-color: white;" required>
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

                    <select id="expUnit" name="unit_code" class="app-input" style="width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; background-color: white;" required>
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

                    <input type="hidden" id="expSrc" value="OTHER">
                    <input type="hidden" id="expBill" value="000">
                    <input type="hidden" id="expPur" value="Office Expenses">
                    <button type="submit" class="submit-btn" style="background: red; width: 100%; padding: 10px; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">व्यय डेटा सेव करें</button>
                </form>
            </div>

            <!-- TAB 3: Expenditure Report Section -->
            <div id="report-section" class="tab-content" style="display: none;">
                <div style="background: #003366; color: white; padding: 12px 20px; border-radius: 8px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; font-size: 16px; font-weight: 600;"><i class="fa-solid fa-file-invoice-dollar me-2"></i> Recent Bill Records</h3>
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
                                <!-- लाइव डेटा यहाँ ऑटोमैटिक लोड होगा -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- TAB 4: Balance Sheet Section -->
            <div id="balance-section" class="tab-content" style="display: block;">
                <div style="background: #1f4e5b; color: white; padding: 12px 20px; border-radius: 8px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; font-size: 16px; font-weight: 600;"><i class="fa-solid fa-scale-balanced me-2"></i> 4. Balance Sheet</h3>
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
    <!-- action में Formspree की लिंक और आपका ईमेल सेट है -->
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
    // 1. मुख्य पेज बदलने के लिए पुराना फंक्शन
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

    // 2. आपके 4 सब-फॉर्म्स / टैब बदलने के लिए नया फंक्शन
    function showSection(sectionId) {
        var contents = document.getElementsByClassName('tab-content');
        for (var i = 0; i < contents.length; i++) {
            contents[i].style.display = 'none';
        }
        var target = document.getElementById(sectionId);
        if(target) {
            target.style.display = 'block';
        }
    }
    </script>
<script>
// स्क्रिप्ट की URL यहाँ पेस्ट करें
const GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyA3ZqLiKnxjfE3g9fo8vbwq4Cks43Ob-EEV5ZI0E3flWRp618kmgCceNFhGJ1h3C4L/exec";

// ऑलॉटमेंट फॉर्म सबमिशन हैंडलर
document.getElementById('altForm').addEventListener('submit', function(e) {
    e.preventDefault();
    submitToGoogleSheet(this, "आवंटन डेटा सेव करें");
});

// नोट: इसी तरह अपने Expenditure Form (जैसे id="expForm") पर भी यह इवेंट लगा लें
// document.getElementById('expForm').addEventListener('submit', function(e) { ... });

function submitToGoogleSheet(formElement, originalBtnText) {
    const btn = formElement.querySelector('button[type="submit"]');
    btn.innerText = "सेव किया जा रहा है...";
    btn.disabled = true;

    const formData = new FormData(formElement);
    
    // यदि फॉर्म में 'type' मैन्युअली सेट नहीं है, तो उसे यहाँ जोड़ें
    // formData.append("type", "Allotment"); 

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
        totalStrip.innerHTML = `
            <div style="background: #fff; padding: 12px; min-width: 140px; border-radius: 8px; border-left: 4px solid #1f4e5b; flex: 1;">
                <p style="size: 11px; color:#777; margin:0;">TOTAL ALLOTMENT</p>
                <p style="font-size:16px; color:#1f4e5b; margin:0; font-weight:bold;">₹${data.totalAllotment.toLocaleString('en-IN')}</p>
            </div>
            <div style="background: #fff; padding: 12px; min-width: 140px; border-radius: 8px; border-left: 4px solid #e74c3c; flex: 1;">
                <p style="size: 11px; color:#777; margin:0;">TOTAL EXPENSE</p>
                <p style="font-size:16px; color:#e74c3c; margin:0; font-weight:bold;">₹${data.totalExpenditure.toLocaleString('en-IN')}</p>
            </div>
            <div style="background: #fff; padding: 12px; min-width: 140px; border-radius: 8px; border-left: 4px solid #2ecc71; flex: 1;">
                <p style="size: 11px; color:#777; margin:0;">NET BALANCE</p>
                <p style="font-size:16px; color:#2ecc71; margin:0; font-weight:bold;">₹${data.netBalance.toLocaleString('en-IN')}</p>
            </div>
        `;
    }

    // 2. लाइव बैलेंस लिस्ट (balanceList) को अपडेट करना
    const balanceList = document.getElementById('balanceList');
    if(balanceList) {
        balanceList.innerHTML = ""; // पुराना डेटा साफ़ करें
        data.headWiseReport.forEach(item => {
            balanceList.innerHTML += `
                <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f4f4f4; font-size: 12px;">
                    <span style="color: #333; font-weight: 500;">Head: ${item.head}</span>
                    <span style="color: ${item.remaining < 5000 ? '#e67e22' : '#2ecc71'}; font-weight: bold;">
                        शेष: ₹${item.remaining.toLocaleString('en-IN')}
                    </span>
                </div>
            `;
        });
    }

    // 3. एक्सपेंडिचर रिपोर्ट टेबल (expBody) को अपडेट करना
    const expBody = document.getElementById('expBody');
    if(expBody) {
        // नोट: यहाँ आप अपने आवश्यकतानुसार फ़ॉर्मेट में हेड-वाइज़ समरी रेंडर कर सकते हैं
    }
}
</script> 
<script>
// अपनी नई जेनरेटेड Google Web App URL यहाँ डालें
const GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyA3ZqLiKnxjfE3g9fo8vbwq4Cks43Ob-EEV5ZI0E3flWRp618kmgCceNFhGJ1h3C4L/exec";

// 1. पेज लोड होते ही पुराना डेटा अपने आप लोड करें (Fetch Data on Load)
document.addEventListener("DOMContentLoaded", function() {
    fetchLiveData();
});

function fetchLiveData() {
    // स्क्रीन पर लोडिंग स्टेट दिखाने के लिए
    const totalStrip = document.getElementById('totalStrip');
    const balanceList = document.getElementById('balanceList');
    const expBody = document.getElementById('expBody');
    
    if(totalStrip) totalStrip.innerHTML = '<p style="padding:10px; color:#666; font-size:12px;"><i class="fa-solid fa-spinner fa-spin me-1"></i> लाइव डेटा लोड हो रहा है...</p>';
    if(balanceList) balanceList.innerHTML = '<p style="padding:10px; color:#666; font-size:12px;">अपडेट किया जा रहा है...</p>';
    if(expBody) expBody.innerHTML = '<tr><td colspan="5" style="padding:15px; text-align:center; color:#666;"><i class="fa-solid fa-spinner fa-spin me-1"></i> रिकॉर्ड्स लोड हो रहे हैं...</td></tr>';

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
    
    // TAB 4: Balance Sheet के मुख्य कार्ड्स अपडेट करना
    const totalStrip = document.getElementById('totalStrip');
    if(totalStrip) {
        totalStrip.innerHTML = `
            <div style="background: #fff; padding: 12px 18px; min-width: 140px; border-radius: 8px; border-left: 4px solid #1f4e5b; flex: 1; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <p style="font-size: 11px; color:#777; margin:0; font-weight:bold; text-transform:uppercase;">TOTAL ALLOTMENT</p>
                <p style="font-size:16px; color:#1f4e5b; margin:0; font-weight:bold;">₹${data.totalAllotment.toLocaleString('en-IN')}</p>
            </div>
            <div style="background: #fff; padding: 12px 18px; min-width: 140px; border-radius: 8px; border-left: 4px solid #e74c3c; flex: 1; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <p style="font-size: 11px; color:#777; margin:0; font-weight:bold; text-transform:uppercase;">TOTAL EXPENSE</p>
                <p style="font-size:16px; color:#e74c3c; margin:0; font-weight:bold;">₹${data.totalExpenditure.toLocaleString('en-IN')}</p>
            </div>
            <div style="background: #fff; padding: 12px 18px; min-width: 140px; border-radius: 8px; border-left: 4px solid #2ecc71; flex: 1; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <p style="font-size: 11px; color:#777; margin:0; font-weight:bold; text-transform:uppercase;">NET BALANCE</p>
                <p style="font-size:16px; color:#2ecc71; margin:0; font-weight:bold;">₹${data.netBalance.toLocaleString('en-IN')}</p>
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
                balanceList.innerHTML += `
                    <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f4f4f4; font-size: 12px;">
                        <span style="color: #333; font-weight: 500;"><i class="fa-solid fa-folder-open text-muted me-2"></i> ${item.head}</span>
                        <span style="color: ${item.remaining < 5000 ? '#e67e22' : '#2ecc71'}; font-weight: bold;">
                            शेष: ₹${item.remaining.toLocaleString('en-IN')}
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
                expBody.innerHTML += `
                    <tr style="border-bottom: 1px solid #eee;">
                        <td style="padding: 10px; font-weight:500;">${exp.bill_no}</td>
                        <td style="padding: 10px; color:#555;">${exp.date}</td>
                        <td style="padding: 10px; color:#003366;">${exp.head}</td>
                        <td style="padding: 10px; font-weight:bold; color:#c65911;">₹${exp.amount.toLocaleString('en-IN')}</td>
                        <td style="padding: 10px; color:#666;">${exp.purpose}</td>
                    </tr>
                `;
            });
        }
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
