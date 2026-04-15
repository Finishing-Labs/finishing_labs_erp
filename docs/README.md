# GitHub Pages Setup Instructions

This folder contains the design documentation website for Finishing Labs ERP. Follow these steps to publish it to GitHub Pages.

## Quick Start

### Step 1: Push the docs folder to GitHub

```bash
# From your project root
git add docs/
git commit -m "Add GitHub Pages documentation"
git push origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Click **Pages** in the left sidebar
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/docs`
5. Click **Save**

### Step 3: Access Your Documentation

After a few minutes, your documentation will be available at:
```
https://<your-username>.github.io/<repository-name>/
```

For example: `https://yourusername.github.io/finishing-labs-erp/`

## Updating the Documentation

After the initial setup, any changes you push to the `docs/` folder will automatically update the website within a few minutes.

```bash
# Make your changes to HTML/CSS files
git add docs/
git commit -m "Update documentation"
git push origin main
```

## Custom Domain (Optional)

To use a custom domain like `docs.yourcompany.com`:

1. In GitHub Settings → Pages, enter your custom domain
2. Add a CNAME record in your DNS settings pointing to `<your-username>.github.io`
3. Wait for DNS propagation (can take up to 24 hours)

## Local Preview

To preview the documentation locally before pushing:

```bash
# Navigate to the docs folder
cd docs/

# Start a simple HTTP server
# Python 3:
python -m http.server 8000

# Then open http://localhost:8000 in your browser
```

## Files Structure

- `index.html` - Landing page with overview
- `user-guide.html` - User documentation
- `developer-guide.html` - Developer/technical documentation
- `style.css` - Styling for all pages

## Customization

You can customize the documentation by editing:
- **Content**: Update the HTML files with your specific information
- **Styling**: Modify `style.css` to match your brand colors
- **Navigation**: Add new pages by creating HTML files and linking them in the nav

## Troubleshooting

**Site not loading?**
- Check that GitHub Pages is enabled in repository settings
- Ensure the `/docs` folder is selected as the source
- Wait a few minutes after enabling (first deployment can take 5-10 minutes)

**Changes not showing?**
- Hard refresh your browser (Ctrl+Shift+R or Cmd+Shift+R)
- Check that changes were pushed to the main branch
- Wait a few minutes for GitHub to rebuild the site

**404 errors?**
- Verify all file paths are relative (no leading /)
- Check that all linked files exist in the docs folder
