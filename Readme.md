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

## 1. Register User (Manager API)

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

### 2. Obtain JWT Access Token

**Endpoint:**

`POST /api/v1/accounts/user/token/`

**Request Body:**

```json
{
    "email": "hello2@gmail.com",
    "password": "12345678"
}
```

**Description:**

This API endpoint is used to obtain a JWT access token for authentication. You need to provide the user's email and password.

**Response:**

* **Status Code:** `200 OK`
* **Content:**
  ```json
  {
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token"
  }


## 3. Get User Profile (For All type user.)

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

## 4. Add New Staff Member (Manager API)

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
    
    
## 5. Get Staff Members Details

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
 
## 6. Update Staff Member Details. (Manager API)

- **Endpoint:** `/api/v1/accounts/staff/update/`
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

## 7. Assign Staff Shift (Manager API)

- **Endpoint:** `/api/v1/master/staff/shift/schedule/`
- **Method:** `POST`
- **Authentication:** Required (JWT)
- **Request Body:**
  ```json
  {
    "employee_id": "string", // Required
    "shift": {
      "day": "string", // Required, e.g., "monday", "tuesday"
      "shift_start": "string", // Required, format: "HH:MM"
      "shift_end": "string" // Required, format: "HH:MM"
    }
  }
 
 * **Request Body:**
  * `employee_id`: (required) Unique identifier for the staff member.
  * `shift`: (required) Contains the details of the shift.
    * `day`: Day of the week the shift is assigned (must be a valid day from `WEEK_DAYS`).
    * `shift_start`: Start time of the shift (format: "HH:MM").
    * `shift_end`: End time of the shift (format: "HH:MM").

* **Response:**
  * **Status Code:** `200 OK`
  * **Content:**
    ```json
    {
      "data": {
        "staff_member_id": "integer",
        "day": "string",
        "shift_start": "string",
        "shift_end": "string"
      }
    }
    ```
    * `staff_member_id`: Unique identifier for the staff member.
    * `day`: Day of the week the shift was assigned.
    * `shift_start`: Start time of the assigned shift.
    * `shift_end`: End time of the assigned shift.

* **Errors:**
  * **Code:** `CannotAssignWeekOffShift`
    * **Description:** Manager can only assign shifts on weekdays, not on weekends.
    * **Response:**
      ```json
      {
        "id": 8,
        "code": "CannotAssignWeekOffShift",
        "status_code": 400,
        "detail": "Manager can only assign shift on week days not for week days.",
        "description": "",
        "count": 1
      }
      ```

  * **Code:** `WrongEmployeeId`
    * **Description:** The provided employee ID is incorrect or does not exist.
    * **Response:**
      ```json
      {
        "id": 9,
        "code": "WrongEmployeeId",
        "status_code": 400,
        "detail": "The provided employee ID is incorrect or does not exist.",
        "description": "",
        "count": 1
      }
      ```

## 8. Assign Staff Weekly Off (Manager API)

- **Endpoint:** `/api/v1/master/staff/weekly-off/assign/`
- **Method:** `POST`
- **Authentication:** Required (JWT)
- **Request Body:**
  ```json
  {
    "employee_id": "string", // Required
    "weekly_off": [
      "string", // Required, e.g., "monday"
      "string"  // Required, e.g., "tuesday"
    ]
  }
* **Request Body:**
  * `employee_id`: (required) Unique identifier for the staff member.
  * `weekly_off`: (required) List of exactly two days for the staff member's weekly off.
    - Each entry must be a valid day from `WEEK_DAYS`.

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
        "role": "integer",
        "weekly_off": [
          "string", // e.g., "monday"
          "string"  // e.g., "tuesday"
        ]
      }
    }
    ```
    * `uuid`: Unique identifier for the staff member.
    * `first_name`: Staff member's first name.
    * `last_name`: Staff member's last name (can be null).
    * `image`: URL to the staff member's profile image (can be null).
    * `email`: Staff member's email address.
    * `role`: Staff member's role, represented as an integer.
    * `weekly_off`: List of days designated as weekly off.

* **Errors:**
  * **Code:** `WrongEmployeeId`
    * **Description:** The provided employee ID is incorrect or does not exist.
    * **Response:**
      ```json
      {
        "id": 9,
        "code": "WrongEmployeeId",
        "status_code": 400,
        "detail": "The provided employee ID is incorrect or does not exist.",
        "description": "",
        "count": 1
      }
      ```

  * **Code:** `MissingFieldError`
    * **Description:** Required fields are missing or invalid.
    * **Response:**
      ```json
      {
        "id": 8,
        "code": "MissingFieldError",
        "status_code": 400,
        "detail": "You must specify exactly two days for weekly off.",
        "description": "",
        "count": 1
      }
      ```

