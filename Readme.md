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

## Project Tree Structure.
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
│-- authentication/
│    ├── __init__.py
├── config/
│    ├── __init__.py
│    ├── asgi.py
│    ├── urls.py
│    ├── wsgi/
│    │   ├── dev.py
│    │   └── prod.py
│    │── settings/
│    │   ├── base.py
│    │   ├── dev.py
│    │   └── prod.py
├── exception/
│    ├── auth.py
│    ├── base.py
│    ├── restapi.py/
├── helper/
│    ├── __init__.py
│    ├── constant.py
│    ├── id_generator.py
│    ├── serilaizers.py/
│    ├── validation.py/
│── schema/
│    ├── __init__.py
│    ├── request.py
│── scripts/
├── .gitignore
├── README.md
├── manage-dev.py
├── manage-prod.py
└── requirements.txt



## Setup

### Requirements

- Python 3.10
- Django==5.0.6
- djangorestframework==3.15.1
- djangorestframework-simplejwt==5.3.1
- pillow==10.3.0
- pytz==2024.1
- requests==2.32.2
- sqlparse==0.5.0
- typing_extensions==4.12.0
- uritemplate==4.1.1
- urllib3==2.2.1

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

## Documentation

API documentation will be added separately. For detailed information about the available endpoints, please refer to the API documentation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you’d like to contribute.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
