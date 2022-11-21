import subprocess
from subprocess import PIPE, Popen

# a=subprocess.run("sudo docker  exec -it  revdebug-devops-1 netstat -tn | grep 42734 | grep ESTABLISHED | wc -l", shell=True, check=True)
# subprocess.run("sudo docker  cp /bin/netstat revdebug-devops-1:/bin/netstat", shell=True, check=True)



# print(dir(a))
# print(a.stdout)

command = "sudo docker  exec -it  revdebug-devops-1 netstat -tn | grep 42734 | grep ESTABLISHED | wc -l"
process = subprocess.Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
output, error = process.communicate()

print(output.decode("utf-8"))