import string

class PlagiarismChecker:
    def __init__(self, reference_path = 'reference.txt'):
        self.reference_path = reference_path

    def clean_text(self,text):
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        return set(text.split())

    def check(self,user_text):
        try:
            with open(self.reference_path, 'r', encoding='utf-8') as file:
                reference_text  = file.read()
        except FileNotFoundError:
            return "Reference File not Found!"

        set1 = self.clean_text(user_text)
        set2 = self.clean_text(reference_text)

        if not set1 or not set2:
            return "One of the texts is empty!"

        intersection = len(set1 & set2)
        union = len(set1 | set2)
        similarity = (intersection / union) * 100
        return f"Plagiarism Detected: {similarity:.2f}% similar to reference.txt"

