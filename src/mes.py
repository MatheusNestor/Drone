import os
from datetime import datetime
from time import sleep
from threading import Thread
from opcua import Client, Server

#Definindo variáveis como globais, por simplicidade
tX = 0
tY = 0
tZ = 0
dX = 0
dY = 0
dZ = 0

#Novo namespace criado pro novo servidor
url = "opc.tcp://localhost:53555"

#Replica cliente do CLP
def cliente_opc():
    global tX, tY, tZ, dX, dY, dZ
    client = Client(url)
    client.connect()


    root = client.get_objects_node()

    drone_folder = None
    try:
        drone_folder = root.get_child(["3:Drone"])
    except Exception:
        for n in root.get_children():
            try:
                name = n.get_browse_name().Name
                if name.lower() == "drone":
                    drone_folder = n
                    break
            except Exception:
                pass
    if drone_folder is None:
        raise RuntimeError("Mes -> Não encontrei a pasta 'Drone' no servidor OPC UA.")

    # Mapeie variáveis por nome (case-insensitive)
    name_to_node = {}
    for v in drone_folder.get_children():
        try:
            nm = v.get_browse_name().Name
            name_to_node[nm.lower()] = v
        except Exception:
            pass

    # Esperadas (ajuste aqui se seus nomes diferirem)
    tX = name_to_node.get("targetx")
    tY = name_to_node.get("targety")
    tZ = name_to_node.get("targetz")
    dX = name_to_node.get("dronex")
    dY = name_to_node.get("droney")
    dZ = name_to_node.get("dronez")

    if not all([tX, tY, tZ, dX, dY, dZ]):
        found = ", ".join(sorted(name_to_node.keys()))
        raise RuntimeError(
            "Mes -> Variáveis esperadas não encontradas. "
            "Quero TargetX, TargetY, TargetZ, DroneX, DroneY, DroneZ. "
            f"Encontradas: {found}"
        )
    return client, (tX, tY, tZ, dX, dY, dZ)

def historiador():
    global tX, tY, tZ, dX, dY, dZ
  

    with open("../Drone/arquivos_texto/mes.txt", "w", encoding="utf-8") as arquivo_txt:
        arquivo_txt.write(f"Mes -> Timestamp, Target tX, Target tY, Target tZ, Posição dX, Posição dY, Posição dZ\n")
        while rodando:
            valor_tX = float(tX.get_value())
            valor_tY = float(tY.get_value())
            valor_tZ = float(tZ.get_value())
            valor_dX = float(dX.get_value())
            valor_dY = float(dY.get_value())
            valor_dZ = float(dZ.get_value())  
            arquivo_txt.write(f"{datetime.now()}, {valor_tX:.2f}, {valor_tY:.2f}, {valor_tZ:.2f}, {valor_dX:.2f}, {valor_dY:.2f}, {valor_dZ:.2f}\n")
            sleep(0.01)

rodando = True
def verifi_rodando():
    global rodando
    while True:
        if rodando == False:
            print("Mes -> Conexão encerrada.")
            os.kill(os.getpid(),9)
            break
        sleep(0.01)

def main():
    cliente = Thread(target=cliente_opc)
    cliente.start()

    sleep(2)
    hist = Thread(target=historiador)
    hist.start()

    verifica_rodando = Thread(target=verifi_rodando)
    verifica_rodando.start()

if __name__ == "__main__":
    main()