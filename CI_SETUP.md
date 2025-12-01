# CI/CD Pipeline Setup Guide

## Overview
This document explains the Continuous Integration (CI) pipeline setup for the SmartPath Learning Platform.

## CI Pipeline Features

The CI pipeline (`.github/workflows/ci.yml`) automatically runs on:
- **Pushes** to any branch except `main`
- **Pull requests** targeting the `main` branch

### Pipeline Jobs

#### 1. Backend CI (`backend-ci`)
- Sets up Python 3.10 environment
- Installs dependencies from `requirements.txt`
- **Linting**: Runs flake8 to check code quality
  - Critical errors check (E9, F63, F7, F82)
  - Code complexity and style checks
- **Testing**: Runs pytest with coverage reporting
- **Docker Build**: Validates backend Dockerfile

#### 2. Frontend CI (`frontend-ci`)
- Sets up Node.js 18 environment
- Installs npm dependencies
- **Linting**: Runs ESLint on React code
- **Testing**: Runs Jest tests with coverage
- **Build**: Validates production build
- **Docker Build**: Validates frontend Dockerfile

#### 3. Docker Compose Validation (`docker-compose-validation`)
- Validates `docker-compose.yml` configuration
- Builds all services
- Tests service startup and health checks

## Setting Up Branch Protection (Part 3)

### Step 1: Push Your Code to GitHub
```bash
git init
git add .
git commit -m "Add CI pipeline and containerization"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Create a Development Branch
```bash
git checkout -b develop
git push -u origin develop
```

### Step 3: Configure Branch Protection Rules

1. Go to your GitHub repository
2. Click **Settings** → **Branches**
3. Click **Add rule** under "Branch protection rules"
4. Configure the following:

   **Branch name pattern**: `main`

   Enable these settings:
   - ✅ **Require a pull request before merging**
   - ✅ **Require status checks to pass before merging**
     - Search and add these required checks:
       - `Backend - Lint, Test & Build`
       - `Frontend - Lint, Test & Build`
       - `Validate Docker Compose`
   - ✅ **Require branches to be up to date before merging**
   - ✅ **Do not allow bypassing the above settings**

5. Click **Create** or **Save changes**

### Step 4: Test the CI Pipeline

#### Test 1: Create a Feature Branch (Success)
```bash
git checkout -b feature/add-new-feature
# Make some changes
git add .
git commit -m "Add new feature"
git push -u origin feature/add-new-feature
```
- CI should run automatically and pass ✅

#### Test 2: Introduce a Linting Error (Failure)
```bash
git checkout -b test/linting-error
# Add a Python file with linting issues (e.g., unused import, long line)
echo "import os, sys, json, random" > backend/app/test_lint.py
git add .
git commit -m "Test linting failure"
git push -u origin test/linting-error
```
- CI should run and **fail** ❌ due to linting errors
- Fix the error and push again to see it pass ✅

#### Test 3: Create a Pull Request
```bash
git checkout -b feature/test-pr
# Make valid changes
git add .
git commit -m "Test PR with CI integration"
git push -u origin feature/test-pr
```
Then on GitHub:
1. Create a Pull Request from `feature/test-pr` to `main`
2. Wait for CI checks to complete
3. Request a code review (if working in a team)
4. Merge once all checks pass and review is approved

## Running Tests Locally

### Backend Tests
```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v --cov=app
flake8 app/ tests/
```

### Frontend Tests
```bash
cd frontend
npm install
npm run lint
npm test -- --coverage --watchAll=false
npm run build
```

## CI Pipeline Files Structure
```
.github/
└── workflows/
    └── ci.yml          # Main CI pipeline configuration

backend/
├── .flake8             # Flake8 linting configuration
├── requirements.txt    # Includes flake8 for linting
└── tests/              # Pytest test files

frontend/
├── package.json        # Includes lint script
└── src/
    └── App.test.js     # Jest test file
```

## Troubleshooting

### CI Fails on Linting
- Run linting locally: `flake8 app/` (backend) or `npm run lint` (frontend)
- Fix all reported issues before pushing

### CI Fails on Tests
- Run tests locally: `pytest tests/` (backend) or `npm test` (frontend)
- Ensure all tests pass before pushing

### CI Fails on Docker Build
- Check Dockerfile syntax
- Ensure all required files are present and not in `.dockerignore`
- Test locally: `docker build -t test .`

## Success Criteria Checklist

- ✅ CI pipeline runs on every push (except to `main`)
- ✅ CI pipeline runs on every pull request to `main`
- ✅ Linting checks enforce code quality
- ✅ Tests must pass for CI to succeed
- ✅ Docker builds must succeed for CI to succeed
- ✅ Branch protection requires CI checks before merging
- ✅ At least 3 successful CI runs documented
- ✅ At least 1 failed run (then fixed) documented
- ✅ At least 1 pull request with CI integration created
