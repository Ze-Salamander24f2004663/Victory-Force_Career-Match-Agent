import re

def extract_skills_from_jd(job_text):
    keywords = re.findall(r"(?i)\b(?:skills?|technologies?|proficient in|experience with):?\b.*", job_text)
    skills = set()
    for line in keywords:
        for skill in re.split(r"[,;]\s*", line):
            s = re.sub(r"(?i)(skills?|technologies?|proficient in|experience with):?", "", skill).strip()
            if len(s) > 1:
                skills.add(s)
    return skills

def extract_stream_from_jd(job_text):
    job_text_lower = job_text.lower()
    if "commerce" in job_text_lower:
        return "Commerce"
    elif "science" in job_text_lower:
        return "Science"
    elif "arts" in job_text_lower or "art" in job_text_lower:
        return "Arts"
    else:
        return "Science"  # default

def evaluate_form_input(skills, experience_years, project_count, communication_score, job_text):
    mandatory = extract_skills_from_jd(job_text)
    if not mandatory:
        mandatory = {"Python", "JavaScript", "SQL", "Version Control"}

    extra_skills = {"React", "Node.js", "MongoDB", "Docker", "CI/CD", "Kubernetes", "AWS", "FastAPI"}

    skill_score = 0
    missing = mandatory - set(skills)
    if not missing:
        skill_score += 10
    else:
        skill_score += max(0, 10 - 2 * len(missing))
    if set(skills) & extra_skills:
        skill_score += 10
    skill_score = min(skill_score, 20)

    exp_score = 20 if experience_years >= 10 else 15 if experience_years >= 5 else 10 if experience_years > 0 else 0
    project_score = min(project_count * 10, 40)
    total = skill_score + exp_score + project_score + communication_score

    if total >= 85:
        fit = "Strong Match"
    elif total >= 65:
        fit = "Good Match"
    elif total >= 45:
        fit = "Average Fit"
    else:
        fit = "Weak Fit"

    suggestions = []
    if missing:
        suggestions.append("Missing mandatory skills: " + ", ".join(missing))
    if exp_score < 20:
        suggestions.append("Consider gaining more experience.")
    if project_score < 40:
        suggestions.append("Include more substantial project work.")
    if communication_score < 20:
        suggestions.append("Consider improving and mentioning language fluency.")

    return total, fit, suggestions
