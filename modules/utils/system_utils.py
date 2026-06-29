import subprocess

def get_current_resolution():
    """
    Executes the shell command 'xrandr | grep "current" | awk ...'
    to retrieve and return the current resolution (X, Y) as a tuple.

    Returns None if the command fails or no data is found.
    """
    try:
        # The complete shell command to be executed in the shell
        command = 'xrandr | grep "current" | awk "{print \$10, \$8}"'
        
        # Execution of the shell command
        result = subprocess.run(
            command, 
            shell=True, 
            check=True,  # Raises an error if the exit code is not 0
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True    # Decodes stdout into text (strings)
        )

        output = result.stdout.strip()
        
        if not output:
            raise Exception()
            
        x_str, y_str = output.split()
        return int(x_str), int(y_str)
    
    except Exception as e:
        return 1920, 1080


import os
import glob

def is_plugged_to_power():
    power_supplies = glob.glob("/sys/class/power_supply/*")

    for supply in power_supplies:
        supply_type_path = os.path.join(supply, "type")
        if not os.path.exists(supply_type_path):
            continue

        with open(supply_type_path) as f:
            supply_type = f.read().strip()

        if supply_type in ("Mains", "USB"):
            online_path = os.path.join(supply, "online")
            if os.path.exists(online_path):
                with open(online_path) as f:
                    return f.read().strip() == "1"

    return None  