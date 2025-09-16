# Authors: Code written by Daniel Holgate
# Date: 15/09/2025
# Description: Code for taking a vocabulary of phonemes, generating random a random number for each representing the times
# someone using the ART messed up that phoneme and then selecting the worst five (highest random numbers) to incorporate into
# the story generation process.

import random

# Output file.
# Change to whatever you want.
OUTPUT_FILE = ""

def get_mistakes(filename):

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    errors = [["", 0] for _ in range(len(lines)-1)]
    
    del lines[0]
    del lines[len(lines)-1]
    
    count = 0
    
    for line in lines:
        line.strip()
        word = line.split(":")[0]
        num = random.randint(1, 10)
        word = word.strip().strip("\"")
        errors[count][0] = word
        errors[count][1] = str(num)
        count+=1
        
    maxi = 0
    max_word = ""
    delete = 0
    output = ""
    for j in range(5):
        for i in range(len(errors)):
            number = int(errors[i][1])
            if number > maxi:
                maxi = number
                max_word = errors[i][0]
                delete = i
        output = output +  max_word + " " 
        maxi = 0
        del errors[delete]
        delete = 0
        max_word = ""
        
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output.strip())

get_mistakes("phoneme_vocab_display.json")