# Household Services Application - V2

## Overview

Household Services Application is a **multi-user platform** that connects **customers** with **service professionals** for home maintenance and repairs. The application allows **admins** to manage services, professionals, and customers efficiently.

This project is built using:

-   **Flask** for backend API
-   **Vue.js** for frontend UI
-   **SQLite** for data storage
-   **Redis & Celery** for caching and background jobs
-   **Bootstrap** for styling

---

## Project Organization

-   **Backend**:  
    Contains REST API definitions in `resources.py` and database models in `models.py`. It implements authentication, authorization, and role-based access control (RBAC), sets up email notifications and asynchronous jobs with Celery and Redis, and integrates Google Spaces webhooks.
-   **Frontend**:  
    Developed using Vue.js, the frontend features a structured `src` folder containing various components and views. Pinia is used for state management, and Bootstrap ensures a responsive design.

## Installation & Setup

### Clone the Repository

```bash
git clone https://github.com/your-repo/household-services-app.git
cd household-services-app
```

### Activate virtual environment and start backend

```bash
cd household-services-app/backend
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

### Install node modules

```bash
cd household-services-app/frontend
npm install
npm run dev
```

### Start Redis server

```bash
redis-server
```

### Start MailHog

```bash
~/go/bin/MailHog
```

### Start Celery worker

```bash
celery -A app.celery worker --loglevel INFO
```

### Start Celery beat

```bash
celery -A app.celery beat --loglevel INFO
```
