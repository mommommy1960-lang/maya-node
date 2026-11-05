import React from 'react';
import { Link } from 'react-router-dom';
import './Consultation.css';
const Consultation = () => (
  <div className="consultation"><section className="section"><div className="container">
    <h1>Ask About a $150 Founding-Client Checkup</h1>
    <p>We are gathering interest in a human-led AI Privacy &amp; Accuracy Checkup for the first three founding clients. It reviews up to three public or fictional AI examples and includes a report, 30-day checklist and 20-minute discussion.</p>
    <p>No paid bookings, checkout or sensitive-business-record intake are active. Please do not include passwords, customer files, employee records, payment information or other confidential data.</p>
    <Link to="/contact" className="btn btn-primary">Send a general inquiry (no payment)</Link>
  </div></section></div>
);
export default Consultation;
