from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Validate_form
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

def swot(request):
    return render(request,"dashboard/swot.html")

def feasibility(request):
    return render(request, 'dashboard/feasibility.html')


def risk(request):
    return render(request, "dashboard/risk.html")

# ==============================================================Read Operation====================================================
def history(request):
    entries = Validate_form.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "dashboard/history.html", {"submissions": entries})

@login_required
def delete_submission(request,id):
    entry = get_object_or_404(Validate_form, id=id, user=request.user)
    if request.method == "POST":
        entry.delete()
        messages.success(request, "Submission deleted.")
    return redirect('dashboard:history')

@login_required
def update_message(request,id):
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
    return render(request,"dashboard/update.html",{'entry': entry})



@login_required
def dashboard(request):
    if request.method=="POST":
        user=request.user
        print("Logged in user:", user)
        startup_idea = request.POST.get("startup_idea")
        business_domain = request.POST.get("business_domain")
        problem_statement = request.POST.get("problem_statement")

        business_goal = request.POST.get("business_goal")
        monetization_strategy = request.POST.get("monetization_strategy")
        social_impact = request.POST.get("social_impact")
        timeline = request.POST.get("timeline")
# ========================================================Creating an object=============================================================
        form = Validate_form(
            user=request.user,
            startup_idea=startup_idea,
            business_domain=business_domain,
            problem_statement=problem_statement,
            business_goal=business_goal,
            monetization_strategy=monetization_strategy,
            social_impact=social_impact,
            timeline=timeline,
        )
        form.save()
        print("User in POST request:", request.user)

        return redirect("dashboard:dashboard")

    return render(request,"dashboard/dashboard.html")


# ============================================SWOT Page===============================================================================
@login_required
def swot(request):
    
    return render(request,"dashboard/swot.html")

