# The Watchman's Bible Reading Plan - Landing Page

A beautiful, mobile-friendly landing page and intake form for **The Watchman's Bible Reading Plan** — a personalized daily Bible reading plan for Christian married men.

## 🎯 Purpose

This landing page collects user information to generate personalized daily Bible readings featuring:
- **Five daily readings** (Wisdom, Husband's Post, Father's Charge, Citizen's Stand, Evening Peace)
- **Personalized content** with family names and birthdays
- **Flexible delivery** via Email, Telegram, or PDF downloads

## 📋 Features

### Design
- **Dark navy/gold color scheme** — masculine, biblical aesthetic
- **Clean typography** using Google Fonts (Playfair Display + Inter)
- **Mobile-first responsive** design
- **Smooth transitions** between form steps (Typeform-style UX)
- **Subtle cross/shield iconography**

### User Flow

1. **Landing Section**
   - Hero with title and tagline
   - Description of the Five-Watch system
   - Call-to-action: "Build Your Plan"

2. **Intake Form** (9 steps, one question at a time)
   - Your first name
   - Your wife's name
   - Your wife's birthday (MM/DD)
   - Number of children (1-10 slider)
   - For each child: name + birthday (MM/DD)
   - Optional: Other family members for birthday readings
   - Start date for the plan (default: today)
   - Delivery method: Email / Telegram / Download PDFs
   - Contact info (email or Telegram handle)

3. **Preview Section**
   - Shows a Day 1 reading preview
   - Personalized with user's wife's name in "Husband's Post"
   - Personalized with children's names in "Father's Charge"

4. **Confirmation**
   - "Your plan is ready!" message
   - Download button for personalized config JSON

## 🚀 Deployment

### GitHub Pages (Recommended)

1. Create a new repository (e.g., `watchman-bible-plan`)
2. Copy `index.html` to the repository root
3. Enable GitHub Pages in Settings → Pages
4. Set source to `main` branch, root directory
5. Your page will be live at `https://yourusername.github.io/watchman-bible-plan/`

### Local Testing

Simply open `index.html` in any modern browser. No build process required!

```bash
open index.html
# or
python3 -m http.server 8000  # then visit http://localhost:8000
```

## 💾 Data Storage

- User responses are stored in **localStorage** as `watchmanPlan`
- Upon completion, user downloads a **JSON config file** with their personalized plan
- Example config format:

```json
{
  "plan": "The Watchman's Bible Reading Plan",
  "version": "1.0",
  "generated": "2026-03-05T21:45:00.000Z",
  "user": {
    "firstName": "John",
    "wifeName": "Sarah",
    "wifeBirthday": "06/15",
    "childrenCount": 2,
    "children": [
      { "name": "Gideon", "birthday": "03/22" },
      { "name": "Boaz", "birthday": "11/08" }
    ],
    "otherFamily": [],
    "startDate": "2026-03-05",
    "deliveryMethod": "Email",
    "contact": "john@example.com"
  }
}
```

## 🔌 Backend Integration (Future)

This landing page is designed to work standalone, but can be connected to a backend:

1. **Submit endpoint**: Replace `downloadConfig()` with a `fetch()` call to your API
2. **Email/Telegram integration**: Process the JSON config server-side
3. **PDF generation**: Create daily reading PDFs based on user preferences
4. **Scheduling**: Send readings at configured times

Example integration point:

```javascript
async function submitPlan() {
    const response = await fetch('/api/submit-plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    });
    
    if (response.ok) {
        // Show success message
    }
}
```

## 🛠️ Tech Stack

- **Pure HTML/CSS/JavaScript** — no dependencies, no build process
- **Google Fonts** — Playfair Display (headers) + Inter (body)
- **localStorage API** — client-side data persistence
- **Blob/Download API** — JSON config export

## 📱 Browser Support

Works on all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile Safari (iOS 14+)
- Chrome Mobile (Android 90+)

## 🎨 Customization

### Colors

Edit CSS variables in the `<style>` section:

```css
:root {
    --navy: #0a1929;
    --navy-light: #1a2942;
    --gold: #d4af37;
    --gold-light: #f4d470;
}
```

### Typography

Change Google Fonts in the `<link>` tag:

```html
<link href="https://fonts.googleapis.com/css2?family=Your+Font&display=swap" rel="stylesheet">
```

### Content

Update the Five-Watch descriptions in the `.five-watches` section:

```html
<div class="watch-item">
    <h3>📖 Your Title</h3>
    <p>Your description</p>
</div>
```

## 📄 License

Built by **MOOP** for **USMC Ministries**

## 🙏 Credits

- **Design inspiration**: Typeform, modern landing pages
- **Typography**: Google Fonts (Playfair Display, Inter)
- **Iconography**: Unicode emoji (✝️, ✠, 📖, 💑, 👨‍👧‍👦, ⚔️, 🌙)

---

**Stand watch. Lead well. Rest in Him.**
