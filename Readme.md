# AttendanceHub Api

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

4. Apply database Migrations:
 ```bash
   python manage-dev.py makemigrations
   python manage-dev.py migrate
  ```

5. Run Error code Script to store all predefined error code in db:
```bash
   python manage-dev.py shell
  ```

6. **Import the `create_error` function** from the `scripts` module:
    ```python
    from scripts import create_error
    ```

7. **Run the function** to store all predefined error codes in the database:
    ```python
    create_error()
    ```

8. **Exit the Django Shell**:
    ```python
    exit()
    ```

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

## 2. Obtain JWT Access Token

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

## 3. Update User API

**Endpoint:** `PATCH /api/v1/accounts/user/update/`

**Authentication:** JWT Authentication

**Request Body:**

```json
{
    "first_name": "string",
    "last_name": "string",
    "image": "file",
    "role": "staff"
}
```

**Response Schema:**

```json
{
    "data": {
        "uuid": "5259ffa0-e77a-4fe4-af11-b7f48cc036b4",
        "first_name": "Aftab",
        "last_name": null,
        "image": "http://127.0.0.1:8000/media/profile_images/1000000550_49hrcza.jpg",
        "email": "hello82@gmail.com",
        "role": 1
    }
}
```

**Errors:**

*   **Code:** `MissingFieldError`
    
    *   **Description:** Required fields are missing or invalid.
    *   **Response:**

```json
    {
        "id": 9,
        "code": "MissingFieldError",
        "status_code": 400,
        "detail": "Required fields are missing or invalid.",
        "description": "",
        "count": 1
    }
```


## 4. Get User Profile (For All type user.)

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

## 5. Add New Staff Member (Manager API)

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
    
    
## 6. Get Staff Members Details

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
 
## 7. Update Staff Member Details. (Manager API)

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

## 8. Assign Staff Shift (Manager API)

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

## 9. Assign Staff Weekly Off (Manager API)

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

## 10. Get Staff Member Assigned Shifts (Staff Member API)

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

## 11. Mark Staff Attendance (Staff Member API)

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


## 12. Request for Interchange Shifts

**Endpoint:**

`POST /api/v1/master/staff/shift/interchange/request/`

**Request Body:**

