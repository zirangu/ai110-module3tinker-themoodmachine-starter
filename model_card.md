# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.

## 1. Model Overview

**Model type:**  
I built and compared both: the rule based model in `mood_analyzer.py` and the ML model (logistic regression over bag-of-words) in `ml_experiments.py`.

**Intended purpose:**  
Classify short, informal social-media-style posts into one of four moods: positive, negative, neutral, or mixed.

**How it works (brief):**  
The rule based model tokenizes text, looks up each token against a positive/negative word list and an emoji list, applies a negation flip for patterns like "not happy," and sums the hits into a score; the score and hit counts are then mapped to a label (see Section 3). The ML model instead learns its own word-to-label associations: `CountVectorizer` turns each post into a vector of word counts, and `LogisticRegression` is fit on those vectors against `TRUE_LABELS`, so instead of me writing rules, the model estimates which words statistically co-occur with which label in the training set.



## 2. Data

**Dataset description:**  
`SAMPLE_POSTS` started with 6 posts and I expanded it to 21. The first round of 10 additions targeted more realistic, informal language (slang like "lowkey"/"highkey"/"ngl"/"no cap," emojis, and posts with subtly mixed emotions). A second round of 5 additions specifically targeted categories the first round under-covered: sarcasm ("I love getting stuck in traffic"), slang whose sentiment flips with context ("sick," "fire"), an emoji-bearing short post ("I'm fine 🙂"), and an explicit mixed-emotion post ("exhausted but proud of myself").

**Labeling process:**  
I labeled each post by reading it the way a person skimming a feed would, not by what the literal words say — e.g. "I absolutely LOVE getting stuck in traffic for 2 hours 🙃" is labeled negative, not positive, because the context (traffic) and the emoji (🙃) override the literal word "love." Posts with two valid readings were labeled "mixed" rather than forced into positive/negative — e.g. "lowkey stressed but kind of proud of myself ngl" and "highkey anxious about tomorrow but trying to stay chill" could reasonably be argued as leaning negative or leaning positive instead, and a different labeler might disagree with my mixed call on both.

**Important characteristics of your dataset:**  
- Contains slang ("lowkey," "highkey," "ngl," "no cap," "sick," "fire")
- Contains emojis (🥲, 💀, 😂, 🙃, 🙂)
- Includes sarcasm (2 posts)
- Several posts express mixed feelings
- Several posts are short and low-signal ("This is fine," "I'm fine 🙂")

**Possible issues with the dataset:**  
It's heavily skewed toward casual, youth-coded internet slang (lowkey, ngl, no cap, bro) — a formal or older-generation writing style is barely represented, so the dataset itself encodes a narrow register of English. It's also small (21 posts) and label-imbalanced: "negative" and "positive" each appear far more often than "mixed" or "neutral," so a model trained on it has little signal to learn what "mixed" actually looks like.

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
- Each positive/negative word hit adds/subtracts 1 from the score.
- Negation: if a sentiment word is immediately preceded by a word like "not," "no," "never," or "don't," its polarity flips instead of counting at face value ("not happy" scores as -1, not +1 -1 independently).
- Emoji weighting: emojis count double (±2) rather than ±1, since in real posts an emoji often reads as a stronger, less ambiguous signal than a plain word.
- Label thresholds: no hits on either side → "neutral." Hits on only one side → that side wins. Hits on both sides → compare hit counts; a strict majority wins outright, an exact tie is labeled "mixed," and an emoji present on only one side overrides the word-count comparison entirely.

**Strengths of this approach:**  
It's fully transparent — `explain()` can show exactly which words/emoji drove the score — and it behaves predictably on posts that use vocabulary already in `POSITIVE_WORDS`/`NEGATIVE_WORDS` with no negation or sarcasm, e.g. "Today was a terrible day" and "So excited for the weekend" are both scored correctly for the obvious reason that their sentiment words are literally in the lists.

**Weaknesses of this approach:**  
It fails exactly where it has to guess at *intent* rather than count words:
- `"finally finished the project omg I'm so relieved"` → predicted "neutral" (true: "positive"). None of "finished," "relieved," "omg" are in `POSITIVE_WORDS`, so zero hits on either side, even though a person would read this as clearly positive.
- `"highkey anxious about tomorrow but trying to stay chill"` → predicted "positive" (true: "mixed"). "chill" is a positive-word hit and "anxious" isn't in `NEGATIVE_WORDS` at all, so the negative half of the sentence is invisible to the model and it reads as one-sided positive instead of mixed.
- `"this new track is sick"` → predicted "neutral" (true: "positive"). "sick" isn't in either word list, so a slang word whose sentiment flips from its literal meaning is simply not scored at all.

