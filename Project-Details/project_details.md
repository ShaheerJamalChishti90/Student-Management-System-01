<h3 style="color: red;">ITS RECOMMENDED TO INSTALL THE EXTENSION: "MARKDOWN PREVIEW ENHANCED" TO VIEW THIS MARKDOWN FILE IN A READABLE MANNER</h3>
<hr>

# How to setup files to run the application
1. Make the root folder where you will place all these files and folders
2. Now create two new folders in this root folder, name them templates and static
3. Now place all the HTML files inside the **templates folder**
4. Place the `logo.png` in the **static folder**
5. Create a new folder named `logs` in the root directory
6. Leave app.py and settings.json files there in the root directory because they are the backend files

> **NOTE: YOU CAN SEE THE FOLDER STRUCTURE BELOW, IT WILL HELP YOU IN PLACING IN YOUR FILES IN THE RIGHT FOLDER**

---
# Project Folder Structure
```
attendance_app/     #Folder
│
├── app.py                  ← Main Flask File
├── Procfile                  ← File to run the flask app live
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
```
---
# Project Pages Links

 1. **Login Page Link - This is the main link for the Attendance Login Page: 
 ```https://attendance-management-system-bcd2ebcee7e6e6d0.canadacentral-01.azurewebsites.net```**
<hr style="background-color: yellow;">

 2. **Admin Logs Page Link - This link is used to access the Admin Logs Panle:
```https://attendance-management-system-bcd2ebcee7e6e6d0.canadacentral-01.azurewebsites.net/admin/logs```**
 <hr style="background-color: yellow;">

 3. **Admin Settings Page Link - This link is used to access the Admin Settings Panel: 
 ```https://attendance-management-system-bcd2ebcee7e6e6d0.canadacentral-01.azurewebsites.net/admin/settings```**
<hr>

# Login Page Access URL

This is the Microsoft Azure URL of the Attendance Submission Page
<img src="/Project-Details/Login Scan.png" width="150px" height="150px"></img>
<hr>

#  How This Attendance System Works?

1. **Student Login Page**  
   Students are directed to the attendance login page via a specific URL.

2. **Entering Student Information**  
   On the login page, students answer a set of questions (e.g., name, student ID, class, etc.) as required.

3. **Daily Excel Log File**  
   All submitted information is saved in an **Excel file** that is automatically created at the start of each day.  
   Only **one Excel file** is generated per day.

4. **Attendance Records**  
   Each student’s responses are recorded in the daily Excel file with their answers to the questions.

5. **Daily Reset**  
   After 24 hours (i.e., the next day), the system resets.  
   Students can submit their attendance again for the new day.

6. **No Duplicate Entries**  
   The system **does not allow duplicate submissions from the same student on the same day**.  
   If a student tries to submit again, they will be redirected to a page indicating that their attendance has already been recorded for the day.

7. **Admin Panel – View Logs**  
   The admin can access a dedicated panel to:
   - View all student attendance records for the current day.
   - Download the daily Excel file.
   - Clear all logs for the day if needed.

8. **Admin Settings Panel**  
   This section allows the admin to customize the appearance and settings of the main attendance login page, including:
   - Changing headings and subheadings.
   - Enabling or disabling specific questions.
