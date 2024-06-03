import requests

def list_categories():
    response = requests.get("http://localhost:8000/categories")
    if response.status_code == 200:
        categories = response.json()
        print("Lista de categorii:")
        for category in categories:
            print(category['name'])
    else:
        print("Eroare la obtinerea listei de categorii.")

def show_category_details(category_id):
    response = requests.get(f"http://localhost:8000/categories/{category_id}")
    if response.status_code == 200:
        category = response.json()
        print(f"Detalii despre categoria {category_id}:")
        print(f"Nume: {category['name']}")
        print(f"Descriere: {category['description']}")
    else:
        print("Eroare la obtinerea detaliilor despre categorie.")

def create_category(name, description):
    data = {'name': name, 'description': description}
    response = requests.post("http://localhost:8000/categories", json=data)
    if response.status_code == 201:
        print("Categoria a fost creata cu succes.")
    elif response.status_code == 400:
        print("Eroare: Datele de intrare nu sunt valide.")
    else:
        print("Eroare la crearea categoriei.")

def delete_category(category_id):
    response = requests.delete(f"http://localhost:8000/categories/{category_id}")
    if response.status_code == 204:
        print("Categoria a fost stearsa cu succes.")
    else:
        print("Eroare la stergerea categoriei.")

def update_category_name(category_id, new_name):
    data = {'name': new_name}
    response = requests.put(f"http://localhost:8000/categories/{category_id}", json=data)
    if response.status_code == 200:
        print("Numele categoriei a fost actualizat cu succes.")
    elif response.status_code == 404:
        print("Eroare: Categoria nu a fost gasita.")
    else:
        print("Eroare la actualizarea numelui categoriei.")

def create_product(category_id, product_name, price):
    data = {'name': product_name, 'price': price}
    response = requests.post(f"http://localhost:8000/categories/{category_id}/products", json=data)
    if response.status_code == 201:
        print("Produsul a fost creat cu succes in categoria specificata.")
    elif response.status_code == 404:
        print("Eroare: Categoria nu a fost gasita.")
    else:
        print("Eroare la crearea produsului.")

def list_products(category_id):
    response = requests.get(f"http://localhost:8000/categories/{category_id}/products")
    if response.status_code == 200:
        products = response.json()
        print(f"Lista de produse din categoria {category_id}:")
        for product in products:
            print(f"Nume: {product['name']}, Pret: {product['price']}")
    else:
        print("Eroare la obtinerea listei de produse.")

# Exemplu de utilizare:
if __name__ == "__main__":
    while True:
        print("\nOptiuni:")
        print("1. Lista de categorii")
        print("2. Detalii despre o categorie")
        print("3. Creati o categorie noua")
        print("4. stergeti o categorie")
        print("5. Modificati titlul unei categorii")
        print("6. Creati produse noi intr-o categorie")
        print("7. Lista de produse dintr-o categorie")
        print("0. Iesire")
        choice = input("Introduceti optiunea dvs.: ")

        if choice == "1":
            list_categories()
        elif choice == "2":
            category_id = input("Introduceti ID-ul categoriei: ")
            show_category_details(category_id)
        elif choice == "3":
            name = input("Introduceti numele categoriei noi: ")
            description = input("Introduceti descrierea categoriei noi: ")
            create_category(name, description)
        elif choice == "4":
            category_id = input("Introduceti ID-ul categoriei de sters: ")
            delete_category(category_id)
        elif choice == "5":
            category_id = input("Introduceti ID-ul categoriei de modificat: ")
            new_name = input("Introduceti noul nume pentru categorie: ")
            update_category_name(category_id, new_name)
        elif choice == "6":
            category_id = input("Introduceti ID-ul categoriei in care sa creati produse noi: ")
            product_name = input("Introduceti numele produsului nou: ")
            price = input("Introduceti pretul produsului nou: ")
            create_product(category_id, product_name, price)
        elif choice == "7":
            category_id = input("Introduceti ID-ul categoriei pentru a vedea lista de produse: ")
            list_products(category_id)
        elif choice == "0":
            print("La revedere!")
            break
        else:
            print("Optiune invalida. Va rugam sa introduceti din nou.")
