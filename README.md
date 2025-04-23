# 🔐 Secure File Sharing Platform

A collaborative course project built with **Django**, this web app allows users to upload, encrypt, share, and manage files securely. Designed to simulate real-world file security workflows, it leverages cryptography to store sensitive content safely and enables sharing with access control.

---

### **Live Demo**

- **Frontend + Backend (Render):** [https://sfh-web.onrender.com](https://sfh-web.onrender.com)

---

### **Key Features**

- **User Registration & Login:** Authenticate securely with built-in Django auth.
- **Encrypted Uploads:** Files are encrypted using Fernet (AES) before being stored.
- **Secure Downloads:** Only the uploader or shared users can decrypt and download.
- **File Previews:** Inline preview support for images, PDFs, text, and videos.
- **Access Control:** Share files with selected registered users.
- **PostgreSQL Integration:** Persistent database powered by Render PostgreSQL.
- **Admin Dashboard:** Django admin enabled for managing users and files.

---

### **Technology Stack**

| Layer       | Tools / Frameworks                              |
|-------------|--------------------------------------------------|
| Backend     | Django (Python), Django ORM, PostgreSQL          |
| Security    | cryptography (Fernet encryption), session-based auth |
| Frontend    | Django Templates with custom CSS                 |
| Hosting     | Render (free tier for web service + database)    |

---

### **Getting Started**

#### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/secure-file-sharing.git
cd secure-file-sharing
```

#### **2. Setup Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### **3. Configure Environment**
Create a `.env` file at the root:
```env
DEBUG=True
SECRET_KEY=your-django-secret-key
ENCRYPTION_KEY=your-base64-fernet-key
MAX_FILE_SIZE_MB=20
DATABASE_URL=sqlite:///db.sqlite3  # or your PostgreSQL URL
```

#### **4. Run Migrations and Start Server**
```bash
python manage.py migrate
python manage.py runserver
```

---

### **App Overview**

| Route               | Description                                       |
|--------------------|---------------------------------------------------|
| `/`                | Homepage                                          |
| `/register/`       | User registration                                |
| `/login/`          | User login                                       |
| `/upload/`         | Upload encrypted files                           |
| `/dashboard/`      | View uploaded and shared files                   |
| `/share/<id>/`     | Share file with other users                      |
| `/share-multiple/` | Share multiple files with a selected user        |
| `/preview/<id>/`   | Preview decrypted content (if allowed)           |
| `/download/<id>/`  | Download and decrypt file                        |

---

### **HTML Template Breakdown**

| File                  | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `home.html`           | Landing page of the site (publicly accessible)                         |
| `login.html`          | Login form for registered users                                        |
| `register.html`       | Registration form with validations                                     |
| `file_dashboard.html` | Main user dashboard — shows uploaded/shared files                      |
| `upload.html`         | Upload page with file encryption + preview logic                       |
| `share.html`          | Used when sharing an individual file from the dashboard                |
| `share_multiple.html` | Bulk sharing of multiple files with a selected user                    |
| `nav.html`            | Reusable navigation bar — included across pages via `{% include %}`    |

---

## 📸 UI Previews

### **Home Page**
![Home Page](https://github.com/miashub/file-sharing/blob/c73db836bb737936fb8bd54538f6a795df72ca75/screenshots/home.png)

---

### **File Dashboard**
![File Dashboard](https://raw.githubusercontent.com/miashub/secure_file_sharing/main/screenshots/file%20dashboard.png)

---

### **Single File Share Screen**
![Single File to Many](https://raw.githubusercontent.com/miashub/secure_file_sharing/main/screenshots/selected%20one%20file%20to%20many.png)

---

### **Bulk Share Page**
![Share with Many](https://raw.githubusercontent.com/miashub/secure_file_sharing/main/screenshots/share%20with%20many.png)

---

### **Upload File Page**
![Upload File](https://raw.githubusercontent.com/miashub/secure_file_sharing/main/screenshots/upload%20file.png)

---

### **Deployment Notes (Render)**

- Make sure `gunicorn` is installed and added to `requirements.txt`
- Set root directory to the folder where `manage.py` exists
- Add environment variables in Render Dashboard:
  - `DEBUG=False`
  - `SECRET_KEY=...`
  - `ENCRYPTION_KEY=...`
  - `DATABASE_URL=...` (from Render PostgreSQL)

---

### **Team & Contribution**

This was a final course project built collaboratively by:
- Mia Shajahan (@miashub)
- Classmate(s) [Name, GitHub if applicable]

To contribute:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

---

### **License**

This project is licensed under the **MIT License** — free to use, modify, and distribute for educational purposes.

---

### **Contact**

- **Email:** [fathimas0207.email@example.com](mailto:fathimas0207.email@example.com)  
- **GitHub:** [github.com/miashub](https://github.com/miashub)  
- **LinkedIn:** [linkedin.com/in/mia-shajahan](https://linkedin.com/in/mia-shajahan)

