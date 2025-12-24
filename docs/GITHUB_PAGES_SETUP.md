# GitHub Pages Setup

## Quick Setup

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add GitHub Pages site"
   git push origin main
   ```

2. **Enable GitHub Pages:**
   - Go to your repo on GitHub
   - Click **Settings**
   - Scroll to **Pages** section
   - Under **Source**, select `main` branch and `/docs` folder
   - Click **Save**

3. **Wait a minute, then visit:**
   ```
   https://yourusername.github.io/devcli
   ```

## What's Included

### `docs/index.html`
Beautiful single-page landing site with:
- Hero section with CTA buttons
- Feature grid (6 key features)
- Interactive terminal demo
- Comparison table
- Professional footer
- Responsive design
- Purple gradient theme

### Design Features
- ✅ Mobile responsive
- ✅ Fast loading (no external dependencies)
- ✅ Clean, modern design
- ✅ Hover animations
- ✅ Professional typography
- ✅ Accessible color contrast

## Customization

### Update Links
Replace `yourusername` with your GitHub username in:
- Hero CTA buttons
- Footer links
- All GitHub URLs

### Change Colors
The main gradient is defined in `body` style:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

Change to your preferred colors:
- Blue/Cyan: `#667eea 0%, #37c6fc 100%`
- Green: `#56ab2f 0%, #a8e063 100%`
- Orange: `#f857a6 0%, #ff5858 100%`

### Add Sections
The HTML is organized into clear sections:
- `.hero` - Top section
- `.features` - Feature grid
- `.demo` - Terminal demo
- `.comparison` - Comparison table
- `footer` - Footer

Add new sections between existing ones.

## Testing Locally

You can test the site locally by opening the HTML file:

```bash
cd docs
python -m http.server 8000
# Visit: http://localhost:8000
```

Or just open `docs/index.html` in your browser.

## Domain Name (Optional)

Once your site is live on GitHub Pages, you can add a custom domain:

1. Buy a domain (e.g., devcli.dev)
2. Add CNAME record pointing to `yourusername.github.io`
3. Create file `docs/CNAME` with your domain:
   ```
   devcli.dev
   ```
4. Push to GitHub
5. Wait for DNS propagation (~1 hour)

## SEO Tips

The site includes:
- ✅ Meta description
- ✅ Semantic HTML
- ✅ Clear headings
- ✅ Alt text ready (add to images when you add them)

To improve SEO:
1. Add favicon
2. Add Open Graph tags
3. Add schema.org markup
4. Submit to Google Search Console

## Analytics (Optional)

Add Google Analytics by inserting before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## Screenshots (Recommended)

Add screenshots to make it even better:

1. Take screenshot of DevCLI in action
2. Save as `docs/screenshot.png`
3. Add to demo section:
   ```html
   <img src="screenshot.png" alt="DevCLI Screenshot" style="max-width: 100%; border-radius: 12px;">
   ```

## Social Media Cards

Add Open Graph tags for better social sharing:

```html
<meta property="og:title" content="DevCLI - Free AI Coding Assistant">
<meta property="og:description" content="Claude Code's UI + Free Models">
<meta property="og:image" content="https://yourusername.github.io/devcli/og-image.png">
<meta property="og:url" content="https://yourusername.github.io/devcli">
<meta name="twitter:card" content="summary_large_image">
```

## Maintenance

The site is a single HTML file, so updates are easy:
1. Edit `docs/index.html`
2. Test locally
3. Push to GitHub
4. Changes live in ~1 minute

That's it! Your professional landing page is ready! 🚀
