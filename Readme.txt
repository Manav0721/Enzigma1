Project: File Upload and Candidate Details Extraction

This project is a web-based application for uploading files (PDFs or images), extracting text using Optical Character Recognition (OCR), and parsing candidate details (name, email, phone) to save them in a MySQL database. The project also allows viewing the saved candidate records.

Features
- Upload multiple files (PDFs or images) through a web interface.
- Extract text from uploaded files using OCR (pytesseract).
- Parse candidate details from the extracted text.
- Store candidate details (name, email, phone) in a MySQL database.
- View all saved candidate records through a web interface.

---

Prerequisites

Before running this project, ensure the following are installed:
1. Python 2.x
2. Flask
3. pytesseract
4. pdf2image
5. Pillow
6. MySQL server

Install Python Dependencies
Run the following command to install required Python libraries:
```bash
pip install flask mysql-connector-python pytesseract pdf2image pillow
```

Install Tesseract OCR
Follow the instructions for your operating system:
- Ubuntu/Debian:
  ```bash
  sudo apt update
  sudo apt install tesseract-ocr
  ```
- Windows:
  Download and install from [Tesseract GitHub page](https://github.com/tesseract-ocr/tesseract).

MySQL Configuration
- Install MySQL Server and create a database named `onboarding`.
- Update the `DB_CONFIG` dictionary in `app.py` with your MySQL credentials.

Run the following SQL query to create the `candidates` table:
```sql
CREATE TABLE IF NOT EXISTS candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20)
);
```

---

Project Structure
```
project-directory/
|-- Test1.py                # Flask application code
|-- templates/
|   |-- index.html        # HTML template for the web interface
|-- uploads/              # Directory for storing uploaded files
|-- README.md             # Project documentation
```

---

Instructions to Run the Project

Step 1: Clone or Download the Project
Clone the repository or download the source code to your local machine.

Step 2: Start the Flask Server
Run the following command in the project directory:
```bash
python app.py
```
This will start the server at `http://127.0.0.1:5000/`.

Step 3: Access the Application
Open your browser and navigate to `http://127.0.0.1:5000/` to access the file upload and record viewing interface.

Step 4: Upload Files
1. Use the "Upload Files" section to upload PDFs or images.
2. The application will extract text, parse candidate details, and store them in the database.

Step 5: View Records
Use the "View All Records" section to retrieve and view saved candidate details from the database.

---

Notes
- Ensure that the `uploads/` directory has appropriate write permissions.
- For production, replace `debug=True` in `app.run()` with appropriate production configurations.
- Extend the `parse_details` function in `app.py` to improve parsing logic based on specific document formats.

---

License
This project is open-source 

