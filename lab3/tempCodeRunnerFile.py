import socket
import dns.resolver

def resolve_domain(domain, dns_server=None):
    try:
        if dns_server:
            resolver = dns.resolver.Resolver(configure=False)
            resolver.nameservers = [dns_server]
            answers = resolver.resolve(domain)
        else:
            answers = dns.resolver.resolve(domain)

        ips = [str(answer) for answer in answers]
        return ips
    except dns.resolver.NXDOMAIN:
        return None
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.Timeout:
        return None

def resolve_ip(ip, dns_server=None):
    try:
        if dns_server:
            resolver = dns.resolver.Resolver(configure=False)
            resolver.nameservers = [dns_server]
            domains = resolver.query(dns.reversename.from_address(ip), 'PTR')
        else:
            domains = dns.resolver.resolve_address(ip)

        domain_names = [str(domain) for domain in domains]
        return domain_names
    except dns.resolver.NXDOMAIN:
        return None
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.Timeout:
        return None

def main():
    default_dns = socket.gethostbyname(socket.gethostname())
    current_dns = default_dns
    print(f"DNS serverul implicit este: {default_dns}")

    while True:
        command = input("\nIntroduceți comanda dorita resolve <> sau use dns <>: ")

        if command.startswith("resolve "):
            _, query = command.split(" ", 1)
            if ":" in query:  # IP address
                result = resolve_ip(query, current_dns)
                if result:
                    print("Domeniile asociate cu adresa IP sunt:")
                    for domain in result:
                        print(domain)
                else:
                    print("Nu s-au putut găsi domenii asociate cu adresa IP.")
            else:  # Domain
                result = resolve_domain(query, current_dns)
                if result:
                    print("Adresele IP asociate cu domeniul sunt:")
                    for ip in result:
                        print(ip)
                else:
                    print("Nu s-au putut găsi adrese IP asociate cu domeniul.")
        
        elif command.startswith("use dns "):
            _, new_dns = command.split(" ", 1)
            try:
                socket.inet_aton(new_dns)
                current_dns = new_dns
                print(f"DNS-ul a fost schimbat cu succes la: {new_dns}")
            except socket.error:
                print("Adresa IP a DNS-ului este invalidă.")

        else:
            print("Comandă invalidă. Comenzile valide sunt 'resolve' și 'use dns'.")

if __name__ == "__main__":
    main()
