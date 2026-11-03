import React from 'react';
import { Link } from 'react-router-dom';
import './Consultation.css';
const Consultation = () => (
  <div className="consultation"><section className="section"><div className="container">
    <h1>Checkup Research &amp; Contact</h1>
    <p>Our AI Privacy &amp; Accuracy Checkup is in prototype development. We are not accepting paid bookings or sensitive business records through this page.</p>
    <p>For general questions about Civic Continuum, use our contact page. Do not include passwords, customer files, employee records, payment information, or other confidential data.</p>
    <Link to="/contact" className="btn btn-primary">Contact Civic Continuum</Link>
  </div></section></div>
);
export default Consultation;
