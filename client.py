import socket
import time
import uuid
import psutil

HOST     = "127.0.0.1"
PORT     = 9000
T        = 5                              
AGENT_ID = "agent-" + str(uuid.uuid4())[:8]  
HOSTNAME = socket.gethostname()

def connecter():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

def envoyer(s, message):
    s.send((message + "\n").encode())
    reponse = s.recv(1024).decode().strip()
    print(f"  envoyé  : {message}")
    print(f"  reçu    : {reponse}")
    return reponse

def collecter():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().used / (1024 * 1024)  
    return round(cpu, 2), round(ram, 2)

def main():
    print(f" Agent ID : {AGENT_ID}")
    print(f" Hostname : {HOSTNAME}")
    print(f" Connexion à {HOST}:{PORT} ...")

    try:
        s = connecter()
        print(" Connecté au serveur\n")

        rep = envoyer(s, f"HELLO {AGENT_ID} {HOSTNAME}")
        if rep != "OK":
            print(" Le serveur a refusé l'enregistrement.")
            s.close()
            return

        print(f"\n Envoi des métriques toutes les {T} secondes\n")
        while True:
            time.sleep(T)
            cpu, ram = collecter()
            ts  = int(time.time())
            msg = f"REPORT {AGENT_ID} {ts} {cpu} {ram}"
            rep = envoyer(s, msg)
            if rep != "OK":
                print(" Erreur serveur sur REPORT")

    except KeyboardInterrupt:
        print("\n Arrêt de l'agent...")
        try:
            envoyer(s, f"BYE {AGENT_ID}")
        except:
            pass

    except ConnectionRefusedError:
        print(" Impossible de se connecter. Le serveur est-il lancé ?")

    finally:
        try:
            s.close()
        except:
            pass
        print(" Agent déconnecté proprement.")


if __name__ == "__main__":
    main()