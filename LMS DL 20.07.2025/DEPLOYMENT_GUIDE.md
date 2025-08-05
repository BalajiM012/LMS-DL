# Library Management System - Deployment Guide

## Overview

This guide will help you deploy the frontend to Netlify while keeping the backend running locally.

## Prerequisites

- Node.js 18+ installed
- Python 3.8+ installed
- PostgreSQL running locally
- Netlify account (free tier works)

## Step 1: Backend Setup (Local)

### 1.1 Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Ensure PostgreSQL is running
# Create database if not exists
createdb library_db
```

### 1.2 Configure Environment

```bash
# Create .env file for backend
cp .env.example .env
# Edit .env with your local database credentials
```

### 1.3 Initialize Database

```bash
# Run database migrations
python create_tables.py
python create_admin_user.py
```

### 1.4 Start Backend Server

```bash
# Start Flask backend
python app.py
# Backend will run on http://localhost:5000
```

## Step 2: Frontend Setup for Netlify

### 2.1 Install Dependencies

```bash
# Install Node.js dependencies
npm install
```

### 2.2 Configure API URL

The frontend is already configured to use `NEXT_PUBLIC_API_URL` from environment variables.

### 2.3 Build Frontend

```bash
# Build the frontend
npm run build
```

## Step 3: Deploy to Netlify

### Option A: Netlify CLI (Recommended)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy
netlify deploy --prod --dir=.next
```

### Option B: GitHub Integration

1. Push your code to GitHub
2. Connect your GitHub repo to Netlify
3. Set build command: `npm run build`
4. Set publish directory: `.next`
5. Add environment variables in Netlify dashboard

### Option C: Manual Upload

1. Build the project: `npm run build`
2. Go to Netlify dashboard
3. Drag and drop the `.next` folder (after build)

## Step 4: Environment Variables in Netlify

Add these environment variables in Netlify dashboard:

- `NEXT_PUBLIC_API_URL`: Your backend URL (e.g., `http://your-backend.com`)
- `NODE_VERSION`: `18`

## Step 5: CORS Configuration

### 5.1 Update Backend CORS

Ensure your Flask app allows CORS for the Netlify domain:

```python
# In your Flask app configuration
from flask_cors import CORS

app = create_app()
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:8000",
    "https://your-netlify-domain.netlify.app"
])
```

## Step 6: Testing

### 6.1 Local Testing

```bash
# Terminal 1: Start backend
python app.py

# Terminal 2: Start frontend
npm run dev
```

### 6.2 Production Testing

1. Deploy to Netlify
2. Ensure backend is accessible from the deployed frontend
3. Test all API endpoints

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure CORS is properly configured in backend
2. **API URL Issues**: Check `NEXT_PUBLIC_API_URL` is set correctly
3. **Build Failures**: Ensure all dependencies are installed

### Debug Commands

```bash
# Check backend is running
curl http://localhost:5000/api/health

# Check frontend build
npm run build
```

## Production Considerations

### Backend Deployment Options

When ready to deploy backend:

- **Railway**: Easy PostgreSQL + Flask deployment
- **Render**: Free tier available
- **Heroku**: Good for Python apps
- **DigitalOcean**: VPS option

### Database Migration

For production, consider:

- Using environment-specific database URLs
- Setting up database migrations
- Using connection pooling

## Support

If you encounter issues:

1. Check browser console for frontend errors
2. Check backend logs for API errors
3. Verify environment variables are set correctly