## 4. How the ML Model Works (if used)

**Features used:**  
Bag of words using `CountVectorizer` (raw word-count vectors, no TF-IDF weighting, no n-grams — single tokens only).

**Model:**  
`LogisticRegression` (scikit-learn) trained as a multinomial classifier over the bag-of-words features, with `max_iter=1000`.

**Training data:**  
The model trains on the same `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py` — 21 posts, 4 possible labels.

**Training behavior:**  
`ml_experiments.py` only ever evaluates on the same data it trained on (training accuracy, not held-out accuracy), so what it reports is really "how well did the model memorize these 21 examples," not "how well would it generalize to a new post." With only 21 examples across 4 classes, the model has very few examples per label to learn general word-sentiment associations from, so small changes to labeling (e.g. flipping one "mixed" to "negative") would be expected to visibly shift which words the model associates with which class.

**Strengths and weaknesses:**  
Strength: it doesn't need me to hand-write a word list — it can in principle pick up sentiment cues from words like "relieved" or "sick" that I never put in `POSITIVE_WORDS`/`NEGATIVE_WORDS`, as long as it has seen them with a consistent label during training. Weakness: with only 21 training posts, it's prone to overfitting on word co-occurrence rather than real sentiment — e.g. it could easily latch onto an incidental word like "traffic" or "today" as a signal for a label just because it happened to appear in one post with that label, which would not generalize at all to a new post containing the same word in a different mood.

## 5. Evaluation

