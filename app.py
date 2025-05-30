from flask import Flask, request, render_template, redirect, session, send_file, url_for
from datetime import datetime
import os
import json
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

SETTINGS_FILE = 'settings.json'
LOGS_DIR = 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

# Helper: Load settings
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {
            "page_title": "Attendance Login",
            "subtitle": "Please log in below",
            "logo_url": "",
            "form_name_label": "Full Name",
            "enable_question_1": True,
            "question_1_label": "Student ID",
            "enable_question_2": False,
            "question_2_label": "Department",
            "submit_button_label": "Log In",
            "form_enabled": True
        }
    with open(SETTINGS_FILE, 'r') as f:
        return json.load(f)

# Helper: Save settings
def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# Helper: Get today's Excel file path
def get_today_excel_filename():
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"attendance_{today}.xlsx"
    return os.path.join(LOGS_DIR, filename)


@app.route('/')
def index():
    settings = load_settings()
    student_id = session.get('student_id')
    today_file = get_today_excel_filename()

    # Check if already logged in today
    if student_id and os.path.exists(today_file):
        try:
            df = pd.read_excel(today_file)
            if student_id in df['Student ID'].values:
                return render_template('already_logged_in.html', settings=settings)
        except Exception as e:
            print("Error reading Excel:", e)

    return render_template('form.html', settings=settings)


@app.route('/submit', methods=['POST'])
def submit():
    settings = load_settings()
    name = request.form.get('name', '').strip()
    student_id = request.form.get('question1', '').strip()  # Student ID is Question 1
    q2 = request.form.get('question2', '').strip()

    if not name or not student_id:
        return "Full Name and Student ID are required", 400

    today_file = get_today_excel_filename()
    timestamp = datetime.now().strftime('%Y-%m-%d')

    new_data = {
        'Student ID': student_id,
        'Name': name,
        'Question 2': q2 if settings['enable_question_2'] else '',
        'Timestamp': timestamp
    }

    # Try to read existing data
    if os.path.exists(today_file):
        try:
            df_old = pd.read_excel(today_file, dtype={'Student ID': str})
            if student_id in df_old['Student ID'].values:
                session['duplicate_attempt'] = True
                return redirect(url_for('already_logged_in'))
        except Exception as e:
            print("Error during duplicate check:", e)
            return "System error: Could not verify attendance", 500

    # Proceed with saving new entry
    try:
        if os.path.exists(today_file):
            df_old = pd.read_excel(today_file)
            df_new = pd.DataFrame([new_data])
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_combined = pd.DataFrame([new_data])

        df_combined.to_excel(today_file, index=False)
        session['student_id'] = student_id
        session.pop('duplicate_attempt', None)

    except Exception as e:
        print("Error saving data:", e)
        return "System error: Failed to save attendance", 500

    return redirect(url_for('success'))


@app.route('/success')
def success():
    settings = load_settings()
    return render_template('success.html', settings=settings)


@app.route('/already_logged_in')
def already_logged_in():
    settings = load_settings()
    if not session.get('duplicate_attempt'):
        return redirect(url_for('index'))
    return render_template('already_logged_in.html', settings=settings)


# === ADMIN PANEL ===

@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    if request.method == 'POST':
        updated = {
            "page_title": request.form.get("page_title"),
            "subtitle": request.form.get("subtitle"),
            "logo_url": request.form.get("logo_url"),
            "form_name_label": request.form.get("form_name_label"),
            "enable_question_1": 'enable_question_1' in request.form,
            "question_1_label": request.form.get("question_1_label"),
            "enable_question_2": 'enable_question_2' in request.form,
            "question_2_label": request.form.get("question_2_label"),
            "submit_button_label": request.form.get("submit_button_label"),
            "form_enabled": 'form_enabled' in request.form
        }
        save_settings(updated)
        return redirect(url_for('admin_settings'))

    settings = load_settings()
    return render_template('admin_settings.html', settings=settings)


@app.route('/admin/logs')
def view_logs():
    settings = load_settings()
    today_file = get_today_excel_filename()
    if not os.path.exists(today_file):
        return render_template('admin_logs.html', headers=[], logs=[], settings=settings)

    try:
        df = pd.read_excel(today_file)
        headers = df.columns.tolist()
        logs = df.to_dict(orient='records')
    except Exception as e:
        print("Error loading logs:", e)
        headers = []
        logs = []

    return render_template('admin_logs.html', headers=headers, logs=logs, settings=settings)


@app.route('/admin/download')
def download_log():
    today_file = get_today_excel_filename()
    if not os.path.exists(today_file):
        return "No log file found", 404
    return send_file(today_file, as_attachment=True)


@app.route('/admin/clear')
def clear_logs():
    today_file = get_today_excel_filename()
    if os.path.exists(today_file):
        os.remove(today_file)
    return redirect(url_for('view_logs'))


if __name__ == '__main__':
    app.run(debug=True)