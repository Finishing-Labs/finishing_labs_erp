# Finishing Labs ERP - HTMX + Jinja2 Reference Guide

This is a **working reference implementation** of Flask + Jinja2 + HTMX for seamless single-page-app navigation without JavaScript.

---

##  How It Works: The Big Picture

### Traditional Multi-Page App (MPA)
```
User clicks link → Browser loads entire new page → Flash/flicker → Sidebar/topbar reload
```

### This HTMX Implementation (SPA-like)
```
User clicks link → HTMX makes AJAX request → Only content area swaps → Sidebar/topbar stay put
```

**The Magic**: HTMX sends a special header `HX-Request: true` with every navigation click. Flask detects this and returns either full pages or partial content.

---

## 📂 File Structure

```
finishing_labs_erp/
├── app.py                      # Flask app factory with HTMX detection
├── config.py                   # Configuration settings
├── requirements.txt            # Dependencies (Flask, Jinja2)
│
├── controllers/                # Flask blueprints (like mini-apps)
│   ├── __init__.py            # Registers all blueprints
│   ├── dashboard.py           # Homepage routes
│   ├── orders.py              # Purchase order routes
│   ├── production.py          # Work order routes
│   └── customers.py           # Customer CRUD routes
│
├── templates/
│   ├── base_layout.html       # 🔑 Master template with sidebar/topbar
│   │
│   ├── components/            # Reusable UI pieces
│   │   ├── sidebar.html       # Left navigation with HTMX links
│   │   └── topbar.html        # Top bar with page title
│   │
│   ├── dashboard/
│   │   ├── index.html         # Full page (for direct URL access)
│   │   └── content.html       # Content only (for HTMX swaps)
│   │
│   ├── orders/
│   │   ├── index.html         # Full PO list page
│   │   ├── content.html       # PO list content only
│   │   ├── create.html        # Full new PO form
│   │   └── create_content.html # Form content only
│   │
│   └── production/
│       ├── index.html         # Full work order list
│       ├── content.html       # WO list content only
│       ├── builder.html       # Full WO builder page
│       └── builder_content.html # Builder content only
│
└── models/                    # Database models (not used yet)
```

---

## 🔧 How HTMX Navigation Works

### 1. Sidebar Has HTMX Attributes

**File**: `templates/components/sidebar.html`

```html
<a href="/orders" 
   hx-get="/orders"           <!-- AJAX GET request to this URL -->
   hx-target="#content"       <!-- Put response into div with id="content" -->
   hx-swap="innerHTML"        <!-- Replace inner HTML -->
   hx-push-url="true">        <!-- Update browser URL bar -->
    <span class="material-symbols-outlined">list_alt</span>
    Purchase Orders
</a>
```

**What happens when clicked:**
1. HTMX intercepts the click
2. Makes AJAX request to `/orders` with header `HX-Request: true`
3. Flask controller detects HTMX and returns `orders/content.html` (not full page)
4. HTMX swaps content into `<div id="content">`
5. Browser URL changes to `/orders` (bookmarkable!)

---

### 2. Controllers Detect HTMX Requests

**File**: `controllers/orders.py`

```python
@orders_bp.route('/')
def index():
    """
    List all purchase orders
    
    HOW HTMX DETECTION WORKS:
    - Check request.headers for 'HX-Request' header
    - If present: return content-only template
    - If absent: return full page template
    """
    is_htmx = request.headers.get('HX-Request') == 'true'
    
    if is_htmx:
        # HTMX navigation: return just the content
        return render_template('orders/content.html', page_title='Purchase Orders')
    else:
        # Direct URL access: return full page with sidebar/topbar
        return render_template('orders/index.html', page_title='Purchase Orders')
```

**Why this matters:**
- First visit to `/orders`: User sees full page with sidebar
- Clicking "Purchase Orders" in sidebar: Only content area updates
- No page flash, no sidebar reload, smooth experience!

---

### 3. Base Template Structure

**File**: `templates/base_layout.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}ERP{% endblock %}</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>  <!-- HTMX library -->
    <script src="https://cdn.tailwindcss.com"></script>        <!-- Tailwind CSS -->
</head>
<body>
    {% include 'components/sidebar.html' %}  <!-- Always present -->
    
    <main>
        {% include 'components/topbar.html' %}  <!-- Always present -->
        
        <!-- THIS IS WHERE CONTENT SWAPS HAPPEN -->
        <div id="content">
            {% block content %}{% endblock %}  <!-- Pages fill this -->
        </div>
    </main>
</body>
</html>
```

---

### 4. Full Page vs Content-Only Templates

**Full Page** (`dashboard/index.html`) - For direct URL access:
```html
<!DOCTYPE html>
<html>
<head>
    <!-- Full HTML head with all assets -->
</head>
<body>
    <aside><!-- Sidebar --></aside>
    <main>
        <header><!-- Topbar --></header>
        <div id="content">
            <!-- Dashboard content here -->
        </div>
    </main>
</body>
</html>
```

**Content Only** (`dashboard/content.html`) - For HTMX swaps:
```html
<div class="px-8 pb-12">
    <!-- Just the dashboard content, no sidebar/topbar -->
    <h2>Operations Dashboard</h2>
    <!-- Metrics, tables, etc. -->
</div>
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd finishing_labs_erp
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

Application starts at: `http://127.0.0.1:5000`

### 3. What to Expect

**First Load** (`http://127.0.0.1:5000/`):
- Full dashboard page loads
- Sidebar and topbar appear
- Content area shows dashboard metrics

