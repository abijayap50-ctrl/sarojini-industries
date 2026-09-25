# Sarojini Steel Works &bull; Fabrication Showcase Website

A modern, high-performance, 100% open-source showcase platform for a professional welder and structural steel fabrication workshop.

## Features Built
1. **Dark Obsidian & Arc-Welding Spark Amber Theme**: Matches the approved high-fidelity design mockup.
2. **Section-by-Section Categorized Showcase**:
   - Heavy Gates & Entrances (Sliding, Swing, Laser-Cut CNC)
   - Steel Roofs & Structural Sheds (Clear-Span Truss, Polycarbonate Sit-Outs)
   - Car Parking Sheds (Cantilever Double-Car & Curved Arch)
   - Staircases & Architectural Railings (Mono-Stringer & Balcony Grills)
   - Safety Grills & Custom Repairs
3. **Zero-Crash Dynamic Category Engine**: The welder can add infinite new services and sections from the mobile admin without modifying code.
4. **Client Inquiries & Instant WhatsApp Deep-Linking**: Collects phone numbers, locations, and blueprints, while enabling instant WhatsApp quoting.
5. **Mobile-First Welder Admin Portal**: Mobile-friendly admin to manage inquiries, upload photos, and update workshop details.

## How to Run
```bash
# 1. Apply migrations (already done)
python manage.py migrate

# 2. Seed showcase data (already done)
python manage.py seed_showcase

# 3. Start local development server
python manage.py runserver 8000
```
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Credentials
- **Admin & Welder Control Portal**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin123`