```json
{
    "target_email": "target@example.com",
    "requester_shift_id": 1,
    "target_shift_id": 2
}
**Description:**

This API endpoint allows a staff user to request an interchange of shifts with another staff member.

**Success Response:**

* **Status Code:** `200 OK`
* **Content:**
  ```json
  {
    "data": {
      "id": 3,
      "requester": {
        "user": {
          "uuid": "3dfe1abe-512c-4a0a-8020-924da1ad9183",
          "first_name": "Nobu",
          "last_name": "staff2",
          "image": null,
          "email": "staff2@gmail.com",
          "role": "staff",
          "created_on": "2024-07-21T18:47:02.875884+05:30",
          "updated_on": "2024-07-21T18:48:52.769292+05:30"
        },
        "employee_id": "emp_b0e69c",
        "weekly_off": [
          "saturday",
          "tuesday"
        ]
      },
      "target": {
        "user": {
          "uuid": "806dfcd5-a560-4192-9216-d213d10b8beb",
          "first_name": "Aftab",
          "last_name": null,
          "image": null,
          "email": "aftabahmad41442@gmail.com",
          "role": "staff",
          "created_on": "2024-07-21T18:46:13.711844+05:30",
          "updated_on": "2024-07-21T18:46:13.916094+05:30"
        },
        "employee_id": "emp_532b30",
        "weekly_off": [
          "saturday",
          "sunday"
        ]
      },
      "requester_shift": {
        "id": 15,
        "staff_member_id": 6,
        "day": "sunday",
        "shift_start": "18:03",
        "shift_end": "10:00"
      },
      "target_shift": {
        "id": 16,
        "staff_member_id": 5,
        "day": "sunday",
        "shift_start": "18:30",
        "shift_end": "22:06"
      },
      "status": "approved"
    }
  }
  ```

**Errors:**

* **Code:** `StaffUserNotFound`
  
  * **Description:** The staff user with the provided email was not found.
  * **Response:**
    ```json
    {
      "id": 1,
      "code": "StaffUserNotFound",
      "status_code": 404,
      "detail": "The staff user with the provided email was not found.",
      "description": "",
      "count": 1
    }
    ```

* **Code:** `RequesterShiftNotFound`
  
  * **Description:** The shift with the provided ID for the requester was not found.
  * **Response:**
    ```json
    {
      "id": 2,
      "code": "RequesterShiftNotFound",
      "status_code": 404,
      "detail": "The shift with the provided ID for the requester was not found.",
      "description": "",
      "count": 1
    }
    ```

* **Code:** `TargetedShiftNotFound`
  
  * **Description:** The shift with the provided ID for the target was not found.
  * **Response:**
    ```json
    {
      "id": 3,
      "code": "TargetedShiftNotFound",
      "status_code": 404,
      "detail": "The shift with the provided ID for the target was not found.",
      "description": "",
      "count": 1
    }
    ```

* **Code:** `SameDayMustInInterchange`
  
  * **Description:** Both shifts must be on the same day to request an interchange.
  * **Response:**
    ```json
    {
      "id": 4,
      "code": "SameDayMustInInterchange",
      "status_code": 400,
      "detail": "Both shifts must be on the same day to request an interchange.",
      "description": "",
      "count": 1
    }
    ```

* **Code:** `ShiftInterchangeRequestAlreadyPending`
  
  * **Description:** There is already a pending interchange request for these shifts.
  * **Response:**
    ```json
    {
      "id": 5,
      "code": "ShiftInterchangeRequestAlreadyPending",
      "status_code": 400,
      "detail": "There is already a pending interchange request for these shifts.",
      "description": "",
      "count": 1
    }
    ```

## 12. Shift Interchange Request List API

**Endpoint:** `GET /api/v1/master/staff/shift/interchange/request/list/`

**Description:** Retrieves a list of shift interchange requests for the authenticated staff user.

**Authentication:** Required (JWT Authentication)

**Response Schema:**

* **Success:**
  ```json
  {
    "data": [
      {
        "id": 1,
        "requester": {
          "user": {
            "uuid": "user-uuid-1",
            "first_name": "RequesterFirstName",
            "last_name": "RequesterLastName",
            "image": null,
            "email": "requester@example.com",
            "role": "staff",
            "created_on": "2024-07-21T18:47:02.875884+05:30",
            "updated_on": "2024-07-21T18:48:52.769292+05:30"
          },
          "employee_id": "emp_12345",
          "weekly_off": [
            "saturday",
            "tuesday"
          ]
        },
        "target": {
          "user": {
            "uuid": "user-uuid-2",
            "first_name": "TargetFirstName",
            "last_name": "TargetLastName",
            "image": null,
            "email": "target@example.com",
            "role": "staff",
            "created_on": "2024-07-21T18:46:13.711844+05:30",
            "updated_on": "2024-07-21T18:46:13.916094+05:30"
          },
          "employee_id": "emp_67890",
          "weekly_off": [
            "saturday",
            "sunday"
          ]
        },
        "requester_shift": {
          "id": 1,
          "staff_member_id": 1,
          "day": "sunday",
          "shift_start": "09:00",
          "shift_end": "17:00"
        },
        "target_shift": {
          "id": 2,
          "staff_member_id": 2,
          "day": "sunday",
          "shift_start": "17:00",
          "shift_end": "01:00"
        },
        "status": "pending"
      }
    ]
  } 
  ```

**Errors:**

* **Code:** `UserMustBeStaffMember`

  * **Description:** The authenticated user must be a staff member to access this resource.
  * **Response:**
    ```json
    {
      "id": 6,
      "code": "UserMustBeStaffMember",
      "status_code": 403,
      "detail": "The authenticated user must be a staff member to access this resource.",
      "description": "",
      "count": 1
    }
    ```


## 13. Shift Interchange Request Status Update API

**Endpoint:** `POST /api/v1/master/staff/shift/interchange/request/status/update/`

**Description:** Updates the status of a shift interchange request.

**Authentication:** Required (JWT Authentication)

**Request Body:**

```json
{
  "request_id": 1,
  "status": "approved" or "rejected"
}

**Response Schema:**

* **Success:**

```json
{
  "data": {
    "id": 1,
    "requester": {
      "user": {
        "uuid": "user-uuid-1",
        "first_name": "RequesterFirstName",
        "last_name": "RequesterLastName",
        "image": null,
        "email": "requester@example.com",
        "role": "staff",
        "created_on": "2024-07-21T18:47:02.875884+05:30",
        "updated_on": "2024-07-21T18:48:52.769292+05:30"
      },
      "employee_id": "emp_12345",
      "weekly_off": [
        "saturday",
        "tuesday"
      ]
    },
    "target": {
      "user": {
        "uuid": "user-uuid-2",
        "first_name": "TargetFirstName",
        "last_name": "TargetLastName",
        "image": null,
        "email": "target@example.com",
        "role": "staff",
        "created_on": "2024-07-21T18:46:13.711844+05:30",
        "updated_on": "2024-07-21T18:46:13.916094+05:30"
      },
      "employee_id": "emp_67890",
      "weekly_off": [
        "saturday",
        "sunday"
      ]
    },
    "requester_shift": {
      "id": 1,
      "staff_member_id": 1,
      "day": "sunday",
      "shift_start": "09:00",
      "shift_end": "17:00"
    },
    "target_shift": {
      "id": 2,
      "staff_member_id": 2,
      "day": "sunday",
      "shift_start": "17:00",
      "shift_end": "01:00"
    },
    "status": "approved"
  }
}
```
**Errors:**

* **Code:** `InterchangeRequestNotFound`
  
  * **Description:** The specified shift interchange request was not found.
  * **Response:**

```json
{
  "id": 7,
  "code": "InterchangeRequestNotFound",
  "status_code": 404,
  "detail": "The specified shift interchange request was not found.",
  "description": "",
  "count": 1
}
```