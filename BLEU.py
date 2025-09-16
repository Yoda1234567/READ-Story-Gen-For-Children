# Authors: Code written by ChatGPT online and Daniel Holgate
# Date: 16/09/2025
# Description: Combined sacreBLEU and NLTK BLEU for corpus-level BLEU-1 to BLEU-4

import sacrebleu
from nltk.translate.bleu_score import corpus_bleu, SmoothingFunction
import numpy as np
from itertools import cycle, islice

# Input and output files. 
# Change to matching source and output stories files.
GENER_FILE = ""
SOURCE_FILE = ""
# Change to name you want.
SACRE_AND_BLEU_OUT = ""
# Change to dataset name.
D_NAME = ""

# Reads in the generated stories.
with open(GENER_FILE, "r", encoding="utf-8") as f:
    candidates_raw = f.read().strip().split("\n\n")

# Reads in the matching source stories.
with open(SOURCE_FILE, "r", encoding="utf-8") as f:
    references_raw = f.read().strip().split("\n\n")

# Tokenises candidates and references for using nltk BLEU.
candidates_tok = [cand.split() for cand in candidates_raw]
references_tok = [[ref.split()] for ref in references_raw]  

# Splits candidates and 
candidates_text = [cand.strip() for cand in candidates_raw]
references_texts = [ref.strip() for ref in references_raw]
references_for_sacre = [references_texts]

# Calculates and saves sacrebleu score.
corpus_score = sacrebleu.corpus_bleu(candidates_text, references_for_sacre)
with open(SACRE_AND_BLEU_OUT, "a", encoding="utf-8") as f:
    f.write(f"{D_NAME} - Corpus-level BLEU-4 (all-vs-all references, sacreBLEU)\n\n")
    f.write(f"BLEU-4: {corpus_score.score:.4f}\n\n\n")

# Sets the smoothing function and weights to use for nltk BLEU calculations.
smooth = SmoothingFunction().method1
weights_list = [
    (1, 0, 0, 0),               # BLEU-1
    (0.5, 0.5, 0, 0),           # BLEU-2
    (0.33, 0.33, 0.33, 0),      # BLEU-3
    (0.25, 0.25, 0.25, 0.25)    # BLEU-4
]

# Ensures number of candidates and references are equal, which is needed for nltk BLEU. 
# If more generated texts than candidates, cycles over the references multiple times.
# If more reference (sourc) texts, only selects the necessary number of candidates.
num_candidates = len(candidates_tok)
num_references = len(references_tok)
if num_references < num_candidates:
    references_tok = list(islice(cycle(references_tok), num_candidates))
elif num_references > num_candidates:
    references_tok = references_tok[:num_candidates]

# Calculates the corpus BLEU score using nltk for BLEU-1 to BLEU-4.
bleu_scores_corpus = []
for weights in weights_list:
    score = corpus_bleu(references_tok, candidates_tok, weights=weights, smoothing_function=smooth)
    bleu_scores_corpus.append(score)

# Saves all the nltk corpus BLEU scores.
with open(SACRE_AND_BLEU_OUT, "a", encoding="utf-8") as f:
    f.write(f"{D_NAME} - Corpus-level BLEU (NLTK, BLEU-1 to BLEU-4)\n\n")
    for i, score in enumerate(bleu_scores_corpus, 1):
        f.write(f"BLEU-{i}: {score:.4f}\n")
    f.write("\n\n")
