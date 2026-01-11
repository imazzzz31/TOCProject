from .lexical_analyzer import LexicalAnalyzer
from .google_search import GoogleSearch

class PlagiarismChecker:
    def __init__(self, google_api_key=None, google_cse_id=None):
        self.lexical = LexicalAnalyzer()
        self.google_search = GoogleSearch(google_api_key, google_cse_id) if google_api_key and google_cse_id else None

    def check_text(self, text):
        """Perform lexical analysis"""
        user_tokens = self.lexical.analyze(text)

        result = {
            "tokens": {
                "user_tokens": user_tokens
            },
            "lexical_analysis": {
                "user": {
                    "total_tokens": len(user_tokens),
                    "unique_tokens": len(set(user_tokens)),
                    "keyword_count": sum(1 for t in user_tokens if "[Keyword:" in t)
                }
            }
        }

        return result

    def check_web(self, text, num_results=5):
        """Check text similarity using Google search and calculate token overlap"""
        lexical_result = self.check_text(text)

        if not self.google_search:
            lexical_result["similarity_score"] = "0%"
            lexical_result["interpretation"] = "Google API not configured"
            return lexical_result

        # Get Google search results
        search_results = self.google_search.search(text, num_results=num_results)
        lexical_result["web_results"] = search_results

        # Collect reference tokens from search snippets
        reference_tokens = set()
        for result in search_results:
            snippet_tokens = set(self.lexical.analyze(result.get("snippet", "")))
            reference_tokens.update(snippet_tokens)

        # Calculate token overlap similarity
        user_tokens_set = set(lexical_result["tokens"]["user_tokens"])
        overlap_count = len(user_tokens_set & reference_tokens)
        similarity_score = (overlap_count / len(user_tokens_set) * 100) if user_tokens_set else 0

        # Update lexical_result with reference stats
        lexical_result["tokens"]["reference_tokens"] = list(reference_tokens)
        lexical_result["lexical_analysis"]["reference"] = {
            "total_tokens": len(reference_tokens),
            "unique_tokens": len(reference_tokens),
            "keyword_count": sum(1 for t in reference_tokens if "[Keyword:" in t)
        }

        # Add similarity score and interpretation
        lexical_result["similarity_score"] = f"{similarity_score:.2f}%"
        if similarity_score < 20:
            interpretation = "Low similarity"
        elif similarity_score < 50:
            interpretation = "Moderate similarity"
        else:
            interpretation = "High similarity"
        lexical_result["interpretation"] = interpretation

        return lexical_result
