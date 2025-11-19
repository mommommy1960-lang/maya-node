const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
require('dotenv').config();

const consultationRoutes = require('./routes/consultation');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Routes
app.use('/api/consultation', consultationRoutes);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'MayaNode API'
  });
});

// Root endpoint
app.get('/api', (req, res) => {
  res.json({
    message: 'MayaNode API Server',
    version: '1.0.0',
    endpoints: {
      health: '/api/health',
      consultation: '/api/consultation',
      consultationSubmit: '/api/consultation/submit',
      consultationContact: '/api/consultation/contact'
    }
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: err.message
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    path: req.path
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════╗
║   MayaNode API Server Running        ║
║   Port: ${PORT}                      ║
║   Environment: ${process.env.NODE_ENV || 'development'}           ║
║   Time: ${new Date().toISOString()}  ║
╚═══════════════════════════════════════╝
  `);
});

module.exports = app;
