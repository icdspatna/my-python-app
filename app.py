from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# --- बेस HTML टेम्पलेट (Bootstrap 5 नेविगेशन बार के साथ) ---
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rudra Tech - ICDS Budget App</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://jsdelivr.net" rel="stylesheet">
    <!-- FontAwesome Logos के लिए -->
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding-bottom: 70px; }
        .navbar-custom { background-color: #2c3e50; }
        .card-custom { border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: none; }
        .nav-tabs .nav-link.active { background-color: #3498db; color: white; border-color: #3498db; }
        
        /* बॉटम नेविगेशन बार (5 बटन मोबाइल स्टाइल) */
        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 60px; background-color: #ffffff; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); display: flex; justify-content: space-around; align-items: center; z-index: 1000; }
        .bottom-nav a { text-decoration: none; color: #7f8c8d; text-align: center; font-size: 12px; width: 20%; }
        .bottom-nav a.active { color: #3498db; font-weight: bold; }
        .bottom-nav i { font-size: 20px; display: block; margin-bottom: 2px; }
    </style>
</head>
<body>

    <!-- टॉप हेडर -->
    <nav class="navbar navbar-dark navbar-custom py-2 shadow shadow-sm mb-4">
        <div class="container text-center">
            <span class="navbar-brand mb-0 h1 mx-auto"><i class="fa-solid fa-calculator me-2"></i>ICDS आवंटन एवं व्यय प्रबंधन प्रणाली</span>
        </div>
    </nav>

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <!-- 5 पेज का बॉटम नेविगेशन बटन -->
    <div class="bottom-nav">
        <a href="/" class="{% if active_page == 'home' %}active{% endif %}">
            <i class="fa-solid fa-house"></i>Home
        </a>
        <a href="/notice" class="{% if active_page == 'notice' %}active{% endif %}">
            <i class="fa-solid fa-bell"></i>Notice
        </a>
        <a href="/service" class="{% if active_page == 'service' %}active{% endif %}">
            <i class="fa-solid fa-gears"></i>Service
        </a>
        <a href="/about" class="{% if active_page == 'about' %}active{% endif %}">
            <i class="fa-solid fa-building"></i>About Me
        </a>
        <a href="/contact" class="{% if active_page == 'contact' %}active{% endif %}">
            <i class="fa-solid fa-envelope"></i>Contact Us
        </a>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://jsdelivr.net"></script>
</body>
</html>
"""

# --- 1. HOME PAGE (Welcome Screen) ---
HOME_HTML = """
{% extends "base" %}
{% block content %}
<div class="row justify-content-center text-center mt-5">
    <div class="col-md-8">
        <div class="card card-custom p-5 bg-white">
            <img src="https://flaticon.com" style="width: 100px;" class="mx-auto mb-4" alt="Logo">
            <h1 class="display-5 text-dark fw-bold mb-3">डिजिटल बजट मैनेजर में आपका स्वागत है</h1>
            <p class="lead text-muted">यहाँ से आप ICDS कार्यालय के विभिन्न बजट हेड, आवंटन (Allotment) और व्यय (Expenditure) का लेखा-जोखा आसानी से प्रबंधित कर सकते हैं।</p>
            <hr class="my-4">
            <div class="d-grid gap-2 d-sm-flex justify-content-sm-center">
                <a href="/service" class="btn btn-primary btn-lg px-4 gap-3"><i class="fa-solid fa-play me-2"></i>काम शुरू करें</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# --- 2. NOTICE BOARD PAGE ---
NOTICE_HTML = """
{% extends "base" %}
{% block content %}
<div class="card card-custom p-4 bg-white">
    <h3 class="text-danger border-bottom pb-2 mb-3"><i class="fa-solid fa-bullhorn me-2"></i>आकर्षक सूचना पट्ट (Notice Board)</h3>
    <div class="alert alert-warning d-flex align-items-center" role="alert">
        <i class="fa-solid fa-triangle-exclamation me-3 fs-4"></i>
        <div>
            <strong>महत्वपूर्ण सूचना:</strong> वित्तीय वर्ष 2026-27 के लिए सभी यूनिट हेड का व्यय प्रतिवेदन 31 तारीख तक जमा करना अनिवार्य है।
        </div>
    </div>
    <div class="list-group">
        <div class="list-group-item list-group-item-action py-3">
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1 text-primary">नया आवंटन प्राप्त हुआ (Source: HQ Patna)</h5>
                <small class="text-muted">आज</small>
            </div>
            <p class="mb-1">मद संख्या 2235 के अंतर्गत आंगनबाड़ी मानदेय हेतु राशि आवंटित कर दी गई है। कृपया ऑलॉटमेंट एंट्री चेक करें।</p>
        </div>
        <div class="list-group-item list-group-item-action py-3">
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">बजट कोड वाइज रिपोर्ट अपडेटेड</h5>
                <small class="text-muted">2 दिन पहले</small>
            </div>
            <p class="mb-1">गूगल शीट सिंक को पूरी तरह से दुरुस्त कर दिया गया है। रिपोर्ट टैब लाइव है।</p>
        </div>
    </div>
</div>
{% endblock %}
"""

# --- 3. SERVICE PAGE (4 Tabs for Reports & Entries) ---
SERVICE_HTML = """
{% extends "base" %}
{% block content %}
<div class="card card-custom p-4 bg-white">
    <h3 class="mb-4 text-primary border-bottom pb-2"><i class="fa-solid fa-gears me-2"></i>मुख्य सेवाएं एवं प्रविष्टियां</h3>
    
    <!-- 4 मुख्य टैब्स -->
    <ul class="nav nav-tabs mb-4" id="serviceTabs" role="tablist">
        <li class="nav-item"><a class="nav-link active" id="report-tab" data-bs-toggle="tab" href="#report" role="tab">1. Report</a></li>
        <li class="nav-item"><a class="nav-link" id="expenditure-tab" data-bs-toggle="tab" href="#expenditure" role="tab">2. Expenditure Entry</a></li>
        <li class="nav-item"><a class="nav-link" id="allotment-tab" data-bs-toggle="tab" href="#allotment" role="tab">3. Allotment Entry</a></li>
    </ul>

    <div class="tab-content" id="serviceTabsContent">
        <!-- 1. REPORT TAB -->
        <div class="tab-pane fade show active" id="report" role="tabpanel">
            <h4 class="text-secondary mb-3">वित्तीय रिपोर्ट गैलरी</h4>
            <div class="row g-3">
                <div class="col-md-6">
                    <div class="p-3 border rounded bg-light">
                        <h5>1. Expenditure Report (ALL Bill)</h5>
                        <p class="text-muted small">कुल खर्च किए गए सभी बिलों की विस्तृत सूची।</p>
                        <button class="btn btn-sm btn-outline-primary">देखें</button>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="p-3 border rounded bg-light">
                        <h5>2. Expenditure Budget Code-wise</h5>
                        <p class="text-muted small">बजट कोड के अनुसार कुल व्यय का विवरण।</p>
                        <button class="btn btn-sm btn-outline-primary">देखें</button>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="p-3 border rounded bg-light">
                        <h5>3. Total Balance Budget Code-wise</h5>
                        <p class="text-muted small">किस कोड में कितना बैलेंस बचा है (आवंटन - व्यय)।</p>
                        <button class="btn btn-sm btn-outline-success">बैलेंस देखें</button>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="p-3 border rounded bg-light">
                        <h5>4. Total Balance ALL</h5>
                        <p class="text-muted small">कार्यालय का संचित कुल शेष बजट विवरण।</p>
                        <button class="btn btn-sm btn-outline-success">समरी देखें</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. EXPENDITURE ENTRY TAB -->
        <div class="tab-pane fade" id="expenditure" role="tabpanel">
            <h4 class="text-danger mb-3">व्यय प्रविष्टि (Expenditure Entry)</h4>
            <form action="/submit-expenditure" method="POST">
                <div class="row g-3">
                    <div class="col-md-6"><label class="form-label">1. Order No.</label><input type="text" name="order_no" class="form-control" required></div>
                    <div class="col-md-6"><label class="form-label">2. Date</label><input type="date" name="date" class="form-control" required></div>
                    <div class="col-md-6"><label class="form-label">3. Budget Head</label><input type="text" name="budget_head" class="form-control" placeholder="उदा: 2235" required></div>
                    <div class="col-md-6"><label class="form-label">4. Unit Head</label><input type="text" name="unit_head" class="form-control" required></div>
                    <div class="col-md-4"><label class="form-label">5. Mad (मद)</label><input type="text" name="mad" class="form-control" required></div>
                    <div class="col-md-4"><label class="form-label">6. Amount (राशि ₹)</label><input type="number" name="amount" class="form-control" required></div>
                    <div class="col-md-4"><label class="form-label">7. Remarks</label><input type="text" name="remarks" class="form-control"></div>
                </div>
                <button type="submit" class="btn btn-danger mt-4 w-100"><i class="fa-solid fa-floppy-disk me-2"></i>व्यय डेटा सेव करें</button>
            </form>
        </div>

        <!-- 3. ALLOTMENT ENTRY TAB -->
        <div class="tab-pane fade" id="allotment" role="tabpanel">
आवंटन प्रविष्टि (Allotment Entry)


1. Source (स्रोत)
2. Order No.
3. Budget Head
4. Unit Code
5. Amount (प्राप्त राशि ₹)
6. Remark

आवंटन डेटा सेव करें




{% endblock %}
"""

--- 4. ABOUT ME PAGE ---

ABOUT_HTML = """
{% extends "base" %}
{% block content %}

Rudra Tech Pvt Ltd
हम सरकारी कार्यालयों और व्यवसायों के लिए उच्च गुणवत्ता वाले सॉफ्टवेयर और डिजिटल टूल्स का निर्माण करते हैं।

हमारे सोशल साइट्स से जुड़ें:

WhatsApp
Facebook
LinkedIn


{% endblock %}
"""

--- 5. CONTACT US PAGE ---

CONTACT_HTML = """
{% extends "base" %}
{% block content %}

Contact Us (एडमिन को सन्देश भेजें)

आपका नाम
विषय (Subject)
सन्देश बॉक्स (Message Box)
डायरेक्ट मैसेज भेजें


{% endblock %}
"""

--- URL ROUTING (राउट्स) ---

@app.route('/')
def home():
return render_template_string(BASE_TEMPLATE + HOME_HTML, active_page='home')
@app.route('/notice')
def notice():
return render_template_string(BASE_TEMPLATE + NOTICE_HTML, active_page='notice')
@app.route('/service')
def service():
return render_template_string(BASE_TEMPLATE + SERVICE_HTML, active_page='service')
@app.route('/about')
def about():
return render_template_string(BASE_TEMPLATE + ABOUT_HTML, active_page='about')
@app.route('/contact')
def contact():
return render_template_string(BASE_TEMPLATE + CONTACT_HTML, active_page='contact')

--- फॉर्म सबमिशन हैंडल्स (डेटा रिसीव करने के लिए) ---

@app.route('/submit-expenditure', methods=['POST'])
def submit_expenditure():
# यहाँ पर हम आगे गूगल शीट का कोड जोड़ेंगे
print(request.form)
return "व्यय (Expenditure) डेटा प्राप्त हुआ! गूगल शीट सेटअप के बाद यह वहाँ दिखने लगेगा।वापस जाएं"
@app.route('/submit-allotment', methods=['POST'])
def submit_allotment():
print(request.form)
return "आवंटन (Allotment) डेटा प्राप्त हुआ! गूगल शीट सेटअप के बाद यह वहाँ दिखने लगेगा।वापस जाएं"
@app.route('/submit-contact', methods=['POST'])
def submit_contact():
print(request.form)
return "आपका सन्देश एडमिन को भेज दिया गया है!वापस जाएं"
if name == 'main':
app.run(debug=True)
