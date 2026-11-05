import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => (
  <div className="home">
    <section className="hero section">
      <div className="container">
        <h1 className="hero-title">Use AI with confidence. <span className="highlight">Keep people accountable.</span></h1>
        <p className="hero-description">Civic Continuum helps small organizations check public AI-generated content for accuracy, privacy concerns and clear human oversight.</p>
        <p className="hero-footnote"><strong>FREE for the first three participating businesses:</strong> One public or fictional AI-generated example reviewed, with three practical suggestions. No payment or confidential information required. Availability is confirmed individually.</p>
        <div className="hero-actions">
          <Link to="/contact" className="btn btn-primary">Ask for a free mini-checkup</Link>
          <a href="#checkup" className="btn btn-outline">How it works</a>
        </div>
      </div>
    </section>
    <section id="checkup" className="features section">
      <div className="container">
        <h2 className="text-center">AI Privacy &amp; Accuracy Mini-Checkup</h2>
        <p className="text-center">A small human-led introductory review, not an automated or certified audit.</p>
        <div className="grid grid-3">
          <div className="card"><h3>One safe example</h3><p>Choose one publicly available or fictional AI-written business message. Never share customer records or passwords.</p></div>
          <div className="card"><h3>Three practical suggestions</h3><p>Identify potential unsupported claims, privacy risks and missing human review.</p></div>
          <div className="card"><h3>Human oversight</h3><p>Learn simple ways to verify facts and correct mistakes before publishing.</p></div>
        </div>
        <p><strong>Limit:</strong> Three free introductory participants. No checkout or sensitive-data intake. Full-scope services are separate and not included in this offer.</p>
      </div>
    </section>
    <section className="cta section"><div className="container"><div className="cta-content text-center">
      <h2>People over profit. Truth over appearances.</h2>
      <p>Maya Node, SAGE, Aurora and Flux remain research and development initiatives, not products offered through this mini-checkup.</p>
      <Link to="/contact" className="btn btn-primary">Contact Civic Continuum</Link>
    </div></div></section>
  </div>
);
export default Home;
