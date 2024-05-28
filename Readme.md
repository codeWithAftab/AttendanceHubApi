# Gym Buddy App API

This API allows gym administrators to manage their gyms, including registering gyms, adding users, tracking attendance, managing fees, and sending notifications. Users can use the app to check in/out, receive payment reminders, and more.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [Auth](#auth)
  - [Gym](#gym)
  - [Users](#users)
  - [Attendance](#attendance)
  - [Payments](#payments)
  - [Notifications](#notifications)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

- Python 3.x
- pip (Python package installer)
- Django
- Django REST framework
- PostgreSQL (or any preferred database)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/gym-management-api.git
    ```

2. Navigate to the project directory:
    ```bash
    cd gym-management-api
    ```

3. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Set up environment variables:
    Create a `.env` file in the root directory and add the following:
    ```env
    SECRET_KEY=your_secret_key
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=your_database_host
    DB_PORT=your_database_port
    ```

6. Run migrations:
    ```bash
    python manage.py migrate
    ```

7. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

8. Start the server:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Auth

#### Register Admin
- **URL:** `/api/auth/register/`
- **Method:** `POST`
- **Description:** Register a new gym administrator.
- **Request Body:**
    ```json
    {
      "username": "admin_username",
      "password": "admin_password",
      "email": "admin@example.com"
    }
    ```

#### Login Admin
- **URL:** `/api/auth/login/`
- **Method:** `POST`
- **Description:** Login as a gym administrator.
- **Request Body:**
    ```json
    {
      "username": "admin_username",
      "password": "admin_password"
    }
    ```

### Gym

#### Register Gym
- **URL:** `/api/gyms/`
- **Method:** `POST`
- **Description:** Register a new gym.
- **Request Body:**
    ```json
    {
      "name": "Gym Name",
      "location": "Gym Location",
      "contact": "Contact Information",
      "operating_hours": "Operating Hours"
    }
    ```

#### Get Gyms
- **URL:** `/api/gyms/`
- **Method:** `GET`
- **Description:** Get a list of all registered gyms.

### Users

#### Add User
- **URL:** `/api/users/`
- **Method:** `POST`
- **Description:** Add a new user to the gym.
- **Request Body:**
    ```json
    {
      "username": "user_username",
      "password": "user_password",
      "email": "user@example.com",
      "gym_id": "Gym ID"
    }
    ```

#### Get Users
- **URL:** `/api/users/`
- **Method:** `GET`
- **Description:** Get a list of all users in a gym.

### Attendance

#### Mark Attendance
- **URL:** `/api/attendance/`
- **Method:** `POST`
- **Description:** Mark user attendance.
- **Request Body:**
    ```json
    {
      "user_id": "User ID",
      "gym_id": "Gym ID",
      "check_in": "Check-in Time",
      "check_out": "Check-out Time"
    }
    ```

#### Get Attendance
- **URL:** `/api/attendance/`
- **Method:** `GET`
- **Description:** Get attendance records for a gym or user.

### Payments

#### Record Payment
- **URL:** `/api/payments/`
- **Method:** `POST`
- **Description:** Record a payment from a user.
- **Request Body:**
    ```json
    {
      "user_id": "User ID",
      "amount": "Payment Amount",
      "date": "Payment Date"
    }
    ```

#### Get Payments
- **URL:** `/api/payments/`
- **Method:** `GET`
- **Description:** Get payment records for a gym or user.

### Notifications

#### Send Notification
- **URL:** `/api/notifications/`
- **Method:** `POST`
- **Description:** Send a notification to users.
- **Request Body:**
    ```json
    {
      "user_id": "User ID",
      "message": "Notification Message"
    }
    ```

## Running Tests

To run tests, use the following command:
```bash
python manage.py test
