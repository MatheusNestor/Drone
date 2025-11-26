
# Instruções de compilação

## 1.1. Preparando o ambiente:
É necessário ter instalado em sua máquina os dois simuladores (acesse os sites oficiais para mais instruções):
- Prosys OPC UA Simulation Server
- CoppeliaSim

Todo o projeto foi desenvolvido na versão 3.13.7 do Python. É altamente aconselhável que seja nesta versão que tente executar o código.

Além disso, é necessário instalar as seguintes bibliotecas:
- opcua (pip install opcua)
- customtkinter (pip install customtkinter)
- tkinter (pip install tkinter)

## 1.2. Execução:
No geral, para garantir que não seja apresentado nenhum erro, é necessário abrir os arquivos dos dois simuladores: “drone.uasim” e “drone.ttt”.

### 1.2.1. Windows
- Faça o download da pasta do projeto.
- Acesse a pasta (Drone) pelo terminal.
- Execute o arquivo "run.py".

Obs: o "run.py" é na verdade um método mais eficiente de rodar os vários arquivos, na ordem certa e no mesmo terminal. Ou seja, é mais fácil e mais prático. Caso não funcione tente executar o arquivo conforme a ordem da própria sessão.

### 1.2.2. Linux
- Acesse a pasta (Drone) pelo terminal.
- Execute o arquivo "run.py".

E então execute cada um dos arquivos que seguem, em ordem, cada um uma nova janela do terminal:
1º - brigde.py
2º - CLP.py34
3º - chainedserver.py
4º - sinotico.py
5º - mes.py

Essa ordem é uma sugestão, mas é provavelmente a mais coerente pela forma como o projeto foi desenvolvido. Isto é, é possível rodar o CLP e então o chainedserver, e por fim o mes, por exemplo. Mas na prática, todas as variáveis seriam 0, já que quem controla o sistema (sinotico) não foi inicializado.

Obs: pode ser necessário trocar o valor da variável IP, dos arquivos em que ela está presente, para o IPv4 da máquina em que se roda o projeto.

# Instruções de operação do sistema

Se tudo deu certo, será exibida uma janela. Ela está dividida em 3 blocos principais.

## 2.1. Bloco 1 (esquerda)
Esse é, efetivamente, o bloco que melhor controla o drone. São três controles deslizantes (sliders), um para cada variável de target. Ao iniciar, todas estão configuradas para permanecer em 0. Ao fazer qualquer mudança, o valor de target muda e é exibido acima do respectivo controle.

Em especial, destaca-se que os sliders de target de X e Y vão de -4 a 4 (para limitar no simulador, já que o drone poderia vagar mais livremente se fosse desejado). O referente ao target de Z vai de 0 a 10.

## 2.2. Bloco 2 (direita superior)
Ele apenas exibe o valor da posição atual do drone, separado por variável.

Obs: o sistema não é, por definição, de tempo real. Ou seja, não é necessário nem esperado que o valor configurado seja instantaneamente mostrado. Isso também quer dizer que o drone leva um certo tempo até estabilizar na posição configurada.

## 2.3. Bloco 3 (direita inferior)
Contém três botões para facilitar para o operador:

### 2.3.1. "Voltar para posição inicial"
Como o nome sugere, configura os targets para 0. Dessa forma, o drone retorna à posição inicial. Depois de acioná-lo, ainda é possível utilizar os sliders para controlar o drone.

### 2.3.2. "Encerrar conexão"
Força o encerramento da conexão do drone com os sistemas, encerrando todos os processos.

### 2.3.3. "Fazer volta padrão"
Faz com que o drone visite pontos previamente configurados, em ordem, e então retorne a posição inicial, parando 45 segundos em cada um desses pontos. Essa opção desabilita qualquer tipo de controle manual, até o fim do ciclo completo; dessa forma, a interface fica "travada" por pelo menos 225 segundos. A ideia é simular uma situação automática real, em que o drone faz a varredura de todas as plataformas sozinho.
