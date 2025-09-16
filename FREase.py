# Authors: Code mostly written by ChatGPT online and the comments were done by Daniel Holgate.
# Date: 16/09/2025
# Description: Code for calculating Flesch Reading Ease, Grade Level, SMOG Index and Automated Readability Index for each story.

import textstat

# Input and output files. 
# Change to output stories file.
GENER_FILE = ""
# Change to name you want.
OUTPUT_FILE = ""
# Change to dataset name.
D_NAME = ""

with open(GENER_FILE, "r", encoding="utf-8") as f:
        content = f.read()
        
content.strip()
texts = content.split("\n\n")

with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
    f.write(f"{D_NAME}\n")
    f.write("\n")
    
    # Goes through each text and calculates Flesch Reading Ease Score, Grade Level, SMOG Index, Automated Readability Index.
    # Saves each of the scores.
    for text in texts:
        score = textstat.flesch_reading_ease(text)
        f.write(f"Flesch Reading Ease Score: {score}\n")
        f.write(f"Grade Level: {textstat.flesch_kincaid_grade(text)}\n")
        f.write(f"SMOG Index: {textstat.smog_index(text)}\n")
        f.write(f"Automated Readability Index: {textstat.automated_readability_index(text)}\n")
        f.write("\n")
        f.write("\n")
    

        
    
