import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => (
  <div className="home">
    <section className="hero section">
      <div className="container">
        <h1 className="hero-title">Use AI with confidence. <span className="highlight">Keep people accountable.</span></h1>
        <p className="hero-description">Civic Continuum helps small organizations examine how they protect sensitive information and check important AI-generated answers. Technology should serve humanity, not the other way around.</p>
        <p className="hero-footnote"><strong>In development:</strong> Founding-client rate: $150 for the first three human-led checkups. General inquiries welcome; no payment or booking is active. Please do not submit confidential information.</p>
        <div className="hero-actions">
          <a href="#checkup" className="btn btn-primary">Explore the Checkup</a>
          <Link to="/contact" className="btn btn-outline">Contact Civic Continuum</Link>
        </div>
      </div>
    </section>
    <section id="checkup" className="features section">
      <div className="container">
        <h2 className="text-center">AI Privacy &amp; Accuracy Checkup</h2>
        <p className="text-center">A focused, human-reviewed approach to finding practical safeguards, not another automatic certificate.</p>
        <div className="grid grid-3">
          <div className="card"><h3>Protect information</h3><p>Identify approved AI tools and establish rules for sensitive customer, employee, and business information.</p></div>
          <div className="card"><h3>Verify AI answers</h3><p>Clarify when a person must check facts against trusted sources before acting on an AI-generated result.</p></div>
          <div className="card"><h3>Correct problems</h3><p>Assign responsible people, document issues, and create a prioritized improvement plan.</p></div>
        </div>
        <p><strong>Current status:</strong> Fictional sample reports and no-payment inquiries only. No production Maya Node processing, live billing, or claims of NIST endorsement.</p>
      </div>
    </section>
    <section className="cta section">
      <div className="container">
        <div className="cta-content text-center">
          <h2>People over profit. Truth over appearances.</h2>
          <p>Our mission is to make responsibility visible, keep human decisions accountable, and make correction possible.</p>
          <p>Maya Node, SAGE, Aurora, and Flux remain research and development work, not services offered for purchase here.</p>
          <Link to="/about" className="btn btn-primary">Our Mission</Link>
        </div>
      </div>
    </section>
  </div>
);
export default Home;
