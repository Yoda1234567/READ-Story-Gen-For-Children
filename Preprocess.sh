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
#SBATCH --time=3:00:00

# Job name: This will appear in the squeue output.
#SBATCH --job-name="Story-Processing"

# Output file for standard output (stdout)
# %j will be replaced by the job ID.
#SBATCH --output=LLaMA-Extraction_%j.out

# Error file for standard error (stderr)
# %j will be replaced by the job ID.
#SBATCH --error=LLaMA-Extraction_%j.err

# Load the specified Python module.
# This uses the miniconda3-py3.12 environment.
module load python/miniconda3-py3.12

echo "Starting GlotSort.py..."
python GlotSort.py
if [ $? -ne 0 ]; then
    echo "Error: GlotSort.py failed. Exiting."
    exit 1
fi
echo "GlotSort.py finished."

echo "Starting FabClean.py..."
python FabClean.py
if [ $? -ne 0 ]; then
    echo "Error: FabClean.py failed. Exiting."
    exit 1
fi
echo "FabClean.py finished."

echo "Starting Few150.py..."
python Few150.py
if [ $? -ne 0 ]; then
    echo "Error: Few150.py failed. Exiting."
    exit 1
fi
echo "Few150.py finished."

echo "Starting Few400.py..."
python Few400.py
if [ $? -ne 0 ]; then
    echo "Error: Few400.py failed. Exiting."
    exit 1
fi
echo "Few400.py finished."

echo "Starting Few800.py..."
python Few400.py
if [ $? -ne 0 ]; then
    echo "Error: Few800.py failed. Exiting."
    exit 1
fi
echo "Few400.py finished."

echo "Starting More800.py..."
python More800.py
if [ $? -ne 0 ]; then
    echo "Error: More800.py failed. Exiting."
    exit 1
fi
echo "More800.py finished."


echo "All Python scripts finished."
