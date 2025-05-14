class SuggestionGenerator:
    def __init__(self, extracted_skills, all_skills):
        self.extracted_skills = [skill.lower() for skill in extracted_skills]
        self.all_skills = [skill.lower() for skill in all_skills]

    def generate_suggestions(self):
        # 1. Key Skills (Update for case-insensitive matching)
        key_skills = [skill for skill in self.extracted_skills if skill in self.all_skills]

        # 2. Categorize tips
        tips = []
        if len(self.extracted_skills) < 5:
            tips.append("🔍 Try to highlight more technical and soft skills.")
        if not any(skill in self.extracted_skills for skill in ['python', 'java', 'c++']):
            tips.append("💡 Mention at least one core programming language.")
        if not any(skill in self.extracted_skills for skill in ['html', 'css', 'javascript']):
            tips.append("🌐 Add front-end or web development experience if applicable.")

        # 3. Final suggestions message
        suggestions = {
            "key_skills": key_skills[:10],  # only show top 10
            "tips": tips if tips else ["✅ Resume looks good. Just ensure it's up-to-date!"]
        }

        return suggestions
