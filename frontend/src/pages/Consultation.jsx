import React, { useState } from 'react';
import './Consultation.css';

const Consultation = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    // Step 1: Contact Information
    name: '',
    email: '',
    company: '',
    phone: '',
    
    // Step 2: Project Information
    projectName: '',
    projectStage: '',
    projectDescription: '',
    
    // Step 3: Service Selection
    serviceType: '',
    timeline: '',
    budget: '',
    
    // Step 4: Additional Information
    challenges: '',
    goals: '',
    additionalNotes: ''
  });

  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const nextStep = () => {
    setStep(step + 1);
  };

  const prevStep = () => {
    setStep(step - 1);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('/api/consultation/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          timestamp: new Date().toISOString()
        })
      });

      if (response.ok) {
        setSubmitted(true);
      }
    } catch (error) {
      console.error('Error submitting consultation request:', error);
      alert('There was an error submitting your request. Please try again or book directly via Calendly.');
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="form-step fade-in">
            <h3>Step 1: Contact Information</h3>
            <div className="form-group">
              <label htmlFor="name">Full Name *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email Address *</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="company">Company / Organization</label>
              <input
                type="text"
                id="company"
                name="company"
                value={formData.company}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="phone">Phone Number (optional)</label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
              />
            </div>
          </div>
        );

      case 2:
        return (
          <div className="form-step fade-in">
            <h3>Step 2: Project Information</h3>
            <div className="form-group">
              <label htmlFor="projectName">Project Name *</label>
              <input
                type="text"
                id="projectName"
                name="projectName"
                value={formData.projectName}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="projectStage">Project Stage *</label>
              <select
                id="projectStage"
                name="projectStage"
                value={formData.projectStage}
                onChange={handleChange}
                required
              >
                <option value="">Select stage...</option>
                <option value="idea">Idea / Concept</option>
                <option value="planning">Planning</option>
                <option value="development">In Development</option>
                <option value="testing">Testing / Beta</option>
                <option value="launched">Launched</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="projectDescription">Project Description *</label>
              <textarea
                id="projectDescription"
                name="projectDescription"
                rows="5"
                value={formData.projectDescription}
                onChange={handleChange}
                placeholder="Tell us about your project..."
                required
              />
            </div>
          </div>
        );

      case 3:
        return (
          <div className="form-step fade-in">
            <h3>Step 3: Service Selection</h3>
            <div className="form-group">
              <label htmlFor="serviceType">Service Type *</label>
              <select
                id="serviceType"
                name="serviceType"
                value={formData.serviceType}
                onChange={handleChange}
                required
              >
                <option value="">Select service...</option>
                <option value="snapshot">Snapshot Lite ($297)</option>
                <option value="clarity">Clarity Session ($997)</option>
                <option value="documentation">Technical Documentation</option>
                <option value="safety">Safety Frameworks</option>
                <option value="blueprints">Engineering Blueprints</option>
                <option value="verification">Commons Verification</option>
                <option value="custom">Custom Engagement</option>
                <option value="unsure">Not Sure Yet</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="timeline">Desired Timeline *</label>
              <select
                id="timeline"
                name="timeline"
                value={formData.timeline}
                onChange={handleChange}
                required
              >
                <option value="">Select timeline...</option>
                <option value="urgent">Urgent (1-2 weeks)</option>
                <option value="soon">Soon (2-4 weeks)</option>
                <option value="flexible">Flexible (1-2 months)</option>
                <option value="planning">Just Planning</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="budget">Budget Range</label>
              <select
                id="budget"
                name="budget"
                value={formData.budget}
                onChange={handleChange}
              >
                <option value="">Select budget range...</option>
                <option value="under-1k">Under $1,000</option>
                <option value="1k-5k">$1,000 - $5,000</option>
                <option value="5k-10k">$5,000 - $10,000</option>
                <option value="10k-25k">$10,000 - $25,000</option>
                <option value="25k-plus">$25,000+</option>
                <option value="unsure">Not Sure Yet</option>
              </select>
            </div>
          </div>
        );

      case 4:
        return (
          <div className="form-step fade-in">
            <h3>Step 4: Tell Us More</h3>
            <div className="form-group">
              <label htmlFor="challenges">What challenges are you facing? *</label>
              <textarea
                id="challenges"
                name="challenges"
                rows="4"
                value={formData.challenges}
                onChange={handleChange}
                placeholder="e.g., unclear documentation, regulatory concerns, investor requirements..."
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="goals">What are your goals for this engagement? *</label>
              <textarea
                id="goals"
                name="goals"
                rows="4"
                value={formData.goals}
                onChange={handleChange}
                placeholder="e.g., pass due diligence, secure funding, launch safely..."
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="additionalNotes">Additional Notes</label>
              <textarea
                id="additionalNotes"
                name="additionalNotes"
                rows="3"
                value={formData.additionalNotes}
                onChange={handleChange}
                placeholder="Anything else we should know?"
              />
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  if (submitted) {
    return (
      <div className="consultation">
        <section className="section">
          <div className="container">
            <div className="success-container card text-center fade-in">
              <div className="success-icon">✅</div>
              <h2>Consultation Request Received!</h2>
              <p className="text-muted">
                Thank you for your interest in MayaNode services. We've received your consultation request 
                and will review it carefully.
              </p>
              <p className="text-muted">
                You'll hear from us within 24 hours to schedule your clarity call.
              </p>
              <div className="success-actions">
                <a href="/" className="btn btn-primary">
                  Return to Home
                </a>
                <a href="https://calendly.com/mayanode1" className="btn btn-outline" target="_blank" rel="noopener noreferrer">
                  Or Book Directly on Calendly
                </a>
              </div>
            </div>
          </div>
        </section>
      </div>
    );
  }

  return (
    <div className="consultation">
      <section className="section">
        <div className="container">
          <h1 className="text-center fade-in">Book a Consultation</h1>
          <p className="consultation-intro text-center text-muted fade-in">
            Complete this form to help us understand your needs and schedule the perfect clarity call.
          </p>

          <div className="consultation-content">
            <div className="progress-bar">
              <div className={`progress-step ${step >= 1 ? 'active' : ''}`}>
                <div className="step-number">1</div>
                <div className="step-label">Contact</div>
              </div>
              <div className={`progress-step ${step >= 2 ? 'active' : ''}`}>
                <div className="step-number">2</div>
                <div className="step-label">Project</div>
              </div>
              <div className={`progress-step ${step >= 3 ? 'active' : ''}`}>
                <div className="step-number">3</div>
                <div className="step-label">Service</div>
              </div>
              <div className={`progress-step ${step >= 4 ? 'active' : ''}`}>
                <div className="step-number">4</div>
                <div className="step-label">Details</div>
              </div>
            </div>

            <form className="consultation-form card" onSubmit={handleSubmit}>
              {renderStep()}

              <div className="form-actions">
                {step > 1 && (
                  <button type="button" onClick={prevStep} className="btn btn-secondary">
                    Previous
                  </button>
                )}
                {step < 4 ? (
                  <button type="button" onClick={nextStep} className="btn btn-primary">
                    Next Step
                  </button>
                ) : (
                  <button type="submit" className="btn btn-primary">
                    Submit Request
                  </button>
                )}
              </div>
            </form>

            <div className="consultation-alternative text-center">
              <p className="text-muted">
                Prefer to book directly?
              </p>
              <a href="https://calendly.com/mayanode1" className="btn btn-outline" target="_blank" rel="noopener noreferrer">
                View Calendar & Book Now
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Consultation;
