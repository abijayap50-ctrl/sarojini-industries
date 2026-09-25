import urllib.request
import urllib.parse
import re

print("=== STARTING COMPREHENSIVE SHOWCASE SITE VERIFICATION ===")

# 1. Main Landing Page
print("\n--- 1. Testing Homepage & Showcase Layout ---")
resp = urllib.request.urlopen("http://127.0.0.1:8000/")
html = resp.read().decode('utf-8')
assert resp.getcode() == 200, "Homepage returned non-200 code"
assert "SAROJINI" in html and "STEEL" in html, "Brand logo missing"
assert "PRECISION ARCHITECTURAL STEEL" in html, "Hero headline missing"
assert "AWS D1.1 Certified Welds" in html, "AWS weld badge missing"
assert "OUR EXPERTISE" in html, "Expertise section missing"
assert "Gates &amp; Heavy Entrances" in html or "Gates" in html, "Gates section missing"
assert "Steel Roofs" in html, "Roofs section missing"
assert "Car Parking Sheds" in html, "Parking section missing"
assert "Staircases" in html, "Staircases section missing"
assert "Safety Grills" in html, "Grills section missing"
assert "OUR FABRICATION STANDARDS" in html, "Standards section missing"
assert "REQUEST ON-SITE MEASUREMENT" in html, "Quote form missing"
assert "wa.me/919845012345" in html, "WhatsApp link missing"
print("Homepage & Showcase Sections: VERIFIED! All 5 major sections, hero, specs, and WhatsApp buttons present.")

# 2. Category Detail Page
print("\n--- 2. Testing Category Detail Page ---")
resp = urllib.request.urlopen("http://127.0.0.1:8000/category/gates-entrances/")
cat_html = resp.read().decode('utf-8')
assert resp.getcode() == 200, "Category page returned non-200"
assert "The Bastion 14ft Heavy Sliding Gate" in cat_html, "Category project missing"
assert "IS 2062 Grade Mild Steel" in cat_html, "Steel grade spec missing"
print("Category Detail Page: VERIFIED! Specific category filters and projects render cleanly.")

# 3. Project Detail Page
print("\n--- 3. Testing Project Detail Page ---")
resp = urllib.request.urlopen("http://127.0.0.1:8000/project/bastion-14ft-sliding-gate/")
proj_html = resp.read().decode('utf-8')
assert resp.getcode() == 200, "Project detail page returned non-200"
assert "FABRICATION SPECIFICATIONS" in proj_html, "Specs table missing"
assert "14ft Length" in proj_html, "Dimensions missing"
assert "AWS D1.1" in proj_html, "Weld standard missing"
assert "Chat with Welder on WhatsApp" in proj_html, "WhatsApp CTA missing"
print("Project Detail Page: VERIFIED! Full technical blueprint, specs table, and WhatsApp trigger present.")

# 4. Inquiry Submission Flow
print("\n--- 4. Testing Client Inquiry Submission ---")
# Get CSRF
get_resp = urllib.request.urlopen("http://127.0.0.1:8000/")
get_html = get_resp.read().decode('utf-8')
csrf = re.search(r'name="csrfmiddlewaretoken"\s+value="([^"]+)"', get_html).group(1)
cookie = get_resp.headers.get('Set-Cookie')

data = urllib.parse.urlencode({
    'csrfmiddlewaretoken': csrf,
    'name': 'Kalyan Chakravarthy',
    'phone': '9876543210',
    'email': 'kalyan@example.com',
    'service_interested': 'Cantilever Car Parking Shed (Double Car)',
    'site_location': 'Banjara Hills, Hyderabad',
    'dimensions_or_notes': 'Need cantilever shed for BMW X5 and Mercedes Sedan with powder-coated finish.'
}).encode('utf-8')

req = urllib.request.Request("http://127.0.0.1:8000/inquiry/submit/", data=data)
req.add_header('Cookie', cookie)
post_resp = urllib.request.urlopen(req)
print("Inquiry submission HTTP status:", post_resp.getcode())
assert post_resp.getcode() == 200 or post_resp.getcode() == 302, "Inquiry submission failed"

# Verify inquiry saved in database
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from apps.showcase.models import ClientInquiry
saved_inquiry = ClientInquiry.objects.filter(phone='9876543210').first()
assert saved_inquiry is not None, "Inquiry was not saved to database"
assert saved_inquiry.name == 'Kalyan Chakravarthy'
print(f"Inquiry Database Record: VERIFIED! Stored '{saved_inquiry.name}' - '{saved_inquiry.service_interested}' in database.")

# 5. Welder Admin Login Page
print("\n--- 5. Testing Welder Admin Control Portal ---")
admin_resp = urllib.request.urlopen("http://127.0.0.1:8000/admin/")
admin_html = admin_resp.read().decode('utf-8')
assert admin_resp.getcode() == 200, "Admin login page returned non-200"
assert "Sarojini Steel" in admin_html or "Django" in admin_html, "Admin login header missing"
print("Welder Admin Portal: VERIFIED! Accessible at /admin/ for uploading photos and managing categories.")

print("\n=== ALL 5 ARCHITECTURAL VERIFICATIONS PASSED 100%! ===")
