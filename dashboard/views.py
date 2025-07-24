from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Validate_form
from django.contrib import messages
import requests

# API Key (ensure security in production)
api_key = "AIzaSyCGqjrH4vDQVeKu_cepFVYxI5hy_rtJNQw"

# ====================== PAGES ======================
def swot(request):
    return render(request, "dashboard/swot.html")

def feasibility(request):
    return render(request, 'dashboard/feasibility.html')

def risk(request):
    return render(request, "dashboard/risk.html")

def guide(request):
    return render(request, "dashboard/guide.html")

# =================== CRUD Operations ====================
@login_required
def dashboard(request):
    if request.method == "POST":
        user = request.user
        startup_idea = request.POST.get("startup_idea")
        business_domain = request.POST.get("business_domain")
        problem_statement = request.POST.get("problem_statement")
        business_goal = request.POST.get("business_goal")
        monetization_strategy = request.POST.get("monetization_strategy")
        social_impact = request.POST.get("social_impact")
        timeline = request.POST.get("timeline")

        form = Validate_form(
            user=user,
            startup_idea=startup_idea,
            business_domain=business_domain,
            problem_statement=problem_statement,
            business_goal=business_goal,
            monetization_strategy=monetization_strategy,
            social_impact=social_impact,
            timeline=timeline,
        )
        form.save()
        messages.success(request, "Startup idea submitted successfully.")
        return redirect("dashboard:dashboard")

    return render(request, "dashboard/dashboard.html")

@login_required
def history(request):
    entries = Validate_form.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "dashboard/history.html", {"submissions": entries})

@login_required
def delete_submission(request, id):
    entry = get_object_or_404(Validate_form, id=id, user=request.user)
    if request.method == "POST":
        entry.delete()
        messages.success(request, "Submission deleted.")
    return redirect('dashboard:history')

@login_required
def update_message(request, id):
    entry = get_object_or_404(Validate_form, id=id, user=request.user)
    if request.method == "POST":
        entry.startup_idea = request.POST.get("startup_idea")
        entry.business_domain = request.POST.get("business_domain")
        entry.problem_statement = request.POST.get("problem_statement")
        entry.business_goal = request.POST.get("business_goal")
        entry.monetization_strategy = request.POST.get("monetization_strategy")
        entry.social_impact = request.POST.get("social_impact")
        entry.timeline = request.POST.get("timeline")
        entry.save()
        messages.success(request, "Submission updated successfully.")
        return redirect("dashboard:history")
    return render(request, "dashboard/update.html", {'entry': entry})

# ================== AI Sugg Feature ===================
@login_required
def ai_sugg(request):
    if request.method == "POST":
        query = request.POST.get("query")
        response = generate_response(query)
        parameters = {
            "response": response,
        }
        return render(request, "dashboard/ai_sugg.html", parameters)
    return render(request, "dashboard/ai_sugg.html")

def generate_response(query):
    prompt = "You are a startup validator expert who has all the knowledge of the market and have good skills to validate a startup idea. By using simple hinglish, respond to the user who will ask their query to you related to their startup idea. The idea is: " + query

    api = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + api_key
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(api, json=payload, headers=headers)
    print(response.status_code)

    response_text = eval(response.text)["candidates"][0]["content"]["parts"][0]["text"]
    return response_text
