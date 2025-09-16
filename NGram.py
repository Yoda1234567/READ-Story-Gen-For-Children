# Authors: Code mostly written by ChatGPT online and the comments were done by Daniel Holgate.
# Date: 16/09/2025
# Description: Code for calculating the N-Gram score for a corpus using 4 different Ns.

from collections import Counter

# Input and output files. 
# Change to matching source and output stories files.
GENER_FILE = ""
SOURCE_FILE = ""
# Change to name you want.
OUTPUT_FILE = ""
# Change to dataset name.
D_NAME = ""

# Method returning all n-consecutive tokens. E.g. all pairs of consectuive tokens if n = 2 and single tokens if n = 1.
def get_ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

# Method for counting the occurences of each set of n-consecutive tokens.
def corpus_ngrams(texts, n):
    counter = Counter()
    for text in texts:
        tokens = text.lower().split()
        counter.update(get_ngrams(tokens, n))
    return counter

# Method for determining n-gram overlap between source and generated texts on precision, recall and F1.
def corpus_ngram_overlap(candidates, references, n=1):
    cand_counts = corpus_ngrams(candidates, n)
    ref_counts  = corpus_ngrams(references, n)

    overlap = sum((cand_counts & ref_counts).values())

    # Precision score calculation: how many generated text n-grams are present in references
    precision = overlap / sum(cand_counts.values()) if cand_counts else 0

    # Recall score calculation: how many reference n-grams are covered by the generated texts
    recall = overlap / sum(ref_counts.values()) if ref_counts else 0

    # F1 score calculation.
    f1 = (2*precision*recall / (precision+recall)) if (precision+recall)>0 else 0

    return precision, recall, f1

# Extracts and splits generated texts into individual texts.
with open(GENER_FILE, "r", encoding="utf-8") as f:
        content = f.read()   
content = content.strip()
candidates = content.split("\n\n")
check = len(candidates)

# Extracts and splits source texts into individual texts.
with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
content = content.strip()
references = content.split("\n\n")[:check]

# Calculates and saves n-gram scores for n = 1, 2, 3, 4.
with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
    f.write(f"{D_NAME}\n")
    f.write("\n")
    for n in range(1,5):
        p, r, f1 = corpus_ngram_overlap(candidates, references, n)
        f.write(f"{p:.4f}\n{r:.4f}\n{f1:.4f}\n\n")
    f.write("\n\n")

