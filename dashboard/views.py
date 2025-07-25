from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Validate_form
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
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
        return redirect("dashboard:feasibility")
    return render(request,"dashboard/update.html",{'entry': entry})

# ================== AI Sugg Feature ===================
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
        # Save data to session for later use in SWOT page
        request.session["startup_data"] = {
        "startup_idea": startup_idea,
        "business_domain": business_domain,
        "problem_statement": problem_statement,
        "business_goal": business_goal,
        "monetization_strategy": monetization_strategy,
        "social_impact": social_impact,
        "timeline": timeline
        }


        # request.session["startup_data"] = form

        return redirect("dashboard:swot")

    return render(request,"dashboard/dashboard.html")


# ============================================SWOT Page===============================================================================
# @login_required
# def swot(request):
    
#     return render(request,"dashboard/swot.html")

# =================================================feasibility_score====================================================================

def generate_response(prompt):
    api = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=AIzaSyCGqjrH4vDQVeKu_cepFVYxI5hy_rtJNQw"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()

        candidates = result.get("candidates")
        if not candidates or not isinstance(candidates, list):
            return "⚠️ Error: No valid candidates in AI response."

        parts = candidates[0].get("content", {}).get("parts")
        if not parts or not isinstance(parts, list):
            return "⚠️ Error: No valid parts in AI response."

        ai_text = parts[0].get("text")
        if not ai_text:
            return "⚠️ Error: AI response was empty."

        return ai_text.strip()

    
    except requests.exceptions.RequestException as e:
        print("Network/API error:", e)
    
    # Handle 429 separately if response exists
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code == 429:
                return "⚠️ API Limit Reached: Too many requests."

        return f"⚠️ API Error: {str(e)}"


    except Exception as e:
        print("Unexpected error:", e)
        return f"⚠️ Unexpected Error: {str(e)}"


# def feasibility(request):
    
#     return render(request,"dashboard/feasibility_score.html")


# newwwwww with polish style 
@login_required
def swot(request):
    startup_data = request.session.get("startup_data")

    if not startup_data:
        return redirect("dashboard:dashboard")

    # Safe data extraction with fallback to empty string
    idea = startup_data.get('startup_idea', '')
    domain = startup_data.get('business_domain', '')
    problem = startup_data.get('problem_statement', '')
    goal = startup_data.get('business_goal', '')
    monetization = startup_data.get('monetization_strategy', '')
    social_impact = startup_data.get('social_impact', '')
    timeline = startup_data.get('timeline', '')

    prompt = f"""
IMPORTANT: Do NOT include triple backticks or markdown. Output clean HTML only.

Based on the following startup details, provide a SWOT Analysis in HTML boxes:

Idea: {idea}
Domain: {domain}
Problem: {problem}
Goal: {goal}
Monetization: {monetization}
Social Impact: {social_impact}
Timeline: {timeline}

FORMAT REQUIREMENTS:
- Wrap each section in a <div class="swot-box swot-[type]"> with proper class:
  - swot-strength, swot-weakness, swot-opportunity, swot-threat.
- Each section should have <h2> and a <ul><li> list.
- Example:
  <div class="swot-box swot-strength">
    <h2>Strengths</h2>
    <ul><li>Point 1</li><li>Point 2</li></ul>
  </div>
- Use clean business language and avoid robotic phrasing.
- NO markdown, NO ```html.

Now generate only the HTML.
"""

    swot_text = generate_response(prompt)

    # Strip markdown markers if accidentally added
    if swot_text.startswith("```html"):
        swot_text = swot_text.replace("```html", "").strip()
    if swot_text.endswith("```"):
        swot_text = swot_text.rsplit("```", 1)[0].strip()

    return render(request, "dashboard/swot.html", {"swot_raw": swot_text})


# === Feasibility View ===
type(requests)
@login_required
def feasibility(request):
    startup_data = request.session.get("startup_data")
    if not startup_data:
        return redirect("dashboard:dashboard")

    # Extract startup details
    idea = startup_data.get('startup_idea', '')
    domain = startup_data.get('business_domain', '')
    problem = startup_data.get('problem_statement', '')
    goal = startup_data.get('business_goal', '')
    monetization = startup_data.get('monetization_strategy', '')
    impact = startup_data.get('social_impact', '')
    timeline = startup_data.get('timeline', '')

    # Prompt for JSON data (NOT HTML)
    prompt = f"""
IMPORTANT: Give output ONLY JSON. NO HTML, NO markdown.

Startup Details:
Idea: {idea}
Domain: {domain}
Problem: {problem}
Goal: {goal}
Monetization: {monetization}
Impact: {impact}
Timeline: {timeline}

JSON FORMAT:
{{
  "score": 82,
  "level": "HIGH",
  "emoji": "🟢",
  "summary": "This feasibility score reflects...",
  "market_demand": {{
    "level": "HIGH",
    "emoji": "🟢",
    "text": "The market is highly receptive..."
  }},
  "competition": {{
    "level": "MEDIUM",
    "emoji": "🟡",
    "text": "Moderate competition exists..."
  }},
  "technical_feasibility": {{
    "level": "HIGH",
    "emoji": "🟢",
    "text": "Technology requirements are easy..."
  }},
  "financial_feasibility": {{
    "level": "LOW",
    "emoji": "🔴",
    "text": "Financial risks are present..."
  }}
}}
"""

    raw_response = generate_response(prompt)

    # Fix: Remove ```json and ``` if present
    if raw_response.startswith("```json"):
        raw_response = raw_response.replace("```json", "").strip()
    if raw_response.endswith("```"):
        raw_response = raw_response.rsplit("```", 1)[0].strip()

