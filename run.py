from subprocess import Popen
from time import sleep

ponte = Popen(["python", "src/brigde.py"])

clp = Popen(["python", "src/clp.py"])
sleep(2)
chainedserver=Popen(["python", "src/chainedserver.py"])
sleep(2)

sinotipo=Popen(["python", "src/sinotico.py"])
mes=Popen(["python", "src/mes.py"])

sinotipo.wait()

mes.kill()
chainedserver.kill()
clp.kill()
