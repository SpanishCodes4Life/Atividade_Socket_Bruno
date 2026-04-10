import socket
import random

TCP_IP = '127.0.0.1' # REDE LOCAL DESKTOP
TCP_PORTA = 10737 # PORTA COMO RA DO DEV
BUFFER = 1024

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((TCP_IP, TCP_PORTA))
servidor.listen(1)

print("*~"*20)
print("SERVIDOR RPG ONLINE")
print("*~"*20)
print("Esperando jogador...")

conn, addr = servidor.accept()
print("Conectado:", addr)

# Recebe nome
nome = conn.recv(BUFFER).decode()

# Status do jogador
vida = random.randint(10, 20)
defesa = random.randint(1, 5)

print(f"Jogador: {nome} | Vida: {vida} | Defesa: {defesa}")

# Inimigo
inimigos = ["Goblin", "Orc", "Esqueleto"]
inimigo = random.choice(inimigos)
vida_inimigo = random.randint(8, 15)

# Envia introdução

msg = f"Bem-vindo {nome}!\nVocê encontrou um {inimigo}!\nSua vida: {vida}\nVida do: {inimigo}: {vida_inimigo}\n\n1 - Atacar\n2 - Fugir"
conn.send(msg.encode())

while True:
    data = conn.recv(BUFFER)
    if not data:
        break

    escolha = data.decode()

    if escolha == "1":
        dano = random.randint(1, 6)
        vida_inimigo -= dano

        resposta = f"\nVocê causou {dano} de dano no {inimigo}!"

        if vida_inimigo <= 0:
            resposta += "\nVocê venceu!"
            conn.send(resposta.encode())
            break

        dano_inimigo = random.randint(1, 5)
        dano_real = max(0, dano_inimigo - defesa)
        vida -= dano_real

        resposta += f"\nO {inimigo} causou {dano_real} de dano!"

        if vida <= 0:
            resposta += "\nVocê morreu 😢"
            conn.send(resposta.encode())
            break

        # 🔥STATUS COMPLETO
        resposta += f"\n\n=== STATUS ATUAL ==="
        resposta += f"\nSua vida: {vida}"
        resposta += f"\nVida do {inimigo}: {vida_inimigo}"
        resposta += "\n\n1 - Atacar\n2 - Fugir"

        conn.send(resposta.encode())

    elif escolha == "2":
        conn.send("Você fugiu da batalha!".encode())
        break

    else:
        conn.send("Opção inválida!\n1 - Atacar\n2 - Fugir".encode())

conn.close()
servidor.close()