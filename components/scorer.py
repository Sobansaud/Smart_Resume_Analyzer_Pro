class Score:
    def __init__(self, extracted_skills, all_skills):
        self.extracted_skills = extracted_skills
        self.all_skills = all_skills

    def calculate(self):
        if not self.all_skills:
            return 0.0
        matched = len(self.extracted_skills)
        total = len(self.all_skills)
        score = (matched / total) * 100
        return round(score, 2)

    def display_feedback(self, score):
        if score >= 75:
            return "✅ Great! Your Resume Is Well-Optimized"
        elif score >= 50:
            return "🟡 Good! Your Resume Has Some Strong Points"
        else:
            return "⚠️ Needs Improvement. Add more relevant skills."
