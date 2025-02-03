# Household Services Application - V2

## Overview

Household Services Application is a **multi-user platform** that connects **customers** with **service professionals** for home maintenance and repairs. The application allows **admins** to manage services, professionals, and customers efficiently.

This project is built using:

- **Flask** for backend API
- **Vue.js** for frontend UI
- **SQLite** for data storage
- **Redis & Celery** for caching and background jobs
- **Bootstrap** for styling

---

## Features

### 🔹 **User Roles**

1. **Admin** (Superuser)

   - Manages users and services
   - Approves service professionals
   - Blocks fraudulent users
   - Monitors service requests

2. **Service Professional**

   - Accepts/rejects service requests
   - Provides services to customers

3. **Customer**
   - Searches & books services
   - Posts reviews & remarks
   - Manages service requests

---

### 🔹 **Core Functionalities**

- **Authentication & Role-Based Access (RBAC)**
  - Admin, professional, and customer logins
  - Token based authentication
- **Admin Dashboard**
  - Manage users, approve professionals, block/unblock accounts
- **Service Management (Admin)**

  - Create, update, delete services

- **Service Requests (Customer)**

  - Book, edit, and close service requests

- **Professional Actions**

  - Accept/reject assigned requests
  - Close requests after completion

---

### 🔹 **Backend Jobs**

- **Scheduled Jobs**

  - **Daily Reminders**: Notify professionals of pending requests (via Google Chat, SMS, or Email)
  - **Monthly Reports**: Summarize activities for customers (via email)

- **User-Triggered Async Jobs**
  - **Export Closed Service Requests** (CSV)

---

## Technologies Used

| Component       | Technology     |
| --------------- | -------------- |
| Backend         | Flask          |
| Frontend        | Vue.js         |
| Database        | SQLite         |
| Caching         | Redis          |
| Batch Jobs      | Redis & Celery |
| Styling         | Bootstrap      |
| Auth            | Flask-Security |
| Background Jobs | Celery         |

---

<!-- ## Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-repo/household-services-app.git
cd household-services-app
``` -->
