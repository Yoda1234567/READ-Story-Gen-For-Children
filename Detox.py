# Authors: Code mostly written by ChatGPT online and the comments were done by Daniel Holgate.
# Date: 16/09/2025
# Description: Code for predicting levels of various types of toxicity in each individual text using Detoxify.

from detoxify import Detoxify

# Input and output files. 
# Change to generated story file from which you are wanting to score texts.
GENER_FILE = ""
# Change to name you want.
OUTPUT_FILE = ""
# Change to dataset name.
D_NAME = ""

# Loads the original Detoxify model. This was selected as the unbiased version was taking too long to run.
model = Detoxify("original")

# Reads in all the generated stories. 
with open(GENER_FILE, "r", encoding="utf-8") as f:
    content = f.read()
    
# Splits into individual stories.
content = content.strip()
candidates = content.split("\n\n")

# Determines number of generated texts.
total = len(candidates)

with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
    f.write(f"{D_NAME}\n")
    # For each generated text, the model predicts how likely it is that certain types of toxic text will be present. 
    for i, text in enumerate(candidates, start=1):
        score = model.predict(text)
        
        numbers = [str(float(v)) for v in score.values()]

        # Saves all the toxicity scores for each individual text.
        for num in numbers:
            f.write(num + "\n")
        f.write("\n")
