from django import forms
from .models import ClientInquiry, WorkCategory

class ClientInquiryForm(forms.ModelForm):
    class Meta:
        model = ClientInquiry
        fields = ['name', 'phone', 'email', 'service_interested', 'site_location', 'dimensions_or_notes', 'attachment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 text-sm transition',
                'placeholder': 'Your Full Name (e.g. Rajesh Kumar)',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 text-sm transition font-mono',
                'placeholder': 'Your 10-digit Phone Number (e.g. 98450 12345)',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 text-sm transition',
                'placeholder': 'Email Address (Optional)'
            }),
            'service_interested': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 text-sm transition',
                'placeholder': 'e.g. Heavy Sliding Gate / Cantilever Car Parking Shed'
            }),
            'site_location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 text-sm transition',
                'placeholder': 'Site / Project Location (e.g. Jubilee Hills, Hyderabad)'
            }),
            'dimensions_or_notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500 text-sm transition resize-none',
                'rows': 3,
                'placeholder': 'Approximate sizes, requirements, or design preferences...'
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 bg-slate-950 border border-slate-700/80 rounded-xl text-xs text-slate-400 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-amber-500/20 file:text-amber-400 hover:file:bg-amber-500/30'
            }),
        }
