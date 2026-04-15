import socket
import threading
import time
import csv
import os

agents = {}
lock   = threading.Lock()
T = 5  

def gerer_client(conn, addr):
    print(f" Connexion : {addr}")
    try:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            print(f"[reçu de {addr}] {data}")
            parties = data.split()

            if len(parties) == 0:
                conn.send(b"ERROR\n")
                continue

            
            if parties[0] == "HELLO" and len(parties) == 3:
                agent_id = parties[1]
                hostname = parties[2]
                with lock:
                    agents[agent_id] = {
                        "hostname":  hostname,
                        "cpu":       0.0,
                        "ram":       0.0,
                        "last_seen": time.time()
                    }
                conn.send(b"OK\n")

            
            elif parties[0] == "REPORT" and len(parties) == 5:
                try:
                    aid  = parties[1]
                    cpu  = float(parties[3])
                    ram  = float(parties[4])
                    if not (0.0 <= cpu <= 100.0) or ram < 0:
                        conn.send(b"ERROR\n")
                    elif aid not in agents:
                        conn.send(b"ERROR\n")  
                    else:
                        with lock:
                            agents[aid]["cpu"]       = cpu
                            agents[aid]["ram"]       = ram
                            agents[aid]["last_seen"] = time.time()
                        conn.send(b"OK\n")
                except ValueError:
                    conn.send(b"ERROR\n")

            
            elif parties[0] == "BYE" and len(parties) == 2:
                with lock:
                    agents.pop(parties[1], None)
                conn.send(b"OK\n")
                break

            else:
                conn.send(b"ERROR\n")

    except Exception as e:
        print(f" Erreur client {addr} : {e}")
    finally:
        conn.close()
        print(f" Déconnexion : {addr}")



def nettoyer_inactifs():
    while True:
        time.sleep(T)
        now = time.time()
        with lock:
            inactifs = [
                aid for aid, info in agents.items()
                if now - info["last_seen"] > 3 * T
            ]
            for aid in inactifs:
                print(f"[inactif] Agent {aid} retiré (timeout)")
                del agents[aid]



def afficher_stats():
    while True:
        time.sleep(T)
        with lock:
            nb = len(agents)
            if nb == 0:
                print("\n[stats] Aucun agent actif\n")
            else:
                moy_cpu = sum(a["cpu"] for a in agents.values()) / nb
                moy_ram = sum(a["ram"] for a in agents.values()) / nb
                print(f"\n[stats] Agents actifs : {nb} | "
                      f"CPU moy : {moy_cpu:.1f}% | "
                      f"RAM moy : {moy_ram:.0f} MB")
                for aid, info in agents.items():
                    print(f"        {aid} ({info['hostname']}) "
                          f"CPU={info['cpu']}% RAM={info['ram']}MB")
                print()
                
                exporter_csv()


def exporter_csv():
    fichier = "stats.csv"
    existe  = os.path.isfile(fichier)
    with open(fichier, "a", newline="") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["timestamp", "agent_id", "hostname", "cpu", "ram"])
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        for aid, info in agents.items():
            writer.writerow([ts, aid, info["hostname"], info["cpu"], info["ram"]])


def main():
    HOST = "0.0.0.0"
    PORT = 9000

    threading.Thread(target=afficher_stats,  daemon=True).start()
    threading.Thread(target=nettoyer_inactifs, daemon=True).start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)
    print(f" Serveur démarré sur {HOST}:{PORT} — intervalle T={T}s")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(
                target=gerer_client,
                args=(conn, addr),
                daemon=True
            ).start()
    except KeyboardInterrupt:
        print("\n Serveur arrêté proprement.")
    finally:
        server.close()


if __name__ == "__main__":
    main()