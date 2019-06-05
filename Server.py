import random
import socket
import sys
import tkinter


class matrix:
    def __init__(self):

        self.matrix = [[0 for x in range(10)] for y in range(10)]
        self.submarino_list = []

        self.shipcount = 0

        self.create_matrix()

        self.vida = 30
        self.vida_jogador = 30

        self.host = ''
        self.port = ''


        if len(sys.argv) == 3:

            print("Endereço escolhido: ", sys.argv[1])
            self.host = sys.argv[1].encode("utf-8")
            print("Porta escolhida: ", sys.argv[2])
            self.port = int(sys.argv[2])

            self.start_server(self.host, self.port)
        else:

            print("Endereço e porta nao foram passados como parâmetro, digite da seguinte forma para continuar:")
            print("Servidor.py <Endereco> <Porta>")




    def start_server(self, host, port):
        # Cria socket TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # vinculando socket a porta
        server_address = (host, port)
        print(sys.stderr, 'Iniciando servidor no endereco %s na porta %s' % server_address)
        sock.bind(server_address)

        # Escutando porta
        sock.listen(1)

        while True:
            # Esperando por uma conexao
            print(sys.stderr, 'Esperando conexao')
            connection, client_address = sock.accept()

            try:
                print(sys.stderr, 'Conectado com o cliente ', client_address)

                # recebe dados em pequenos pedaços
                while True:
                    data = connection.recv(16)
                    print('Mensagem recebida: "%s"' % data)

                    # se dado recebido for invalido, ataca novamente com outra posição,
                    # caso contrario, ataca normalmente
                    if data == b'-,-':

                        pos = self.atacar()
                        print("Escolhendo novamente _> ",pos)
                        atacou_pos = b'novo ataque'
                        print('Enviando mensagem de volta para o cliente ', atacou_pos+pos)
                    else:
                        pos = self.atacar()
                        atacou_pos = self.check_position(data)

                        print('Enviando mensagem de volta para o cliente ', atacou_pos)


                    connection.sendall(atacou_pos+pos)



            finally:
                connection.close()
                print("Conexão encerrada")

    # escolhe uma posição aleatoria para atacar
    def atacar(self):
        print("atacando posição: str(random.randint(0,9))",str(random.randint(0,9))+','+str(random.randint(0,9)))
        return bytes('-'+str(random.randint(0,9))+','+str(random.randint(0,9)),'utf-8')


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

    # Confere se posição recebida e retorna se a mesma é uma posição invalida, se acertou ou se errou um barco
    def check_position(self, data):

        pos = data.decode('UTF-8')



        self.resposta = ''

        if self.matrix[int(pos[0])][int(pos[2])] != "x":

            if self.matrix[int(pos[0])][int(pos[2])] == 0:
                print("Errou")
                self.matrix[int(pos[0])][int(pos[2])] = "x"
                self.resposta = b'errou'
            else:
                print("acertou")
                self.matrix[int(pos[0])][int(pos[2])] = "x"
                self.resposta = b'acertou'
                self.vida -=1


        else:
            self.resposta = b'posicao invalida'



        #mostra quantidade de vidas e quem ganhou
        if self.vida >= 0:
            print("vida-servidor: ",self.vida)

            print("vida-jogador: ",self.vida_jogador)
        elif self.vida == 0:
            print("Fim do jogo - Parabens, você venceu")
        elif self.vida_jogador == 0:
            print("Fim do Jogo - Você perdeu")

        return self.resposta




root = tkinter.Tk()
root.title("Battleship - Servidor")

root.mainloop()
matrix()
