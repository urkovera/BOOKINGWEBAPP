# Classroom Booking System

A comprehensive web-based classroom booking and management system built with Flask and PostgreSQL. This system enables students to reserve classrooms and professors to approve or decline reservation requests with an intuitive interface.

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Database Schema](#database-schema)
- [User Roles & Permissions](#user-roles--permissions)
- [Application Workflow](#application-workflow)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)

## Features

### For Students
-  User registration and authentication
-  View available classrooms by date
-  Book classrooms with reason for usage
-  View booking history with status indicators
-  Real-time booking status updates (Pending/Approved/Declined/Completed)

### For Professors
-  Approve or decline student booking requests
-  Filter requests by room, date, or time range
-  View complete approval history
-  Automatic cascade decline for conflicting reservations
-  Manage classroom availability

### System Features
-  Color-coded status system for easy visualization
  - **Yellow**: Pending requests
  - **Red**: Booked and approved
  - **Green**: Approved upcoming booking
  - **Grey**: Completed booking
-  Role-based access control
-  Room details display (chairs, projector, AC, computers)
-  Responsive design
-  Fully containerized with Docker

##  System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Client Browser                     │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP/HTTPS
┌──────────────────────▼──────────────────────────────┐
│              Gunicorn Web Server                     │
│                    (Port 8000)                       │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              Flask Application                       │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Routes    │  │  Templates   │  │  Models    │ │
│  │  (Views)    │  │  (Jinja2)    │  │ (SQLAlch)  │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
└──────────────────────┬──────────────────────────────┘
                       │ SQLAlchemy ORM
┌──────────────────────▼──────────────────────────────┐
│           PostgreSQL Database                        │
│                 (Port 5432)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │   User   │  │ Reserve  │  │   Room   │          │
│  └──────────┘  └──────────┘  └──────────┘          │
└──────────────────────────────────────────────────────┘
```

##  Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend Framework** | Flask | 3.0.0 |
| **Template Engine** | Jinja2 | 3.1.2 |
| **WSGI Server** | Gunicorn | 21.2.0 |
| **Database** | PostgreSQL | 15 (Alpine) |
| **ORM** | SQLAlchemy | 2.0.23 |
| **Containerization** | Docker & Docker Compose | - |
| **Language** | Python | 3.11 |

##  Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10 or higher)
  - [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (version 2.0 or higher)
  - [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Git** (for cloning the repository)

### Verify Installation

```bash
docker --version
docker-compose --version
```

## Installation

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd classroom-booking-system
```

### Step 2: Create Project Structure

Ensure your project structure looks like this:

```
classroom-booking-system/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── app/
    ├── app.py
    ├── models.py           # (to be created)
    ├── routes.py           # (to be created)
    ├── templates/
    │   └── index.html
    └── static/             # (optional - for CSS/JS)
```

Create the app directory structure:

```bash
mkdir -p app/templates app/static
```

### Step 3: Set Up Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your preferred settings:

```bash
nano .env
# or
vim .env
# or use any text editor
```

**Important**: Change the following values in production:
- `SECRET_KEY` - Generate a secure random key
- `POSTGRES_PASSWORD` - Use a strong password

To generate a secure secret key:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

##  Configuration

### Environment Variables

The `.env` file contains all configuration:

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `POSTGRES_USER` | Database username | `booking_user` | ✅ |
| `POSTGRES_PASSWORD` | Database password | `CPE101PASS` | ✅ |
| `POSTGRES_DB` | Database name | `classroom_booking` | ✅ |
| `DB_PORT` | Database port | `5432` | ✅ |
| `APP_PORT` | Application port | `8000` | ✅ |
| `FLASK_ENV` | Flask environment | `development` | ✅ |
| `SECRET_KEY` | Flask secret key | `your-secret-key...` | ✅ |
| `GUNICORN_WORKERS` | Number of workers | `4` | ✅ |
| `GUNICORN_TIMEOUT` | Request timeout (seconds) | `120` | ✅ |
| `DATABASE_URL` | Full database connection string | Auto-generated | ✅ |

### Database Configuration

The PostgreSQL database is configured with:
- Automatic health checks every 10 seconds
- Persistent volume storage
- Isolated network for security
- Connection retry mechanism (5 retries, 5s timeout)

## Running the Application

### Development Mode

1. **Build and start all services**:

```bash
docker-compose up --build
```

This command will:
- Build the Flask application Docker image
- Pull the PostgreSQL image
- Create and start both containers
- Set up the network and volumes
- Display logs in the terminal

2. **Run in detached mode** (background):

```bash
docker-compose up -d --build
```

3. **Access the application**:

- **Web Application**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Database** (for external tools): localhost:5432

### Viewing Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100
```

### Stopping the Application

```bash
# Stop containers (keeps data)
docker-compose stop

# Stop and remove containers (keeps volumes)
docker-compose down

# Stop and remove everything including volumes (⚠️ deletes all data)
docker-compose down -v
```

### Restarting Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart web
```

## Database Schema

### User Table

```sql
User
├── Username       VARCHAR(16)     PRIMARY KEY
├── Name          TEXT            NOT NULL
├── Role          ENUM            NOT NULL (Student/Professor)
├── HashPassword  TEXT            NOT NULL
├── StdId         VARCHAR(11)     NULLABLE
└── RegisterDate  DATE            NOT NULL
```

### Room Table

```sql
Room
├── RoomID         VARCHAR(7)      PRIMARY KEY
├── Chair          INTEGER         NOT NULL
├── Projector      BOOLEAN         NOT NULL
├── AirConditioner INTEGER         NOT NULL
└── Computer       BOOLEAN         NOT NULL
```

### Reserve Table

```sql
Reserve
├── ReserveId     INTEGER         PRIMARY KEY AUTO INCREMENT
├── RoomID        VARCHAR(7)      FOREIGN KEY → Room(RoomID)
├── BookDate      DATE            NOT NULL
├── Status        ENUM            NOT NULL (Pending/Approved/Declined/Completed)
├── ApproveBy     VARCHAR(16)     FOREIGN KEY → User(Username)
├── ApproveDate   DATE            NULLABLE
├── ReserveBy     VARCHAR(16)     FOREIGN KEY → User(Username)
├── ReserveDate   DATE            NOT NULL
├── StartTime     DATETIME        NOT NULL
└── EndTime       DATETIME        NOT NULL
```

### Relationships

- `Reserve.RoomID` → `Room.RoomID` (Many-to-One)
- `Reserve.ReserveBy` → `User.Username` (Many-to-One)
- `Reserve.ApproveBy` → `User.Username` (Many-to-One)

## User Roles & Permissions

### Student Role

| Permission | Access |
|-----------|--------|
| Register/Login | ✅ |
| View Available Rooms | ✅ |
| Create Booking | ✅ |
| View Own History | ✅ |
| Approve Requests | ❌ |
| View All Bookings | ❌ |

### Professor Role

| Permission | Access |
|-----------|--------|
| Register/Login | ✅ |
| View Available Rooms | ✅ |
| Create Booking | ✅ |
| View Own History | ✅ |
| Approve Requests | ✅ |
| View All Bookings | ✅ |
| Filter Requests | ✅ |
| View Approval History | ✅ |

## 📊 Application Workflow

### 1. Authentication Flow

```
User → Login/Register → Role Detection (Student/Professor) → Dashboard
```

### 2. Booking Flow (Student)

```
Dashboard → Make Booking → Select Date → View Available Rooms
→ Choose Room & Time → Provide Reason → Submit
→ Status: Pending (Yellow) → Wait for Professor Approval
```

### 3. Approval Flow (Professor)

```
Dashboard → Approve Requests → View Pending Queue
→ Filter (Optional: by room/date/time) → Review Request
→ Approve/Decline → Cascade Decline Conflicts (if approved)
→ Update Status
```

### 4. Status Lifecycle

```
Pending (Yellow) → Approved (Green) → Completed (Grey)
                ↘ Declined (Red)
```

## API Endpoints

### Health Check

```
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "app": "Classroom Booking System"
}
```

### Main Routes (To Be Implemented)

```
GET  /                    # Home page
GET  /login              # Login page
POST /login              # Login handler
GET  /register           # Registration page
POST /register           # Registration handler
GET  /dashboard          # User dashboard
GET  /booking            # Booking page
POST /booking            # Create booking
GET  /history            # User booking history
GET  /approval           # Professor approval page (Professor only)
POST /approval/approve   # Approve booking (Professor only)
POST /approval/decline   # Decline booking (Professor only)
GET  /logout             # Logout
```

## Development

### Database Initialization

Create an initialization script `app/init_db.py`:

```python
from app import app, db
from models import User, Room, Reserve

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
```

Run initialization:

```bash
docker-compose exec web python init_db.py
```

### Adding New Dependencies

1. Add to `requirements.txt`
2. Rebuild the container:

```bash
docker-compose up --build
```

### Database Access

Connect to PostgreSQL directly:

```bash
docker-compose exec db psql -U booking_user -d classroom_booking
```

Useful SQL commands:

```sql
-- List all tables
\dt

-- Describe table structure
\d users
\d rooms
\d reserves

-- Query data
SELECT * FROM users;
SELECT * FROM rooms;
SELECT * FROM reserves WHERE status = 'Pending';
```

### Hot Reload

The development setup includes volume mounting, so changes to Python files will automatically reload the application (when using Gunicorn with `--reload` flag).

For immediate changes:

```bash
docker-compose restart web
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

**Error**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution**:
```bash
# Find process using the port
lsof -i :8000  # On Mac/Linux
netstat -ano | findstr :8000  # On Windows

# Kill the process or change APP_PORT in .env
```

#### 2. Database Connection Failed

**Error**: `could not connect to server`

**Solution**:
```bash
# Check database logs
docker-compose logs db

# Verify database is healthy
docker-compose ps

# Restart database
docker-compose restart db
```

#### 3. Permission Denied

**Error**: `Permission denied` when running Docker

**Solution**:
```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER

# Log out and log back in
```

#### 4. Container Build Fails

**Solution**:
```bash
# Clean Docker cache
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up
```

#### 5. Database Data Lost After Restart

**Issue**: Data disappears after `docker-compose down`

**Solution**: Use `docker-compose stop` instead of `down`, or ensure volume persistence:
```bash
# Check volumes
docker volume ls

# Never use -v flag unless you want to delete data
docker-compose down  # ✅ Keeps data
docker-compose down -v  # ❌ Deletes data
```

### Debugging Commands

```bash
# Check container status
docker-compose ps

# Execute commands in container
docker-compose exec web bash
docker-compose exec db bash

# View container resource usage
docker stats

# Inspect container
docker inspect classroom_booking_app

# Check network
docker network ls
docker network inspect classroom-booking-system_booking_network
```

## Security Considerations

### Production Deployment Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Update `POSTGRES_PASSWORD` to a secure password
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS/SSL
- [ ] Use environment-specific `.env` files
- [ ] Implement rate limiting
- [ ] Add CSRF protection
- [ ] Enable security headers
- [ ] Regular database backups
- [ ] Update dependencies regularly
- [ ] Implement logging and monitoring
- [ ] Use secrets management (e.g., Docker secrets, HashiCorp Vault)

### Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use strong passwords** with special characters
3. **Implement password hashing** (use Werkzeug's security functions)
4. **Validate all user inputs** to prevent SQL injection
5. **Use prepared statements** (SQLAlchemy ORM handles this)
6. **Implement session management** with secure cookies
7. **Add rate limiting** for login attempts
8. **Regular security audits** and dependency updates

### Generating Secure Keys

```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# Generate strong password
python3 -c "import secrets; import string; chars = string.ascii_letters + string.digits + string.punctuation; print(''.join(secrets.choice(chars) for i in range(20)))"
```

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

## Next Steps

To complete the application, implement:

1. **Authentication System**
   - User registration with password hashing
   - Login/logout functionality
   - Session management
   - Role-based middleware

2. **Database Models**
   - User model with relationships
   - Room model with facilities
   - Reserve model with status tracking

3. **Booking System**
   - Date picker for booking
   - Room availability checker
   - Conflict detection
   - Booking form with validation

4. **Approval System**
   - Pending requests dashboard
   - Filter functionality
   - Approve/decline actions
   - Cascade decline logic

5. **History View**
   - Personal booking history
   - Status indicators
   - Booking details

6. **UI/UX**
   - Responsive design
   - Color-coded status system
   - Form validation feedback
   - Loading states

## License

This project is developed for educational purposes as part of the CPE101 course.

## Contributors

[Add your team members here]

---

**Need Help?** Open an issue or contact the development team.

**Last Updated**: November 2025