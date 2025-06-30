# NBFC Django Project

A comprehensive Django-based Non-Banking Financial Company (NBFC) management system that handles employee management, loan processing, attendance tracking, salary management, and more.

## 🚀 Quick Deployment Script

**The fastest way to deploy on a new VM:**

Use the automated deployment script that handles everything for you:

```bash
./deploy.sh <NEW_IP_ADDRESS>
```

**Example:**
```bash
./deploy.sh 40.90.224.166
```

### What the deployment script does:
- ✅ Backs up existing configuration
- ✅ Creates new `.env` from template
- ✅ Updates HOST_IP automatically
- ✅ Stops old containers
- ✅ Builds and starts new containers
- ✅ Waits for services to initialize
- ✅ Provides access URLs and next steps

### Script Features:
- **Automatic Backup**: Creates timestamped backup of existing `.env`
- **Zero Configuration**: Just provide the IP address
- **Health Checks**: Verifies deployment success
- **User Guidance**: Shows next steps and access URLs
- **Error Handling**: Graceful failure with helpful logs

## 🎯 Manual IP Configuration

**For manual deployments, you only need to update ONE value:**

1. Copy `.env.example` to `.env`
2. Update the `HOST_IP` value in `.env`:
   ```bash
   HOST_IP=YOUR_NEW_VM_IP_HERE
   ```
3. Everything else (Django settings, Docker, nginx, API endpoints) automatically syncs!

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

### 🚀 Automated Deployment (Recommended)

**For new VM deployment using the deployment script:**

1. **Clone the repository**:
```bash
git clone <repository-url>
cd nbfc-django
```

2. **Make script executable**:
```bash
chmod +x deploy.sh
```

3. **Deploy with one command**:
```bash
./deploy.sh YOUR_VM_IP_ADDRESS
```

4. **Create superuser** (after deployment):
```bash
docker compose exec web python manage.py createsuperuser
```

5. **Test the deployment**:
```bash
curl http://YOUR_VM_IP:8000/api/
```

### 🎯 Manual VM Deployment

1. **Clone and configure**:
```bash
git clone <repository-url>
cd nbfc-django
cp .env.example .env
```

2. **Update ONLY the IP address** in `.env`:
```bash
# Edit .env file
HOST_IP=40.90.224.166  # Replace with your VM IP
```

3. **Deploy with Docker**:
```bash
docker-compose up -d
```

That's it! Everything else automatically syncs from the HOST_IP value.

### 🛠️ Local Development

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

**Note**: If you plan to use PostgreSQL, install the PostgreSQL adapter:
```bash
pip install psycopg2-binary
```

For development, SQLite is used by default and requires no additional setup.

4. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with HOST_IP=127.0.0.1 for local development
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Create superuser:

```bash
python manage.py createsuperuser
```

7. Run development server:

```bash
python manage.py runserver
```

## 🌐 Dynamic Configuration Features

- **Single Point Configuration**: Update only `HOST_IP` in `.env`
- **Auto-generated Settings**: Django settings automatically adapt
- **Flexible nginx**: Works with any IP or domain
- **Docker Integration**: Compose file uses environment variables
- **API Compatibility**: All endpoints work with any host configuration
- **Deployment Script**: One-command deployment with automatic configuration

## Deployment Commands Reference

### Using Deployment Script
```bash
# Deploy to new IP
./deploy.sh 40.90.224.166

# Check deployment status
docker compose ps

# View logs
docker compose logs

# Create superuser
docker compose exec web python manage.py createsuperuser
```

### Manual Docker Commands
```bash
# Stop services
docker compose down

# Build and start
docker compose up -d --build

# View logs
docker compose logs -f

# Access container shell
docker compose exec web bash
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

