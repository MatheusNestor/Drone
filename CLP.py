#Cria um CLP  que contém um cliente OPC UA e um servidor TCP/IP
import socket
from threading import Thread
from opcua import Client 

url = "opc.tcp://Matheus:53530/OPCUA/SimulationServer"

def cliente_opc():
    client = Client(url)
    client.connect()
    print("teste")

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
        raise RuntimeError("Não encontrei a pasta 'Drone' no servidor OPC UA.")

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
            "Variáveis esperadas não encontradas. "
            "Quero TargetX, TargetY, TargetZ, DroneX, DroneY, DroneZ. "
            f"Encontradas: {found}"
        )

    print("[OPC] Vars bound:",
          "TargetX/TargetY/TargetZ & DroneX/DroneY/DroneZ")
    
    tX.set_value(4)
    tY.set_value(4)
    tZ.set_value(4)
    return client, (tX, tY, tZ, dX, dY, dZ)


def servidor_TCP():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    adress = ('localhost', 53444)
    sock.bind(adress)
    sock.listen(1)

    while True:
        connection, adress =  sock.accept()
        print("Conectado a ",adress)
        try:
            while True:
                data = connection.recv(3200)
                if data:
                    msg = str(data)
                    msg = msg + "sei la"
                    msg = bytes(msg, 'utf-8')
                    connection.sendall(msg)
                else:
                    break
        except:
            print("erro")
        finally:
            connection.close()
    print("teste_2")

def main():
    cliente = Thread(target=cliente_opc)
    servidor = Thread(target=servidor_TCP)
    
    cliente.start()
    servidor.start()
    


if __name__ == "__main__":
    main()
