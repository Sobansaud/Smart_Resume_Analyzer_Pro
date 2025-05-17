

import os
import cohere
# from cohere.errors import CohereError

def generate_cv_cohere_chat(name, email, education, experience, skills, interests):
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    
    prompt = (
        f"Please write a professional CV in markdown format with the following details:\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Education: {education}\n"
        f"Experience: {experience}\n"
        f"Skills: {skills}\n"
        f"Interests: {interests}\n"
        f"Make sure the CV is well-structured, clean, and ready for job applications."
    )

    try:
        response = co.chat(
            model="command-xlarge-nightly",
            message=prompt,  # 👈 Corrected from 'messages' to 'message'
            temperature=0.7,
            max_tokens=800,
            stop_sequences=["--END--"]
        )
        return response.text.strip()

    # except CohereError as e:
    #     return f"❌ Failed to generate CV: {e}"

    except Exception as e:
        return f"❌ Unexpected error occurred: {e}"
