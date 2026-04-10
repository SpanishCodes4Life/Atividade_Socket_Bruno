import socket
import threading
import os

HOST = '0.0.0.0'
PORT = 5000

clientes = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# evita erro de porta ocupada
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen()

print("Sistema Gerenciador de Entregas Acadêmicas rodando...")
print("Aguardando conexões...")


def handle_client(conn, addr):
    try:
        nome = conn.recv(1024).decode().strip()
        print(f"{nome} conectado de {addr}")

        while True:
            tipo = conn.recv(1024).decode().strip()

            if not tipo:
                break

            # mensagem
            if tipo == "MSG":
                msg = conn.recv(1024).decode()
                print(f"[{nome}]: {msg}")

            # arquivo
            elif tipo == "FILE":
                nome_arquivo = conn.recv(1024).decode().strip()
                tamanho = int(conn.recv(1024).decode().strip())

                pasta = f"entregas/{nome}"
                os.makedirs(pasta, exist_ok=True)

                caminho = os.path.join(pasta, nome_arquivo)

                with open(caminho, "wb") as f:
                    bytes_recebidos = 0
                    while bytes_recebidos < tamanho:
                        data = conn.recv(1024)
                        f.write(data)
                        bytes_recebidos += len(data)

                print(f"{nome} enviou: {nome_arquivo}")

    except Exception as e:
        print(f"Erro com {addr}: {e}")

    finally:
        print(f"{addr} desconectado!!")
        conn.close()
        if conn in clientes:
            clientes.remove(conn)


def aceitar_conexoes():
    while True:
        conn, addr = server.accept()
        clientes.append(conn)

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


aceitar_conexoes()