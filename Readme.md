# AttendanceHub

---

## Overview

**AttendanceHub** is an API service designed for managing staff attendance, shifts, and rosters. It provides functionality for marking attendance, managing shifts, and tracking staff details. The system supports roles for managers and staff members, ensuring secure and efficient management of employee schedules and attendance.

## Features

- **Authentication & Authorization**: 
  - Managers can create, edit, and view rosters.
  - Staff can mark their attendance and view their shifts.

- **Roster Management**:
  - Managers can add new staff members, set working days and shifts, and set weekly offs.
  - Staff can interchange shifts among themselves.

- **Attendance Management**:
  - Staff can mark attendance by uploading an image within their shift timings.


## Project Tree Structure

```bash
AttendanceHub/
├── apps/
│   ├── accounts/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── decorators.py
│   │   ├── managers.py
│   │   ├── models.py
│   │   ├── queries.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   └── views.py
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── serializers.py
│   │       ├── urls.py
│   │       └── views.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   └── views.py
│   ├── attendance/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── queries.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── validations.py
│   │   └── views.py
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── serializers.py
│   │       ├── urls.py
│   │       └── views.py
│   └── authentication/
│       ├── __init__.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   ├── wsgi/
│   │   ├── dev.py
│   │   └── prod.py
│   └── settings/
│       ├── base.py
│       ├── dev.py
│       └── prod.py
├── exception/
│   ├── auth.py
│   ├── base.py
│   └── restapi.py
├── helper/
│   ├── __init__.py
│   ├── constant.py
│   ├── id_generator.py
│   ├── serializers.py
│   └── validation.py
├── schema/
│   ├── __init__.py
│   ├── request.py
├── scripts/
├── .gitignore
├── README.md
├── manage-dev.py
├── manage-prod.py
└── requirements.txt
```



## Setup

### Requirements

- Python 3.10+
- Django
- DjangoRestFramework
- DjangoRestFramework-SimpleJWT
- Pillow

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/codeWithAftab/AttendanceHubApi.git
   cd AttendanceHubApi

2. Create a virtual environment using `virtualenv`:
   ```bash
   pip install virtualenv
   virtualenv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the requirements:
   ```bash
   pip install -r requirements.txt

# API Documentation

## Register User (Manager)

- **Endpoint:** `/api/v1/accounts/user/register/`
- **Method:** `POST`
- **Authentication:** None
- **Request Body:**
  ```json
 {
    "first_name": "string",   // required
    "last_name": "string",    // optional
    "image": "file",          // optional
    "email": "string",        // required
    "password": "string",     // required
    "role": "string"          // optional
  }

