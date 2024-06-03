import socket

def resolve_domain(domain, dns_server):
    try:
        ips = socket.gethostbyname_ex(domain)
        print("Adresele IP pentru domeniul {} sunt: {}".format(domain, ips[2]))
    except socket.gaierror as e:
        print("Eroare: Nu s-au putut rezolva adresele IP pentru domeniul {}. {}".format(domain, e))

def resolve_ip(ip, dns_server):
    try:
        domains = socket.gethostbyaddr(ip)
        print("Domeniile asociate adresei IP {} sunt: {}".format(ip, domains[0]))
    except socket.herror as e:
        print("Eroare: Nu s-au putut rezolva domeniile asociate adresei IP {}. {}".format(ip, e))

def change_dns_server(new_dns_server):
    try:
        socket.gethostbyname("google.com") # Verificăm dacă există conectivitate la internet înainte de a schimba DNS-ul
        socket.setdns(new_dns_server)
        print("DNS-ul a fost schimbat cu succes la {}".format(new_dns_server))
    except OSError as e:
        print("Eroare: Nu s-a putut schimba DNS-ul la {}. {}".format(new_dns_server, e))

def main():
    current_dns_server = socket.gethostbyname("google.com")
    print("DNS-ul curent este setat la:", current_dns_server)

    print("\nIntroduceți una dintre următoarele comenzi:")
    print(" - resolve <domain> sau resolve <ip>")
    print(" - use dns <ip> pentru a schimba serverul DNS")

    while True:
        command = input("Introduceți comanda: ").strip().split()

        if command[0] == "resolve":
            if len(command) != 2:
                print("Eroare: Comandă invalidă. Folosiți 'resolve <domain>' sau 'resolve <ip>'.")
                continue

            if "." in command[1]: # Verificăm dacă este un domeniu sau o adresă IP
                resolve_domain(command[1], current_dns_server)
            else:
                resolve_ip(command[1], current_dns_server)

        elif command[0] == "use" and command[1] == "dns":
            if len(command) != 3:
                print("Eroare: Comandă invalidă. Folosiți 'use dns <ip>'.")
                continue

            new_dns_server = command[2]
            change_dns_server(new_dns_server)
            current_dns_server = new_dns_server

        else:
            print("Eroare: Comandă invalidă.")

if __name__ == "__main__":
    main()
