from time import sleep
from threading import Thread
from opcua import Client, Server


ip = "localhost"
url = f"opc.tcp://{ip}:53530/OPCUA/SimulationServer"

#Definindo variáveis como globais, por simplicidade
tX = None
tY = None
tZ = None
dX = None
dY = None
dZ = None

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
        raise RuntimeError("Chainedserver -> Não encontrei a pasta 'Drone' no servidor OPC UA.")

    # Mapeie variáveis por nome (case-insensitive)
    name_to_node = {}
    for v in drone_folder.get_children():
        try:
            nm = v.get_browse_name().Name
            name_to_node[nm.lower()] = v
        except Exception:
            pass

    tX = name_to_node.get("targetx")
    tY = name_to_node.get("targety")
    tZ = name_to_node.get("targetz")
    dX = name_to_node.get("dronex")
    dY = name_to_node.get("droney")
    dZ = name_to_node.get("dronez")

    if not all([tX, tY, tZ, dX, dY, dZ]):
        found = ", ".join(sorted(name_to_node.keys()))
        raise RuntimeError(
            "Chainedserver -> Variáveis esperadas não encontradas. "
            "Quero TargetX, TargetY, TargetZ, DroneX, DroneY, DroneZ. "
            f"Encontradas: {found}"
        )
    
    return client, (tX, tY, tZ, dX, dY, dZ)

def servidor_opc():
    global tX, tY, tZ, dX, dY, dZ
    server = Server(shelffile=None, iserver=None)
    server.set_server_name("Servidor MES")
    server.set_endpoint("opc.tcp://localhost:53555")
    idx = server.register_namespace("mes.py")
    server.start()

    objetos = server.get_objects_node()

    pasta = objetos.add_folder(idx,"drone")

    targetx = pasta.add_variable(idx,"targetx",0)
    targety = pasta.add_variable(idx,"targety",0)
    targetz = pasta.add_variable(idx,"targetz",0)
    dronex = pasta.add_variable(idx,"dronex",0)
    droney = pasta.add_variable(idx,"droney",0)
    dronez = pasta.add_variable(idx,"dronez",0)
    


    while True:
        targetx.set_value(tX.get_value())
        targety.set_value(tY.get_value())
        targetz.set_value(tZ.get_value())
        dronex.set_value(dX.get_value())
        droney.set_value(dY.get_value())
        dronez.set_value(dZ.get_value())

    
    
def main():
    cliente = Thread(target=cliente_opc)
    cliente.start()

    sleep(2)
    servidor_opc()


if __name__ == "__main__":
    main()