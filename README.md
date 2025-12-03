SmartPath — Guiding Students Toward Smarter Learning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React 18+](https://img.shields.io/badge/react-18+-61dafb.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)

Production URL
Live Application: 🔗
Figma Architecture :https://www.figma.com/board/qOjKZB2UtkLKjXADCSCOnh/SmartPath-Azure-Web-App-Architecture?node-id=0-1&t=cDyMcd33Wh9Qbq5f-1

SmartPath Context
In many African learning environments, students struggle to access organized and affordable online educational resources. **SmartPath** bridges this gap by providing a simple, accessible, and interactive learning platform that supports students in exploring lessons, taking quizzes, and tracking progress.

Target Users
-  High school and university students
-  Educators creating digital learning materials
-  Independent learners seeking accessible study resources
-  Students in areas with limited access to quality education

Core Features (Implemented)

###  Phase 1 - MVP (Current Release)
-  **User Registration & Login:** Secure authentication system with password hashing
-  **Landing Page:** Modern, responsive home page with platform overview
-  **Learning Modules:** Browse categorized study topics and lessons
-  **Interactive Quizzes:** Multiple-choice quizzes with instant feedback and scoring
-  **User Dashboard:** Personalized view of courses and progress
-  **Admin Panel:** Content management for courses and quizzes
-  **Profile Management:** Users can update their information
-  **RESTful API:** Complete backend API with proper error handling

### Phase 2 - Enhancements (Upcoming)
-  **Progress Tracking:** Visual analytics of learning journey
-  **Achievements & Badges:** Gamification elements
-  **Discussion Forums:** Community learning features
-  **Mobile Optimization:** Progressive Web App (PWA)
-  **Notifications:** Learning reminders and updates

##  Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Frontend** | React.js | 18.2.0 | UI Framework |
| | React Router | 6.15.0 | Client-side routing |
| | CSS3 | - | Styling |
| **Backend** | Flask | 2.3.3 | Web framework |
| | Flask-CORS | 4.0.0 | Cross-origin support |
| | SQLite | 3 | Database |
| **Security** | Werkzeug | - | Password hashing |
| | JWT | (future) | Token authentication |
| **Testing** | pytest | 7.4.0 | Backend testing |
| | Jest | - | Frontend testing |
| **DevOps** | Git | - | Version control |
| | GitHub Actions | - | CI/CD (future) |

##  Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (v16.0.0 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.10 or higher) - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/)
- **npm** (comes with Node.js)
- **pip** (comes with Python)

##  Installation and Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Kosisookeke/smartpath.git
cd smartpath
```

### Step 2: Backend Setup

#### 2.1 Navigate to Backend Directory
```bash
cd backend
```

#### 2.2 Create Virtual Environment
**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2.4 Initialize Database
```bash
python init_db.py
```

#### 2.5 Run Backend Server
```bash
python app.py
```
The backend API will run on `http://localhost:5000`

#### 2.6 (Optional) Run Backend Tests
```bash
pytest tests/
```

### Step 3: Frontend Setup

#### 3.1 Open New Terminal & Navigate to Frontend
```bash
cd frontend
```

#### 3.2 Install Dependencies
```bash
npm install
```

#### 3.3 Start Development Server
```bash
npm start
```
The app will open automatically at `http://localhost:3000`

#### 3.4 (Optional) Run Frontend Tests
```bash
npm test
```

##  Project Structure

```
smartpath/
├── backend/                    # Python Flask backend
│   ├── app/                   # Application package
│   │   ├── __init__.py       # Flask app factory
│   │   ├── models.py         # Database models (User, Course, Quiz, etc.)
│   │   ├── auth.py           # Authentication routes
│   │   ├── courses.py        # Course management routes
│   │   ├── quizzes.py        # Quiz functionality routes
│   │   ├── admin.py          # Admin panel routes
│   │   └── utils.py          # Helper functions
│   ├── tests/                # Backend unit tests
│   │   ├── test_auth.py
│   │   ├── test_courses.py
│   │   └── test_quizzes.py
│   ├── database/             # SQLite database location
│   │   └── smartpath.db
│   ├── app.py               # Main application entry point
│   ├── init_db.py           # Database initialization script
│   ├── requirements.txt     # Python dependencies
│   └── .env.example        # Environment variables template
│
├── frontend/                 # React frontend
│   ├── public/              # Static files
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   │   ├── Navbar.js
│   │   │   ├── Footer.js
│   │   │   ├── CourseCard.js
│   │   │   ├── QuizCard.js
│   │   │   └── ProtectedRoute.js
│   │   ├── pages/           # Page components
│   │   │   ├── Home.js
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Courses.js
│   │   │   ├── CourseDetail.js
│   │   │   ├── Quiz.js
│   │   │   ├── QuizResult.js
│   │   │   ├── Profile.js
│   │   │   └── Admin.js
│   │   ├── services/        # API communication
│   │   │   └── api.js
│   │   ├── context/         # React Context (Auth)
│   │   │   └── AuthContext.js
│   │   ├── App.js          # Main app component
│   │   ├── App.css         # Global styles
│   │   └── index.js        # Entry point
│   ├── package.json
│   └── .gitignore
│
├── .gitignore
├── LICENSE                  # MIT License
└── README.md               # This file
```

##  API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/user` - Get current user info
- `PUT /api/auth/user` - Update user profile

### Courses
- `GET /api/courses` - Get all courses
- `GET /api/courses/<id>` - Get specific course
- `POST /api/courses` - Create course (admin only)
- `PUT /api/courses/<id>` - Update course (admin only)
- `DELETE /api/courses/<id>` - Delete course (admin only)

### Quizzes
- `GET /api/quizzes` - Get all quizzes
- `GET /api/quizzes/<id>` - Get specific quiz
- `POST /api/quizzes/<id>/submit` - Submit quiz answers
- `GET /api/quizzes/<id>/results` - Get quiz results
- `POST /api/quizzes` - Create quiz (admin only)

### Admin
- `GET /api/admin/stats` - Get platform statistics
- `GET /api/admin/users` - Get all users
- `PUT /api/admin/users/<id>` - Update user role

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest tests/ -v
pytest tests/test_auth.py -v  # Test specific module
pytest --cov=app tests/       # With coverage report
# Linting
flake8 app/ tests/
```

### Frontend Testing
```bash
cd frontend
npm test                      # Run all tests
npm test -- --coverage       # With coverage report
# Linting
npm run lint
```


##  CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment.

### Pipeline Features
-  Automated linting (flake8 for Python, ESLint for JavaScript)
-  Automated testing (pytest and Jest)
-  Docker image building and validation
-  Branch protection on `main`
-  Required status checks before merging

### Workflow Triggers
- Pushes to any branch except `main`
- Pull requests targeting `main`

For detailed CI/CD setup instructions, see [CI_SETUP.md](CI_SETUP.md)

##  Default User Accounts

For testing purposes, the following accounts are created:

**Admin Account:**
- Email: `admin@smartpath.com`
- Password: `admin123`

**Student Account:**
- Email: `student@smartpath.com`
- Password: `student123`

##  Security Features

-  Password hashing using Werkzeug security
-  CORS protection configured
-  Input validation and sanitization
-  SQL injection prevention (parameterized queries)
-  XSS protection
-  JWT token authentication (coming soon)
-  Rate limiting (coming soon)

##  Troubleshooting

### Backend Issues

**Issue:** `ModuleNotFoundError: No module named 'flask'`
```bash
# Ensure virtual environment is activated and reinstall
pip install -r requirements.txt
```

**Issue:** Database errors
```bash
# Delete and recreate database
rm database/smartpath.db
python init_db.py
```

**Issue:** Port 5000 already in use
```bash
# Change port in app.py or kill process using port
# Windows: netstat -ano | findstr :5000
# Linux/Mac: lsof -i :5000
```

### Frontend Issues

**Issue:** `npm install` fails
```bash
# Clear npm cache and retry
npm cache clean --force
npm install
```

**Issue:** Cannot connect to backend
- Ensure backend is running on `http://localhost:5000`
- Check `proxy` setting in `package.json`

##  Development Guidelines

### Branching Strategy
- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent fixes

### Commit Message Format
```
type(scope): subject

body

footer
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(auth): add password reset functionality

- Add password reset endpoint
- Create email template for reset link
- Add frontend form for password reset

Closes #123
```

##  Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   # Backend
   cd backend && pytest
   
   # Frontend
   cd frontend && npm test
   ```
5. **Commit your changes**
   ```bash
   git commit -m 'feat: add some AmazingFeature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
7. **Open a Pull Request**

### Code Standards
- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript
- Write tests for new features
- Update documentation

##  License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Acknowledgments
- SmartPath Development Team
- All contributors and supporters
- The open-source community
- React and Flask communities

##  Contact & Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/Kosisookeke/smartpath/issues)
- **Email:** support@smartpath.com
- **Documentation:** [Full documentation](https://github.com/Kosisookeke/smartpath/wiki)

##  Roadmap

### Q1 2025
-  MVP Launch (Authentication, Courses, Quizzes)
-  Mobile responsiveness improvements
-  Progress tracking dashboard

### Q2 2025
-  Progressive Web App (PWA)
-  Email notifications
-  Gamification features

### Q3 2025
-  Discussion forums
-  Video lessons support
-  Multi-language support

### Q4 2025
-  AI-powered recommendations
-  Advanced analytics
-  Third-party integrations

---

<div align="center">
  <p>Made with ❤️ by the SmartPath Team</p>
  <p>Empowering learners across Africa and beyond</p>
  
   Star this repository if you find it helpful!
</div>
