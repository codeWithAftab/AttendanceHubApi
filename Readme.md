# AttendanceHub

**AttendanceHub** is an API service designed for managing staff attendance, shifts, and rosters. It provides endpoints for marking attendance, managing shifts, and tracking staff details. The system supports roles for managers and staff members, ensuring secure and efficient management of employee schedules and attendance.

## Features

- **Authentication & Authorization**: 
  - Managers can create, edit, and view rosters.
  - Staff can mark their attendance and view their shifts.

- **Roster Management**:
  - Managers can add new staff members, set working days and shifts, and set weekly offs.
  - Staff can interchange shifts among themselves.

- **Attendance Management**:
  - Staff can mark attendance by uploading an image within their shift timings.

## Endpoints

### Authentication

- **POST** `/api/token/` - Obtain authentication tokens.
- **POST** `/api/token/refresh/` - Refresh authentication tokens.

### Staff Management

- **POST** `/api/staff/` - Create a new staff member.
- **GET** `/api/staff/` - List all staff members.
- **GET** `/api/staff/{id}/` - Retrieve details of a specific staff member.
- **PUT** `/api/staff/{id}/` - Update a specific staff member.
- **DELETE** `/api/staff/{id}/` - Delete a specific staff member.

### Shift Management

- **POST** `/api/shifts/` - Create a new shift.
- **GET** `/api/shifts/` - List all shifts.
- **GET** `/api/shifts/{id}/` - Retrieve details of a specific shift.
- **PUT** `/api/shifts/{id}/` - Update a specific shift.
- **DELETE** `/api/shifts/{id}/` - Delete a specific shift.

### Attendance Management

- **POST** `/api/mark-attendance/` - Mark attendance with image upload.

## Setup

### Requirements

- Python 3.x
- Django
- Django REST Framework

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/attendancehub.git
   cd attendancehub
