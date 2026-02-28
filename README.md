# Task Management Application

A comprehensive task management system built with Django and Django REST Framework that allows users to manage tasks with completion reports and worked hours tracking.

## Features

### User Roles
- **SuperAdmin**: Can manage all users, admins, and tasks across the system
- **Admin**: Can create and assign tasks to their assigned users, view completion reports
- **User**: Can view their assigned tasks, update status, and submit completion reports

### API Endpoints

#### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (returns JWT tokens)
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile

#### Tasks
- `GET /api/tasks/` - Get all tasks for the logged-in user
- `POST /api/tasks/create/` - Create a new task (Admin/SuperAdmin only)
- `PUT /api/tasks/{id}/` - Update task status and details
- `GET /api/tasks/{id}/report/` - Get task completion report (Admin/SuperAdmin only)

### Admin Panel
Web-based admin interface with role-based access control:
- **Dashboard**: Overview of tasks and statistics
- **User Management**: Create, update, delete users (SuperAdmin only)
- **Admin Management**: Create, update, delete admins (SuperAdmin only)
- **Task Management**: Create, assign, and manage tasks
- **Task Reports**: View completion reports and worked hours

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd task-manager
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Usage

### API Usage

1. **Register a new user**
   ```bash
   curl -X POST http://localhost:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "password": "password123",
       "password_confirm": "password123",
       "first_name": "Test",
       "last_name": "User",
       "role": "user"
     }'
   ```

2. **Login**
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "password123"
     }'
   ```

3. **Get tasks (with JWT token)**
   ```bash
   curl -X GET http://localhost:8000/api/tasks/ \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

### Admin Panel Usage

1. Access the admin panel at `http://localhost:8000/`
2. Login with your superuser credentials
3. Navigate through different sections using the navigation menu

## Task Workflow

1. **Task Creation**: Admins/SuperAdmins create tasks and assign them to users
2. **Task Management**: Users can update task status (Pending → In Progress → Completed)
3. **Completion Report**: When marking a task as completed, users must provide:
   - Completion Report: Details about what was done, challenges faced, etc.
   - Worked Hours: Number of hours spent on the task
4. **Report Viewing**: Admins and SuperAdmins can view completion reports for monitoring

## Database Schema

### User Model
- Extended Django User model with role field
- Roles: user, admin, superadmin
- assigned_admin: Foreign key for user-to-admin assignment

### Task Model
- title: Task title
- description: Detailed description
- assigned_to: User assigned to the task
- created_by: User who created the task
- due_date: Task deadline
- status: Task status (pending, in_progress, completed)
- completion_report: Report submitted on completion
- worked_hours: Hours worked on the task

## Security Features

- JWT Authentication for API endpoints
- Role-based access control
- Permission decorators for admin panel
- Input validation and sanitization
- CORS configuration for frontend integration

## Technologies Used

- **Backend**: Django 4.2.7, Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (development ready)
- **Frontend**: Bootstrap 5, Font Awesome icons
- **Security**: CORS headers, permission classes

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Superuser Creation
```bash
python manage.py createsuperuser
```

## Deployment Notes

1. Change `SECRET_KEY` in production
2. Set `DEBUG=False` in production
3. Configure appropriate database (PostgreSQL recommended)
4. Set up proper CORS origins
5. Configure static file serving
6. Set up SSL/HTTPS

## API Documentation

### Authentication Endpoints

#### Register
- **URL**: `POST /api/auth/register/`
- **Body**: JSON with user details
- **Response**: User data and JWT tokens

#### Login
- **URL**: `POST /api/auth/login/`
- **Body**: JSON with username and password
- **Response**: User data and JWT tokens

#### Logout
- **URL**: `POST /api/auth/logout/`
- **Headers**: Authorization Bearer token
- **Response**: Success message

### Task Endpoints

#### Get Tasks
- **URL**: `GET /api/tasks/`
- **Headers**: Authorization Bearer token
- **Response**: List of tasks for the user

#### Update Task
- **URL**: `PUT /api/tasks/{id}/`
- **Headers**: Authorization Bearer token
- **Body**: JSON with task updates
- **Response**: Updated task data

#### Get Task Report
- **URL**: `GET /api/tasks/{id}/report/`
- **Headers**: Authorization Bearer token
- **Response**: Task completion report (Admin/SuperAdmin only)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
