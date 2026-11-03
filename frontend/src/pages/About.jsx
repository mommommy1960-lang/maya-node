import React from 'react';
import { Link } from 'react-router-dom';
import './About.css';
const About = () => (
  <div className="about"><section className="section"><div className="container">
    <h1>About Civic Continuum</h1>
    <div className="about-content">
      <div className="about-intro"><h2>Technology should serve humanity. Period.</h2>
        <p>Civic Continuum works toward accountable technology and systems that protect human dignity, privacy, and meaningful correction.</p>
        <p><strong>People over profit. Humanity over hierarchy. Progress over power.</strong></p>
      </div>
      <div className="about-mission"><h2>Our current focus</h2>
        <p>We are developing an AI Privacy &amp; Accuracy Checkup for small organizations using generative AI. It is a prototype undergoing evaluation, not a certified audit or a paid service currently available.</p>
      </div>
      <div className="about-values grid grid-2">
        <div className="card"><h3>Truth over appearances</h3><p>We distinguish what is demonstrated, unknown, and still under development.</p></div>
        <div className="card"><h3>Prevention and correction</h3><p>We want people to identify problems early, stop harmful processes, and verify that fixes work.</p></div>
      </div>
      <div className="about-approach"><h2>Research and development</h2>
        <p>These initiatives remain part of Civic Continuum's research portfolio. They are not currently presented as purchasable services.</p>
        <ul>
          <li><strong>Maya Node:</strong> permissions, evidence, accountability, and correction infrastructure under development.</li>
          <li><strong>SAGE:</strong> proposed human-guidance interface.</li>
          <li><strong>Aurora:</strong> long-memory and sovereign-agent research.</li>
          <li><strong>Flux:</strong> exploratory physics and propulsion research, not a demonstrated travel technology.</li>
        </ul>
      </div>
      <div className="about-cta text-center"><h2>Better systems are built together.</h2>
        <Link to="/contact" className="btn btn-primary">Contact Civic Continuum</Link>
      </div>
    </div>
  </div></section></div>
);
export default About;
