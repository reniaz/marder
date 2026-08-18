import os 
import subprocess

def clear_screen():
    if os.name == 'nt':
        subprocess.run("cls", shell=True)
    else:
        subprocess.run(["clear"], check=False)
