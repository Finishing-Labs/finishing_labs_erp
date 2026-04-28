# Finishing Labs ERP - Deployment Guide

Complete step-by-step guide for deploying and maintaining the Finishing Labs ERP system in production.

---

## Table of Contents

1. [Initial Deployment Setup](#initial-deployment-setup)
2. [Deploying Code Changes](#deploying-code-changes)
3. [Deploying Database Changes](#deploying-database-changes)
4. [Monitoring and Maintenance](#monitoring-and-maintenance)
5. [Troubleshooting](#troubleshooting)

---

## Initial Deployment Setup

### Prerequisites

- GitHub account with repository pushed
- Render account (free tier available)
- PostgreSQL client tools installed locally (psql)
- Python 3.13+ installed locally

### Step 1: Prepare Application for Deployment

#### 1.1 Create Procfile

In your project root directory, create a file named `Procfile` (no extension):

```bash
cd finishing_labs_erp
echo "web: gunicorn app:app" > Procfile
```

**What this does:** Tells Render how to start your Flask application using Gunicorn (production web server).

#### 1.2 Add Gunicorn to Requirements

```bash
echo "gunicorn>=21.2.0" >> requirements.txt
```

#### 1.3 Verify Requirements.txt

Make sure your `requirements.txt` contains:
```
Flask==3.0.0
Jinja2==3.1.2
python-dotenv==1.0.0
Werkzeug==3.0.1
psycopg[binary]>=3.3.0
gunicorn>=21.2.0
```

#### 1.4 Commit Changes

```bash
git add .
git commit -m "Add production deployment files"
git push origin main
```

---

### Step 2: Create Render Account and PostgreSQL Database

#### 2.1 Sign Up for Render

1. Go to https://render.com
2. Click "Get Started" or "Sign Up"
3. Sign up using your GitHub account (recommended) or email
4. Verify your email if required

#### 2.2 Create PostgreSQL Database

1. In Render Dashboard, click **"New +"** button (top right)
2. Select **"PostgreSQL"**
3. Fill in database details:
   - **Name:** `finishing-labs-db` (or any name you prefer)
   - **Database:** `finishing_labs_erp`
   - **User:** `finishing_lab_user` (or any username)
   - **Region:** Choose closest to your users (e.g., Oregon, Ohio, Frankfurt)
   - **PostgreSQL Version:** 16 or latest
   - **Instance Type:** 
     - **Free** - For testing (expires after 90 days)
     - **Starter ($7/month)** - For production use
4. Click **"Create Database"**
5. Wait 2-5 minutes for database to provision

#### 2.3 Save Database Connection Info

Once created, you'll see the database dashboard. **SAVE THESE VALUES:**

- **Internal Database URL:** Used by Render services (starts with `postgresql://...dpg-...`)
- **External Database URL:** Used from your local computer (ends with `.render.com`)
- **PSQL Command:** Copy this for connecting from your terminal

Example External URL:
```
postgresql://finishing_lab_user:PASSWORD@dpg-xxxxx.oregon-postgres.render.com/finishing_labs_erp
```

**⚠️ IMPORTANT:** Keep the password secure. You'll need this URL for:
- Setting environment variables
- Running migrations from your computer
- Database backups

---

### Step 3: Initialize Database Schema

#### 3.1 Connect to Production Database

Open PowerShell in your project directory and connect using the **External Database URL**:

```powershell
psql "postgresql://finishing_lab_user:PASSWORD@dpg-xxxxx.oregon-postgres.render.com/finishing_labs_erp"
```

You should see:
```
finishing_labs_erp=>
```

#### 3.2 Run Migration

From the psql prompt:

```sql
\i migrations/001_initial_schema.sql
```

#### 3.3 Verify Tables Created

```sql
\dt
```

You should see:
```
              List of relations
 Schema |      Name       | Type  |      Owner       
--------+-----------------+-------+------------------
 public | customers       | table | finishing_lab_user
 public | line_items      | table | finishing_lab_user
 public | packing_slips   | table | finishing_lab_user
 public | purchase_orders | table | finishing_lab_user
 public | work_orders     | table | finishing_lab_user
```

#### 3.4 Exit psql

```sql
\q
```

---

### Step 4: Deploy Web Application to Render

#### 4.1 Create Web Service

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Click **"Connect GitHub"** (if not already connected)
3. Select your repository: `finishing_labs_erp`

#### 4.2 Configure Web Service

Fill in the following:

- **Name:** `finishing-labs-erp` (this becomes your URL)
- **Region:** Same as database (e.g., Oregon)
- **Branch:** `main`
- **Root Directory:** Leave blank (or `finishing_labs_erp` if repo has multiple folders)
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Instance Type:**
  - **Free** - For testing (sleeps after 15 min inactivity)
  - **Starter ($7/month)** - For production

#### 4.3 Set Environment Variables

Scroll down to **"Environment Variables"** section and add:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | (Paste **Internal Database URL** from Step 2.3) |
| `SECRET_KEY` | (Generate using command below) |
| `FLASK_ENV` | `production` |

**Generate SECRET_KEY:**
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output and paste as SECRET_KEY value.

#### 4.4 Create Web Service

1. Click **"Create Web Service"**
2. Wait 2-5 minutes for deployment
3. Watch the logs for any errors

#### 4.5 Verify Deployment

Once you see **"Your service is live 🎉"** in logs:

1. Click the URL (e.g., `https://finishing-labs-erp.onrender.com`)
2. Test all pages:
   - Dashboard
   - Customers
   - Purchase Orders
   - Work Orders
   - Packing Slips
3. Try creating a test customer

**✅ If everything loads, your initial deployment is complete!**

---

## Deploying Code Changes

Follow these steps every time you make code changes (controllers, templates, services, etc.) that don't involve database schema changes.

### Step 1: Make Changes Locally

Edit your code files as needed:
- Controllers (`controllers/`)
- Services (`services/`)
- Templates (`templates/`)
- Static files (`static/`)

### Step 2: Test Locally

```powershell
python app.py
```

Visit `http://127.0.0.1:5000` and verify your changes work correctly.

### Step 3: Commit Changes

```powershell
git add .
git commit -m "Brief description of what you changed"
```

Example commit messages:
- `git commit -m "Add customer search functionality"`
- `git commit -m "Fix purchase order date display"`
- `git commit -m "Update dashboard layout"`

### Step 4: Push to GitHub

```powershell
git push origin main
```

### Step 5: Automatic Deployment

Render automatically detects the push and deploys:

1. Go to Render Dashboard → Your Web Service
2. Click **"Events"** tab to watch deployment
3. Wait 1-3 minutes for deployment to complete
4. Look for **"Deploy live for..."** message

### Step 6: Verify Production

1. Visit your production URL
2. Test the changes you made
3. Check logs if anything isn't working:
   - Render Dashboard → Your Service → **"Logs"** tab

### Troubleshooting Code Deployments

**Deployment failed?**
1. Check the build logs in Render Dashboard
2. Common issues:
   - Syntax error in Python code
   - Missing import
   - Missing file in git commit
3. Fix locally, commit, and push again

**Code deployed but not working?**
1. Check application logs in Render Dashboard
2. Look for Python tracebacks
3. Verify environment variables are set correctly

---

## Deploying Database Changes

Follow these steps when you need to add/modify database tables, columns, or indexes.

### Important Rules

⚠️ **ALWAYS do database changes in this order:**
1. Create migration file
2. Test locally
3. Run on production database FIRST
4. Then deploy code that uses the new schema
5. Never skip steps or reverse the order

### Step 1: Create Migration File

Create a new SQL file in `migrations/` directory with sequential numbering:

```powershell
# Example: Adding a vendor_id to customers table
New-Item migrations/002_add_vendor_to_customers.sql
```

Edit the file with your SQL changes:

```sql
-- migrations/002_add_vendor_to_customers.sql
-- Add vendor relationship to customers

ALTER TABLE customers 
ADD COLUMN vendor_id INTEGER;

ALTER TABLE customers 
ADD CONSTRAINT fk_customers_vendor 
FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id);

CREATE INDEX idx_customers_vendor ON customers(vendor_id);
```

### Step 2: Test Migration Locally

**If you have local PostgreSQL:**

```powershell
# Connect to local database
psql finishing_labs_erp

# Run migration
\i migrations/002_add_vendor_to_customers.sql

# Verify changes
\d customers
```

**If no local PostgreSQL, skip to Step 3 but be extra careful.**

### Step 3: Run Migration on Production Database

```powershell
# Connect to production database (use External URL)
psql "postgresql://finishing_lab_user:PASSWORD@dpg-xxxxx.oregon-postgres.render.com/finishing_labs_erp"

# Run migration
\i migrations/002_add_vendor_to_customers.sql

# Verify changes
\d customers

# If successful, exit
\q
```

**⚠️ If migration fails:**
- Fix the SQL errors in your migration file
- You may need to manually clean up (DROP table, ROLLBACK, etc.)
- Test locally before trying production again

### Step 4: Commit Migration File

```powershell
git add migrations/002_add_vendor_to_customers.sql
git commit -m "Add vendor_id to customers table"
git push origin main
```

### Step 5: Update Code to Use New Schema

Now you can safely update your code:

**Example - Update service to use new column:**

```python
# services/customer_service.py

def create_customer(company_name, email, phone=None, vendor_id=None):
    """Create new customer with vendor relationship"""
    sql = """
        INSERT INTO customers 
        (company_name, contact_email, phone, vendor_id, active, created_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        RETURNING customer_id
    """
    return DB.execute_returning_id(sql, [company_name, email, phone, vendor_id, True])
```

### Step 6: Test Locally

```powershell
python app.py
```

Test that your code works with the new database schema.

### Step 7: Deploy Code Changes

```powershell
git add .
git commit -m "Update customer service to use vendor_id"
git push origin main
```

Render will auto-deploy the code changes.

### Step 8: Verify Production

1. Visit production URL
2. Test the new functionality
3. Verify database changes are working

---

## Common Database Change Scenarios

### Adding a New Table

**Migration file: `migrations/003_add_vendors_table.sql`**

```sql
CREATE TABLE vendors (
    vendor_id SERIAL PRIMARY KEY,
    vendor_name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    phone VARCHAR(50),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_vendors_active ON vendors(active);
```

**Steps:**
1. Create migration file
2. Run on production: `\i migrations/003_add_vendors_table.sql`
3. Commit migration: `git add migrations/003_add_vendors_table.sql && git commit -m "Add vendors table"`
4. Create service file: `services/vendor_service.py`
5. Create controller: `controllers/vendors.py`
6. Create templates: `templates/vendors/`
7. Test locally
8. Push: `git push origin main`

### Adding a Column to Existing Table

**Migration file: `migrations/004_add_phone_extension.sql`**

```sql
ALTER TABLE customers 
ADD COLUMN phone_extension VARCHAR(20);
```

**Steps:**
1. Create migration file
2. Run on production
3. Commit migration
4. Update service to include new field
5. Update templates to show/edit field
6. Test and push

### Removing a Column (Careful!)

**Migration file: `migrations/005_remove_old_field.sql`**

```sql
ALTER TABLE customers 
DROP COLUMN old_field_name;
```

**⚠️ WARNING:** Make sure no code is using this column before dropping!

**Steps:**
1. Update all code to stop using the column
2. Deploy code changes
3. Test production
4. Create drop column migration
5. Run migration on production
6. Commit migration file

### Adding an Index for Performance

**Migration file: `migrations/006_add_performance_indexes.sql`**

```sql
CREATE INDEX idx_purchase_orders_date ON purchase_orders(order_date);
CREATE INDEX idx_work_orders_status ON work_orders(status);
```

**Steps:**
1. Create migration file
2. Run on production (safe, doesn't affect existing code)
3. Commit migration

---

## Monitoring and Maintenance

### Daily Checks

**View Application Logs:**

1. Render Dashboard → Your Web Service → **"Logs"** tab
2. Look for errors or warnings
3. Common issues to watch:
   - Database connection errors
   - Python exceptions
   - Slow query warnings

**Check Application Status:**

1. Visit your production URL
2. Click through main pages
3. Verify everything loads

### Weekly Tasks

**Create Database Backup:**

```powershell
# Connect and create backup
pg_dump "postgresql://finishing_lab_user:PASSWORD@dpg-xxxxx.oregon-postgres.render.com/finishing_labs_erp" > backup_2026-04-28.sql
```

Store backups safely (external drive, cloud storage).

**Review Logs:**

1. Render Dashboard → Database → **"Logs"** tab
2. Look for connection issues or performance problems

### Monthly Tasks

**Update Dependencies:**

Check for security updates:

```powershell
pip list --outdated
```

Update if needed:
```powershell
pip install --upgrade flask psycopg gunicorn
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

---

## Troubleshooting

### Application Won't Start After Deployment

**Symptoms:** Render shows "Deploy failed" or service crashes immediately

**Steps:**
1. Check Render logs for error message
2. Common causes:
   - Syntax error in Python → Fix and redeploy
   - Missing environment variable → Add in Render settings
   - Import error → Check requirements.txt
3. Test locally: `python app.py`
4. Fix issue, commit, push

### Database Connection Errors

**Symptoms:** "could not connect to database" in logs

**Steps:**
1. Check DATABASE_URL is set in Render environment variables
2. Verify it's the **Internal Database URL** (not External)
3. Check database is running in Render dashboard
4. Restart web service: Render Dashboard → Manual Deploy → "Clear build cache & deploy"

### Migration Failed - Database in Bad State

**Symptoms:** Migration ran partially, some tables exist, some don't

**Steps:**
1. Connect to database: `psql "..."`
2. Check what exists: `\dt`
3. Drop problematic tables: `DROP TABLE table_name CASCADE;`
4. Fix migration file
5. Run again: `\i migrations/00X_fixed_migration.sql`

### Application Running But Pages Show Errors

**Symptoms:** 500 errors, blank pages, or error messages

**Steps:**
1. Check Render logs for Python tracebacks
2. Common causes:
   - Missing database table → Check migrations ran
   - Template error → Check template syntax
   - Service function error → Check SQL queries
3. Test locally with same data
4. Fix and redeploy

### Rollback a Deployment

**If deployment breaks production:**

```powershell
# Option 1: Revert code locally and push
git revert HEAD
git push origin main

# Option 2: Use Render dashboard
# Render Dashboard → Events → Click previous successful deploy → "Redeploy"
```

**If database migration caused issues:**

Manual rollback (create reverse migration):

```sql
-- migrations/00X_rollback_previous.sql
-- Reverses changes from migration 00X

DROP TABLE new_table CASCADE;
-- or
ALTER TABLE customers DROP COLUMN new_field;
```

Run rollback migration on production.

---

## Production URLs and Access

**Application URL:**
- `https://finishing-labs-erp.onrender.com` (or your custom domain)

**Render Dashboard:**
- https://dashboard.render.com

**Database Access:**
- Use External URL from Render database dashboard
- `psql "postgresql://...render.com/..."`

**GitHub Repository:**
- Push changes to `main` branch for auto-deployment

---

## Quick Reference Commands

```powershell
# Deploy code changes
git add .
git commit -m "Description"
git push origin main

# Connect to production database
psql "EXTERNAL_DATABASE_URL_FROM_RENDER"

# Run migration
\i migrations/00X_migration_name.sql

# View database tables
\dt

# Describe table structure
\d table_name

# Create database backup
pg_dump "DATABASE_URL" > backup.sql

# Restore database backup
psql "DATABASE_URL" < backup.sql

# View Render logs
# Go to: https://dashboard.render.com → Your Service → Logs

# Generate new SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Deployment Checklist

**Before Every Deployment:**

- [ ] Test changes locally (`python app.py`)
- [ ] All pages load without errors
- [ ] Database migrations tested (if applicable)
- [ ] Code committed with clear message
- [ ] Pushed to GitHub

**After Every Deployment:**

- [ ] Check Render deployment succeeded
- [ ] Visit production URL
- [ ] Test changed functionality
- [ ] Check logs for errors
- [ ] Verify database changes (if applicable)

**Before Database Migrations:**

- [ ] Migration file created and tested
- [ ] Backward compatibility considered
- [ ] Migration runs on production database FIRST
- [ ] Code deployed AFTER migration succeeds

---

## Getting Help

**Render Documentation:**
- https://render.com/docs

**PostgreSQL Documentation:**
- https://www.postgresql.org/docs/

**Flask Documentation:**
- https://flask.palletsprojects.com/

**Project Documentation:**
- See `docs/developer-guide.html` for code architecture
- See `HTMX_REFERENCE.md` for frontend patterns

---

**Last Updated:** April 28, 2026
