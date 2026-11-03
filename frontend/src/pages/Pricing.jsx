import React from 'react';
import { Link } from 'react-router-dom';
import './Pricing.css';
const Pricing = () => (
  <div className="pricing"><section className="section"><div className="container">
    <h1 className="text-center">AI Privacy &amp; Accuracy Checkup</h1>
    <p className="pricing-intro text-center">Founding-client rate: <strong>$150</strong> for each of the first three agreed engagements. Inquiries welcome; payment and booking are not yet active.</p>
    <div className="pricing-card card"><h2>Human-reviewed, fixed-scope checkup</h2>
      <p>Review up to three public or fictional AI-generated examples for factual accuracy, privacy exposure and human oversight gaps.</p>
      <p>Receive concise findings, prioritized recommendations, a 30-day checklist and a 20-minute findings discussion.</p>
      <p><strong>Price:</strong> $150 founding-client rate, limited to the first three engagements, subject to agreed written terms and business readiness.</p>
      <p><strong>Payment:</strong> No checkout, deposit, or payment link is active. Please do not send confidential records or private login details.</p>
      <p>Educational review only, not a certified audit, legal advice or a guarantee of compliance.</p>
      <Link to="/contact" className="btn btn-primary">Ask about availability (no payment)</Link>
    </div>
  </div></section></div>
);
export default Pricing;
