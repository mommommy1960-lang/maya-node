import React from 'react';
import { Link } from 'react-router-dom';
import './Pricing.css';
const Pricing = () => (
  <div className="pricing"><section className="section"><div className="container">
    <h1 className="text-center">Checkup Availability</h1>
    <p className="pricing-intro text-center">The Civic Continuum AI Privacy &amp; Accuracy Checkup is in development. It is not available for purchase.</p>
    <div className="pricing-card card"><h2>Proposed human-reviewed checkup</h2>
      <p>Planned scope: privacy and accuracy safeguards, evidence review, and a prioritized 30-day improvement plan.</p>
      <p><strong>Price:</strong> Not established. A $250 price has been discussed as a research hypothesis, not an offer.</p>
      <p><strong>Billing:</strong> Disabled for this prototype. No checkout or payment link is provided.</p>
      <p>This is not a NIST certification, security audit, or legal compliance determination.</p>
      <Link to="/services" className="btn btn-primary">Read about the Checkup</Link>
    </div>
  </div></section></div>
);
export default Pricing;
