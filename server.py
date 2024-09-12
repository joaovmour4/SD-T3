import rpyc
import time
import threading
import os
from rpyc.utils.server import ThreadPoolServer

class Barbeiro(rpyc.Service):
    fila = []
    busy = False
    # def on_connect(self, conn):
    #     print('Conexão estabelecida')
    #     self.clients.append(conn)
    # def on_disconnect(self, conn):
    #     print('Conexão encerrada')
    #     self.clients.append(conn)

    @staticmethod
    def trabalha(operacao, cliente):
        os.system('cls')
        Barbeiro.print_fila()
        trabalho = ''
        tempo = 0

        match operacao:
            case 1:
                trabalho = 'Cortando cabelo'
                tempo = 5
            case 2:
                trabalho = 'Cortando barba'
                tempo = 4
            case 3:
                trabalho = 'Cortando bigode'
                tempo = 3
            case _:
                trabalho = ''
                tempo = 0

        Barbeiro.busy = True
        print(f'{trabalho} do cliente {cliente}')
        time.sleep(tempo)
        print(f'Finalizado.')
        conn = rpyc.connect("localhost", 12346)
        conn.root.notify()
        conn.close()
        Barbeiro.busy = False
    
    @staticmethod
    def print_fila():
        fila = []
        for item in Barbeiro.fila:
            fila.append(f'Cliente {item[1]}')
        print('Fila: ', fila)
    
    @staticmethod
    def gerencia_fila():
        while True:
            if Barbeiro.busy == True:
                pass
            elif Barbeiro.fila:
                Barbeiro.trabalha(Barbeiro.fila[0][0], Barbeiro.fila[0][1])
                Barbeiro.fila.pop(0)

    def exposed_cortarCabelo(self, client):
        Barbeiro.fila.append([1, client]) # Operação 1: Corte de cabelo
        return f'O cliente {client} está na fila para Corte de cabelo'
    
    def exposed_cortarBarba(self, client):
        Barbeiro.fila.append([2, client]) # Operação 2: Corte de barba
        return f'O cliente {client} está na fila para Corte de barba'

    def exposed_cortarBigode(self, client):
        Barbeiro.fila.append([3, client]) # Operação 3: Corte de bigode
        return f'O cliente {client} está na fila para Corte de bigode'


if __name__ == '__main__':
    port = 12345
    server = ThreadPoolServer(Barbeiro, port=port) # Server que utiliza pool de threads
    print(f'Server listening on port {port}')
    threading.Thread(target=Barbeiro.gerencia_fila, daemon=True).start()
    server.start()