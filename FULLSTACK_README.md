# MayaNode - Commons Verified Engineering

Full-stack web application for MayaNode's Commons Verified Engineering & Knowledge Services.

## Project Structure

```
maya-node/
├── frontend/          # React + Vite frontend application
│   ├── src/
│   │   ├── pages/    # Page components
│   │   ├── Navbar.jsx
│   │   ├── App.jsx
│   │   └── Theme.css
│   └── package.json
├── backend/           # Node.js + Express API server
│   ├── routes/       # API route handlers
│   ├── utils/        # Utility functions
│   ├── server.js     # Main server file
│   └── intake_log.json  # Consultation intake logs
└── README.md
```

## Features

### Frontend (React + Vite)
- **Modern React Application**: Built with Vite for fast development and optimized builds
- **Full Page Suite**: 
  - Home - Hero section with service overview
  - About - Mission, values, and approach
  - Services - Detailed service offerings
  - Pricing - Transparent pricing with Stripe integration
  - Contact - Contact form with backend integration
  - Consultation - Multi-step consultation request pipeline
- **Responsive Design**: Mobile-first, fully responsive across all devices
- **Theme System**: Centralized theme with CSS variables
- **Stripe Integration**: Ready for payment processing
- **React Router**: Client-side routing for smooth navigation

### Backend (Node.js + Express)
- **RESTful API**: Clean, well-documented API endpoints
- **Consultation Pipeline**: Multi-step consultation request handling
- **Intake Logging**: JSON-based logging system for all requests
- **Session Management**: Utility functions for validation and data handling
- **CORS Enabled**: Ready for frontend integration
- **Error Handling**: Comprehensive error handling middleware

## Installation

### Prerequisites
- Node.js 18+ and npm
- Git

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:5173`

### Backend Setup

```bash
cd backend
npm install

# Copy environment template
cp .env.example .env

# Start server
npm start
```

The backend API will run on `http://localhost:5000`

## Development

### Frontend Development
```bash
cd frontend
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
```

### Backend Development
```bash
cd backend
npm start        # Start server
npm run dev      # Start with nodemon (requires installation)
```

## API Endpoints

### Health Check
```
GET /api/health
```

### Consultation Routes
```
GET  /api/consultation           # Get all consultations
POST /api/consultation/submit    # Submit full consultation request
POST /api/consultation/contact   # Submit contact form
GET  /api/consultation/:id       # Get consultation by ID
```

## Environment Variables

### Backend (.env)
```
PORT=5000
NODE_ENV=development
```

See `backend/.env.example` for full configuration options.

## Deployment

### Frontend (Static Site)
```bash
cd frontend
npm run build
# Deploy the 'dist' folder to your static hosting (Netlify, Vercel, etc.)
```

### Backend (Node.js Server)
```bash
cd backend
# Set environment variables
NODE_ENV=production
PORT=5000

# Start server
npm start
```

## Tech Stack

### Frontend
- React 18
- Vite
- React Router DOM
- CSS Variables (Custom Theme)
- Stripe Buy Button

### Backend
- Node.js
- Express
- CORS
- Body Parser
- dotenv

## License

This project is licensed under CERL-1.0 (Commons Ethical Reciprocity License).

## Contact

- Website: https://mommommy1960-lang.github.io/maya-node/
- Calendly: https://calendly.com/mayanode1

## Commons Verified

This project follows CERL-1.0 governance principles and represents ethical, Black-led technical excellence in the Commons ecosystem.

---

Built with ❤️ by MayaNode
