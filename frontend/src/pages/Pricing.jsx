import React from 'react';
import './Pricing.css';

const Pricing = () => {
  return (
    <div className="pricing">
      <section className="section">
        <div className="container">
          <h1 className="text-center fade-in">Pricing & Offers</h1>
          <p className="pricing-intro text-center text-muted fade-in">
            Transparent pricing for Commons Verified Engineering services. Choose the option that fits your needs.
          </p>

          <div className="pricing-grid grid grid-3">
            <div className="pricing-card card fade-in">
              <div className="pricing-badge">Quick Start</div>
              <h3>Snapshot Lite</h3>
              <div className="pricing-price">
                <span className="price-amount">$297</span>
                <span className="price-period">one-time</span>
              </div>
              <p className="pricing-description">
                Perfect for early-stage projects needing immediate clarity on documentation needs.
              </p>
              <ul className="pricing-features">
                <li>30-minute rapid assessment</li>
                <li>High-level documentation outline</li>
                <li>Priority recommendations</li>
                <li>Next steps roadmap</li>
                <li>Email support for 1 week</li>
              </ul>
              <div className="pricing-action">
                <stripe-buy-button
                  buy-button-id="buy_btn_1SUE64FFZvHRvAyGNWQFxtzJ"
                  publishable-key="pk_live_51SSi1lFFZvHRvAyGArN5osMN9hKFjmNhd10RtIUFav2ZbBTMCKBV6TUj6hWxY9N78GpORe0q5KCzt7zzd2gZkzIp00G4tF1y7G">
                </stripe-buy-button>
              </div>
            </div>

            <div className="pricing-card card featured fade-in">
              <div className="pricing-badge featured">Most Popular</div>
              <h3>Clarity Session</h3>
              <div className="pricing-price">
                <span className="price-amount">$997</span>
                <span className="price-period">per session</span>
              </div>
              <p className="pricing-description">
                Deep-dive consultation to align your project and create an actionable clarity roadmap.
              </p>
              <ul className="pricing-features">
                <li>90-minute 1:1 consultation</li>
                <li>Project assessment & scoping</li>
                <li>Stakeholder analysis</li>
                <li>Documentation gap analysis</li>
                <li>Customized action plan</li>
                <li>2 weeks email support</li>
                <li>Follow-up check-in call</li>
              </ul>
              <div className="pricing-action">
                <a href="https://calendly.com/mayanode1" className="btn btn-primary full-width" target="_blank" rel="noopener noreferrer">
                  Book Clarity Session
                </a>
              </div>
            </div>

            <div className="pricing-card card fade-in">
              <div className="pricing-badge">Enterprise</div>
              <h3>Custom Engagement</h3>
              <div className="pricing-price">
                <span className="price-amount">Custom</span>
                <span className="price-period">quote</span>
              </div>
              <p className="pricing-description">
                Full-service Commons Verified documentation, safety frameworks, and engineering blueprints.
              </p>
              <ul className="pricing-features">
                <li>Complete technical documentation</li>
                <li>Safety & compliance frameworks</li>
                <li>Engineering blueprints</li>
                <li>Commons Verification</li>
                <li>Dedicated project manager</li>
                <li>Unlimited revisions</li>
                <li>6 months support</li>
              </ul>
              <div className="pricing-action">
                <a href="https://calendly.com/mayanode1" className="btn btn-outline full-width" target="_blank" rel="noopener noreferrer">
                  Request Quote
                </a>
              </div>
            </div>
          </div>

          <div className="pricing-faq">
            <h2 className="text-center">Frequently Asked Questions</h2>
            <div className="faq-grid grid grid-2">
              <div className="faq-item card">
                <h4>What is Commons Verified?</h4>
                <p>
                  Commons Verified means your documentation meets CERL-1.0 ethical governance standards 
                  and has been independently reviewed for transparency, safety, and compliance.
                </p>
              </div>

              <div className="faq-item card">
                <h4>How long does a typical engagement take?</h4>
                <p>
                  Snapshot Lite delivers in 3-5 business days. Clarity Sessions are scheduled within 1 week. 
                  Custom engagements vary from 2-8 weeks depending on scope.
                </p>
              </div>

              <div className="faq-item card">
                <h4>Do you offer refunds?</h4>
                <p>
                  We stand behind our work. If you're not satisfied with a Snapshot Lite or Clarity Session, 
                  contact us within 7 days for a full refund.
                </p>
              </div>

              <div className="faq-item card">
                <h4>Can I upgrade my service?</h4>
                <p>
                  Absolutely! Snapshot Lite and Clarity Session fees can be applied toward a Custom Engagement 
                  if you decide to expand your project scope.
                </p>
              </div>
            </div>
          </div>

          <div className="pricing-cta text-center">
            <h2>Still have questions?</h2>
            <p className="text-muted">
              Schedule a free 15-minute intro call to discuss your project and find the right service.
            </p>
            <a href="https://calendly.com/mayanode1" className="btn btn-primary" target="_blank" rel="noopener noreferrer">
              Schedule Free Intro Call
            </a>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Pricing;
