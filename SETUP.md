# Quick Setup Guide

## One-Time Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## Running the Application

### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm start
```

## Access the Application
Open your browser and go to: http://localhost:3000

## Troubleshooting

### Port Already in Use
**Backend (Port 5000):**
```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9  # macOS/Linux
```

**Frontend (Port 3000):**
- The browser will prompt to use a different port (e.g., 3001)

### CORS Issues
Make sure the backend is running before starting the frontend.

### Module Not Found
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## Sample Data
The application comes pre-loaded with fake data including:
- 50 User Stories
- 60 Pull Requests
- 80 Test Cases
- 70 Support Tickets
- 40 Production Issues

Perfect for exploring all features!
