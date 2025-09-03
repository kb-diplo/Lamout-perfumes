# PythonAnywhere Deployment Guide for Lamout Perfume

This guide will walk you through deploying your Lamout Perfume Django application to PythonAnywhere.

## Prerequisites

1. **PythonAnywhere Account**: Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. **GitHub Repository**: Your code is already at https://github.com/kb-diplo/Lamout-perfumes.git

## Step 1: Clone Your Repository

1. Open a **Bash console** in PythonAnywhere
2. Clone your repository:
```bash
git clone https://github.com/kb-diplo/Lamout-perfumes.git
cd Lamout-perfumes
```

## Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure Environment Variables

Create a `.env` file for production settings:
```bash
nano .env
```

Add these contents:
```
SECRET_KEY=your-super-secret-production-key-here-make-it-long-and-random
PYTHONANYWHERE_DOMAIN=yourusername.pythonanywhere.com
```

**Important**: Replace `yourusername` with your actual PythonAnywhere username.

## Step 4: Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Populate products (if needed)
python categorize_products.py
```

## Step 5: Collect Static Files

```bash
# Create static files directory
mkdir -p /home/yourusername/Lamout-perfumes/staticfiles

# Collect static files
python manage.py collectstatic --noinput
```

## Step 6: Configure Web App

1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10**

### Configure WSGI File

Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:

```python
import os
import sys

# Add your project directory to sys.path
path = '/home/yourusername/Lamout-perfumes'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'lamoutperfumes.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Configure Virtual Environment

In the **Web** tab:
- **Virtualenv**: `/home/yourusername/Lamout-perfumes/venv`

### Configure Static Files

In **Static files** section:
- **URL**: `/static/`
- **Directory**: `/home/yourusername/Lamout-perfumes/staticfiles/`

Add another static files mapping:
- **URL**: `/media/`
- **Directory**: `/home/yourusername/Lamout-perfumes/media/`

## Step 7: Environment Variables in PythonAnywhere

1. Go to **Files** tab
2. Edit `.bashrc` file in your home directory
3. Add these lines:
```bash
export SECRET_KEY="your-super-secret-production-key-here"
export PYTHONANYWHERE_DOMAIN="yourusername.pythonanywhere.com"
```

## Step 8: Final Configuration

### Update Django Settings

Ensure your `settings.py` has:
```python
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Security settings for production
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-local-development-key-change-in-production")
DEBUG = False  # Always False in production
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".pythonanywhere.com", "yourusername.pythonanywhere.com"]

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Step 9: Reload and Test

1. Click **Reload** button in Web tab
2. Visit your site: `https://yourusername.pythonanywhere.com`
3. Test all functionality:
   - Home page loads
   - Product catalog works
   - Shopping cart functions
   - Custom admin accessible at `/custom-admin/`

## Step 10: SSL Certificate (Optional but Recommended)

1. Go to **Web** tab
2. In **Security** section, enable **Force HTTPS**
3. PythonAnywhere provides free SSL certificates

## Troubleshooting

### Common Issues:

1. **500 Internal Server Error**:
   - Check error logs in **Web** tab → **Error log**
   - Ensure all environment variables are set
   - Verify WSGI configuration

2. **Static Files Not Loading**:
   - Run `python manage.py collectstatic` again
   - Check static files mapping in Web tab

3. **Database Issues**:
   - Ensure migrations are run: `python manage.py migrate`
   - Check database file permissions

4. **Import Errors**:
   - Verify virtual environment path
   - Check all dependencies are installed

### Useful Commands:

```bash
# View error logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log

# Restart web app (alternative to reload button)
touch /var/www/yourusername_pythonanywhere_com_wsgi.py

# Check Django configuration
python manage.py check --deploy
```

## Security Checklist

✅ **DEBUG = False** in production  
✅ **SECRET_KEY** set via environment variable  
✅ **ALLOWED_HOSTS** properly configured  
✅ **HTTPS enabled** (Force HTTPS)  
✅ **Static files** served correctly  
✅ **Media files** accessible but secure  

## Post-Deployment

1. **Test all features** thoroughly
2. **Create regular backups** of your database
3. **Monitor error logs** regularly
4. **Update dependencies** periodically

Your Lamout Perfume website will be live at:
**https://yourusername.pythonanywhere.com**

## Support

- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **Django Deployment**: https://docs.djangoproject.com/en/4.2/howto/deployment/
- **Your Repository**: https://github.com/kb-diplo/Lamout-perfumes.git

---

**© 2023-2025 Lamout Perfume. All rights reserved.**
