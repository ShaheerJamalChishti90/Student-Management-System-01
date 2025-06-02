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

# Translation dictionary
translations = {
    'en': {
        'already_registered_subtitle': 'You have already been registered today.',
        'switch_en': 'English',
        'switch_es': 'Español',
        'today_logs': "Today's Logs",
        'download_excel': 'Download Excel',
        'clear_logs': 'Clear Logs',
        'confirm_clear': 'Are you sure you want to clear all logs?',
        'no_logs': 'No attendance logs found.',
        'edit_settings': 'Edit Settings',
        'back_to_login': 'Back to Login',
        'back_to_top': 'Back to Top'
    },
    'es': {
        'already_registered_subtitle': 'Ya te has registrado hoy.',
        'switch_en': 'English',
        'switch_es': 'Español',
        'today_logs': 'Registros de Hoy',
        'download_excel': 'Descargar Excel',
        'clear_logs': 'Borrar Registros',
        'confirm_clear': '¿Estás seguro de borrar todos los registros?',
        'no_logs': 'No se encontraron registros.',
        'edit_settings': 'Editar Configuración',
        'back_to_login': 'Volver al Inicio',
        'back_to_top': 'Volver Arriba'
    }
}

# Helper: Load settings
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {
            "enable_question_1": True,
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
    lang = request.args.get('lang', 'en')
    t = translations.get(lang, translations['en'])
    settings = load_settings()

    # Always allow visiting /index
    return render_template('form.html', settings=settings, t=t, lang=lang)


@app.route('/submit', methods=['POST'])
def submit():
    lang = request.args.get('lang', 'en')
    t = translations.get(lang, translations['en'])
    settings = load_settings()

    name = request.form.get('name', '').strip()
    lastname = request.form.get('lastname', '').strip()
    q1 = request.form.get('question1', '').strip() if settings['enable_question_1'] else ''
    q2 = request.form.get('question2', '').strip() if settings['enable_question_2'] else ''

    if not name or not lastname:
        return "Full Name and Last Name are required", 400

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    today_file = get_today_excel_filename()

    try:
        if os.path.exists(today_file):
            df_old = pd.read_excel(today_file)

            # Check for duplicate by name + last name
            match_found = ((df_old['Name'] == name) & (df_old['Last Name'] == lastname)).any()
            if match_found:
                session['duplicate_attempt'] = True
                session['phone_number'] = q1
                session['name'] = name
                session['lastname'] = lastname
                return redirect(url_for('already_logged_in', lang=lang))

        new_data = {
            'Name': name,
            'Last Name': lastname
        }

        if settings['enable_question_1']:
            q1_label = settings.get("question_1_label", "Question 1")
            new_data[q1_label] = q1

        if settings['enable_question_2']:
            q2_label = settings.get("question_2_label", "Question 2")
            new_data[q2_label] = q2

        new_data['Timestamp'] = timestamp

        if os.path.exists(today_file):
            df_old = pd.read_excel(today_file)
            df_new = pd.DataFrame([new_data])
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_combined = pd.DataFrame([new_data])

        df_combined.to_excel(today_file, index=False)

        session.pop('duplicate_attempt', None)
        session['phone_number'] = q1
        session['name'] = name
        session['lastname'] = lastname

    except Exception as e:
        print("Error saving data:", e)
        return "System error: Failed to save attendance", 500

    return redirect(url_for('success', lang=lang))


@app.route('/success')
def success():
    lang = request.args.get('lang', 'en')
    settings = load_settings()
    return render_template('success.html', settings=settings, lang=lang)


@app.route('/already_logged_in')
def already_logged_in():
    lang = request.args.get('lang', 'en')
    t = translations.get(lang, translations['en'])
    settings = load_settings()
    if not session.get('duplicate_attempt'):
        return redirect(url_for('index', lang=lang))
    
    full_name = session.get('name', '') + ' ' + session.get('lastname', '')
    if full_name.strip():
        t['already_registered_subtitle'] += f" ({full_name})"

    return render_template('already_logged_in.html', settings=settings, t=t, lang=lang)


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

    lang = request.args.get('lang', 'en')
    t = translations.get(lang, translations['en'])
    settings = load_settings()
    return render_template('admin_settings.html', settings=settings, t=t, lang=lang)


@app.route('/admin/logs')
def view_logs():
    lang = request.args.get('lang', 'en')
    t = translations.get(lang, translations['en'])
    settings = load_settings()
    today_file = get_today_excel_filename()

    if not os.path.exists(today_file):
        return render_template('admin_logs.html', headers=[], logs=[], settings=settings, t=t, lang=lang)

    try:
        df = pd.read_excel(today_file)
        headers = list(df.columns)
        logs = df.to_dict(orient='records')
    except Exception as e:
        print("Error loading logs:", e)
        headers = []
        logs = []

    return render_template('admin_logs.html', headers=headers, logs=logs, settings=settings, t=t, lang=lang)

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