from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from .models import Project, Resume

def index(request):
    projects = Project.objects.order_by('order')
    return render(request, 'site_portfolio/index.html', {'projects': projects})

def project_detail(request, slug):
    projects = get_object_or_404(Project, slug=slug)
    return render(request, 'site_portfolio/project_detail.html', {'projects': projects})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # Basic validation
        if not name or not email or not message:
            messages.error(request, "All fields are required.")
            return redirect('site_portfolio:contact')

        subject = f"Portfolio Contact: Message from {name}"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject=subject,
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,  # Your site email
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Goes to you
                fail_silently=False,
            )
            messages.success(request, "Thank you for reaching out! Your message has been sent successfully.")
            return redirect('site_portfolio:contact')

        except BadHeaderError:
            messages.error(request, "Invalid header found.")
            return redirect('site_portfolio:contact')

        except Exception as e:
            print("Error sending contact email:", e)
            messages.error(request, "Something went wrong. Please try again later.")
            return redirect('site_portfolio:contact')

    # GET request — just render the contact form
    return render(request, 'site_portfolio/contact.html')

def download_resume(request):
    latest_resume = Resume.objects.order_by('-uploaded_at').first()
    if not latest_resume:
        raise Http404("Resume not found.")
    return FileResponse(latest_resume.file.open('rb'), as_attachment=True, filename=latest_resume.file.name.split('/')[-1])
