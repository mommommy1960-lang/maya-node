# MayaNode Quick Start Guide

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/mommommy1960-lang/maya-node.git
cd maya-node
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`

### 3. Backend Setup (in a new terminal)
```bash
cd backend
npm install
npm start
```
The API will be available at `http://localhost:5000`

## Quick Test

### Test Frontend
Open your browser to `http://localhost:5173` and navigate through:
- Home page with hero section
- About page
- Services page
- Pricing page
- Contact page
- Consultation page (multi-step form)

### Test Backend API
```bash
# Health check
curl http://localhost:5000/api/health

# API info
curl http://localhost:5000/api

# Get consultations
curl http://localhost:5000/api/consultation
```

## Project Structure
```
maya-node/
├── frontend/              # React + Vite app
│   ├── src/
│   │   ├── pages/        # All page components
│   │   ├── App.jsx       # Main app with routing
│   │   ├── Navbar.jsx    # Navigation component
│   │   └── Theme.css     # Global theme
│   └── package.json
│
├── backend/               # Node.js + Express API
│   ├── routes/           # API routes
│   ├── utils/            # Utilities (session.js)
│   ├── server.js         # Main server
│   └── intake_log.json   # Consultation logs
│
└── FULLSTACK_README.md   # Complete documentation
```

## Key Features

### Frontend
- ✅ React 18 + Vite
- ✅ React Router for navigation
- ✅ Responsive design
- ✅ Theme system with CSS variables
- ✅ Stripe payment integration
- ✅ 6 complete pages (Home, About, Services, Pricing, Contact, Consultation)
- ✅ Multi-step consultation form

### Backend
- ✅ Express REST API
- ✅ CORS enabled
- ✅ Consultation intake system
- ✅ JSON-based logging
- ✅ Session utilities
- ✅ Error handling

## Build for Production

### Frontend
```bash
cd frontend
npm run build
# Output will be in frontend/dist/
```

### Backend
```bash
cd backend
NODE_ENV=production npm start
```

## Next Steps

1. **Configure Environment**: Copy `backend/.env.example` to `backend/.env` and configure
2. **Customize Content**: Update page content in `frontend/src/pages/`
3. **API Integration**: Connect frontend to backend (update API URLs)
4. **Deploy**: 
   - Frontend: Deploy `frontend/dist/` to static hosting
   - Backend: Deploy to Node.js hosting

## Support

For issues or questions:
- Check `FULLSTACK_README.md` for detailed documentation
- Visit: https://calendly.com/mayanode1

---

Built with Commons Verified Engineering principles 🌟
