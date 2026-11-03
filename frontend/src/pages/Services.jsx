import React from 'react';
import { Link } from 'react-router-dom';
import './Services.css';
const Services = () => (
  <div className="services"><section className="section"><div className="container">
    <h1 className="text-center">AI Privacy &amp; Accuracy Checkup</h1>
    <p className="services-intro text-center">Civic Continuum is developing one focused offering for small organizations using generative AI. This is a prototype, not yet a purchasable service.</p>
    <div className="services-grid grid grid-2">
      <div className="service-card card"><h2>Privacy safeguards</h2><p>Review approved AI tools, sensitive-information rules, and staff awareness. Do not send us customer records or other confidential materials.</p></div>
      <div className="service-card card"><h2>Accuracy safeguards</h2><p>Review human approval, independent fact-checking, and procedures for correcting AI-generated errors.</p></div>
      <div className="service-card card"><h2>Human-reviewed findings</h2><p>Our proposed service would examine evidence of safeguards and distinguish unknowns from verified gaps.</p></div>
      <div className="service-card card"><h2>30-day action plan</h2><p>Prioritize practical improvements, owners, and follow-up checks. The current demonstration uses fictional information only.</p></div>
    </div>
    <p><strong>Status:</strong> Research and development. No certification, legal compliance determination, hosted customer-data intake, or payment processing is offered through this page.</p>
    <Link to="/contact" className="btn btn-primary">Contact us with general questions</Link>
  </div></section></div>
);
export default Services;
