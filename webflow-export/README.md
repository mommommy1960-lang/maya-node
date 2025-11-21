# MayaNode Webflow Export

This folder contains a complete, Webflow-ready multipage site for MayaNode Commons Verified Engineering.

## 🎨 Design Theme

- **Colors**: Black + White + Soft Gold
- **Aesthetic**: Clean, modern, professional
- **Animations**: Smooth scroll interactions, subtle reveals
- **Responsive**: Mobile-first design with full responsive support

## 📁 Structure

```
webflow-export/
├── index.html              # Home page
├── about-commons.html      # About the Commons
├── aurora-origin.html      # Aurora Origin story
├── consultation.html       # Consultation services
├── contact.html            # Contact form
├── legal.html              # CERL-1.0 License & legal
├── volume-i.html           # Volume I table of contents
├── css/
│   └── global.css          # All styles in one file
├── js/
│   └── main.js             # All interactions in vanilla JS
└── volume-i/
    ├── chapter-1.html      # Genesis
    ├── chapter-2.html      # Foundations
    ├── chapter-3.html      # Architecture
    ├── chapter-4.html      # Ethics
    ├── chapter-5.html      # Implementation
    └── chapter-6.html      # Future
```

## 📄 Pages

### Main Pages
1. **Home** - Hero with mission statement, technology pillars, founder section
2. **About the Commons** - CERL-1.0 framework, Commons values
3. **Aurora Origin** - Aurora's story and capabilities
4. **Volume I** - Complete table of contents with chapter links
5. **Consultation** - Services overview with pricing
6. **Contact** - Contact form and information
7. **Legal** - CERL-1.0 license details

### Volume I Chapters
1. **Chapter 1: Genesis** - Full content (origin story)
2. **Chapter 2: Foundations** - Placeholder with structure
3. **Chapter 3: Architecture** - Placeholder with structure
4. **Chapter 4: Ethics** - Placeholder with structure
5. **Chapter 5: Implementation** - Placeholder with structure
6. **Chapter 6: Future** - Placeholder with structure

## ✨ Features

### Navigation
- Fixed navbar with scroll effect
- Dropdown menu for Volume I chapters
- Mobile-responsive hamburger menu
- Smooth scroll to anchors

### Interactions
- Fade-in animations on scroll
- Smooth transitions on hover
- Card hover effects with elevation
- Button animations

### Components
- Responsive grid layouts
- Consistent card styling
- Form validation
- Chapter navigation (prev/next)

### Buttons
- "Start Consultation" links to `/consult`
- "Download Volume I PDF" placeholder
- CTA buttons throughout

## 🚀 Webflow Import Instructions

1. **Create New Project** in Webflow
2. **Copy HTML Files**:
   - Use the HTML from each file as page structure
   - Import pages one at a time
3. **Add Global Styles**:
   - Copy all CSS from `css/global.css` into Webflow's custom code (Site Settings > Custom Code > Head Code)
   - Wrap in `<style>` tags
4. **Add JavaScript**:
   - Copy `js/main.js` into Webflow's custom code (Site Settings > Custom Code > Footer Code)
   - Wrap in `<script>` tags
5. **Set Up Pages**:
   - Create pages matching the file structure
   - Copy HTML content for each page
6. **Configure Links**:
   - Update `/consult` links to your actual consultation booking URL
   - Update email addresses as needed

## 🎯 Key Sections

### Home Page
- Hero with gradient background
- Mission statement with 3-column grid
- Technology pillars (6 cards)
- Founder vision section
- CTA buttons

### Volume I
- Table of contents with 6 chapters
- Chapter navigation (prev/next)
- Download PDF button (placeholder)
- Chapter 1 has full sample content

## 📱 Responsive Design

- **Desktop**: Full navigation, multi-column grids
- **Tablet**: Responsive grids, adjusted spacing
- **Mobile**: Hamburger menu, single-column layouts

## 🎨 Color Palette

```css
--color-black: #000000;
--color-white: #ffffff;
--color-gold: #D4AF37;
--color-gold-light: #E8C868;
--color-gold-dark: #B8941F;
--color-gray-dark: #1a1a1a;
--color-gray: #333333;
--color-gray-lighter: #999999;
```

## 🔗 Important Links

- Consultation: `/consult` (update to your booking URL)
- Email: `hello@mayanode.com` (update as needed)
- Legal email: `legal@mayanode.com` (update as needed)

## ⚠️ Notes

- **No React** - Pure HTML, CSS, and vanilla JavaScript
- **No sound/music** - As requested
- **Clean import** - Optimized for Webflow's page structure
- **Chapter content** - Chapter 1 is complete, others are placeholders

## 🛠️ Customization

To customize:
1. **Colors**: Update CSS variables in `global.css`
2. **Content**: Edit HTML files directly
3. **Styles**: Modify classes in `global.css`
4. **Interactions**: Adjust functions in `main.js`

## ✅ Checklist

- [x] 7 main pages created
- [x] 6 Volume I chapter pages created
- [x] Black + white + soft gold theme
- [x] Responsive design
- [x] Smooth scroll interactions
- [x] Dropdown navigation for Volume I
- [x] "Start Consultation" buttons
- [x] Mission statement section
- [x] Founder section
- [x] Technology pillars section
- [x] "Download Volume I PDF" button
- [x] No music/sound
- [x] Plain HTML/CSS/JS (no React)
- [x] Ready for Webflow import

---

**Built for MayaNode** | Commons Verified Engineering  
Licensed under CERL-1.0
