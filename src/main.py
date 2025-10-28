from flask import Flask, render_template, request
from modules.lexical_analyzer import LexicalAnalyzer
from modules.plagiarism_checker import PlagiarismChecker

app = Flask(__name__)

lexical = LexicalAnalyzer()
plagiarism = PlagiarismChecker()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    selected_option = "lexical"

    if request.method == 'POST':
        text_input = request.form.get('text_input', '')
        selected_option = request.form.get('operation', 'lexical')

        if not text_input.strip():
            result = "Please enter or paste some text!"
        else:
            if selected_option == "lexical":
                result = lexical.analyze(text_input)
            else:
                result = plagiarism.check(text_input)

    return render_template('index.html', result=result, selected_option=selected_option)

if __name__ == '__main__':
    app.run(debug=True)
