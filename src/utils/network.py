def ping(address):
    import subprocess
    try:
        output = subprocess.check_output(["ping", "-c", "4", address], stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Ping failed: {e.output}"

def traceroute(address):
    import subprocess
    try:
        output = subprocess.check_output(["traceroute", address], stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Traceroute failed: {e.output}"