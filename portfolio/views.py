from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Project, Experience, Certification
from .forms import ContactForm

NAV_LINKS = [
    ("About", "about"), ("Projects", "projects"),
    ("Experience", "experience"), ("Education", "education"),
    ("Certifications", "certifications"), ("Contact", "contact")
]

HERO_STATS = [
    {"value": "3.8", "label": "Current GPA"}, 
    {"value": "3+", "label": "Internships"},
    {"value": "4+", "label": "Projects Built"}, 
    {"value": "4", "label": "Certifications"}
]

ABOUT_FACTS = [
    {"label": "Degree", "value": "B.S. Software Engineering"},
    {"label": "University", "value": "NUML, Faisalabad"},
    {"label": "GPA", "value": "3.8 / 4.0 (Sem 6)"},
    {"label": "Location", "value": "Faisalabad, Pakistan"},
    {"label": "Focus", "value": "ML / Data Science"},
    {"label": "Status", "value": "Open to Opportunities"},
]

SKILLS = [
    {"name": "Python", "pct": 90}, 
    {"name": "Machine Learning", "pct": 82},
    {"name": "Data Analysis", "pct": 85}, 
    {"name": "Django / Flask", "pct": 75},
    {"name": "SQL Databases", "pct": 78}, 
    {"name": "NLP & Text ML", "pct": 72},
]

EXTRA_TOOLS = [
    "NumPy", "Pandas", "Scikit-Learn", "Matplotlib", "Seaborn",
    "FastAPI", "Streamlit", "Flutter", "MySQL", "SQLite",
    "Git", "Linux", "Wireshark", "Jupyter", "VS Code"
]

OWNER = {
    "name": "Muhammad Arslan Ahmad",
    "title": "Python ML Developer & Data Science ETL → ML → LLMs-GenAI ",
    "location": "Faisalabad, Pakistan",
    "email": "developer.arslanahmad@gmail.com", # <--- UPDATE THIS
    "github": "https://github.com/MianArslan09", 
    "linkedin": "https://www.linkedin.com/in/-arslan-ahmad/", # <--- UPDATE THIS
    "about": "I am a Software Engineering student at NUML (7th Semester, GPA 3.8/4.0) with hands-on internship experience in ML, Data Science, and MarTech. I love turning raw data into impactful products.",
    "education": {
        "institution": "National University of Modern Languages (NUML)",
        "degree": "Bachelor of Science in Software Engineering",
        "semester": "7th Semester",
        "current_gpa": "3.8 / 4.0",
        "cgpa": "3.31 / 4.0",
    },
    "extracurricular": ["Active Member - NUML Debating Society"]
}

class HomeView(TemplateView):
    template_name = "portfolio/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["owner"] = OWNER
        ctx["nav_links"] = NAV_LINKS
        ctx["hero_stats"] = HERO_STATS
        ctx["about_facts"] = ABOUT_FACTS
        ctx["skills"] = SKILLS
        ctx["extra_tools"] = EXTRA_TOOLS
        ctx["featured_projects"] = Project.objects.filter(is_featured=True).order_by("order")
        ctx["all_projects"] = Project.objects.all().order_by("order")
        ctx["experiences"] = Experience.objects.all().order_by("order", "-start_date")
        ctx["certifications"] = Certification.objects.all().order_by("order")
        
        cat_map = {}
        for p in ctx["all_projects"]:
            if p.category not in cat_map:
                cat_map[p.category] = {"label": p.get_category_display(), "count": 0}
            cat_map[p.category]["count"] += 1
        
        ctx["project_categories"] = cat_map
        
        ctx["contact_info"] = [
            {"label": "Email", "value": OWNER["email"], "href": f"mailto:{OWNER['email']}", "icon": "fas fa-envelope"},
            {"label": "GitHub", "value": "github.com/MianArslan09", "href": OWNER["github"], "icon": "fab fa-github"},
            {"label": "LinkedIn", "value": "linkedin.com/in/-arslan-ahmad", "href": OWNER["linkedin"], "icon": "fab fa-linkedin"},
            {"label": "Location", "value": OWNER["location"], "href": "https://maps.google.com/?q=Faisalabad,+Pakistan", "icon": "fas fa-map-marker-alt"},
        ]
        ctx["contact_form"] = ContactForm()
        return ctx

class ContactFormView(View):
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        
        if form.is_valid():
            msg = form.save(commit=False)
            xf = request.META.get("HTTP_X_FORWARDED_FOR")
            msg.ip_address = xf.split(",")[0] if xf else request.META.get("REMOTE_ADDR")
            msg.save()
            
            if is_ajax: 
                return JsonResponse({"success": True})
            messages.success(request, "Message received! I will reply soon.")
            return redirect("portfolio:home")
        
        if is_ajax:
            return JsonResponse({"success": False, "errors": form.errors.get_json_data()}, status=400)
        
        ctx = HomeView().get_context_data()
        ctx["contact_form"] = form
        return render(request, "portfolio/index.html", ctx, status=422)