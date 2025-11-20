import socket
import os
from datetime import datetime
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


def att_X(valor):
    global tX
    tX = valor


def att_Y(valor):
    global tY
    tY = valor


#Define uma pequena volta automática que passa por todos os pontos principais
#Bloqueia propositalmente toda alteração manual
def volta():
    global tX, tY, tZ
    cont = 0
    posic_padr=[[-0.32, -1.92, 1.7],[1.88, 0.16, 1.7],[-0.399, 2.16, 1.15],[-2.64, 1.12, 1.15],[0, 0, 0]]
    while cont<5:
        tX = posic_padr[cont][0]
        tY = posic_padr[cont][1]
        tZ = posic_padr[cont][2]
        sleep(42)
        cont=cont+1
    

def retornar():
    global tY,tX,tZ
    tX = 0
    tY = 0
    tZ = 0

def encerrar():
    global rodando
    rodando=False


rodando = True
def verifi_rodando():
    global rodando
    while True:
        if rodando == False:
            print("Conexão encerrada. O Drone voltará para (0,0,0).")
            os.kill(os.getpid(),9)
            break
        sleep(0.01)

#Atualiza as varíaveis de texto exibidas nos labels
def exibirdX_aluatilzado():
    global  text_dx, dX, app
    text_dx.set(f"X: {dX:.2f}")
    app.after(100,exibirdX_aluatilzado)

def exibirdY_aluatilzado():
    global  text_dy, dY, app
    text_dy.set(f"Y: {dY:.2f}")
    app.after(100,exibirdY_aluatilzado)

def exibirdZ_aluatilzado():
    global  text_dz, dZ, app
    text_dz.set(f"Z (altura): {dZ:.2f}")
    app.after(100,exibirdZ_aluatilzado)

def exibirtX_aluatilzado():
    global  text_tx, tX, app
    text_tx.set(f"X: {tX:.2f}")
    app.after(100,exibirtX_aluatilzado)

def exibirtY_aluatilzado():
    global  text_ty, tY, app
    text_ty.set(f"Y: {tY:.2f}")
    app.after(100,exibirtY_aluatilzado)

def exibirtZ_aluatilzado():
    global  text_tz, tZ, app
    text_tz.set(f"Z (altura): {tZ:.2f}")
    app.after(100,exibirtZ_aluatilzado)

#Define o cliente que se comunica com o Servidor TPC/IP no CLP.py
def cliente_TCP(): 
    global tX, tY, tZ, dX, dY, dZ
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    adress = ('localhost', 53444)
    sock.connect(adress)
    print("Conectado ao servidor.") 
    try:
        while True:
            msg = f"{tX},{tY},{tZ}"
            sock.sendall(bytes(msg, 'utf-8'))

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



    finally:
        sock.close()


def aplicativo():
    global app, tX, tY, tZ, dX, dY, dZ, text_tx, text_ty, text_tz, text_dx, text_dy, text_dz

    # Configurando estética e config. padrões
    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode('light')
    app = ctk.CTk()
    app.title('Controle do Drone')
    app.geometry('700x520')
    app.resizable(False,False)
    app.protocol("WM_DELETE_WINDOW",encerrar)
    
    
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
    frame_esquerda_titulo = ctk.CTkLabel(frame_esquerda, text="Target", font=("Arial", 16))
    frame_esquerda_titulo.pack(pady=10)   
    
    
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
    frame_direita_titulo = ctk.CTkLabel(frame_direita, text="Posição Atual", font=("Arial", 16))
    frame_direita_titulo.pack(pady=10)   
    

    
    #Exibir tX
    text_tx = ctk.DoubleVar()
    text_tx.set(f"X: {tX:.2f}")
    exibirtX = ctk.CTkLabel(frame_esquerda, textvariable=text_tx)
    exibirtX.pack(pady=10)
    exibirtX_aluatilzado()

    #Controle deslizante X
    barra_EixoX = ctk.CTkSlider(frame_esquerda, from_=-4.0, to=4.0, command=att_X)
    barra_EixoX.pack(pady=10)

    #Exibir dX
    text_dx = ctk.DoubleVar()
    text_dx.set(f"X: {dX:.2f}")
    exibirdX = ctk.CTkLabel(frame_direita, textvariable=text_dx)
    exibirdX.pack(pady=10)
    exibirdX_aluatilzado()



    #Exibir tY
    text_ty = ctk.DoubleVar()
    text_ty.set(f"Y: {tY:.2f}")
    exibirtY = ctk.CTkLabel(frame_esquerda, textvariable=text_ty)
    exibirtY.pack(pady=10)
    exibirtY_aluatilzado()

    #Controle deslizante Y
    barra_EixoY = ctk.CTkSlider(frame_esquerda, from_=-4.0, to=4.0, command=att_Y)
    barra_EixoY.pack(pady=10)

    #Exibir dY    
    text_dy = ctk.DoubleVar()
    text_dy.set(f"Y: {dY:.2f}")
    exibirdY = ctk.CTkLabel(frame_direita, textvariable=text_dy)
    exibirdY.pack(pady=10)
    exibirdY_aluatilzado()

    #Exibir tZ
    text_tz = ctk.DoubleVar()
    text_tz.set(f"Z (altura): {tZ:.2f}")
    exibirtZ = ctk.CTkLabel(frame_esquerda, textvariable=text_tz)
    exibirtZ.pack(pady=10)
    exibirtZ_aluatilzado()

    #Controle deslizante altura
    barra_altura = ctk.CTkSlider(frame_esquerda, from_=0.0, to=5, command=att_alt)
    barra_altura.number_of_steps=10
    barra_altura.pack(pady=10)
    
    #Exibir dZ    
    text_dz = ctk.DoubleVar()
    text_dz.set(f"Z: {dZ:.2f}")
    exibirdZ = ctk.CTkLabel(frame_direita, textvariable=text_dz)
    exibirdZ.pack(pady=10)
    exibirdZ_aluatilzado()
    
    app.mainloop()

def historiador():
    with open("historiador.txt", "w", encoding="utf-8") as arquivo_txt:
        arquivo_txt.write(f"Timestamp, Target tX, Target tY, Target tZ, Posição dX, Posição dY, Posição dZ\n")
        while rodando:
            arquivo_txt.write(f"{datetime.now()}, {tX:.2f}, {tY:.2f}, {tZ:.2f}, {dX:.2f}, {dY:.2f}, {dZ:.2f}\n")
            sleep(0.01)


def main():
    cliente = Thread(target=cliente_TCP)
    cliente.start()

    visual = Thread(target=aplicativo)
    visual.start()
    
    verifica_rodando = Thread(target=verifi_rodando)
    verifica_rodando.start()

    hist = Thread(target=historiador)
    hist.start()

if __name__ == "__main__":
    main()
