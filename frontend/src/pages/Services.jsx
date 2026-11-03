import React from 'react';
import { Link } from 'react-router-dom';
import './Services.css';
const Services = () => (
  <div className="services"><section className="section"><div className="container">
    <h1 className="text-center">AI Privacy &amp; Accuracy Mini-Checkup</h1>
    <p className="services-intro text-center">FREE for the first three confirmed participants. A small, human-led introduction to Civic Continuum's approach.</p>
    <div className="services-grid grid grid-2">
      <div className="service-card card"><h2>One public or fictional example</h2><p>We examine one AI-generated business message without collecting customer files, passwords or confidential information.</p></div>
      <div className="service-card card"><h2>Three practical suggestions</h2><p>Receive three useful ideas related to accuracy, privacy awareness or human oversight.</p></div>
      <div className="service-card card"><h2>No payment required</h2><p>No card, subscription, booking fee or obligation. Participation must be confirmed before the review begins.</p></div>
      <div className="service-card card"><h2>Clear boundaries</h2><p>Educational feedback only, not a legal, regulatory or certified security audit.</p></div>
    </div>
    <p><strong>Separate service:</strong> Our more extensive multi-example checkup is not included in this free introductory offer. Maya Node does not process customer data for this review.</p>
    <Link to="/contact" className="btn btn-primary">Ask about a free mini-checkup</Link>
  </div></section></div>
);
export default Services;
