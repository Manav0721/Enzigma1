import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import mysql.connector
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure MySQL database
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '0721',
    'database': 'onboarding'
}

# Initialize database table
def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        email VARCHAR(255),
                        phone VARCHAR(20)
                      )''')
    conn.commit()
    conn.close()

init_db()

# OCR processing function
def extract_text(file_path):
    if file_path.endswith('.pdf'):
        images = convert_from_path(file_path)
        text = ''
        for image in images:
            text += pytesseract.image_to_string(image)
    elif file_path.endswith(('.png', '.jpg', '.jpeg')): 
        text = pytesseract.image_to_string(Image.open(file_path))
    else:
        text = ''
    return text

# Parse text to extract candidate details (basic example)
def parse_details(text):
    lines = text.split('\n')
    details = {}
    for line in lines:
        if 'Name:' in line:
            details['name'] = line.split('Name:')[1].strip()
        elif 'Email:' in line:
            details['email'] = line.split('Email:')[1].strip()
        elif 'Phone:' in line:
            details['phone'] = line.split('Phone:')[1].strip()
    return details

# Save candidate details to database
def save_to_db(details):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO candidates (name, email, phone) VALUES (%s, %s, %s)''',
                   (details.get('name'), details.get('email'), details.get('phone')))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files part'}), 400

    files = request.files.getlist('files[]')
    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the uploaded file
        text = extract_text(file_path)
        details = parse_details(text)
        if details:
            save_to_db(details)

    # Fetch all records after processing
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM candidates')
    records = cursor.fetchall()
    conn.close()

    # Render the success page with the records
    return render_template('upload_success.html', records=records)

@app.route('/records', methods=['GET'])
def get_records():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM candidates')
    records = cursor.fetchall()
    conn.close()

    # Render the records page with dynamic data
    return render_template('view_records.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
