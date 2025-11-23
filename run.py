from subprocess import Popen
from time import sleep

ponte = Popen(["python", "brigde.py"])

clp = Popen(["python", "clp.py"])
sleep(2)
chainedserver=Popen(["python", "chainedserver.py"])
sleep(2)

sinotipo=Popen(["python", "sinotipo.py"])
mes=Popen(["python", "mes.py"])

sinotipo.wait()

mes.kill()
chainedserver.kill()
clp.kill()