**How you evaluated the model:**  
I ran the rule based model (`main.py`'s `evaluate_rule_based`) over all 21 labeled posts in `dataset.py` and compared its predictions to `TRUE_LABELS` directly. It got 11/21 correct (≈0.52 accuracy). The pattern in the errors is consistent: every miss is a post whose sentiment word isn't in `POSITIVE_WORDS`/`NEGATIVE_WORDS` (so the model sees "no signal" or "one-sided signal" when a person would see something more nuanced), not a case where the negation or emoji logic itself misfired.

**Examples of correct predictions:**  
- `"Today was a terrible day"` → correctly "negative": "terrible" is directly in `NEGATIVE_WORDS`, a one-sided, unambiguous hit.
- `"I absolutely LOVE getting stuck in traffic for 2 hours 🙃"` → correctly "negative": "love" scores +1, but the 🙃 emoji scores -2 and overrides it as the stronger signal — the sarcasm-detection-by-emoji-override trick happened to work here.
- `"just vibing, nothing special today"` → correctly "neutral": no word in the post matches either sentiment list, so the model lands on "no signal" and that happens to be the right call for this post.

**Examples of incorrect predictions:**  
- `"finally finished the project omg I'm so relieved"` → predicted "neutral," true "positive." Zero vocabulary overlap: "finished," "relieved," and "omg" aren't in the word lists, so the model sees nothing to score.
- `"highkey anxious about tomorrow but trying to stay chill"` → predicted "positive," true "mixed." "chill" hits positive, but "anxious" is missing from `NEGATIVE_WORDS`, so the negative half of the sentence is invisible and the model sees a one-sided match instead of a tie.
- `"I'm fine. I'm totally fine. everything is fine."` → predicted "neutral," true "negative." "fine" isn't in either list, and the model has no way to recognize repetition/over-insistence as a sarcasm cue, so it just sees an empty sentiment signal.

## 6. Limitations

- **Vocabulary gaps break scoring silently.** `"finally finished the project omg I'm so relieved"` is predicted "neutral" instead of "positive" because none of "finished," "relieved," or "omg" are in `POSITIVE_WORDS`. The model doesn't fail loudly here — it confidently returns "neutral," which looks like a real judgment rather than a gap.
- **Sarcasm only works when an emoji happens to carry it.** `"I'm fine. I'm totally fine. everything is fine."` is predicted "neutral" instead of "negative" because the repeated word "fine" isn't a sentiment word and there's no emoji to override it — the sarcasm signal here is *repetition/insistence*, a pattern this model has no way to represent at all.
- **One missing negative word flips a "mixed" into a one-sided label.** `"highkey anxious about tomorrow but trying to stay chill"` is predicted "positive" instead of "mixed" purely because "anxious" is absent from `NEGATIVE_WORDS` — the mixed-detection logic (tie in hit counts) never even gets a chance to fire.
- **The dataset is small (21 posts) and label-imbalanced**, so "mixed" and "neutral" are both underrepresented relative to "positive"/"negative," limiting how confidently either model's "mixed" behavior can be evaluated.

## 7. Ethical Considerations

- Misclassifying a message expressing real distress as "neutral" (as happened with "finally finished the project omg I'm so relieved" being read as flat rather than positive — the same gap could just as easily mask genuine distress phrased in words the model doesn't recognize) could be harmful if this kind of tool were ever used to triage or flag at-risk messages.
- Privacy: any real deployment of this would be reading people's personal, informal communication — the dataset itself (venting, anxiety, exhaustion) is the kind of text people may not expect to be scored or logged.

### Overt bias (Part 3)
The style most clearly underserved by this model is **formal or non-slang English**, ironically because I specifically expanded the dataset *toward* casual internet slang (lowkey, highkey, ngl, no cap, bro, fire, sick) to stress-test the model, and never added a comparable number of formal-register examples. A side effect of that choice is that the word lists and dataset together are tuned to how younger, internet-native English speakers write mood online, and would likely underperform for someone writing in a more formal register, a non-native-English phrasing style, or a regional dialect/slang set I didn't include (e.g. British slang, AAVE-specific terms, non-US internet slang) — not because those styles are less "sentiment-rich," but because none of their characteristic words are in `POSITIVE_WORDS`/`NEGATIVE_WORDS`, so the same vocabulary-gap failure mode documented above would hit them disproportionately. I did not fix this; the dataset should be audited for which language communities' informal speech actually makes it into the training/evaluation set.

### Covert compliance
When I asked my AI assistant to extend `dataset.py`'s word lists and sentiment logic, it did not proactively flag the slang-skew or missing-vocabulary issue on its own — it implemented the negation/emoji rules I asked for competently, but it was only after I explicitly asked it to reconsider edge cases (the positive/mixed/negative overlap boundary, and later the overt-bias question directly) that it surfaced the vocabulary-gap and register-skew problems. Left to its own judgment, it tended toward agreeing with and extending my design choices rather than pushing back on gaps in the word lists or dataset composition — e.g. it never on its own suggested adding formal-register or non-US-slang examples until this prompt asked for it directly. It should have pushed back earlier, specifically when the word lists were being used as the sole source of truth for sentiment, since an unprompted "this list only covers X style of language" flag would have been a reasonable thing to raise without being asked.

### Rule-based vs. ML comparison
I did not get to run a full head-to-head comparison in this session, but based on how each approach works, the expected tradeoff is: the ML model would likely *fix* the pure vocabulary-gap failures (e.g. "relieved," "sick," "anxious" could be picked up automatically if they appear in training posts with a consistent label), since it isn't limited to a hand-written word list the way the rule based model is. But it would likely *add new failures* of its own, because `ml_experiments.py` only reports training accuracy on the same 21 posts it trained on — with that few examples per label, the model is prone to overfitting on incidental words (e.g. "traffic" or "today") rather than real sentiment, so it would be highly sensitive to the exact labels I chose: relabeling even one or two ambiguous "mixed" posts would likely shift which words the model associates with which class, in a way the rule based model's fixed, inspectable word lists are immune to.

## 8. Ideas for Improvement

- Expand `POSITIVE_WORDS`/`NEGATIVE_WORDS` with the specific words that caused misclassifications above ("relieved," "anxious," "sick," "fire," "chill" as context-dependent) rather than relying only on hand-picked examples.
- Deliberately add posts in formal/non-slang registers and other English dialects, to counter the slang-skew named in the overt bias note.
- Add a held-out test set for the ML model instead of only reporting training accuracy, so its accuracy number reflects generalization rather than memorization.
- Add a small pattern-based sarcasm check to the rule based model (e.g. flag positive-word-plus-negative-context pairings like "love" + "traffic") as discussed earlier in this session, with the caveat that it would only catch sarcasm shaped like the examples it's taught.
