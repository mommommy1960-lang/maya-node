const fs = require('fs').promises;
const path = require('path');

/**
 * Session utility functions for MayaNode consultation pipeline
 */

/**
 * Validate email address format
 * @param {string} email - Email address to validate
 * @returns {boolean} - True if valid, false otherwise
 */
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Generate a unique session ID
 * @returns {string} - Unique session ID
 */
function generateSessionId() {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substr(2, 9).toUpperCase();
  return `SESSION-${timestamp}-${random}`;
}

/**
 * Log intake data to intake_log.json
 * @param {Object} intakeData - Data to log
 * @returns {Promise<void>}
 */
async function logIntake(intakeData) {
  const logPath = path.join(__dirname, '..', 'intake_log.json');
  
  try {
    let logs = [];
    
    // Try to read existing log file
    try {
      const existingData = await fs.readFile(logPath, 'utf8');
      logs = JSON.parse(existingData);
    } catch (error) {
      // File doesn't exist or is empty, start with empty array
      if (error.code !== 'ENOENT') {
        console.error('Error reading log file:', error);
      }
    }

    // Add new entry
    logs.push({
      ...intakeData,
      loggedAt: new Date().toISOString()
    });

    // Write back to file
    await fs.writeFile(logPath, JSON.stringify(logs, null, 2), 'utf8');
    
    console.log(`Intake logged: ${intakeData.id || intakeData.type}`);
    
  } catch (error) {
    console.error('Error logging intake:', error);
    throw error;
  }
}

/**
 * Get all intake logs
 * @returns {Promise<Array>} - Array of intake records
 */
async function getIntakeLogs() {
  const logPath = path.join(__dirname, '..', 'intake_log.json');
  
  try {
    const data = await fs.readFile(logPath, 'utf8');
    return JSON.parse(data);
  } catch (error) {
    if (error.code === 'ENOENT') {
      return [];
    }
    throw error;
  }
}

/**
 * Get intake log by ID
 * @param {string} id - Intake record ID
 * @returns {Promise<Object|null>} - Intake record or null if not found
 */
async function getIntakeById(id) {
  const logs = await getIntakeLogs();
  return logs.find(log => log.id === id) || null;
}

/**
 * Update intake status
 * @param {string} id - Intake record ID
 * @param {string} status - New status
 * @returns {Promise<boolean>} - True if updated, false if not found
 */
async function updateIntakeStatus(id, status) {
  const logPath = path.join(__dirname, '..', 'intake_log.json');
  const logs = await getIntakeLogs();
  
  const index = logs.findIndex(log => log.id === id);
  if (index === -1) {
    return false;
  }

  logs[index].status = status;
  logs[index].lastUpdated = new Date().toISOString();

  await fs.writeFile(logPath, JSON.stringify(logs, null, 2), 'utf8');
  return true;
}

/**
 * Sanitize user input to prevent injection attacks
 * @param {string} input - User input to sanitize
 * @returns {string} - Sanitized input
 */
function sanitizeInput(input) {
  if (typeof input !== 'string') {
    return input;
  }
  
  // Remove any potentially harmful characters
  return input
    .replace(/[<>]/g, '') // Remove HTML tags
    .trim();
}

/**
 * Create a consultation summary
 * @param {Object} consultationData - Consultation data
 * @returns {string} - Human-readable summary
 */
function createConsultationSummary(consultationData) {
  const {
    name,
    email,
    company,
    projectName,
    projectStage,
    serviceType,
    timeline,
    budget
  } = consultationData;

  return `
Consultation Request Summary
============================
Name: ${name}
Email: ${email}
Company: ${company || 'Not provided'}
Project: ${projectName || 'Not specified'}
Stage: ${projectStage || 'Not specified'}
Service: ${serviceType || 'Not specified'}
Timeline: ${timeline || 'Not specified'}
Budget: ${budget || 'Not specified'}
Submitted: ${new Date().toISOString()}
  `.trim();
}

module.exports = {
  validateEmail,
  generateSessionId,
  logIntake,
  getIntakeLogs,
  getIntakeById,
  updateIntakeStatus,
  sanitizeInput,
  createConsultationSummary
};
