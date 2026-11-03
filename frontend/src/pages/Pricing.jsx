import React from 'react';
import { Link } from 'react-router-dom';
import './Pricing.css';
const Pricing = () => (
  <div className="pricing"><section className="section"><div className="container">
    <h1 className="text-center">Free Introductory Mini-Checkup</h1>
    <p className="pricing-intro text-center"><strong>$0 for the first three participating businesses.</strong> No payment, no obligation, and no confidential records.</p>
    <div className="pricing-card card">
      <h2>One example. Three suggestions.</h2>
      <p>We review one public or fictional AI-generated business example for possible factual errors, privacy concerns and missing human approval.</p>
      <p>You receive three practical suggestions from a human reviewer. This is not the full multi-example service or a 30-day consulting engagement.</p>
      <p><strong>Availability:</strong> Limited to the first three participants confirmed by Civic Continuum. Expressing interest does not guarantee a slot.</p>
      <p><strong>Payment:</strong> None. No checkout, deposit, subscription or card information.</p>
      <p>This is an educational demonstration, not legal advice, a certified audit or a compliance guarantee.</p>
      <Link to="/contact" className="btn btn-primary">Express interest for free</Link>
    </div>
  </div></section></div>
);
export default Pricing;
