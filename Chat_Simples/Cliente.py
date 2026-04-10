import socket

TCP_IP = '127.0.0.1' #REDE LOCAL DESKTOP
TCP_PORTA = 10737 # PORTA COMO RA DO DEV
BUFFER = 1024

print("*~"*20)
print("ENTRANDO NO RPG")
print("*~"*20)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((TCP_IP, TCP_PORTA))

# envia nome
nome = input("Digite o nome do personagem: ")
cliente.send(nome.encode())

while True:
    data = cliente.recv(BUFFER)
    if not data:
        break

    print(data.decode())

    # se jogo acabou
    if "venceu" in data.decode().lower() or "morreu" in data.decode().lower() or "fugiu" in data.decode().lower():
        break

    escolha = input("Escolha: ")
    cliente.send(escolha.encode())

cliente.close()