**Click "Purchase Orders" in Sidebar**:
- No page reload!
- Only content area changes
- Smoothly swaps to PO list
- URL updates to `/orders`
- Browser back button works!

**Click "Work Orders" in Sidebar**:
- Again, no page reload
- Content swaps to work order list
- URL updates to `/production`

---

## 📝 How to Add a New Page

Let's add a "Packing Slips" page as an example.

### Step 1: Create Controller

**File**: `controllers/packing_slips.py`

```python
from flask import Blueprint, render_template, request

packing_slips_bp = Blueprint('packing_slips', __name__)

@packing_slips_bp.route('/')
def index():
    """List all packing slips"""
    is_htmx = request.headers.get('HX-Request') == 'true'
    
    if is_htmx:
        return render_template('packing_slips/content.html', page_title='Packing Slips')
    else:
        return render_template('packing_slips/index.html', page_title='Packing Slips')
```

### Step 2: Register Blueprint

**File**: `controllers/__init__.py`

```python
def register_blueprints(app):
    # ... existing blueprints ...
    
    from .packing_slips import packing_slips_bp
    app.register_blueprint(packing_slips_bp, url_prefix='/packing_slips')
```

### Step 3: Create Templates

**File**: `templates/packing_slips/content.html`

```html
<div class="px-8 pb-12">
    <h2 class="text-5xl font-bold">Packing Slips</h2>
    <p>Your packing slip content here...</p>
</div>
```

**File**: `templates/packing_slips/index.html` (copy structure from dashboard/index.html)

### Step 4: Add to Sidebar

**File**: `templates/components/sidebar.html`

```html
<a href="/packing_slips" 
   hx-get="/packing_slips" 
   hx-target="#content" 
   hx-swap="innerHTML" 
   hx-push-url="true"
   class="flex items-center px-4 py-3 rounded-sm ...">
    <span class="material-symbols-outlined mr-3">local_shipping</span>
    <span>Packing Slips</span>
</a>
```

**Done!** Restart Flask and test the new page.

---

## 🎨 Design System

### Colors
```
Primary (Industrial Blue):   #001d2e
Secondary (Metallic Gray):   #446180
Tertiary (Chemical Green):   #131e00 / #c8f17a
Error Red:                    #ba1a1a
Surface Containers:          #f6f9ff, #ebf5ff, #ffffff
```

### Fonts
- **Headlines**: Space Grotesk (bold, industrial)
- **Body**: Inter (clean, readable)
- **Icons**: Material Symbols Outlined

### Components
- Metric cards with large numbers
- Data tables with hover states
- Progress bars for work order tracking
- Status badges (Pending, In Progress, Completed)

---

## 🐛 Troubleshooting

### Problem: Clicking sidebar does nothing
**Fix**: Check browser console for HTMX errors. Ensure `<script src="https://unpkg.com/htmx.org@1.9.10"></script>` is loading.

### Problem: Full page reloads on navigation
**Fix**: Verify `hx-get`, `hx-target`, and `hx-push-url` attributes are present in sidebar links.

### Problem: Content doesn't appear
**Fix**: Check Flask console for template errors. Ensure both `index.html` and `content.html` versions exist.

### Problem: Styles look broken
**Fix**: Clear browser cache. Tailwind CDN should load automatically.

---

## 📚 Key Concepts Reference

### HTMX Attributes
| Attribute | Purpose |
|-----------|---------|
| `hx-get="/url"` | Make GET request to URL |
| `hx-post="/url"` | Make POST request to URL |
| `hx-target="#id"` | Put response into element with this ID |
| `hx-swap="innerHTML"` | How to insert (innerHTML, outerHTML, beforeend, etc.) |
| `hx-push-url="true"` | Update browser URL for bookmarking |
| `hx-trigger="click"` | What triggers request (click, change, load, etc.) |

### Jinja2 Template Syntax
| Syntax | Purpose |
|--------|---------|
| `{% block name %}...{% endblock %}` | Define replaceable block |
| `{% extends 'base.html' %}` | Inherit from base template |
| `{% include 'file.html' %}` | Insert another template |
| `{{ variable }}` | Output variable value |
| `{{ var\|default('text') }}` | Default value if var is None |
| `{% if condition %}...{% endif %}` | Conditional rendering |
| `{# comment #}` | Template comment (not in output) |

### Flask Request Object
```python
request.headers.get('HX-Request')  # Check if HTMX request
request.endpoint  # Current route name (e.g., 'orders.index')
request.args.get('param')  # Get URL parameter
request.form.get('field')  # Get form field value
```

---

## 🎯 What to Do Next

1. **Test Navigation**: Click through all sidebar links, verify smooth transitions
2. **Add Real Data**: Connect models to controllers, replace hardcoded values
3. **Build Forms**: Create POST handlers for new PO/WO creation
4. **Add Validation**: Use HTMX `hx-post` for form submission with inline errors
5. **Pagination**: Use HTMX to load next page without full reload
6. **Search/Filter**: Use `hx-get` with query parameters for dynamic filtering

---

## 📖 Additional Resources

- **HTMX Docs**: https://htmx.org/docs/
- **Flask Docs**: https://flask.palletsprojects.com/
- **Jinja2 Docs**: https://jinja.palletsprojects.com/
- **Tailwind CSS**: https://tailwindcss.com/docs

---

**This is your reference**. Study how the pieces connect, then extend it for your full ERP system.
