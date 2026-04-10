import socket
import os
import time

HOST = '127.0.0.1'
PORT = 5000


def enviar_mensagem(sock):
    msg = input("Digite a mensagem: ")
    sock.send("MSG".encode())
    time.sleep(0.1)
    sock.send(msg.encode())


def enviar_arquivo(sock):
    caminho = input("Digite o nome da atividade: ").strip().replace('"','')

    if not os.path.exists(caminho):
        print("Arquivo não encontrado!")
        return

    nome = os.path.basename(caminho)
    tamanho = os.path.getsize(caminho)

    # envia tipo
    sock.send("FILE".encode())
    time.sleep(0.1)

    # envia nome
    sock.send(nome.encode())
    time.sleep(0.1)

    # envia tamanho
    sock.send(str(tamanho).encode())
    time.sleep(0.1)

    # envia conteúdo
    with open(caminho, "rb") as f:
        while True:
            dados = f.read(1024)
            if not dados:
                break
            sock.send(dados)

    print("Arquivo enviado com sucesso!")


def menu(sock):
    while True:
        print("\n MENU")
        print("1 - Enviar mensagem")
        print("2 - Enviar atividade")
        print("3 - Sair")

        op = input("Escolha: ")

        if op == "1":
            enviar_mensagem(sock)

        elif op == "2":
            enviar_arquivo(sock)

        elif op == "3":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("🔄 Conectando ao servidor...")
    client.connect((HOST, PORT))
    print("✅ Conectado!")

    nome = input("Digite seu nome: ")
    client.send(nome.encode())

    menu(client)

    client.close()


main()