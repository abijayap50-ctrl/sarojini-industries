from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from urllib.parse import quote_plus
from .models import WorkshopProfile, WorkCategory, ProjectShowcase, ClientInquiry
from .forms import ClientInquiryForm

def get_common_context():
    profile = WorkshopProfile.get_settings()
    categories = WorkCategory.objects.filter(is_active=True).prefetch_related('projects')
    return {
        'profile': profile,
        'categories': categories,
    }

def index_view(request):
    context = get_common_context()
    featured_projects = ProjectShowcase.objects.filter(is_active=True, is_featured=True).select_related('category')
    all_projects = ProjectShowcase.objects.filter(is_active=True).select_related('category').prefetch_related('gallery_images')
    inquiry_form = ClientInquiryForm()

    # Pre-build WhatsApp link generator helper
    profile = context['profile']
    wa_default_msg = f"Hello {profile.name}, I was viewing your welding & steel fabrication website and would like to request a quote / site measurement."
    wa_default_url = f"https://wa.me/{profile.whatsapp_number}?text={quote_plus(wa_default_msg)}"

    context.update({
        'featured_projects': featured_projects,
        'all_projects': all_projects,
        'inquiry_form': inquiry_form,
        'wa_default_url': wa_default_url,
    })
    return render(request, 'showcase/index.html', context)


def category_detail_view(request, slug):
    context = get_common_context()
    category = get_object_or_404(WorkCategory, slug=slug, is_active=True)
    projects = category.active_projects.prefetch_related('gallery_images')
    inquiry_form = ClientInquiryForm(initial={'service_interested': category.name})

    context.update({
        'selected_category': category,
        'projects': projects,
        'inquiry_form': inquiry_form,
    })
    return render(request, 'showcase/category_detail.html', context)


def project_detail_view(request, slug):
    context = get_common_context()
    project = get_object_or_404(ProjectShowcase, slug=slug, is_active=True)
    gallery_images = project.gallery_images.all()
    inquiry_form = ClientInquiryForm(initial={'service_interested': f"{project.title} ({project.category.name})"})

    profile = context['profile']
    wa_project_msg = f"Hello {profile.name}, I am interested in getting a quote for '{project.title}' ({project.dimensions}) as shown on your website."
    wa_project_url = f"https://wa.me/{profile.whatsapp_number}?text={quote_plus(wa_project_msg)}"

    context.update({
        'project': project,
        'gallery_images': gallery_images,
        'inquiry_form': inquiry_form,
        'wa_project_url': wa_project_url,
    })
    return render(request, 'showcase/project_detail.html', context)


def submit_inquiry_view(request):
    if request.method == 'POST':
        form = ClientInquiryForm(request.POST, request.FILES)
        if form.is_valid():
            inquiry = form.save()
            profile = WorkshopProfile.get_settings()
            
            # Prepare pre-filled WhatsApp message for user
            wa_text = f"Hi {profile.name}, I just submitted an inquiry on your website!\n\nName: {inquiry.name}\nPhone: {inquiry.phone}\nService: {inquiry.service_interested}\nLocation: {inquiry.site_location}\nNotes: {inquiry.dimensions_or_notes}"
            wa_url = f"https://wa.me/{profile.whatsapp_number}?text={quote_plus(wa_text)}"

            if request.headers.get('HX-Request'):
                return render(request, 'showcase/partials/inquiry_success.html', {
                    'inquiry': inquiry,
                    'profile': profile,
                    'wa_url': wa_url
                })

            messages.success(request, f"Thank you, {inquiry.name}! Your request has been received. Our master welder will call you shortly.")
            return redirect('showcase:index')
        else:
            messages.error(request, "Please check the phone number and required fields.")
    return redirect('showcase:index')
