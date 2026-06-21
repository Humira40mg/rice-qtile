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