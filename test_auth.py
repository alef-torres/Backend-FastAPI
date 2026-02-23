import requests
import random
import string

BASE_URL = "http://127.0.0.1:8000"


def gerar_email_aleatorio():
    prefixo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefixo}@teste.com"


def test_fluxo_autenticacao():
    email = gerar_email_aleatorio()
    senha = "senha123"
    nome = "Usuario Teste"

    # 1. Testar Criação de Usuário
    print(f"Testando Criação de Usuário({email}) - --")
    payload_create = {
        "email": email,
        "senha": senha,
        "nome": nome
    }
    response = requests.post(f"{BASE_URL}/auth/criar-usuario", json=payload_create)
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    assert response.status_code == 201

    # 2. Testar Login
    print("Testando Login ")
    payload_login = {
        "email": email,
        "senha": senha
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=payload_login)
    print(f"Status: {response.status_code}")
    login_data = response.json()
    print(f"Resposta: {login_data}")
    assert response.status_code == 200
    assert "access_token" in login_data
    assert "refresh_token" in login_data

    access_token = login_data["access_token"]
    refresh_token = login_data["refresh_token"]

    # 3. Testar Refresh Token
    # Na implementação atual, o endpoint /refresh aceita um token válido via Bearer
    print(" Testando Refresh Token ")
    headers = {
        "Authorization": f"Bearer {refresh_token}"
    }
    response = requests.get(f"{BASE_URL}/auth/refresh", headers=headers)
    print(f"Status: {response.status_code}")
    refresh_data = response.json()
    print(f"Resposta: {refresh_data}")
    assert response.status_code == 200
    assert "access_token" in refresh_data

    print(f"✅ Todos os testes de autenticação passaram!")

    if __name__ == "__main__":
        try:
            test_fluxo_autenticacao()
        except requests.exceptions.ConnectionError:
            print(
                f" ❌ Erro: O servidor não está rodando Inicie o FastAPI com 'uvicorn main:app --reload'antes de rodar os testes.")
        except AssertionError as e:
            print(f"❌ Falha no teste: {e} ")
        except Exception as e:
            print(f" ❌ Ocorreu umerro inesperado: {e} ")