# Debug again
    print("CLEANED AI RESPONSE:\n", raw_response)

    print("RAW AI RESPONSE:\n", raw_response)


    import json
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError:
        data = {
            "score": 0, "level": "N/A", "emoji": "⚠️", "summary": "⚠️ Error parsing AI response.",
            "market_demand": {"level": "N/A", "emoji": "⚠️", "text": "No data"},
            "competition": {"level": "N/A", "emoji": "⚠️", "text": "No data"},
            "technical_feasibility": {"level": "N/A", "emoji": "⚠️", "text": "No data"},
            "financial_feasibility": {"level": "N/A", "emoji": "⚠️", "text": "No data"},
        }

    return render(request, "dashboard/feasibility_score.html", {"data": data})

@login_required
def monetization(request):
    startup_data = request.session.get("startup_data")

    if not startup_data:
        return redirect("dashboard:dashboard")

    # Extract startup details
    idea = startup_data.get('startup_idea', '')
    domain = startup_data.get('business_domain', '')
    problem = startup_data.get('problem_statement', '')
    goal = startup_data.get('business_goal', '')
    monetization = startup_data.get('monetization_strategy', '')
    impact = startup_data.get('social_impact', '')
    timeline = startup_data.get('timeline', '')

    # Prompt for AI
    prompt = f"""
IMPORTANT: Output ONLY HTML. No markdown. No ```html.

Based on the startup info below, give a revenue model analysis with strategies.

Startup Details:
Idea: {idea}
Domain: {domain}
Problem: {problem}
Goal: {goal}
Monetization Strategy: {monetization}
Impact: {impact}
Timeline: {timeline}

FORMAT:
<div class="revenue-box">
  <h3>Suggested Revenue Model</h3>
  <p>...</p>
</div>

<div class="revenue-box">
  <h3>Pricing Strategy</h3>
  <p>...</p>
</div>

<div class="revenue-box">
  <h3>Financial Risks</h3>
  <p>...</p>
</div>

Keep tone professional and concise. Just output clean HTML for these 3 boxes.
"""

    monetization_html = generate_response(prompt)

    # Clean any markdown markers if accidentally included
    if monetization_html.startswith("```html"):
        monetization_html = monetization_html.replace("```html", "").strip()
    if monetization_html.endswith("```"):
        monetization_html = monetization_html.rsplit("```", 1)[0].strip()

    return render(request, "dashboard/monetization.html", {"monetization_html": monetization_html})




#  # ========================================================= CORRECT API for SWOT =======================================================================
# def generate_response(prompt):
#     api = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=AIzaSyCGqjrH4vDQVeKu_cepFVYxI5hy_rtJNQw"

#     payload = {
#         "contents": [{"parts": [{"text": prompt}]}]
#     }

#     headers = {
#         "Content-Type": "application/json"
#     }

#     try:
#         response = requests.post(api, json=payload, headers=headers, timeout=10)
#         response.raise_for_status()  # Raises HTTPError for bad response

#         result = response.json()

#         # Debug log (remove later)
#         print("AI Response:", result)

#         # Validate structure before accessing
#         candidates = result.get("candidates")
#         if not candidates or not isinstance(candidates, list):
#             return "⚠️ Error: No valid candidates in AI response."

#         parts = candidates[0].get("content", {}).get("parts")
#         if not parts or not isinstance(parts, list):
#             return "⚠️ Error: No valid parts in AI response."

#         swot_text = parts[0].get("text")
#         if not swot_text:
#             return "⚠️ Error: AI response was empty."

#         return swot_text.strip()

    

#     except Exception as e:
#         print("Unexpected error:", e)
#         return f"⚠️ Unexpected Error: {str(e)}"
#     except requests.exceptions.RequestException as e:
#         print("Network/API error:", e)
#     if response.status_code == 429:
#         return "⚠️ API Limit Reached: Too many requests. Please wait and try again."
#     return f"⚠️ API Error: {str(e)}"
#     print("API RESPONSE STATUS:", response.status_code)
#     print("API RAW RESPONSE:", response.text)