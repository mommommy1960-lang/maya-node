import React from 'react';
import './About.css';

const About = () => {
  return (
    <div className="about">
      <section className="section">
        <div className="container">
          <h1 className="fade-in">About MayaNode</h1>
          
          <div className="about-content">
            <div className="about-intro fade-in">
              <h2>Commons Verified Engineering</h2>
              <p>
                MayaNode delivers <strong>high-clarity technical frameworks, safety documentation, 
                and engineering blueprints</strong> that are ready for investors, regulators, and partners.
              </p>
              <p>
                We transform chaotic ideas into audit-ready, fundable engineering through our 
                Commons Verified methodology—ethical, Black-led, and built on the CERL-1.0 governance framework.
              </p>
            </div>

            <div className="about-mission fade-in">
              <h2>Our Mission</h2>
              <p>
                To make technical excellence accessible and verifiable. We believe that every project 
                deserves clear, professional documentation that speaks to the seriousness of the work.
              </p>
            </div>

            <div className="about-values grid grid-2 fade-in">
              <div className="card">
                <h3>🎯 Clarity</h3>
                <p>We cut through technical noise to deliver clear, actionable frameworks.</p>
              </div>
              
              <div className="card">
                <h3>🤝 Ethics</h3>
                <p>All work follows CERL-1.0 governance principles—transparent and accountable.</p>
              </div>
              
              <div className="card">
                <h3>🌍 Black-Led Excellence</h3>
                <p>Proud to center Black technical leadership in the Commons ecosystem.</p>
              </div>
              
              <div className="card">
                <h3>✨ Professional Grade</h3>
                <p>Documentation and frameworks built for serious stakeholder review.</p>
              </div>
            </div>

            <div className="about-approach fade-in">
              <h2>Our Approach</h2>
              <p>
                Every engagement begins with a <strong>Clarity Session</strong> where we understand 
                your project, stakeholders, and goals. From there, we deliver:
              </p>
              <ul>
                <li>Technical documentation that passes due diligence</li>
                <li>Safety frameworks that demonstrate responsibility</li>
                <li>Engineering blueprints ready for implementation</li>
                <li>Commons Verification that proves ethical compliance</li>
              </ul>
            </div>

            <div className="about-cta text-center fade-in">
              <h2>Ready to work with us?</h2>
              <a href="https://calendly.com/mayanode1" className="btn btn-primary" target="_blank" rel="noopener noreferrer">
                Book a Clarity Call
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
