const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs').promises;
const { logIntake, validateEmail } = require('../utils/session');

// Get all consultation requests (for admin/monitoring purposes)
router.get('/', async (req, res) => {
  try {
    const logPath = path.join(__dirname, '..', 'intake_log.json');
    const logData = await fs.readFile(logPath, 'utf8');
    const logs = JSON.parse(logData);
    
    res.json({
      success: true,
      count: logs.length,
      consultations: logs
    });
  } catch (error) {
    // If file doesn't exist, return empty array
    if (error.code === 'ENOENT') {
      res.json({
        success: true,
        count: 0,
        consultations: []
      });
    } else {
      console.error('Error reading consultation logs:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to retrieve consultation logs'
      });
    }
  }
});

// Submit full consultation request
router.post('/submit', async (req, res) => {
  try {
    const consultationData = req.body;
    
    // Validate required fields
    if (!consultationData.name || !consultationData.email) {
      return res.status(400).json({
        success: false,
        error: 'Name and email are required'
      });
    }

    // Validate email format
    if (!validateEmail(consultationData.email)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid email address'
      });
    }

    // Add metadata
    const intakeRecord = {
      ...consultationData,
      type: 'full_consultation',
      submittedAt: new Date().toISOString(),
      status: 'pending',
      id: `CONSULT-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`
    };

    // Log the intake
    await logIntake(intakeRecord);

    // Send success response
    res.json({
      success: true,
      message: 'Consultation request submitted successfully',
      consultationId: intakeRecord.id,
      nextSteps: 'You will receive an email within 24 hours to schedule your clarity call.'
    });

  } catch (error) {
    console.error('Error submitting consultation:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to submit consultation request'
    });
  }
});

// Submit contact form (simpler)
router.post('/contact', async (req, res) => {
  try {
    const { name, email, company, message } = req.body;
    
    // Validate required fields
    if (!name || !email || !message) {
      return res.status(400).json({
        success: false,
        error: 'Name, email, and message are required'
      });
    }

    // Validate email format
    if (!validateEmail(email)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid email address'
      });
    }

    // Create contact record
    const contactRecord = {
      name,
      email,
      company: company || 'Not provided',
      message,
      type: 'contact_form',
      submittedAt: new Date().toISOString(),
      status: 'pending',
      id: `CONTACT-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`
    };

    // Log the intake
    await logIntake(contactRecord);

    // Send success response
    res.json({
      success: true,
      message: 'Contact message submitted successfully',
      contactId: contactRecord.id
    });

  } catch (error) {
    console.error('Error submitting contact form:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to submit contact message'
    });
  }
});

// Get consultation by ID
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const logPath = path.join(__dirname, '..', 'intake_log.json');
    const logData = await fs.readFile(logPath, 'utf8');
    const logs = JSON.parse(logData);
    
    const consultation = logs.find(log => log.id === id);
    
    if (!consultation) {
      return res.status(404).json({
        success: false,
        error: 'Consultation not found'
      });
    }

    res.json({
      success: true,
      consultation
    });

  } catch (error) {
    console.error('Error retrieving consultation:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to retrieve consultation'
    });
  }
});

module.exports = router;
