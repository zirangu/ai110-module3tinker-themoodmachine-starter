# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import string
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS

# Words that flip the meaning of the sentiment word right after them
# ("not happy" should read negative, not positive).
NEGATION_WORDS = {"not", "no", "never", "n't", "cant", "can't", "dont", "don't"}

# Emojis treated as strong, unambiguous signals, the way people actually
# skim texts: an emoji often carries more weight than any single word, and
# can override a tied word-level verdict.
POSITIVE_EMOJIS = {"😂", "🥳", "❤️", "😍", "👍", ":)", ":-)", ":d"}
NEGATIVE_EMOJIS = {"🥲", "😢", "😭", "💀", "👎", ":(", ":-(", "🙃"}

# Punctuation to strip, but keep apostrophes (so "don't" stays one token)
# and leave emoji characters untouched.
_PUNCT_TO_STRIP = string.punctuation.replace("'", "").replace(":", "")


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        cleaned = text.strip().lower()
        # Strip punctuation (but keep apostrophes and colons so "don't" and
        # emoticons like ":)" survive intact).
        cleaned = cleaned.translate(str.maketrans("", "", _PUNCT_TO_STRIP))
        tokens = cleaned.split()

        print(f"Tokens: {tokens}")
        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def _analyze_tokens(self, tokens: List[str]) -> Dict[str, object]:
        """
        Shared scoring pass used by score_text, predict_label, and explain.

        Returns a dict with:
          - "score": the net numeric score
          - "positive_hits": list of positive word tokens that counted
          - "negative_hits": list of negative word tokens that counted
          - "positive_emoji": whether a positive emoji was seen
          - "negative_emoji": whether a negative emoji was seen
        """
        score = 0
        positive_hits: List[str] = []
        negative_hits: List[str] = []
        positive_emoji = False
        negative_emoji = False

        skip_next = False
        for i, token in enumerate(tokens):
            if skip_next:
                skip_next = False
                continue

            if token in POSITIVE_EMOJIS:
                score += 2
                positive_emoji = True
                continue
            if token in NEGATIVE_EMOJIS:
                score -= 2
                negative_emoji = True
                continue

            is_positive = token in self.positive_words
            is_negative = token in self.negative_words
            if not (is_positive or is_negative):
                continue

            # Negation handling: if the previous token negates this one,
            # flip the polarity instead of counting it at face value.
            negated = i > 0 and tokens[i - 1] in NEGATION_WORDS

            if is_positive:
                if negated:
                    score -= 1
                    negative_hits.append(token)
                else:
                    score += 1
                    positive_hits.append(token)
            else:  # is_negative
                if negated:
                    score += 1
                    positive_hits.append(token)
                else:
                    score -= 1
                    negative_hits.append(token)

        return {
            "score": score,
            "positive_hits": positive_hits,
            "negative_hits": negative_hits,
            "positive_emoji": positive_emoji,
            "negative_emoji": negative_emoji,
        }

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        TODO: You must choose AT LEAST ONE modeling improvement to implement.
        For example:
          - Handle simple negation such as "not happy" or "not bad"
          - Count how many times each word appears instead of just presence
          - Give some words higher weights than others (for example "hate" < "annoyed")
          - Treat emojis or slang (":)", "lol", "💀") as strong signals
        """
        tokens = self.preprocess(text)
        return self._analyze_tokens(tokens)["score"]

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        tokens = self.preprocess(text)
        result = self._analyze_tokens(tokens)
        positive_hits = result["positive_hits"]
        negative_hits = result["negative_hits"]
        positive_emoji = result["positive_emoji"]
        negative_emoji = result["negative_emoji"]

        has_positive = bool(positive_hits) or positive_emoji
        has_negative = bool(negative_hits) or negative_emoji

        # No sentiment signal at all -> neutral.
        if not has_positive and not has_negative:
            return "neutral"

        # Only one side has any signal -> that side wins outright.
        if has_positive and not has_negative:
            return "positive"
        if has_negative and not has_positive:
            return "negative"

        # Both sides have signal: an emoji acts as a tie-breaker override,
        # since we treat emoji as a stronger signal than word counts.
        if positive_emoji and not negative_emoji:
            return "positive"
        if negative_emoji and not positive_emoji:
            return "negative"

        # No emoji override (or emoji on both sides): compare word hit
        # counts. A strict majority on one side wins; an exact tie is
        # genuinely mixed.
        if len(positive_hits) > len(negative_hits):
            return "positive"
        if len(negative_hits) > len(positive_hits):
            return "negative"
        return "mixed"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
