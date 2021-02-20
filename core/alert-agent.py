import subprocess
import pyttsx3

engine = pyttsx3.init()

filename = "E:\\alerts.txt"

f = subprocess.Popen(['powershell','get-content -wait',filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while True:
    line = f.stdout.readline()
    # print(line)
    line = line.decode('utf-8')
    print(line)

    engine.say(line)
    engine.runAndWait()
