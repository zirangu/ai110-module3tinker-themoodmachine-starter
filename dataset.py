"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "lowkey stressed but kind of proud of myself ngl",
    "I absolutely LOVE getting stuck in traffic for 2 hours 🙃",
    "ngl today was actually kind of amazing no cap",
    "idk why I'm crying rn, I think I'm just tired 🥲",
    "finally finished the project omg I'm so relieved",
    "bro really said that to my face 💀 I'm done",
    "just vibing, nothing special today",
    "highkey anxious about tomorrow but trying to stay chill",
    "can't stop smiling today everything is going right 😂",
    "I'm fine. I'm totally fine. everything is fine.",
    "I love getting stuck in traffic",
    "this new track is sick",
    "lmao this whole situation is fire, in the worst way",
    "I'm fine 🙂",
    "exhausted but proud of myself",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "mixed",     # "lowkey stressed but kind of proud of myself ngl"
    "negative",  # sarcasm: "I absolutely LOVE getting stuck in traffic for 2 hours 🙃"
    "positive",  # "ngl today was actually kind of amazing no cap"
    "negative",     # "idk why I'm crying rn, I think I'm just tired 🥲"
    "positive",  # "finally finished the project omg I'm so relieved"
    "negative",  # "bro really said that to my face 💀 I'm done"
    "neutral",   # "just vibing, nothing special today"
    "mixed",     # "highkey anxious about tomorrow but trying to stay chill"
    "positive",  # "can't stop smiling today everything is going right 😂"
    "negative",  # sarcasm: "I'm fine. I'm totally fine. everything is fine."
    "negative",  # sarcasm: "I love getting stuck in traffic"
    "positive",  # slang: "this new track is sick"
    "negative",  # slang, negated: "lmao this whole situation is fire, in the worst way"
    "negative",  # sarcasm/emoji: "I'm fine 🙂"
    "mixed",     # "exhausted but proud of myself"
]

# SAMPLE_POSTS.extend([
#     "lowkey stressed but kind of proud of myself ngl",
#     "I absolutely LOVE getting stuck in traffic for 2 hours 🙃",
#     "ngl today was actually kind of amazing no cap",
#     "idk why I'm crying rn, I think I'm just tired 🥲",
#     "finally finished the project omg I'm so relieved",
#     "bro really said that to my face 💀 I'm done",
#     "just vibing, nothing special today",
#     "highkey anxious about tomorrow but trying to stay chill",
#     "can't stop smiling today everything is going right 😂",
#     "I'm fine. I'm totally fine. everything is fine.",
# ])

# TRUE_LABELS.extend([
#     "mixed",     # "lowkey stressed but kind of proud of myself ngl"
#     "negative",  # sarcasm: "I absolutely LOVE getting stuck in traffic for 2 hours 🙃"
#     "positive",  # "ngl today was actually kind of amazing no cap"
#     "mixed",     # "idk why I'm crying rn, I think I'm just tired 🥲"
#     "positive",  # "finally finished the project omg I'm so relieved"
#     "negative",  # "bro really said that to my face 💀 I'm done"
#     "neutral",   # "just vibing, nothing special today"
#     "mixed",     # "highkey anxious about tomorrow but trying to stay chill"
#     "positive",  # "can't stop smiling today everything is going right 😂"
#     "negative",  # sarcasm/denial: "I'm fine. I'm totally fine. everything is fine."
# ])

# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
