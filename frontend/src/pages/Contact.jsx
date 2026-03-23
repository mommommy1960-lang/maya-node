import React, { useState } from 'react';
import './Contact.css';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    message: ''
  });

  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('/api/consultation/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setSubmitted(true);
        setFormData({ name: '', email: '', company: '', message: '' });
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      alert('There was an error submitting your message. Please try again or email us directly.');
    }
  };

  return (
    <div className="contact">
      <section className="section">
        <div className="container">
          <h1 className="text-center fade-in">Contact Us</h1>
          <p className="contact-intro text-center text-muted fade-in">
            Have questions? We're here to help. Reach out and we'll get back to you within 24 hours.
          </p>

          <div className="contact-content grid grid-2">
            <div className="contact-info fade-in">
              <h2>Get in Touch</h2>
              <p>
                Whether you have a question about our services, pricing, or anything else, 
                our team is ready to answer all your questions.
              </p>

              <div className="contact-methods">
                <div className="contact-method">
                  <div className="method-icon">📅</div>
                  <div className="method-content">
                    <h3>Book a Call</h3>
                    <p>Schedule a free 15-minute intro call to discuss your project.</p>
                    <a href="https://calendly.com/mayanode1" target="_blank" rel="noopener noreferrer" className="btn btn-outline">
                      View Calendar
                    </a>
                  </div>
                </div>

                <div className="contact-method">
                  <div className="method-icon">📧</div>
                  <div className="method-content">
                    <h3>Email Us</h3>
                    <p>For general inquiries and support.</p>
                    <a href="mailto:hello@mayanode.com" className="contact-link">
                      hello@mayanode.com
                    </a>
                  </div>
                </div>

                <div className="contact-method">
                  <div className="method-icon">🌍</div>
                  <div className="method-content">
                    <h3>Location</h3>
                    <p>Remote-first, serving clients worldwide</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="contact-form-container fade-in">
              {submitted ? (
                <div className="success-message card">
                  <div className="success-icon">✅</div>
                  <h3>Thank you for reaching out!</h3>
                  <p>We've received your message and will get back to you within 24 hours.</p>
                  <button onClick={() => setSubmitted(false)} className="btn btn-outline">
                    Send Another Message
                  </button>
                </div>
              ) : (
                <form className="contact-form card" onSubmit={handleSubmit}>
                  <h3>Send us a message</h3>
                  
                  <div className="form-group">
                    <label htmlFor="name">Name *</label>
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
                    <label htmlFor="email">Email *</label>
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
                    <label htmlFor="message">Message *</label>
                    <textarea
                      id="message"
                      name="message"
                      rows="5"
                      value={formData.message}
                      onChange={handleChange}
                      required
                    />
                  </div>

                  <button type="submit" className="btn btn-primary full-width">
                    Send Message
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Contact;
