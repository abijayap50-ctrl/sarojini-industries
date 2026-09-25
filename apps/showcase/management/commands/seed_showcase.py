from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.showcase.models import WorkshopProfile, WorkCategory, ProjectShowcase, ProjectImage, ClientInquiry

class Command(BaseCommand):
    help = "Seeds initial showcase categories, projects, images, and admin credentials"

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding for Sarojini Steel Works...")

        # 1. Create or update Superuser
        admin_user, created = User.objects.get_or_create(username="admin")
        if created:
            admin_user.set_password("admin123")
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))
        else:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write("Admin user already exists, updated password to admin123")

        # 2. Workshop Profile
        profile, _ = WorkshopProfile.objects.get_or_create(id=1)
        profile.name = "SAROJINI STEEL WORKS"
        profile.tagline = "Precision Architectural Steel & Heavy Fabrication"
        profile.master_welder = "Er. Vikram Rao (Master Structural Fabricator)"
        profile.phone = "+91 98450 12345"
        profile.whatsapp_number = "919845012345"
        profile.email = "contact@sarojinisteel.com"
        profile.workshop_address = "Plot 42, Heavy Industrial Fabrications Yard, Phase 2"
        profile.city = "Hyderabad, Telangana"
        profile.working_hours = "Mon - Sat: 8:00 AM - 7:30 PM (Sunday Site Visits on Request)"
        profile.years_experience = 15
        profile.projects_completed = 650
        profile.warranty_years = 10
        profile.certification_badge = "AWS D1.1 Certified Welds & IS 2062 Structural Steel"
        profile.google_maps_url = "https://maps.google.com"
        profile.save()
        self.stdout.write(self.style.SUCCESS("Configured WorkshopProfile settings"))

        # 3. Work Categories
        categories_data = [
            {
                "name": "Gates & Heavy Entrances",
                "slug": "gates-entrances",
                "badge_text": "Architectural & Motorized",
                "icon_svg": "gate",
                "short_description": "Heavy sliding gates, cantilever driveway entrances, and laser-cut sheet steel gates with heavy-duty ball bearing rollers and motorized automation readiness.",
                "display_order": 1,
            },
            {
                "name": "Steel Roofs & Structural Sheds",
                "slug": "steel-roofs-sheds",
                "badge_text": "Heavy Truss & Clear-Span",
                "icon_svg": "roof",
                "short_description": "Engineered factory sheds, terrace sit-out sheds, and polycarbonate/PPGI roofing built with heavy structural MS trusses designed to withstand monsoon storms.",
                "display_order": 2,
            },
            {
                "name": "Car Parking Sheds",
                "slug": "car-parking-sheds",
                "badge_text": "Cantilever & Curved Arch",
                "icon_svg": "parking",
                "short_description": "Single and multi-vehicle cantilever parking canopies with zero obstacle posts on the drive side, finished in weather-resistant zinc primer and epoxy enamel.",
                "display_order": 3,
            },
            {
                "name": "Staircases & Architectural Railings",
                "slug": "staircases-railings",
                "badge_text": "Precision Laser & Wrought Iron",
                "icon_svg": "stairs",
                "short_description": "Spiral staircases, mono-stringer floating stairs with chequered plate steps, and contemporary balcony railings fabricated with tight AWS D1.1 weld seams.",
                "display_order": 4,
            },
            {
                "name": "Safety Grills & Custom Welding",
                "slug": "safety-grills-custom-welding",
                "badge_text": "Anti-Theft & Custom Fitment",
                "icon_svg": "grill",
                "short_description": "Heavy window safety grills, compound wall security spike fencing, on-site structural modifications, and heavy machinery frame welding repairs.",
                "display_order": 5,
            },
        ]

        cat_objs = {}
        for cdata in categories_data:
            cat, _ = WorkCategory.objects.get_or_create(
                slug=cdata["slug"],
                defaults={
                    "name": cdata["name"],
                    "badge_text": cdata["badge_text"],
                    "icon_svg": cdata["icon_svg"],
                    "short_description": cdata["short_description"],
                    "display_order": cdata["display_order"],
                    "is_active": True,
                }
            )
            cat_objs[cdata["slug"]] = cat

        self.stdout.write(self.style.SUCCESS(f"Created {len(cat_objs)} Work Categories"))

        # 4. Project Showcase Data
        projects_data = [
            # GATES
            {
                "category": cat_objs["gates-entrances"],
                "title": "The Bastion 14ft Heavy Sliding Gate with CNC Laser Cut Panel",
                "slug": "bastion-14ft-sliding-gate",
                "subtitle": "Fabricated for luxury residential villa in Jubilee Hills with Italian motorized track",
                "description": "Engineered with 50x50mm 2.5mm heavy-gauge MS hollow sections, featuring precision CNC 3.0mm laser-cut privacy accent panels. Fitted with hardened steel sealed ball-bearing bottom rollers, internal slam-locks, and zinc epoxy primer undercoat.",
                "cover_image_url": "https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=1200&q=80",
                "steel_grade": "IS 2062 Grade Mild Steel (Apollo Tubes)",
                "dimensions": "14ft Length × 7ft Height (500kg Capacity)",
                "thickness_gauge": "2.5mm Heavy Square Tube & 3mm CNC Sheet",
                "coating_finish": "Anti-Rust Zinc Phosphate + Matte Charcoal PU Enamel",
                "weld_standard": "Full-Penetration Structural MIG Welds (AWS D1.1)",
                "estimated_timeline": "5 - 7 Working Days Fabrication",
                "site_location": "Jubilee Hills, Hyderabad",
                "rating_score": 4.9,
                "review_count": 112,
                "is_featured": True,
                "display_order": 1,
            },
            {
                "category": cat_objs["gates-entrances"],
                "title": "Minimalist Dual Swing Entrance Gate with Vertical Louvers",
                "slug": "minimalist-dual-swing-gate",
                "subtitle": "Contemporary architectural swing gate with heavy forged pivot hinges",
                "description": "Fabricated with alternating 40x20mm vertical steel louvers providing both privacy and air circulation. Equipped with heavy 120mm bullet hinges with greased brass washers for buttery-smooth opening.",
                "cover_image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=80",
                "steel_grade": "IS 2062 Heavy MS Pipe & Louvers",
                "dimensions": "12ft Width × 6.5ft Height (Dual 6ft Leaves)",
                "thickness_gauge": "2.0mm Wall Thickness",
                "coating_finish": "Epoxy Zinc Primer + Satin Anthracite Gray",
                "weld_standard": "TIG Dressed Face Welds + Internal MIG Beads",
                "estimated_timeline": "4 - 5 Working Days",
                "site_location": "Gachibowli, Hyderabad",
                "rating_score": 4.8,
                "review_count": 64,
                "is_featured": True,
                "display_order": 2,
            },

            # STEEL ROOFS & SHEDS
            {
                "category": cat_objs["steel-roofs-sheds"],
                "title": "Industrial Warehouse Clear-Span Truss Roof (40ft Width)",
                "slug": "industrial-warehouse-truss-roof",
                "subtitle": "Heavy manufacturing bay structural steel shed with integrated storm water gutter",
                "description": "Constructed using welded Pratt and Warren steel trusses utilizing 75x40mm MS channels and 50x50mm angle iron. Designed for 150 km/h wind shear tolerance with heat-reflective PPGI color-coated roof sheets and transparent polycarbonate skylights.",
                "cover_image_url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1200&q=80",
                "steel_grade": "Heavy Structural Steel (Tata Structura / Jindal)",
                "dimensions": "40ft Clear Span × 80ft Bay Length",
                "thickness_gauge": "3.2mm - 4.5mm Heavy Angle & Channel Sections",
                "coating_finish": "Two Coats Red Oxide + Industrial Silver Aluminum",
                "weld_standard": "AWS D1.1 Certified Structural Arc & MIG",
                "estimated_timeline": "14 - 18 Working Days",
                "site_location": "Patancheru Industrial Area, Hyderabad",
                "rating_score": 5.0,
                "review_count": 155,
                "is_featured": True,
                "display_order": 3,
            },
            {
                "category": cat_objs["steel-roofs-sheds"],
                "title": "Terrace Sit-Out Pergola & Polycarbonate Rain Shed",
                "slug": "terrace-pergola-polycarbonate-shed",
                "subtitle": "Waterproof terrace recreation canopy with UV-protected tinted roofing",
                "description": "Modern minimalist pergola framework fabricated from 80x40mm rectangular steel hollow sections. Topped with 3mm multi-wall UV-coated polycarbonate sheets that provide 100% rain protection while filtering gentle daylight.",
                "cover_image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=80",
                "steel_grade": "IS 2062 Grade RHS & SHS Tubes",
                "dimensions": "20ft × 15ft Terrace Coverage Area",
                "thickness_gauge": "2.0mm Heavy Tube Gauge",
                "coating_finish": "Polyurethane Anti-Corrosion Coating (Matte Black)",
                "weld_standard": "Grind-Flushed Cosmetic Architectural Welds",
                "estimated_timeline": "3 - 4 Working Days",
                "site_location": "Kavuri Hills, Hyderabad",
                "rating_score": 4.9,
                "review_count": 88,
                "is_featured": False,
                "display_order": 4,
            },

            # CAR PARKING SHEDS
            {
                "category": cat_objs["car-parking-sheds"],
                "title": "Cantilever Architectural Double Car Parking Shed",
                "slug": "cantilever-double-car-parking-shed",
                "subtitle": "Single-side post design allowing full door clearance for 2 SUVs",
                "description": "Engineered with heavy 100x100mm 4.0mm MS vertical columns securely anchored into M25 concrete footings with 20mm chemical anchor studs. Curved cantilever overhang shields luxury vehicles from harsh sun, hail, and monsoon downpours.",
                "cover_image_url": "https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1200&q=80",
                "steel_grade": "IS 2062 Grade Structural MS Columns & Arches",
                "dimensions": "18ft Width × 18ft Projection (2 Car Bays)",
                "thickness_gauge": "4.0mm Columns & 2.5mm Arch Purlins",
                "coating_finish": "High-Gloss Marine Epoxy Primer & PU Topcoat",
                "weld_standard": "AWS Certified Full Gusset Penetration Welds",
                "estimated_timeline": "4 - 6 Working Days",
                "site_location": "Madhapur, Hyderabad",
                "rating_score": 4.9,
                "review_count": 96,
                "is_featured": True,
                "display_order": 5,
            },
            {
                "category": cat_objs["car-parking-sheds"],
                "title": "Curved Arch Commercial Parking Canopy (Multi-Bay)",
                "slug": "curved-arch-commercial-parking-canopy",
                "subtitle": "Fabricated for apartment complex and commercial IT park parking lots",
                "description": "Continuous arched modular carport bays constructed using roll-bent 60mm round hollow sections (CHS) and color-coated steel sheeting with built-in drainage spouts to prevent rainwater splashing on parked cars.",
                "cover_image_url": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80",
                "steel_grade": "IS 2062 Circular Hollow Sections (CHS)",
                "dimensions": "50ft Length (Modular 5-Car Bay System)",
                "thickness_gauge": "3.0mm Heavy MS Pipe",
                "coating_finish": "Two Coats Zinc Rich Primer + Exterior Enamel",
                "weld_standard": "MIG Structural Fillet & Butt Welds",
                "estimated_timeline": "7 - 10 Working Days",
                "site_location": "Financial District, Hyderabad",
                "rating_score": 4.8,
                "review_count": 72,
                "is_featured": False,
                "display_order": 6,
            },

            # STAIRCASES & RAILINGS
            {
                "category": cat_objs["staircases-railings"],
                "title": "Industrial Floating Mono-Stringer Steel Staircase",
                "slug": "floating-mono-stringer-steel-staircase",
                "subtitle": "Central heavy box beam spine with precision laser-cut step plates",
                "description": "Architectural interior/exterior staircase supported by a single massive 150x75mm heavy rectangular steel spine. Tread brackets welded with high-tensile MIG beads, designed for wooden planks or 4mm anti-skid chequered steel plates.",
                "cover_image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=80",
                "steel_grade": "Heavy Structural Grade C-Channel & Box Section",
                "dimensions": "10ft Floor-to-Floor Height (16 Risers)",
                "thickness_gauge": "4.5mm Spine & 4.0mm Chequered Step Plates",
                "coating_finish": "Automotive Powder Coat Matte Textured Black",
                "weld_standard": "High-Load AWS Tested Structural Seams",
                "estimated_timeline": "6 - 8 Working Days",
                "site_location": "Banjara Hills, Hyderabad",
                "rating_score": 4.9,
                "review_count": 54,
                "is_featured": True,
                "display_order": 7,
            },

            # SAFETY GRILLS & CUSTOM WELDING
            {
                "category": cat_objs["safety-grills-custom-welding"],
                "title": "Heavy-Duty Laser-Cut Balcony Safety Enclosure & Grills",
                "slug": "heavy-duty-safety-grills-enclosure",
                "subtitle": "Full height safety screen preventing intrusions with architectural aesthetic",
                "description": "Constructed with solid 12x12mm MS bright square bars and decorative CNC border patterns. Embedded directly into RCC lintels with high-tensile expansion anchors for tamper-proof security.",
                "cover_image_url": "https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?auto=format&fit=crop&w=1200&q=80",
                "steel_grade": "Solid Mild Steel Square Bars & Outer 40x40mm Frame",
                "dimensions": "Standard & Custom Window / Balcony Openings",
                "thickness_gauge": "Solid 12mm Square Bars + 2.5mm Outer Frame",
                "coating_finish": "Anti-Corrosive Epoxy Undercoat + Gloss Enamel",
                "weld_standard": "Fully Welded Intersecting Joints (No Rivets)",
                "estimated_timeline": "3 - 5 Working Days",
                "site_location": "Kondapur, Hyderabad",
                "rating_score": 4.8,
                "review_count": 92,
                "is_featured": True,
                "display_order": 8,
            },
        ]

        for pdata in projects_data:
            proj, _ = ProjectShowcase.objects.get_or_create(
                slug=pdata["slug"],
                defaults=pdata
            )

        self.stdout.write(self.style.SUCCESS(f"Created {len(projects_data)} Showcase Projects across all categories"))

        # 5. Create a sample client inquiry
        inquiry, _ = ClientInquiry.objects.get_or_create(
            phone="9845012345",
            name="Rajeshwar Rao",
            defaults={
                "service_interested": "14ft Heavy Sliding Gate & Double Car Parking Shed",
                "site_location": "Jubilee Hills Road No. 36",
                "dimensions_or_notes": "We need a 14ft motorized sliding gate and a curved parking shed for 2 cars before house warming next month.",
                "status": ClientInquiry.STATUS_NEW,
                "admin_remarks": "Customer called from website; scheduled site measurement visit for Saturday 11:00 AM."
            }
        )

        self.stdout.write(self.style.SUCCESS(f"Seeded sample inquiry from {inquiry.name}"))
        self.stdout.write(self.style.SUCCESS("\n[SUCCESS] Database successfully seeded with full showcase content!"))
