import subprocess

result = subprocess.run(['ping', '-n', '10', 'google.com'], stdout=subprocess.PIPE, text=True)