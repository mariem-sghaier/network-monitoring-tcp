import socket
import time
def envoyer(s, msg):
    s.send((msg + "\n").encode())
    rep = s.recv(1024).decode().strip()
    print(f"  {msg}")
    print(f"  {rep}")
    return rep
print("Test 5 : calcul des statistiques\n")
# Agent 1 : CPU 20%, RAM 1000 MB
s1 = socket.socket()
s1.connect(("127.0.0.1", 9000))
envoyer(s1, "HELLO agent-AAA PC1")
envoyer(s1, f"REPORT agent-AAA {int(time.time())} 20.0 1000")
print()
# Agent 2 : CPU 40%, RAM 2000 MB
s2 = socket.socket()
s2.connect(("127.0.0.1", 9000))
envoyer(s2, "HELLO agent-BBB PC2")
envoyer(s2, f"REPORT agent-BBB {int(time.time())} 40.0 2000")
print()
# Agent 3 : CPU 30%, RAM 1500 MB
s3 = socket.socket()
s3.connect(("127.0.0.1", 9000))
envoyer(s3, "HELLO agent-CCC PC3")
envoyer(s3, f"REPORT agent-CCC {int(time.time())} 30.0 1500")
print()
print("Attends 6 secondes pour voir les stats dans le terminal du serveur...")
time.sleep(6)
s1.close()
s2.close()
s3.close()
print("\nTest terminé.")
