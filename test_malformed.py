import socket
s = socket.socket()
s.connect(("127.0.0.1", 9000))
# Message 1 : HELLO sans hostname (mal formé)
s.send(b"HELLO agent1\n")
print("Test 1 :", s.recv(1024).decode().strip())
# Message 2 : commande inconnue
s.send(b"BONJOUR blabla\n")
print("Test 2 :", s.recv(1024).decode().strip())
# Message 3 : REPORT avec des lettres à la place des chiffres
s.send(b"REPORT agent1 abc xyz xyz\n")
print("Test 3 :", s.recv(1024).decode().strip())
# Message 4 : CPU invalide (150 > 100)
s.send(b"REPORT agent1 1700000000 150.0 2048\n")
print("Test 4 :", s.recv(1024).decode().strip()) 
s.close()