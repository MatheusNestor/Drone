import socket
from threading import Thread
import customtkinter as ctk

def att_alt(valor):
    global tZ
    tZ = valor
    print(f"Valor da altura atualizado para {valor}")

def att_X(valor):
    global tX
    tX = valor
    print(f"Valor de X atualizado para {valor}")

def att_Y(valor):
    global tY
    tY = valor
    print(f"Valor de Y atualizado para {valor}")

def cliente_TCP(): 
    global tX, tY, tZ, dX, dY, dZ 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    adress = ('localhost', 53444)
    sock.connect(adress) 
    try:
        while True:
            msg = f"{tX},{tY},{tZ}"
            print(msg)
            sock.sendall(bytes(msg, 'utf-8'))
            print("enviado")

            recebido = 0
            esperado = len(msg)
            while recebido < esperado:
                data = sock.recv(3200)
                data=data.decode()
                data=data.split(",")
                val_atualizados=[]
                for i in range(len(data)):
                    val_atualizados.append(float(data[i]))
                dX = val_atualizados[0]
                dY = val_atualizados[1]
                dZ = val_atualizados[2]
                recebido = recebido + len(msg)

            print(f"Os valores de target atuais são: X={tX},Y={tY} e Z={tZ}")

    finally:
        sock.close()
    
def aplicativo():
    global tX, tY, tZ, dX, dY, dZ
    # Configurando estética
    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode('light')
    app = ctk.CTk()
    app.title('Controle do Drone')
    app.geometry('5000X5000')

    #Controle deslizante altura
    altura = ctk.CTkLabel(app, text='Altura')
    altura.pack(pady=10)
    barra_altura = ctk.CTkSlider(app, from_=0.0, to=10.0, command=att_alt)
    barra_altura.number_of_steps=10
    barra_altura.pack(pady=10)
    
    #Controle deslizante X
    EixoX = ctk.CTkLabel(app, text='X')
    EixoX.pack(pady=10)
    barra_EixoX = ctk.CTkSlider(app, from_=-4.0, to=4.0, command=att_X)
    barra_EixoX.pack(pady=10)
    #exibirY = ctk.CTkLabel(app, textvariable=ctk.StringVar(value=f"Posição atual:{dY}, e está indo para: {tY}"))


    #Controle deslizante Y
    EixoY = ctk.CTkLabel(app, text='Y')
    EixoY.pack(pady=10)
    barra_EixoY = ctk.CTkSlider(app, from_=-4.0, to=4.0, command=att_Y)
    barra_EixoY.pack(pady=10)
    #exibirY = ctk.CTkLabel(app, textvariable=ctk.StringVar(value=f"Posição atual:{dY}, e está indo para: {tY}"))


    app.mainloop()
tX = 0.00
tY = 0.00
tZ = 0.00
dX = 0.00
dY = 0.00
dZ = 0.00
def main():

    cliente = Thread(target=cliente_TCP)
    cliente.start()
    
    visual = Thread(target=aplicativo)
    visual.start()

if __name__ == "__main__":
    main()
