import requests
from requests.exceptions import HTTPError
 
API_URL = "http://127.0.0.1:8000"

def listar_dados():
    response = requests.get(f"{API_URL}/items")
    print("\nDados no banco:")
    for row in response.json():
        print(row)

def inserir_dados():
    nome = input("Nome: ")
    idade = int(input("Idade: "))  # Convert to int
    data = {"nome": nome, "idade": idade}
    response = requests.post(f"{API_URL}/items", json=data)
    print(response.json()["message"])

def atualizar_dados():
    id = int(input("ID do registro a atualizar: "))
    nome = input("Novo Nome: ")
    idade = int(input("Nova Idade: "))
    data = {"nome": nome, "idade": idade}
    response = requests.put(f"{API_URL}/items/{id}", json=data)
    print(response.json()["message"])

def deletar_dados():
    id = int(input("ID do registro a deletar: "))
    response = requests.delete(f"{API_URL}/items/{id}")
    print(response.json()["message"])

def menu():
    while True:
        print("\n1. Listar Dados")
        print("2. Inserir Dados")
        print("3. Atualizar Dados")
        print("4. Deletar Dados")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_dados()
        elif opcao == "2":
            try:
                inserir_dados()
            except Exception as e:
                print(f"\n->Erro: {type(e)}, {e}")
        elif opcao == "3":
            atualizar_dados()
        elif opcao == "4":
            deletar_dados()
        elif opcao == "5":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()