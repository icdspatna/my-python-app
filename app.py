from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- 1. BASE STRUCTURE (मोबाइल स्क्रीन पर 100% फिट रहने के लिए) ---
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ICDS Budget App</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://jsdelivr.net" rel="stylesheet">
    <!-- FontAwesome Logos -->
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        html, body { 
            width: 100%;
            overflow-x: hidden;
            background-color: #f1f3f6; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            padding-bottom: 80px; 
            margin: 0;
        }
        .navbar-custom { background-color: #2c3e50; color: white; padding: 15px 10px; }
        .card-custom { border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: none; margin-bottom: 15px; }
        
        /* मोबाइल इनपुट बॉक्स को बड़ा और साफ़ दिखाने के लिए */
        .form-control {
            padding: 12px;
            font-size: 15px;
            border-radius: 8px;
            border: 1px solid #ced4da;
            margin-bottom: 10px;
        }
        .form-label { font-weight: 600; color: #34495e; font-size: 14px; margin-bottom: 4px; }
        .btn-custom { padding: 12px; font-weight: bold; border-radius: 8px; font-size: 16px; }

        /* प्रोफेशनल मोबाइल बॉटम बार */
        .bottom-nav { 
            position: fixed; 
            bottom: 0; 
            left: 0; 
            width: 100%; 
            height: 65px; 
            background-color: #ffffff; 
            box-shadow: 0 -3px 10px rgba(0,0,0,0.08); 
            display: flex; 
            justify-content: space-around; 
            align-items: center; 
            z-index: 1050; 
        }
        .bottom-nav a { 
            text-decoration: none; 
            color: #8892b0; 
            text-align: center; 
            font-size: 11px; 
            flex-grow: 1;
        }
        .bottom-nav a.active { color: #3498db; font-weight: bold; }
        .bottom-nav i { font-size: 22px; display: block; margin-bottom: 2px; }
    </style>
</head>
<body>
    <div class="navbar-custom text-center shadow-sm">
        <h5 class="m-0 fw-bold"><i class="fa-solid fa-calculator me-2"></i>ICDS आवंटन एवं व्यय प्रबंधन</h5>
    </div>
    
    <div class="container-fluid px-3 pt-3">
        {{ content | safe }}
    </div>

    <div class="bottom-nav">
        <a href="/" class="{% if active == 'home' %}active{% endif %}"><i class="fa-solid fa-house"></i>Home</a>
        <a href="/notice" class="{% if active == 'notice' %}active{% endif %}"><i class="fa-solid fa-bell"></i>Notice</a>
        <a href="/service" class="{% if active == 'service' %}active{% endif %}"><i class="fa-solid fa-gears"></i>Service</a>
        <a href="/about" class="{% if active == 'about' %}active{% endif %}"><i class="fa-solid fa-building"></i>About</a>
        <a href="/contact" class="{% if active == 'contact' %}active{% endif %}"><i class="fa-solid fa-envelope"></i>Contact</a>
    </div>
</body>
</html>
"""

# --- 2. PAGES CONTENT (100% Mobile View Fit) ---
HOME_HTML = """
<div class="card card-custom p-4 text-center bg-white mt-3">
    <img src="https://flaticon.com" style="width: 80px;" class="mx-auto mb-3">
    <h3 class="fw-bold text-dark mb-2">बजट मैनेजर में आपका स्वागत है</h3>
    <p class="text-muted small">यहाँ से आप ICDS कार्यालय के विभिन्न बजट हेड, आवंटन और व्यय का लेखा-जोखा मोबाइल से ही मैनेज कर सकते हैं।</p>
    <a href="/service" class="btn btn-primary btn-custom w-100 mt-3"><i class="fa-solid fa-play me-2"></i>काम शुरू करें</a>
</div>
"""

NOTICE_HTML = """
<div class="card card-custom p-3 bg-white">
    <h4 class="text-danger border-bottom pb-2 mb-3"><i class="fa-solid fa-bullhorn me-2"></i>Notice Board</h4>
    <div class="alert alert-warning py-2 small">
        <strong>महत्वपूर्ण सूचना:</strong> वित्तीय वर्ष के लिए सभी यूनिट हेड का व्यय प्रतिवेदन समय पर जमा करें।
    </div>
</div>
"""

SERVICE_HTML = """
<div class="card card-custom p-3 bg-white">
    <h4 class="mb-3 text-primary border-bottom pb-2"><i class="fa-solid fa-gears me-2"></i>सेवाएं एवं प्रविष्टियां</h4>
    
    <!-- 1. Allotment Entry Form -->
    <div class="p-3 border rounded bg-light mb-4">
        <h5 class="text-success fw-bold mb-3"><i class="fa-solid fa-circle-plus me-2"></i>1. Allotment Entry</h5>
        <form action="/submit" method="POST">
            <input type="hidden" name="type" value="Allotment">
            
            <label class="form-label">Source (स्रोत)</label>
            <input type="text" name="f1" placeholder="उदा: मुख्यालय पटना" class="form-control" required>
            
            <label class="form-label">Order No.</label>
            <input type="text" name="f2" placeholder="आदेश संख्या दर्ज करें" class="form-control" required>
            
            <label class="form-label">Budget Head</label>
            <input type="text" name="f3" placeholder="उदा: 2235" class="form-control" required>
            
            <label class="form-label">Unit Code</label>
            <input type="text" name="f4" placeholder="यूनिट कोड दर्ज करें" class="form-control" required>
            
            <label class="form-label">Amount (प्राप्त राशि ₹)</label>
            <input type="number" name="f5" placeholder="₹ राशि दर्ज करें" class="form-control" required>
            
            <label class="form-label">Remark</label>
            <input type="text" name="f6" placeholder="टिप्पणी (वैकल्पिक)" class="form-control">
            
            <button class="btn btn-success btn-custom w-100 mt-2">आवंटन डेटा सेव करें</button>
        </form>
    </div>

    <!-- 2. Expenditure Entry Form -->
    <div class="p-3 border rounded bg-light">
        <h5 class="text-danger fw-bold mb-3"><i class="fa-solid fa-file-invoice-dollar me-2"></i>2. Expenditure Entry</h5>
        <form action="/submit" method="POST">
            <input type="hidden" name="type" value="Expenditure">
            
            <label class="form-label">Order No.</label>
            <input type="text" name="f1" placeholder="आदेश संख्या दर्ज करें" class="form-control" required>
            
            <label class="form-label">Date (दिनांक)</label>
            <input type="date" name="f2" class="form-control" required>
            
            <label class="form-label">Budget Head</label>
            <input type="text" name="f3" placeholder="उदा: 2235" class="form-control" required>
            
            <label class="form-label">Unit Head</label>
            <input type="text" name="f4" placeholder="यूनिट हेड का नाम" class="form-control" required>
            
            <label class="form-label">Amount (व्यय राशि ₹)</label>
            <input type="number" name="f5" placeholder="₹ राशि दर्ज करें" class="form-control" required>
            
            <button class="btn btn-danger btn-custom w-100 mt-2">व्यय डेटा सेव करें</button>
        </form>
    </div>
</div>
"""

ABOUT_HTML = """
<div class="card card-custom p-4 text-center bg-white">
    <h3 class="text-primary fw-bold mb-2">Rudra Tech Pvt Ltd</h3>
    <p class="text-muted small">हम सरकारी कार्यालयों के लिए सुरक्षित डिजिटल टूल्स का निर्माण करते हैं।</p>
    <hr>
    <a href="https://wa.me" target="_blank" class="btn btn-success btn-custom w-100 mt-2"><i class="fa-brands fa-whatsapp me-2"></i>WhatsApp Chat</a>
</div>
"""

CONTACT_HTML = """
<div class="card card-custom p-3 bg-white">
    <h4 class="text-primary mb-3">Contact Us</h4>
    <form action="/submit" method="POST">
        <input type="hidden" name="type" value="Contact">
        <label class="form-label">आपका नाम</label>
        <input type="text" name="f1" class="form-control" required>
        <label class="form-label">विषय</label>
        <input type="text" name="f2" class="form-control" required>
        <label class="form-label">सन्देश बॉक्स</label>
        <textarea name="f3" class="form-control" rows="4" placeholder="यहाँ संदेश लिखें..." required></textarea>
        <button class="btn btn-primary btn-custom w-100 mt-2">मैसेज भेजें</button>
    </form>
</div>
"""

# --- 3. ROUTES ---
@app.route('/')
def home():
    return render_template_string(BASE_TEMPLATE, content=HOME_HTML, active='home')

@app.route('/notice')
def notice():
    return render_template_string(BASE_TEMPLATE, content=NOTICE_HTML, active='notice')

@app.route('/service')
def service():
    return render_template_string(BASE_TEMPLATE, content=SERVICE_HTML, active='service')

@app.route('/about')
def about():
    return render_template_string(BASE_TEMPLATE, content=ABOUT_HTML, active='about')

@app.route('/contact')
def contact():
    return render_template_string(BASE_TEMPLATE, content=CONTACT_HTML, active='contact')

@app.route('/submit', methods=['POST'])
def submit():
    return f"<div class='card card-custom p-4 text-center bg-white mt-4'><h3>डेटा सफलतापूर्वक प्राप्त हुआ!</h3><p class='text-muted'>प्रकार: {request.form.get('type')}</p><a href='/service' class='btn btn-primary btn-custom w-100 mt-3'>वापस जाएं</a></div>"

if __name__ == '__main__':
    app.run(debug=True)
