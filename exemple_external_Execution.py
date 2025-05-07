import subprocess
import os

# List of .mot files you want to pass as arguments
mot_files = ['scriptA.mot', 'scriptB.mot', 'scriptC.mot']

# Define the path to scriptB.py located in folderB
exec_script_path = os.path.join('..', 'mot4py')

# Loop over each .mot file
for mot_file in mot_files:
    # Define the command with the argument for the current .mot file
    command = ['python', exec_script_path, '-f', mot_file]
    
    # Run the command and wait for the current process to finish before starting the next one
    subprocess.run(command)