from services.llm_service import get_match_score

def evaluate_candidate(resume_text, job_description):
    result = get_match_score(resume_text, job_description)
    return result