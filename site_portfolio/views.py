from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.contrib import messages
import os
import threading
from django.shortcuts import redirect
from .models import Project, Resume

def index(request):
    projects = Project.objects.order_by('order')
    return render(request, 'site_portfolio/index.html', {'projects': projects})

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'site_portfolio/project_detail.html', {'project': project})

def send_email_async(message):
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"✅ Email sent: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not email or not message:
            messages.error(request, "⚠️ Please fill out all fields.")
            return redirect("site_portfolio:contact")

        subject = f"Portfolio Contact: {name}"
        html_content = f"""
            <h2>New Message from Portfolio</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Message:</strong><br>{message}</p>
        """

        try:
            mail = Mail(
                from_email="sarvesvararamar.work@gmail.com",
                to_emails="sarvesvarasar@gmail.com",
                subject=subject,
                html_content=html_content,
            )

            threading.Thread(target=send_email_async, args=(mail,)).start()
            messages.success(request, "✅ Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"❌ Error preparing contact email: {e}")

        return redirect("site_portfolio:contact")

    return render(request, "site_portfolio/contact.html")
    
def download_resume(request):
    latest_resume = Resume.objects.order_by('-uploaded_at').first()
    if not latest_resume:
        raise Http404("Resume not found.")
    return FileResponse(latest_resume.file.open('rb'), as_attachment=True, filename=latest_resume.file.name.split('/')[-1])
