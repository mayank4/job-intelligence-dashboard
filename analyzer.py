import re
from collections import Counter

def extract_skills(text):
    """
    Extract skills from the given text.
    
    Args:
        text (str): The text from which to extract skills.
    
    Returns:
        list: A list of extracted skills.
    """
    # Example skill list (this can be extended as needed)
    skills = ['Python', 'Java', 'SQL', 'Machine Learning', 'Data Analysis', 
              'Project Management', 'Communication', 'Git']
    
    # Use regex to find skills in the text
    extracted_skills = [skill for skill in skills if re.search(r'\b' + re.escape(skill) + r'\b', text)]
    
    return extracted_skills

def analyze_skills(skills_list):
    """
    Analyze the list of skills and return a summary.
    
    Args:
        skills_list (list): A list of skills to analyze.
    
    Returns:
        dict: A dictionary with skill counts.
    """
    return dict(Counter(skills_list))

# Example usage
if __name__ == "__main__":
    sample_text = "Skillful in Python and Java with a background in SQL and Data Analysis."
    skills = extract_skills(sample_text)
    analysis = analyze_skills(skills)
    print(analysis)