## 9. Get Staff Member Assigned Shifts

- **Endpoint:** `/api/v1/master/staff/assigned/shifts/`
- **Method:** `GET`
- **Authentication:** Required (JWT)

- **Response:**
  - **Status Code:** `200 OK`
  - **Content:**
    ```json
    {
      "data": [
        {
          "staff_member_id": "integer",
          "day": "string",
          "shift_start": "string",
          "shift_end": "string"
        }
      ]
    }
    ```
    * `staff_member_id`: Unique identifier for the staff member.
    * `day`: Day of the week for the shift.
    * `shift_start`: Start time of the shift (format: "HH:MM").
    * `shift_end`: End time of the shift (format: "HH:MM").

- **Errors:**
  * **Code:** `UserMustBeStaffMember`
    * **Description:** The user must be a staff member to access this endpoint.
    * **Response:**
      ```json
      {
        "id": 10,
        "code": "UserMustBeStaffMember",
        "status_code": 403,
        "detail": "The user must be a staff member to access this resource.",
        "description": "",
        "count": 1
      }
      ```
  * **Code:** `MissingFieldError`
    * **Description:** Required fields are missing or invalid.
    * **Response:**
      ```json
      {
        "id": 8,
        "code": "MissingFieldError",
        "status_code": 400,
        "detail": "You must specify exactly two days for weekly off.",
        "description": "",
        "count": 1
      }
      ```

## 10. Mark Staff Attendance

- **Endpoint:** `/api/v1/master/staff/attendance/mark/`
- **Method:** `POST`
- **Authentication:** Required (JWT)
- **Request Body:**
  ```json
  {
    "image": "file" // Required
  }

* `image`: (required) Image file for marking attendance.

* **Response:**
  * **Status Code:** `200 OK`
  * **Content:**
    ```json
    {
      "data": {
        "attendance_id": "integer",
        "staff_member_id": "integer",
        "date": "string",
        "status": "string",
        "image_url": "string"
      }
    }
    ```
    * `attendance_id`: Unique identifier for the attendance record.
    * `staff_member_id`: Unique identifier for the staff member.
    * `date`: Date of the attendance.
    * `status`: Status of the attendance (e.g., "Present", "Absent").
    * `image_url`: URL to the uploaded image.

* **Errors:**
  * **Code:** `AttendanceAlreadyMarked`
    * **Description:** Attendance has already been marked for today.
    * **Response:**
      ```json
      {
        "id": 11,
        "code": "AttendanceAlreadyMarked",
        "status_code": 400,
        "detail": "Attendance has already been marked for today.",
        "description": "",
        "count": 1
      }
      ```

  * **Code:** `UserMustBeStaffMember`
    * **Description:** The user must be a staff member to mark attendance.
    * **Response:**
      ```json
      {
        "id": 12,
        "code": "UserMustBeStaffMember",
        "status_code": 403,
        "detail": "The user must be a staff member to access this resource.",
        "description": "",
        "count": 1
      }
      ```

  * **Code:** `WeeklyOffToday`
    * **Description:** The user is on weekly off today.
    * **Response:**
      ```json
      {
        "id": 13,
        "code": "WeeklyOffToday",
        "status_code": 400,
        "detail": "The user is on weekly off today.",
        "description": "",
        "count": 1
      }
      ```

  * **Code:** `NoShiftForToday`
    * **Description:** No shift assigned for today.
    * **Response:**
      ```json
      {
        "id": 14,
        "code": "NoShiftForToday",
        "status_code": 400,
        "detail": "No shift assigned for today.",
        "description": "",
        "count": 1
      }
      ```

  * **Code:** `OutOfShiftHours`
    * **Description:** Attendance marking is outside of shift hours.
    * **Response:**
      ```json
      {
        "id": 15,
        "code": "OutOfShiftHours",
        "status_code": 400,
        "detail": "Attendance marking is outside of shift hours.",
        "description": "",
        "count": 1
      }
      ```

  * **Code:** `OutOfAttendanceWindow`
    * **Description:** Attendance can only be marked within the specified time window.
    * **Response:**
      ```json
      {
        "id": 16,
        "code": "OutOfAttendanceWindow",
        "status_code": 400,
        "detail": "Attendance can only be marked within the specified time window.",
        "description": "",
        "count": 1
      }
      ```


