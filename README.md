# Sarojini Steel Works &bull; Fabrication Showcase Website

A modern, high-performance, 100% open-source showcase platform for a professional welder and structural steel fabrication workshop.

Built with **Django 5.x**, **Tailwind CSS**, **WhiteNoise**, **HTML5 Canvas & 3D Interactive WebGL/CSS**, and ready for 1-click free live deployment.

---

## 🚀 Live Deployment Guide (100% Free, Zero Hosting Fees)

### Option 1: 1-Click Free Cloud Deployment via GitHub + Render.com (Recommended)

Render provides a completely free tier with automatic HTTPS (SSL certificate), continuous deployment (git push auto-deploys), and a free `.onrender.com` domain.

#### Step 1: Create a GitHub Repository
1. Log in to [GitHub](https://github.com/) and create a new public or private repository named `sarojini-industries`.
2. Push this local codebase to your GitHub repository:
   ```bash
   git remote add origin https://github.com/<your-username>/sarojini-industries.git
   git branch -M main
   git push -u origin main
   ```

#### Step 2: Deploy on Render.com
1. Go to [Render.com](https://render.com/) and sign up for a free account (using GitHub).
2. Click **New +** &rarr; **Web Service**.
3. Select **Build and deploy from a Git repository** and connect your `sarojini-industries` repository.
4. Render will auto-detect settings from `render.yaml` or you can enter:
   - **Name**: `sarojini-steel-works`
   - **Language / Runtime**: `Python 3`
   - **Region**: Any (e.g., Singapore or Oregon)
   - **Branch**: `main`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`
   - **Instance Type**: **Free**
5. Under **Environment Variables**, ensure:
   - `DEBUG` = `False`
   - `SECRET_KEY` = (Click "Generate" or provide a random secure string)
   - `ALLOWED_HOSTS` = `.onrender.com,localhost,127.0.0.1`
6. Click **Deploy Web Service**.
7. In ~2 minutes, your website is live worldwide at `https://sarojini-steel-works.onrender.com`!

---

### Option 2: Instant Public Tunnel for Immediate Demonstration (No GitHub Needed)

If you want to send a live working link to clients or review it on a phone immediately right now from your laptop:
```bash
# Using Cloudflare Tunnel (Free, no login needed)
npx cloudflared tunnel --url http://127.0.0.1:8000
```
This generates a temporary public `https://<random>.trycloudflare.com` URL that forwards live traffic directly to your local Django server.

---

## 🛠️ How Future Upgrades Work

The website has been architected with a decoupled, modular design so that scaling and adding features is frictionless:

### 1. Instant Content & Photo Upgrades (No Coding Required)
- Access the mobile-friendly welder portal: `https://your-domain/admin/`
- **Add New Project Blueprints**: Upload photos, steel gauge, dimensions, weld standards (AWS D1.1), and site locations.
- **Add New Fabrication Categories**: Create categories like *Industrial Spiral Stairs*, *Laser Pergolas*, or *Shutter Repair*.
- **Manage Inquiries**: Review inbound inquiries with telephone numbers, site addresses, and requirements.

### 2. Code & UI Upgrades (Continuous Delivery)
Whenever you modify templates, styles, or add new apps:
```bash
git add .
git commit -m "Add new feature / update styling"
git push origin main
```
Render automatically detects the commit, runs `build.sh`, collects static files, applies migrations, and redeploys without downtime.

### 3. Scaling Roadmap & Future Integrations
- **PostgreSQL Database**: When scale expands beyond 5,000 inquiries, connect Render's free PostgreSQL instance with `DATABASE_URL` via `dj-database-url`.
- **Cloudinary / AWS S3**: For storing high-resolution 4K client upload attachments in the cloud.
- **WhatsApp Cloud API Integration**: Automated instant WhatsApp acknowledgment messages to prospective customers when an inquiry is submitted.
- **Custom Domain & Branding**: Connect your custom domain (e.g. `www.sarojinisteel.com`) with free SSL certificates in 1 click under Render custom domains settings.

---

## 💻 Local Development Setup

```bash
# 1. Apply database migrations
python manage.py migrate

# 2. Seed showcase data & admin user
python manage.py seed_showcase

# 3. Test static file compilation
python manage.py collectstatic --no-input

# 4. Start local development server
python manage.py runserver 8000
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

### Default Welder Portal Credentials
- **URL**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin123`
*(Remember to change the password in the admin portal once deployed live!)*
