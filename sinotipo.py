import socket
from threading import Thread
import customtkinter as ctk

def cliente_TCP():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    adress = ('localhost', 53444)
    sock.connect(adress)
    try:
        msg = input()
        sock.sendall(bytes(msg, 'utf-8'))
        print("enviado")

        recebido = 0
        esperado = len(msg)

        while recebido < esperado:
            data = sock.recv(3200)
            recebido = recebido + len(data)
        print(data)

    finally:
        sock.close()
    
def aplicativo():
    # Configurando estética
    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode('light')
    app = ctk.CTk()
    app.title('Controle do Drone')
    app.geometry('5000X5000')

    # Títulos
    altura = ctk.CTkLabel(app, text='Altura')
    altura.pack(pady=10)
    barra_altura = ctk.CTkSlider(app, from_=0, to=10)
    barra_altura.number_of_steps=10
    barra_altura.pack(pady=10)
    

    EixoX = ctk.CTkLabel(app, text='X')
    EixoX.pack(pady=10)
    barra_EixoX = ctk.CTkSlider(app, from_=-4, to=4)
    barra_EixoX.pack(pady=10)


    EixoY = ctk.CTkLabel(app, text='Y')
    EixoY.pack(pady=10)
    barra_EixoY = ctk.CTkSlider(app, from_=-4, to=4)
    barra_EixoY.pack(pady=10)

    app.mainloop()


def main():
    cliente = Thread(target=cliente_TCP)
    cliente.start()
    
    visual = Thread(target=aplicativo)
    visual.start()



if __name__ == "__main__":
    main()
