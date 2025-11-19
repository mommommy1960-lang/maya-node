import React from 'react';
import './Services.css';

const Services = () => {
  return (
    <div className="services">
      <section className="section">
        <div className="container">
          <h1 className="text-center fade-in">Our Services</h1>
          <p className="services-intro text-center text-muted fade-in">
            Commons Verified Engineering & Knowledge Services designed for clarity, compliance, and confidence.
          </p>

          <div className="services-grid grid grid-2">
            <div className="service-card card fade-in">
              <div className="service-icon">📋</div>
              <h3>Technical Documentation</h3>
              <p>
                Transform complex systems into clear, professional documentation that stakeholders trust. 
                Perfect for due diligence, investor presentations, and regulatory compliance.
              </p>
              <ul className="service-features">
                <li>Architecture diagrams & system overviews</li>
                <li>API documentation & integration guides</li>
                <li>Security & compliance frameworks</li>
                <li>User & developer documentation</li>
              </ul>
            </div>

            <div className="service-card card fade-in">
              <div className="service-icon">🛡️</div>
              <h3>Safety Frameworks</h3>
              <p>
                Demonstrate responsibility and ethical governance with comprehensive safety documentation 
                aligned with CERL-1.0 principles.
              </p>
              <ul className="service-features">
                <li>Risk assessment & mitigation plans</li>
                <li>Ethical AI & data governance</li>
                <li>Incident response procedures</li>
                <li>Compliance verification reports</li>
              </ul>
            </div>

            <div className="service-card card fade-in">
              <div className="service-icon">🏗️</div>
              <h3>Engineering Blueprints</h3>
              <p>
                Detailed technical roadmaps and implementation plans ready for development teams 
                and technical stakeholders.
              </p>
              <ul className="service-features">
                <li>System architecture design</li>
                <li>Technology stack recommendations</li>
                <li>Implementation timelines & milestones</li>
                <li>Resource planning & budgeting</li>
              </ul>
            </div>

            <div className="service-card card fade-in">
              <div className="service-icon">✅</div>
              <h3>Commons Verification</h3>
              <p>
                Prove ethical compliance and transparent governance through our Commons Verified certification process.
              </p>
              <ul className="service-features">
                <li>CERL-1.0 compliance audit</li>
                <li>Ethics & governance review</li>
                <li>Transparency documentation</li>
                <li>Verification badge & certificate</li>
              </ul>
            </div>

            <div className="service-card card fade-in">
              <div className="service-icon">💬</div>
              <h3>Clarity Sessions</h3>
              <p>
                1:1 consultation to align your project vision, identify documentation needs, 
                and create an actionable clarity roadmap.
              </p>
              <ul className="service-features">
                <li>Project assessment & scoping</li>
                <li>Stakeholder analysis</li>
                <li>Documentation gap analysis</li>
                <li>Customized action plan</li>
              </ul>
            </div>

            <div className="service-card card fade-in">
              <div className="service-icon">📊</div>
              <h3>Snapshot Lite</h3>
              <p>
                Quick-start technical snapshot for early-stage projects. Get immediate clarity 
                on your project's documentation needs.
              </p>
              <ul className="service-features">
                <li>30-minute rapid assessment</li>
                <li>High-level documentation outline</li>
                <li>Priority recommendations</li>
                <li>Next steps roadmap</li>
              </ul>
            </div>
          </div>

          <div className="services-cta text-center">
            <h2>Not sure which service you need?</h2>
            <p className="text-muted">
              Start with a free clarity call to discuss your project and find the right solution.
            </p>
            <a href="https://calendly.com/mayanode1" className="btn btn-primary" target="_blank" rel="noopener noreferrer">
              Schedule a Free Clarity Call
            </a>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Services;
