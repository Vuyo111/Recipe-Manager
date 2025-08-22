Recipe Manager

A full-stack Python Flask web application to manage recipes with a simple and intuitive interface. This app demonstrates CRUD operations, backend logic, and frontend interaction, making it a great project for a portfolio.

---

Live Demo
[View Live on Render](https://recipe-manager-r8wl.onrender.com)

---

Features:
- **Add recipes** with name and ingredients.
- **Edit recipes** with live updates.
- **Delete recipes** easily.
- **Persistent backend** using Flask with JSON storage.
- **Dynamic frontend** with JavaScript DOM manipulation.
- **Responsive design** and user-friendly interface.

---

Technologies Used:
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask, Flask-CORS
- **Deployment:** Render
- **Version Control:** Git & GitHub

---

Getting Started (Local Setup)

1. **Clone the repo*
```bash
git clone https://github.com/Vuyo111/recipe-manager.git
cd recipe-manager

2. **Create a virtual environment**
python -m venv venv

3. **Activate the virtual environment**

Windows:
venv\Scripts\activate

macOS/Linux:

source venv/bin/activate


4. Install dependencies

pip install -r requirements.txt


5. Run the app

python app.py


6. Open in browser

http://127.0.0.1:5000

Project Structure:
/recipe-manager
│
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
├── /templates
│   └── index.html          # Frontend HTML
├── /static
│   ├── script.js           # Frontend JavaScript
│   └── styles.css          # Frontend styling

How it Works:

~The backend (Flask) handles all CRUD operations and serves the frontend.

~The frontend fetches data from the backend using fetch API calls.

~CORS is handled with flask-cors to allow frontend-backend communication.

~Users can add, edit, delete, and view recipes dynamically without refreshing the page.

Deployment:

The app is deployed on Render, making it accessible online.
You can view it here: https://recipe-manager-r8wl.onrender.com

Author

Ondela T. Passionate full-stack developer building dynamic, practical web applications.
