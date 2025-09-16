# Authors: Code written by ChatGPT online and Daniel Holgate
# Date: 16/09/2025
# Description: BARTScore referenced metric calculation.

import sys
import numpy as np
from tqdm import tqdm

sys.path.append("/mnt/c/Users/danie/LLaMA3.2/transfer/hpc/eval/BARTScore")
from bart_score import BARTScorer

# Input and output files. 
# Change to matching source and output stories.
GENER_FILE = ""
SOURCE_FILE = ""
# Change to name you want.
OUTPUT_FILE = ""
# Change to dataset name.
D_NAME = ""

# Loads the BART model facebook/bart-large-cnn for use on cpu.
bart_scorer = BARTScorer(device='cpu', checkpoint='facebook/bart-large-cnn')

# Loads all generates texts as individual texts.
with open(GENER_FILE, "r", encoding="utf-8") as f:
    content = f.read()
candidates = content.strip().split("\n\n")

# Loads all source texts as individual texts.
with open(SOURCE_FILE, "r", encoding="utf-8") as f:
    content = f.read()
sources = content.strip().split("\n\n")

# Makes sure the there are an equal number of source texts as generated texts.
sources = sources[:len(candidates)]

all_scores = []

# Goes through each source story and calculates the BARTScore for each generated story using the source story as the reference.
# Does this in batches of five stories at a time.
for src in tqdm(sources, desc="Scoring stories", unit="story"):
    srcs = [src] * len(candidates)
    batch_scores = bart_scorer.score(srcs, candidates, batch_size=5)
    all_scores.append(batch_scores)

all_scores = np.array(all_scores)

# Calculates the average score for each generated story.
avg_scores_per_candidate = np.mean(all_scores, axis=0)

# Saves all the BARTScore scores (log likelihood)
with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
    f.write(f"{D_NAME}\n\n")
    for i, score in enumerate(avg_scores_per_candidate):
        f.write(f"Candidate {i+1}: {score:.4f}\n")
    f.write("\n\n")
