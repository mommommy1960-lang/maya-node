import React from 'react';
import { Link } from 'react-router-dom';
import './Services.css';
const Services = () => (
  <div className="services"><section className="section"><div className="container">
    <h1 className="text-center">AI Privacy &amp; Accuracy Checkup</h1>
    <p className="services-intro text-center">A bounded, founder-led review for small organizations using AI in public-facing content. Founding-client rate: $150 for the first three engagements. Inquiries only until written terms and business readiness are confirmed.</p>
    <div className="services-grid grid grid-2">
      <div className="service-card card"><h2>Three public or fictional examples</h2><p>Review up to three AI-generated drafts without collecting confidential records or private logins.</p></div>
      <div className="service-card card"><h2>Accuracy and privacy risks</h2><p>Identify unsupported claims, potentially revealing wording, and missing human fact checks.</p></div>
      <div className="service-card card"><h2>Human-reviewed findings</h2><p>Receive concise findings and prioritized practical recommendations.</p></div>
      <div className="service-card card"><h2>30-day plan and discussion</h2><p>Receive a 30-day action checklist and a 20-minute findings call.</p></div>
    </div>
    <p><strong>Status:</strong> Research inquiries welcome. No payments, certified audits, legal compliance determination, or production Maya Node processing are available through this page.</p>
    <Link to="/contact" className="btn btn-primary">Ask about fit (no payment)</Link>
  </div></section></div>
);
export default Services;
