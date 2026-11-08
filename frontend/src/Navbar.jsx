import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => (
  <nav className="navbar" aria-label="Main navigation">
    <div className="container">
      <div className="nav-content">
        <Link to="/" className="nav-logo">Civic Continuum</Link>
        <div className="nav-links">
          <Link to="/" className="nav-link">Home</Link>
          <a href="/#checkup" className="nav-link">AI Checkup</a>
          <Link to="/about" className="nav-link">Mission &amp; Research</Link>
          <Link to="/contact" className="nav-link">Contact</Link>
        </div>
      </div>
    </div>
  </nav>
);
export default Navbar;
