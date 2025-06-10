# NBFC Django Project

A comprehensive Django-based Non-Banking Financial Company (NBFC) management system that handles employee management, loan processing, attendance tracking, salary management, and more.

## Features

### Core Modules

- **Employee Management**

  - Employee profiles and details
  - Organization-based employee segregation
  - Bulk employee creation
  - Employee statistics and analytics

- **Loan Management**

  - Loan application and processing
  - Multiple loan types support
  - Interest rate management
  - Loan status tracking
  - Bulk loan creation
  - Loan statistics and analytics

- **Attendance System**

  - Daily attendance tracking
  - Multiple attendance statuses (present, absent, late, half-day, leave)
  - Attendance verification
  - Attendance statistics

- **Salary Management**
  - Salary calculation and processing
  - Basic salary, allowances, and deductions
  - Salary approval workflow
  - Salary statistics and analytics

### Additional Features

- Organization-based multi-tenancy
- Role-based access control
- Document management
- Transaction logging
- Dashboard analytics
- Bulk data upload capabilities
- API-first architecture

## Technical Stack

- **Backend**: Django & Django REST Framework
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: JWT-based authentication
- **API Documentation**: Swagger/OpenAPI
- **Frontend**: (To be implemented)

## Project Structure

```
nbfc-django/
├── nbfc_accounts/         # Account management
├── nbfc_attendance/       # Attendance tracking
├── nbfc_auth/            # Authentication and authorization
├── nbfc_bulk_upload/     # Bulk data upload functionality
├── nbfc_dashboard/       # Dashboard and analytics
├── nbfc_documents/       # Document management
├── nbfc_employees/       # Employee management
├── nbfc_loan_deficit/    # Loan deficit tracking
├── nbfc_loans/           # Loan management
├── nbfc_organizations/   # Organization management
├── nbfc_repayments/      # Loan repayment tracking
├── nbfc_salaries/        # Salary management
├── nbfc_settings/        # System settings
├── nbfc_transaction_logs/# Transaction logging
└── nbfc_django/          # Core project settings
```

## Setup and Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd nbfc-django
```

2. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Create superuser:

```bash
python manage.py createsuperuser
```

6. Run development server:

```bash
python manage.py runserver
```

## API Documentation

The API documentation is available at `/api/docs/` when running the development server. The project includes a Postman collection (`nbfc_api_collection.json`) for API testing.

## Development Guidelines

1. **Code Style**

   - Follow PEP 8 guidelines
   - Use meaningful variable and function names
   - Add docstrings for functions and classes

2. **Git Workflow**

   - Create feature branches for new features
   - Write meaningful commit messages
   - Keep commits atomic and focused

3. **Testing**
   - Write unit tests for new features
   - Run tests before committing changes
   - Maintain test coverage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

