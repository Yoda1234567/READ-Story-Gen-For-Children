# Authors: Code mostly written by ChatGPT online and the comments were done by Daniel Holgate.
# Date: 16/09/2025
# Description: Code for running a pre-trained version of the UNION metric.

import subprocess
import os
import sys

# Input and output files.
# Change to generated story file from which you are wanting to score texts.
GENER_FILE = ""
# Change to "UNION/scores/filename" where filename can be what you want.
OUTPUT_FILE = ""
# Change to dataset name.
D_NAME = ""

# Defines the path to your downloaded UNION metric.
# Finds directory where UNION.py is located and assumes the UNION folder is in the same directory.
script_dir = os.path.dirname(os.path.abspath(__file__))
union_repo_dir = os.path.join(script_dir, "UNION")

# Defines the directories where all the input and output files are located.
model_dir = os.path.join(union_repo_dir, "model")
output_dir = os.path.join(union_repo_dir, "scores")
eval_file_name = GENER_FILE
eval_file_path = os.path.join(script_dir, eval_file_name)

# Create the output directory if it doesn't exist.
os.makedirs(output_dir, exist_ok=True)

data_dir = os.path.join(union_repo_dir, "Data/WritingPrompts")
expected_eval_file = os.path.join(data_dir, "ant_data_all.txt")
os.makedirs(data_dir, exist_ok=True)


try:
    with open(eval_file_path, 'r') as f_in, open(expected_eval_file, 'w') as f_out:
        story_id = 0
        for line in f_in:
            if line.strip():  # Only process non-empty lines
                story_id += 1
                f_out.write(f"{story_id} ||| {line.strip()} ||| 0 0 0 0 0 0 0\n")
    print(f"Stories prepared and saved to {expected_eval_file}")
except FileNotFoundError:
    print(f"Error: The evaluation file was not found at {eval_file_path}.")
    sys.exit(1)

# Defines the command to run UNION using run_union.py.
command = [
    sys.executable,
    os.path.join(union_repo_dir, "run_union.py"),
    "--task_name", "pred",
    "--data_dir", data_dir,
    "--output_dir", output_dir,
    "--init_checkpoint", model_dir
]


# Attempts to run run_union.py as specified above.
try:
    result = subprocess.run(command, check=True, capture_output=True, text=True)

    # For some reason does not work to write scores directly to a user specified output file. So need the one it writes to
    # and then the one you save that same output to.
    actual_output_file_name = "UNION/scores/test_probabilities.txt"  
    output_file_path = OUTPUT_FILE

    # Read the content of the output file (non-user defined)
    with open(actual_output_file_name, 'r') as f:
        content = f.read()

    # Saves the output to the user specified output file from the non-user defined one.
    with open(output_file_path, 'a') as f:
        f.write(f"{D_NAME}\n\n")
        f.write(content)

except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")
    print(f"Stdout: {e.stdout}")
    print(f"Stderr: {e.stderr}")