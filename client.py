import rpyc
import threading
from rpyc.utils.server import ThreadPoolServer

class Cliente(rpyc.Service):
    id = 1
    def __init__(self):
        self.id = Cliente.id
        Cliente.id += 1
    
    def exposed_notify(self):
        print(f'Seu serviço foi efetuado')

    def cortarCabelo(self):
        conn = rpyc.connect("localhost", 12345)
        result = conn.root.cortarCabelo(self.id)
        print(result)
        conn.close()

    def cortarBarba(self):
        conn = rpyc.connect("localhost", 12345)
        result = conn.root.cortarBarba(self.id)
        print(result)
        conn.close()

    def cortarBigode(self):
        conn = rpyc.connect("localhost", 12345)
        result = conn.root.cortarBigode(self.id)
        print(result)
        conn.close()

if __name__ == '__main__':
    port = 12346
    server = ThreadPoolServer(Cliente, port=port) # Server que utiliza pool de threads
    print(f'Server listening on port {port}')
    clients = [
        Cliente(),
        Cliente(),
        Cliente(),
        Cliente(),
        Cliente()
    ]
    for client in clients:
        threading.Thread(target=client.cortarCabelo, daemon=True).start()
        threading.Thread(target=client.cortarBarba, daemon=True).start()
        threading.Thread(target=client.cortarBigode, daemon=True).start()
    server.start()