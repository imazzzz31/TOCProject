import re

class LexicalAnalyzer:
    KEYWORDS = {"if", "else", "while", "for", "int", "float", "return",
                "char", "break", "continue", "void", "class", "public", "private", "static"}
    OPERATORS = {'+','-','*','/','=','==','!=','<','>','<=','>=','++','--'}
    SEPARATORS = {';',',','(',')','{','}','[',']'}

    def analyze(self, text):
        tokens = []
        words = re.findall(r"[A-Za-z_]\w*|\d+|==|!=|<=|>=|[+\-*/=<>;(),{}[\]]", text)

        for word in words:
            if word in self.KEYWORDS:
                tokens.append(f"[Keyword: {word}]")
            elif word in self.OPERATORS:
                tokens.append(f"[Operator: {word}]")
            elif word in self.SEPARATORS:
                tokens.append(f"[Separator: {word}]")
            elif word.isdigit():
                tokens.append(f"[Number: {word}]")
            elif re.match(r"[A-Za-z]\w*", word):
                tokens.append(f"[Identifier: {word}]")
            else:
                tokens.append(f"[Unknown: {word}]")

        return tokens
