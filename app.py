from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- 1. BASE STRUCTURE (मोबाइल के लिए 100% फिट) ---
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Rudra Tech - ICDS Budget App</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://jsdelivr.net" rel="stylesheet">
    <!-- FontAwesome Logos -->
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        html, body { 
            width: 100%;
            overflow-x: hidden; /* स्क्रीन को दाएं-बायें हिलने से रोकने के लिए */
            background-color: #f8f9fa; 
            font-family: sans-serif; 
            padding-bottom: 80px; 
        }
        .navbar-custom { background-color: #2c3e50; width: 100%; }
        .card-custom { border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: none; margin-bottom: 20px; }
        
        /* मोबाइल रिस्पॉन्सिव बॉटम नेविगेशन बार */
        .bottom-nav { 
            position: fixed; 
            bottom: 0; 
            left: 0; 
            width: 100%; 
            height: 65px; 
            background-color: #ffffff; 
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1); 
            display: flex; 
            justify-content: space-around; 
            align-items: center; 
            z-index: 1050; 
        }
        .bottom-nav a { 
            text-decoration: none; 
            color: #7f8c8d; 
            text-align: center; 
            font-size: 11px; 
            flex-grow: 1;
            padding: 5px 0;
        }
        .bottom-nav a.active { color: #3498db; font-weight: bold; }
        .bottom-nav i { font-size: 22px; display: block; margin-bottom: 3px; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark navbar-custom py-2 shadow-sm mb-3">
        <div class="container-fluid text-center">
            <span class="navbar-brand mb-0 h1 mx-auto" style="font-size: 1.1rem;"><i class="fa-solid fa-calculator me-2"></i>ICDS आवंटन एवं व्यय प्रबंधन</span>
        </div>
    </nav>
    <div class="container-fluid px-3">
        {{ content | safe }}
    </div>
    <div class="bottom-nav">
        <a href="/" class="{% if active == 'home' %}active{% endif %}"><i class="fa-solid fa-house"></i>Home</a>
        <a href="/notice" class="{% if active == 'notice' %}active{% endif %}"><i class="fa-solid fa-bell"></i>Notice</a>
        <a href="/service" class="{% if active == 'service' %}active{% endif %}"><i class="fa-solid fa-gears"></i>Service</a>
        <a href="/about" class="{% if active == 'about' %}active{% endif %}"><i class="fa-solid fa-building"></i>About</a>
        <a href="/contact" class="{% if active == 'contact' %}active{% endif %}"><i class="fa-solid fa-envelope"></i>Contact</a>
    </div>
    <!-- Bootstrap JS -->
    <script src="https://jsdelivr.net"></script>
</body>
</html>
"""

# --- 2. PAGES CONTENT ---
HOME_HTML = """
<div class="row justify-content-center text-center mt-5">
    <div class="col-md-8">
        <div class="card card-custom p-5 bg-white">
            <img src="https://flaticon.com" style="width: 100px;" class="mx-auto mb-4">
            <h1 class="display-5 text-dark fw-bold mb-3">डिजिटल बजट मैनेजर में स्वागत है</h1>
            <p class="lead text-muted">यहाँ से आप ICDS कार्यालय के विभिन्न बजट हेड, आवंटन (Allotment) और व्यय (Expenditure) का लेखा-जोखा प्रबंधित कर सकते हैं।</p>
            <hr class="my-4">
            <a href="/service" class="btn btn-primary btn-lg px-4"><i class="fa-solid fa-play me-2"></i>काम शुरू करें</a>
        </div>
    </div>
</div>
"""

NOTICE_HTML = """
<div class="card card-custom p-4 bg-white">
    <h3 class="text-danger border-bottom pb-2 mb-3"><i class="fa-solid fa-bullhorn me-2"></i>Notice Board</h3>
    <div class="alert alert-warning">
        <strong>महत्वपूर्ण सूचना:</strong> वित्तीय वर्ष के लिए सभी यूनिट हेड का व्यय प्रतिवेदन समय पर जमा करना अनिवार्य है।
    </div>
</div>
"""

SERVICE_HTML = """
<div class="card card-custom p-4 bg-white">
    <h3 class="mb-4 text-primary border-bottom pb-2"><i class="fa-solid fa-gears me-2"></i>सेवाएं एवं प्रविष्टियां</h3>
    <div class="p-3 border rounded bg-light mb-3">
        <h5>1. Allotment Entry</h5>
        <form action="/submit" method="POST">
            <input type="hidden" name="type" value="Allotment">
            <div class="row g-2">
                <div class="col-6"><input type="text" name="f1" placeholder="Source" class="form-control" required></div>
                <div class="col-6"><input type="text" name="f2" placeholder="Order No" class="form-control" required></div>
                <div class="col-4"><input type="text" name="f3" placeholder="Budget Head" class="form-control" required></div>
                <div class="col-4"><input type="text" name="f4" placeholder="Unit Code" class="form-control" required></div>
                <div class="col-4"><input type="number" name="f5" placeholder="Amount" class="form-control" required></div>
            </div>
            <button class="btn btn-success btn-sm mt-2 w-100">आवंटन डेटा सेव करें</button>
        </form>
    </div>
    <div class="p-3 border rounded bg-light">
        <h5>2. Expenditure Entry</h5>
        <form action="/submit" method="POST">
            <input type="hidden" name="type" value="Expenditure">
            <div class="row g-2">
                <div class="col-6"><input type="text" name="f1" placeholder="Order No" class="form-control" required></div>
                <div class="col-6"><input type="date" name="f2" class="form-control" required></div>
                <div class="col-4"><input type="text" name="f3" placeholder="Budget Head" class="form-control" required></div>
                <div class="col-4"><input type="text" name="f4" placeholder="Unit Head" class="form-control" required></div>
                <div class="col-4"><input type="number" name="f5" placeholder="Amount" class="form-control" required></div>
            </div>
            <button class="btn btn-danger btn-sm mt-2 w-100">व्यय डेटा सेव करें</button>
        </form>
    </div>
</div>
"""

ABOUT_HTML = """
<div class="card card-custom p-4 text-center bg-white">
    <h3 class="text-primary mb-3">Rudra Tech Pvt Ltd</h3>
    <p class="text-muted">हम सरकारी कार्यालयों के लिए डिजिटल टूल्स का निर्माण करते हैं।</p>
    <a href="https://wa.me" target="_blank" class="btn btn-success mt-3"><i class="fa-brands fa-whatsapp me-2"></i>WhatsApp Chat</a>
</div>
"""

CONTACT_HTML = """
<div class="card card-custom p-4 bg-white">
    <h3 class="text-primary mb-3">Contact Us</h3>
    <form action="/submit" method="POST">
        <input type="hidden" name="type" value="Contact">
        <div class="mb-2"><input type="text" name="f1" placeholder="आपका नाम" class="form-control" required></div>
        <div class="mb-2"><input type="text" name="f2" placeholder="विषय" class="form-control" required></div>
        <div class="mb-2"><textarea name="f3" placeholder="सन्देश लिखें..." class="form-control" rows="3" required></textarea></div>
        <button class="btn btn-primary w-100">मैसेज भेजें</button>
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
    return f"<h3>डेटा सफलतापूर्वक प्राप्त हुआ (प्रकार: {request.form.get('type')})!</h3><a href='/service' class='btn btn-primary'>वापस जाएं</a>"

if __name__ == '__main__':
    app.run(debug=True)
