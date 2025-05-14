import pandas as pd
import re

class Skills:
    def __init__(self, text):
        self.text = text.lower()
        self.skills = []

    def load_skills(self, skills_file):
        try:
            skills_df = pd.read_csv(skills_file)
            self.skills_list = skills_df["skills"].str.lower().tolist()
        except Exception as e:
            return f"Error loading skills {e}"
        
    def extracted_skills(self):
        found = []
        for skill in self.skills_list:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, self.text):
                found.append(skill)
        self.skills = found
        return found
