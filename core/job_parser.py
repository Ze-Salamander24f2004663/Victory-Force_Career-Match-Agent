def parse_job_description(text_path):
    with open(text_path, "r", encoding="utf-8") as file:
        return file.read()