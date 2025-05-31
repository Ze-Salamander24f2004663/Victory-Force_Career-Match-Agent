from transformers import pipeline
from config import HUGGINGFACE_API_KEY, LLM_MODEL

def get_match_score(resume_text, job_description):
    prompt = (
        "Evaluate the candidate's resume for the following job description.\n"
        "Resume:\n"
        f"{resume_text}\n\n"
        "Job Description:\n"
        f"{job_description}\n\n"
        "Provide a score from 1 to 100 and a brief explanation."
    )
    pipe = pipeline("text-generation", model=LLM_MODEL, token=HUGGINGFACE_API_KEY)
    response = pipe(prompt, max_length=500, do_sample=False)
    return response[0]["generated_text"]