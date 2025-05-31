# Project Folder Structure
---
```
attendance_app/     #Folder
│
├── app.py                  ← Main Flask File
├── requirements.txt        ← Contains the requirmenets/Packages and Libraries
├── settings.json           ← Will be auto-created
├── static/         #Folder
│   └── logo.png          ← Logo
├── logs/           #Folder
│   └── attendance_'date'.xlxs      ← Will be auto-created
└── templates/      #Folder
    ├── form.html
    ├── success.html
    ├── already_logged_in.html
    ├── admin_settings.html
    ├── admin_logs.html
    └── error.html
```
---
# Project Pages Links

 1. **Login Page Link: ```<a href="{{ url_for('index') }}"</a>```**
 2. **Admin Logs Page Link: ```<a href="/admin/logs">Admin Logs</a>```**
 3. **Admin Settings Page Link: ```<a href="admin/settings">Admin Settings</a>```**