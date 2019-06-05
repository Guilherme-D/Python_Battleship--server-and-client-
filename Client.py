import os
import subprocess
import tkinter
import pickle
import threading
import random
import queue
import socket
import sys


class GuiPart:

    def call(self):
        pass

    def __init__(self, master, queue, endCommand, this):

        self.classtread = this
        self.queue = queue


        #Configurando a interface grafica


        #Criando frames
        self.topFrame = tkinter.Frame(root)
        self.topFrame.pack(pady=10)

        self.bottomFrame = tkinter.Frame(root)
        self.bottomFrame.pack(side=tkinter.LEFT)

        self.spaceFrame = tkinter.Frame(root)
        self.spaceFrame.pack(side=tkinter.LEFT, padx=10)

        self.enemyFrame = tkinter.Frame(root)
        self.enemyFrame.pack(side=tkinter.RIGHT)

        ####################################### TOP FRAME #######################################
        # Criando botão de conectar e campo de texto

        self.client_Field = tkinter.Entry(self.topFrame)
        self.client_Field.insert(0, "localhost")
        self.client_Field.pack(side=tkinter.LEFT, padx=10)

        self.portclient_Field = tkinter.Entry(self.topFrame)
        self.portclient_Field.insert(0, "15200")
        self.portclient_Field.pack(side=tkinter.LEFT, padx=10)


        self.ready_Btn = tkinter.Button(self.topFrame, text="Conectar", bg="cornflowerblue", command=self.conectar)
        self.ready_Btn.pack(side=tkinter.LEFT)
        self.ready_Btn.config(width=25)

        ###################################### spaceFrame ######################################

        #Informações sobre quais cores são cada navio e a quantidade de quadrados em cada um deles

        Porta = tkinter.Label(self.spaceFrame, text="Porta Aviões - Preto - 5 quadrados")
        Porta.pack(side=tkinter.BOTTOM);

        Navios = tkinter.Label(self.spaceFrame, text="Navios-Tanque - Rosa - 4 quadrados")
        Navios.pack(side=tkinter.BOTTOM);

        contra = tkinter.Label(self.spaceFrame, text="Contratorpedeiros - Verde - 3 quadrados")
        contra.pack(side=tkinter.BOTTOM);

        submarino = tkinter.Label(self.spaceFrame, text="Submarino - Amarelo - 2 quadrados")
        submarino.pack(side=tkinter.BOTTOM);



        self.vida = 30
        self.vida_inimigo = 30

        self.matrix = [[0 for x in range(10)] for y in range(10)]
        self.matrix_enemy = [[0 for x in range(10)] for y in range(10)]

        self.submarino_list = []


        self.shipcount = 0

        self.r = ''
        self.c = ''

        self.data = ''

        self.turno = False

        self.thread_cli ="" # = Conexao()

        self.call()
        self.create_matrix()

    ###################################### Criação da matriz do tabuleiro ######################################



    #Cria matriz com os barcos posicionados em uma ordem aleatoria
    def create_matrix(self):


        # seta posição de submarino
        x = random.randint(0, 8)
        y = random.randint(0, 8)

        while self.shipcount < 4:

            if random.randint(0, 1) == 0:
                if ((x, y) not in self.submarino_list) and ((x + 1, y) not in self.submarino_list):
                    print("submarino hor:  ", x, ",", y)
                    print("submarino hor:  ", x + 1, ",", y)
                    self.submarino_list.append(tuple((x, y)))
                    self.submarino_list.append(tuple((x + 1, y)))

                    self.matrix[x][y] = 4
                    self.matrix[x + 1][y] = 4

                    self.shipcount += 1

            else:
                if ((x, y) not in self.submarino_list) and ((x, y + 1) not in self.submarino_list):
                    print("submarino ver:  ", x, ",", y)
                    print("submarino ver:  ", x, ",", y + 1)
                    self.submarino_list.append(tuple((x, y)))
                    self.submarino_list.append(tuple((x, y + 1)))

                    self.matrix[x][y] = 4
                    self.matrix[x][y + 1] = 4

                    self.shipcount += 1

            x = random.randint(0, 8)
            y = random.randint(0, 8)

        # seta posição de contratorpedores
        self.shipcount = 0
        x = random.randint(0, 7)
        y = random.randint(0, 7)

        while self.shipcount < 3:

            if random.randint(0, 1) == 0:

                if ((x, y) not in self.submarino_list) and ((x + 1, y) not in self.submarino_list) and (
                        (x + 2, y) not in self.submarino_list):
                    print("contra hor:", x, ",", y)
                    print("contra hor:", x + 1, ",", y)
                    print("contra hor:", x + 2, ",", y)
                    self.submarino_list.append(tuple((x, y)))
                    self.submarino_list.append(tuple((x + 1, y)))
                    self.submarino_list.append(tuple((x + 2, y)))

                    self.matrix[x][y] = 3
                    self.matrix[x + 1][y] = 3
                    self.matrix[x + 2][y] = 3

                    self.shipcount += 1



            else:
                if ((x, y) not in self.submarino_list) and ((x, y + 1) not in self.submarino_list) and (
                        (x, y + 2) not in self.submarino_list):
                    print("contra ver:", x, ",", y)
                    print("contra ver:", x, ",", y + 1)
                    print("contra ver:", x, ",", y + 2)
                    self.submarino_list.append(tuple((x, y)))
                    self.submarino_list.append(tuple((x, y + 1)))
                    self.submarino_list.append(tuple((x, y + 2)))

                    self.matrix[x][y] = 3
                    self.matrix[x][y + 1] = 3
                    self.matrix[x][y + 2] = 3

                    self.shipcount += 1

            x = random.randint(0, 7)
            y = random.randint(0, 7)

        # seta posição de Navios-tanque
        self.shipcount = 0
        x = random.randint(0, 6)
        y = random.randint(0, 6)

        while self.shipcount < 2:

            if random.randint(0, 1) == 0:

                if ((x, y) not in self.submarino_list) and ((x + 1, y) not in self.submarino_list) and (
                        (x + 2, y) not in self.submarino_list) and ((x + 3, y) not in self.submarino_list):
                    print("navio hor:", x, ",", y)
                    print("navio hor:", x + 1, ",", y)
                    print("navio hor:", x + 2, ",", y)
                    print("navio hor:", x + 3, ",", y)
                    self.submarino_list.append(tuple((x, y)))
                    self.submarino_list.append(tuple((x + 1, y)))
                    self.submarino_list.append(tuple((x + 2, y)))
                    self.submarino_list.append(tuple((x + 3, y)))

                    self.matrix[x][y] = 2
                    self.matrix[x + 1][y] = 2
                    self.matrix[x + 2][y] = 2
                    self.matrix[x + 3][y] = 2

                    self.shipcount += 1


            else:

                if ((x, y) not in self.submarino_list) and ((x, y + 1) not in self.submarino_list) and (
                        (x, y + 2) not in self.submarino_list) and ((x, y + 3) not in self.submarino_list):
                    print("navio ver:", x, ",", y)
                    print("navio ver:", x, ",", y + 1)
                    print("navio ver:", x, ",", y + 2)
                    print("navio ver:", x, ",", y + 3)
                    self.submarino_list.append(tuple((x, y)))
                    self.submarino_list.append(tuple((x, y + 1)))
                    self.submarino_list.append(tuple((x, y + 2)))
                    self.submarino_list.append(tuple((x, y + 3)))

                    self.matrix[x][y] = 2
                    self.matrix[x][y + 1] = 2
                    self.matrix[x][y + 2] = 2
                    self.matrix[x][y + 3] = 2

                    self.shipcount += 1

            x = random.randint(0, 6)
            y = random.randint(0, 6)

        # seta posição de Porta-Aviões
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        self.shipcount = 0

        while self.shipcount < 1:

            if random.randint(0, 1) == 0:

                if ((x, y) not in self.submarino_list) and ((x + 1, y) not in self.submarino_list) and (
                        (x + 2, y) not in self.submarino_list) and ((x + 3, y) not in self.submarino_list) and (
                        (x + 4, y) not in self.submarino_list):
                    print("porta hor:", x, ",", y)
                    print("porta hor:", x + 1, ",", y)
                    print("porta hor:", x + 2, ",", y)
                    print("porta hor:", x + 3, ",", y)
                    print("porta hor:", x + 4, ",", y)
                    self.submarino_list.append(tuple((x, y)))
                    self.submarino_list.append(tuple((x + 1, y)))
                    self.submarino_list.append(tuple((x + 2, y)))
                    self.submarino_list.append(tuple((x + 3, y)))
                    self.submarino_list.append(tuple((x + 4, y)))

                    self.matrix[x][y] = 1
                    self.matrix[x + 1][y] = 1
                    self.matrix[x + 2][y] = 1
                    self.matrix[x + 3][y] = 1
                    self.matrix[x + 4][y] = 1

                    self.shipcount += 1


            else:

                if ((x, y) not in self.submarino_list) and ((x, y + 1) not in self.submarino_list) and (
                        (x, y + 2) not in self.submarino_list) and ((x, y + 3) not in self.submarino_list) and (
                        (x, y + 4) not in self.submarino_list):
                    print("porta ver:", x, ",", y)
                    print("porta ver:", x, ",", y + 1)
                    print("porta ver:", x, ",", y + 2)
                    print("porta ver:", x, ",", y + 3)
                    print("porta ver:", x, ",", y + 4)
                    self.submarino_list.append(tuple((x, y)))
                    self.submarino_list.append(tuple((x, y + 1)))
                    self.submarino_list.append(tuple((x, y + 2)))
                    self.submarino_list.append(tuple((x, y + 3)))
                    self.submarino_list.append(tuple((x, y + 4)))

                    self.matrix[x][y] = 1
                    self.matrix[x][y + 1] = 1
                    self.matrix[x][y + 2] = 1
                    self.matrix[x][y + 3] = 1
                    self.matrix[x][y + 4] = 1

                    self.shipcount += 1

            x = random.randint(0, 5)
            y = random.randint(0, 5)

        for row in self.matrix:
            print(row, " ")

        self.Create_grid(self.matrix)

    ###################################### mostrando graficamente a matriz do tabuleiro ######################################

    # Criando tabuleiros na interface grafica
    def Create_grid(self, matrix):

        for label_Grid in self.bottomFrame.winfo_children():
            label_Grid.destroy()

        for row_index in range(10):
            tkinter.Grid.rowconfigure(self.bottomFrame, row_index, weight=1)
            for col_index in range(10):
                if (matrix[row_index][col_index] != 0):

                    if (matrix[row_index][col_index] == 1):
                        # set label color to black
                        tkinter.Grid.columnconfigure(self.bottomFrame, col_index, weight=1, )
                        label_Grid = tkinter.Label(self.bottomFrame, bg="black", borderwidth=2, relief="groove",
                                                   width="5", height="2",
                                                   name=str(row_index) + " " + str(col_index))
                        label_Grid.grid(row=row_index, column=col_index,
                                        sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
                        # label_Grid.bind("<Button-1>", label_click)

                    if (matrix[row_index][col_index] == 2):
                        # set label color to black
                        tkinter.Grid.columnconfigure(self.bottomFrame, col_index, weight=1, )
                        label_Grid = tkinter.Label(self.bottomFrame, bg="pink", borderwidth=2, relief="groove",
                                                   width="5",
                                                   height="2",
                                                   name=str(row_index) + " " + str(col_index))
                        label_Grid.grid(row=row_index, column=col_index,
                                        sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
                        # label_Grid.bind("<Button-1>", label_click)

                    if (matrix[row_index][col_index] == 3):
                        # set label color to black
                        tkinter.Grid.columnconfigure(self.bottomFrame, col_index, weight=1, )
                        label_Grid = tkinter.Label(self.bottomFrame, bg="green", borderwidth=2, relief="groove",
                                                   width="5",
                                                   height="2",
                                                   name=str(row_index) + " " + str(col_index))
                        label_Grid.grid(row=row_index, column=col_index,
                                        sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
                        # label_Grid.bind("<Button-1>", label_click)

                    if (matrix[row_index][col_index] == 4):
                        # set label color to black
                        tkinter.Grid.columnconfigure(self.bottomFrame, col_index, weight=1, )
                        label_Grid = tkinter.Label(self.bottomFrame, bg="yellow", borderwidth=2, relief="groove",
                                                   width="5",
                                                   height="2",
                                                   name=str(row_index) + " " + str(col_index))
                        label_Grid.grid(row=row_index, column=col_index,
                                        sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
                        # label_Grid.bind("<Button-1>", label_click)

                else:
                    # set label color to white
                    tkinter.Grid.columnconfigure(self.bottomFrame, col_index, weight=1, )
                    label_Grid = tkinter.Label(self.bottomFrame, bg="white", borderwidth=2, relief="groove", width="5",
                                               height="2",
                                               name=str(row_index) + " " + str(col_index))
                    label_Grid.grid(row=row_index, column=col_index,
                                    sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
                    # label_Grid.bind("<Button-1>", label_click)

        # matriz inimigo
        # cria matriz para o que foi descoberto do tabuleiro inimigo
        for row_index in range(10):

            tkinter.Grid.rowconfigure(self.enemyFrame, row_index, weight=1)
            for col_index in range(10):
                tkinter.Grid.columnconfigure(self.enemyFrame, col_index, weight=1, )
                label_enemy = tkinter.Label(self.enemyFrame, bg="white", borderwidth=2, relief="groove", width="5",
                                            height="2", name=str(row_index) + " " + str(col_index))
                label_enemy.grid(row=row_index, column=col_index, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
                label_enemy.bind("<Button-1>", self.label_click)

    # Muda cor do label da matriz do servidor ao clicar em uma posição
    def label_click(self, event):

        if self.turno:
            names = str(event.widget).split(".")[-1]
            names = names.split(" ")

            self.r = int(names[0])
            self.c = int(names[1])

            self.thread_cli.send_message_to(self.r,self.c)

            data_split = self.data.split(b'-')


            if data_split[0] == b'errou':
                print("Acertou agua")
                self.matrix_enemy[self.r][self.c] = "x"
                event.widget.config(bg="blue")
                self.ataque_inimigo(data_split[1])

            elif data_split[0] == b'acertou':
                print("Acertou barco")
                self.matrix_enemy[self.r][self.c] = "x"
                event.widget.config(bg="red")
                self.ataque_inimigo(data_split[1])
                self.vida_inimigo -= 1
            else:
                print("posicao invalida, tente novamente")


        else:
            print("Espere a sua vez")


        # Mostra quantidade de vida e se ganhou ou perdeu
        if self.vida <= 30 and self.vida > 0:
            print("Vida: ", self.vida)
            print("Inimigo: ", self.vida_inimigo)
        elif self.vida == 0:
            print("Fim de Jogo - Voce perdeu")
        elif self.vida_inimigo == 0:
            print("Fim de Jogo - Parabens voce venceu")

    # Verifica se o ataque do servidor acertou ou nao algum barco na maatriz
    def ataque_inimigo(self,pos):
        str_pos = str(pos)
        row_pos = str_pos[2]
        col_pos = str_pos[4]
        int_r = int(str_pos[2])
        int_c = int(str_pos[4])

        #quando acerta alguma posição válida, o valor da matriz naquela posicao passa a valer "x"
        #posições atingidas que possuem barcos, sao marcadas de vermelho, outras posições (água) sao marcadas de azul
        if self.matrix[int_r][int_c] != "x":

            if self.matrix[int_r][int_c] != 0:

                self.matrix[int_r][int_c] = "x"

                print("acertou jogador")
                self.vida -= 1

                for label in self.bottomFrame.winfo_children():
                    if label.winfo_name() == row_pos + " " + col_pos:
                        print(label.winfo_name())
                        label.config(bg="red")

                self.vida -=1


            else:
                print("errou jogador")

                self.matrix[int_r][int_c] = "x"

                for label in self.bottomFrame.winfo_children():
                    if label.winfo_name() == row_pos + " " + col_pos:
                        print(label.winfo_name())
                        label.config(bg="blue")

        else:
            self.thread_cli.go('-','-')

    ####################################### Conexao #######################################

    # Acessa a classe da conexao ao apertar o botao conectar
    def conectar(self):

        self.turno = True
        self.thread_cli = Conexao(self)

##
# TREADEDCLIENT WAS HERE
##

class Conexao:

    def __init__(self,master):


        self.guimaster = master

        #inicia uma thread para a conexão com o servidor
        self.sock_cliente = threading.Thread(target=self.cria_sock_cli())
        self.sock_cliente.start()

    #cria o socket para a conexão
    def cria_sock_cli(self):
        # Cria o socket TCP
        self.sock_client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conecta o socket na porta que o servidor esta escutando
        # valores do endereco e porta sao pegos do campo de texto
        self.server_address2 = (self.guimaster.client_Field.get(), int(self.guimaster.portclient_Field.get()))

        print(sys.stderr, 'Conectando a %s porta %s' % self.server_address2)

        self.sock_client2.connect(self.server_address2)

    #envia mensagem para o servidor e envia resposta
    def send_message_to(self, r, c):

        try:


            # Mensagem a ser enviada
            message2 = str(r)+','+str(c) # str(row) + ',' + str(col)

            print("")
            print(sys.stderr, 'Enviando para o servidor a mensagem: "%s"' % message2)


            self.sock_client2.sendall((message2).encode('utf-8'))


            # Esperando resposta do servidor
            self.guimaster.data = self.sock_client2.recv(1024)


            #caso o servidor escolha uma posicao que ja foi escolhida previamente, deixa o servidor atacar novamente
            if b'novo ataque-' in self.guimaster.data:

                _get = str(self.guimaster.data).split('-')

                self.guimaster.ataque_inimigo("b'"+_get[1])

        except:
            print("Não foi possivel conectar")
        finally:
            print(sys.stderr, 'Fechando socket')
            # self.sock_client2.close()




#Essa classe inicia o programa
class ThreadedClient:

    def __init__(self, master):

        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # self.connection, self.client_address
        self.connection = self.client_address = 0

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication, self)




    def endApplication(self):
        self.running = 0

root = tkinter.Tk()
root.title("GUIPART - multi CLIENTE 2")

client = ThreadedClient(root)
root.mainloop()
