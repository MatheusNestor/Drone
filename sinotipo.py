import socket
from time import sleep
from threading import Thread
import customtkinter as ctk

#Definindo variáveis como globais, por simplicidade
tX = 0
tY = 0
tZ = 0
dX = 0
dY = 0
dZ = 0

#Alteram os valores de target
def att_alt(valor):
    global tZ
    tZ = valor
    #print(f"Valor da altura atualizado para {valor}")

def att_X(valor):
    global tX
    tX = valor
    #print(f"Valor de X atualizado para {valor}")

def att_Y(valor):
    global tY
    tY = valor
    #print(f"Valor de Y atualizado para {valor}")

def volta():
    global tX, tY, tZ
    cont = 0
    posic_padr=[[-0.32, -1.92, 1.7],[1.88, 0.16, 1.7],[-0.399, 2.16, 1.15],[-2.64, 1.12, 1.15],[0, 0, 0]]
    while cont<5:
        tX = posic_padr[cont][0]
        tY = posic_padr[cont][1]
        tZ = posic_padr[cont][2]
        sleep(15)
        cont=cont+1
    

def retornar():
    global tY,tX,tZ
    tX = 0
    tY = 0
    tZ = 0

def encerrar():
    cliente.kill()
    visual.kill()

    
#Define o cliente que se comunica com o Servidor TPC/IP no CLP.py
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

            #print(f"Os valores de target atuais são: X={tX:.2f},Y={tY:.2f} e Z={tZ:.2f}")

    finally:
        sock.close()
    
def aplicativo():
    global tX, tY, tZ, dX, dY, dZ
    # Configurando estética
    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode('light')
    app = ctk.CTk()
    app.title('Controle do Drone')
    app.geometry('700x520')
    app.resizable(False,False)
    
    #Título
    frame_tit = ctk.CTkFrame(app, corner_radius=15)
    frame_tit.pack(pady=10, padx=10, fill='both', expand=False, side='top')
    tit = ctk.CTkLabel(frame_tit, text='Controle do Drone', font=("Arial", 16))
    tit.pack(pady=10)

    #Mensagem em cima
    frame_cima = ctk.CTkFrame(app, corner_radius=15)
    frame_cima.pack(pady=10, padx=10, fill='both', expand=True, side='top') 
    inicial = ctk.CTkLabel(frame_cima, text='O Drone começa, por padrão, em (0,0,0).\nModifique os controles deslizantes para que ele mude sua posição.')
    inicial.pack(pady=10)

    #Controle deslizantes
    frame_esquerda = ctk.CTkFrame(app, corner_radius=15)
    frame_esquerda.pack(pady=10, padx=10, fill='both', expand=True, side='left')
    
    #Forçando o Drone a voltar pra posição inicial e então matar o processo
    frame_baixo = ctk.CTkFrame(app, corner_radius=15, width=200)
    frame_baixo.pack(side='bottom', fill='both', pady=10, padx=10, expand=True) 
    
    botao_voltauto = ctk.CTkButton(frame_baixo, text="Fazer volta padrão", width=200, command=volta)
    botao_retornar = ctk.CTkButton(frame_baixo, text="Voltar para posição inicial", width=200, command=retornar)
    botao_encerrar = ctk.CTkButton(frame_baixo, text="Encerrar conexão", width=200, command=encerrar)

    botao_retornar.pack(pady=10)
    botao_encerrar.pack(pady=10)
    botao_voltauto.pack(pady=10)

    #Valores atualizados
    frame_direita = ctk.CTkFrame(app, corner_radius=15)
    frame_direita.pack(pady=10, padx=10, fill='both', expand=True, side='right')
    frame_direita_titulo = ctk.CTkLabel(frame_direita, text="Posição Atual")
    frame_direita_titulo.pack(pady=10)   
    
    #Controle deslizante X
    EixoX = ctk.CTkLabel(frame_esquerda, text='X')
    EixoX.pack(pady=10)
    barra_EixoX = ctk.CTkSlider(frame_esquerda, from_=-4.0, to=4.0, command=att_X)
    barra_EixoX.pack(pady=10)
    
    #Exibir X
    texto=f"{dX}"
    exibirX = ctk.CTkLabel(frame_direita, textvariable=texto)
    exibirX.pack(pady=10)

    #Controle deslizante Y
    EixoY = ctk.CTkLabel(frame_esquerda, text='Y')
    EixoY.pack(pady=10)
    barra_EixoY = ctk.CTkSlider(frame_esquerda, from_=-4.0, to=4.0, command=att_Y)
    barra_EixoY.pack(pady=10)
    
    text_y = ctk.DoubleVar()
    text_y.set(str(dY))
    exibirY = ctk.CTkLabel(frame_direita, textvariable=text_y)
    exibirY.pack(pady=10)

    #Controle deslizante altura
    altura = ctk.CTkLabel(frame_esquerda, text='Z (Altura)')
    altura.pack(pady=10)
    barra_altura = ctk.CTkSlider(frame_esquerda, from_=0.0, to=5, command=att_alt)
    barra_altura.number_of_steps=10
    barra_altura.pack(pady=10)
    
    
    exibirZ = ctk.CTkLabel(frame_direita, text="dZ")
    exibirZ.pack(pady=10)
    



    app.mainloop()


def main():
    global cliente
    cliente = Thread(target=cliente_TCP)
    cliente.start()
    
    global visual
    visual = Thread(target=aplicativo)
    visual.start()


if __name__ == "__main__":
    main()
