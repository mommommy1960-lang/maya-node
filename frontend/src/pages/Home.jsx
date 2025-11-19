import React from 'react';
import './Home.css';

const Home = () => {
  return (
    <div className="home">
      <section className="hero section">
        <div className="container">
          <h1 className="hero-title fade-in">
            Turn chaotic ideas into <span className="highlight">audit-ready, fundable engineering.</span>
          </h1>
          
          <p className="hero-description fade-in">
            MayaNode is your <strong>Commons Verified Engineering & Knowledge Service</strong>: 
            high-clarity frameworks, safety docs, and technical blueprints ready for investors, 
            regulators, and partners.
          </p>

          <div className="hero-actions fade-in">
            <a href="https://calendly.com/mayanode1" className="btn btn-primary" target="_blank" rel="noopener noreferrer">
              Request a Consult
            </a>
            <a href="#pricing" className="btn btn-outline">
              View Pricing & Offers
            </a>
          </div>

          <div className="hero-stripe fade-in">
            <p className="hero-stripe-label">Or start instantly with Snapshot Lite:</p>
            
            <div className="stripe-button-container">
              <stripe-buy-button
                buy-button-id="buy_btn_1SUE64FFZvHRvAyGNWQFxtzJ"
                publishable-key="pk_live_51SSi1lFFZvHRvAyGArN5osMN9hKFjmNhd10RtIUFav2ZbBTMCKBV6TUj6hWxY9N78GpORe0q5KCzt7zzd2gZkzIp00G4tF1y7G">
              </stripe-buy-button>
            </div>

            <p className="quote-tagline">
              First Commons Initiative deployment to integrate Stripe + Calendly across a verified engineering workflow.
            </p>
          </div>

          <p className="hero-footnote fade-in">
            Built for <span className="text-accent" style={{fontWeight: 600}}>founders, researchers, & organizations</span> tired of messy pitches and vague decks.
          </p>
        </div>
      </section>

      <section className="features section">
        <div className="container">
          <h2 className="text-center">Why MayaNode?</h2>
          <div className="grid grid-3">
            <div className="card">
              <h3>🎯 Clarity First</h3>
              <p>Transform messy ideas into clear, structured documentation that stakeholders trust.</p>
            </div>
            <div className="card">
              <h3>✅ Commons Verified</h3>
              <p>Ethical, transparent engineering backed by CERL-1.0 governance framework.</p>
            </div>
            <div className="card">
              <h3>🚀 Investor Ready</h3>
              <p>Technical blueprints designed for due diligence, audits, and funding rounds.</p>
            </div>
          </div>
        </div>
      </section>

      <section id="pricing" className="cta section">
        <div className="container">
          <div className="cta-content text-center">
            <h2>Ready to get clarity?</h2>
            <p className="text-muted">
              Book a dedicated 1:1 clarity session to align your project, documentation, or technical roadmap.
            </p>
            <a href="https://calendly.com/mayanode1" className="btn btn-primary" target="_blank" rel="noopener noreferrer">
              Schedule a Clarity Session
            </a>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
