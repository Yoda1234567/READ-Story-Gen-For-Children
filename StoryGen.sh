#!/bin/sh
#
# This is a sample Slurm batch script for running Python scripts sequentially on the UCT HPC.
# It requests resources and then executes the Python scripts one after another.

# Slurm Directives:
# These lines start with #SBATCH and tell the Slurm scheduler about your job requirements.

# Account to charge for this job.
#SBATCH --account=compsci

# Specify the partition (queue) to submit your job to.
# Based on your example, 'ada' is used.
#SBATCH --partition=ada

# Request 1 node.
#SBATCH --nodes=1

# Request 1 task (process). This is suitable for single-threaded Python scripts.
#SBATCH --ntasks=1

# Set the maximum time your job will run (e.g., 2 hours).
# Adjust this if the combined runtime of all scripts exceeds this.
#SBATCH --time=24:00:00

# Job name: This will appear in the squeue output.
#SBATCH --job-name="Story-Gen"

# Output file for standard output (stdout)
# %j will be replaced by the job ID.
#SBATCH --output=Story-Gen_%j.out

# Error file for standard error (stderr)
# %j will be replaced by the job ID.
#SBATCH --error=Story-Gen_%j.err

# Loads the necessary Python module.
module load python/miniconda3-py3.12

# --- Executes Python scripts in generation order:
# initial paragraph -> match -> story generation with outline -> story generation without outline  ---

# May find that it works better to run initialParas.py separately from the rest because is inconsistent with actually outputting
# a readable initial paragraph for the following stages to use.
echo "Starting InitialParas.py..."
python InitialParas.py
if [ $? -ne 0 ]; then
    echo "Error: InitialParas.py failed. Exiting."
    exit 1
fi
echo "InitialParas.py finished."

echo "Starting Match.py..."
python Match.py
if [ $? -ne 0 ]; then
    echo "Error: Match.py failed. Exiting."
    exit 1
fi
echo "Match.py finished."

echo "StoryGen.py..."
python StoryGen.py
if [ $? -ne 0 ]; then
    echo "Error: StoryGen.py failed. Exiting."
    exit 1
fi
echo "StoryGen.py finished."

echo "NoOutlineGen.py..."
python NoOutlineGen.py
if [ $? -ne 0 ]; then
    echo "Error: NoOutlineGen.py failed. Exiting."
    exit 1
fi
echo "NoOutlineGen.py finished."

echo "All Python scripts finished."
