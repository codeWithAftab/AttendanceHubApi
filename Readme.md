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
   virtualenv .venv
   source .venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the requirements:
   ```bash
   pip install -r requirements.txt

# API Documentation

## 1. Register User (Manager)

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

* `first_name`: (required) User's first name, max length 20 characters.
* `last_name`: (optional) User's last name, max length 20 characters.
* `image`: (optional) Profile image.
* `email`: (required) User's email address.
* `password`: (required) User's password.
* `role`: (optional) User's role. Possible values are "staff" and "manager". Default is "staff".

* **Response:**
* **Status Code:** `200 OK`
* **Content:**
  ```json
  {
    "data": {
        "uuid": "string",
        "first_name": "string",
        "last_name": "string or null",
        "image": "string or null",
        "email": "string",
        "role": "string",
        "created_on": "string (ISO 8601 date-time)",
        "updated_on": "string (ISO 8601 date-time)"
    }
  }


## 2. Get User Profile

- **Endpoint:** `/api/v1/accounts/user/profile/`
- **Method:** `GET`
- **Authentication:** Required (JWT)
- **Response:**
  - **Status Code:** `200 OK`
  - **Content:**
    ```json
    {
      "status": 200,
      "data": {
        "uuid": "string",
        "first_name": "string",
        "last_name": "string",
        "image": "string",   // URL to the profile image
        "email": "string",
        "role": "string",
        "created_on": "string",  // ISO 8601 date-time string
        "updated_on": "string"   // ISO 8601 date-time string
      }
    }
    ```

## 3. Add New Staff Member

- **Endpoint:** `/api/v1/accounts/staff/add/`
- **Method:** `POST`
- **Authentication:** Required (JWT)
- **Request Body:**
  ```json
  {
    "first_name": "string",   // required
    "last_name": "string",    // optional
    "image": "file",          // optional
    "email": "string",        // required
    "password": "string"      // required
  }
  
* `first_name`: (required) User's first name, max length 20 characters.
* `last_name`: (optional) User's last name, max length 20 characters.
* `image`: (optional) Profile image.
* `email`: (required) User's email address.
* `password`: (required) User's password.

* **Response:**
    * **Status Code:** `200 OK`
    * **Content:**
     ```json
    {
        "data": {
            "uuid": "string",
            "first_name": "string",
            "last_name": "string",
            "image": "string",   // URL to the profile image
            "email": "string",
            "role": "string",
            "created_on": "string",  // ISO 8601 date-time string
            "updated_on": "string"   // ISO 8601 date-time string
          }
    }
    
    
## 4. Get Staff Members Details

- **Endpoint:** `/api/accounts/staff/list/`
- **Method:** `GET`
- **Authentication:** Required (JWT)
 **Response:**
  - **Status Code:** `200 OK`
  - **Content:**
    ```json
    {
      "data": [
        {
          "user": {
            "uuid": "string",
            "first_name": "string",
            "last_name": "string or null",
            "image": "string or null",
            "email": "string",
            "role": "string",
            "created_on": "string (ISO 8601 date-time)",
            "updated_on": "string (ISO 8601 date-time)"
          },
          "employee_id": "string",
          "weekly_off": ["string"] // Array of days of the week
        },
        ...
      ]
    }
    ```
  - `user` object:
    - `uuid`: Unique identifier for the staff member.
    - `first_name`: Staff member's first name.
    - `last_name`: Staff member's last name (can be null).
    - `image`: URL to the staff member's profile image (can be null).
    - `email`: Staff member's email address.
    - `role`: Staff member's role.
    - `created_on`: Timestamp when the staff member was created (ISO 8601 format).
    - `updated_on`: Timestamp when the staff member was last updated (ISO 8601 format).
  - `employee_id`: Unique identifier for the staff member within the system.
  - `weekly_off`: Array of days off for the staff member (e.g., ["sunday", "monday"]).

- **Notes:**
  - The `data` field contains a list of staff member details associated with the authenticated manager.
  - Each staff member entry includes the `user` object with personal and role-related information, as well as `employee_id` and `weekly_off` details.
 
## 5. Update Staff Member Details

- **Endpoint:** `/api/staff/update/`
- **Method:** `PATCH`
- **Authentication:** Required (JWT)
- **Request Body:**
  ```json
  {
    "employee_id": "string",  // required
    "first_name": "string",   // required
    "last_name": "string",    // optional
    "image": "file"           // optional
  }
  
 * `employee_id`: (required) Unique identifier for the staff member.
 * `first_name`: (required) Staff member's first name, max length 20 characters.
 * `last_name`: (optional) Staff member's last name, max length 20 characters.
 * `image`: (optional) Updated profile image.

* **Response:**
  * **Status Code:** `200 OK`
  * **Content:**
    ```json
    {
      "data": {
            "uuid": "string",
            "first_name": "string",
            "last_name": "string",
            "image": "string",   // URL to the profile image
            "email": "string",
            "role": "string",
            "created_on": "string",  // ISO 8601 date-time string
            "updated_on": "string"   // ISO 8601 date-time string
        }
    }
    ```
  * `uuid`: Unique identifier for the staff member.
  * `first_name`: Updated first name of the staff member.
  * `last_name`: Updated last name of the staff member.
  *  `image`:  Profile image url of user.
  * `email`: Staff member's email address.

* **Errors:**
  * **Code:** `MissingFieldError`
    * **Description:** Required fields are missing or invalid.
    * **Response:**
     ```json
    {
          "id": "integer",
          "code": "string",
          "status_code": "integer",
          "detail": "string",
          "description": "string",
          "count": "integer"
    }

      ```
