from fastapi.testclient import TestClient
from backendchallenge.main import backendchallenge

client = TestClient(backendchallenge)

def test_validate_token_valid():
    # Gerar um token válido para o teste
    import jwt

    payload = {
        "Name": "UsuarioValido",
        "Role": "Member",
        "Seed": 17
    }

    token = jwt.encode(payload, key=None, algorithm=None)

    response = client.post("/validate_token", json={"token": token})
    assert response.status_code == 200
    assert response.json() == {"is_valid": True}

def test_validate_token_invalid_name():
    # Token com Name inválido (contém números)
    import jwt

    payload = {
        "Name": "Usuario123",
        "Role": "Member",
        "Seed": 17
    }

    token = jwt.encode(payload, key=None, algorithm=None)

    response = client.post("/validate_token", json={"token": token})
    assert response.status_code == 200
    assert response.json() == {"is_valid": False}

def test_validate_token_invalid_role():
    # Token com Role inválido
    import jwt

    payload = {
        "Name": "UsuarioValido",
        "Role": "InvalidRole",
        "Seed": 17
    }

    token = jwt.encode(payload, key=None, algorithm=None)

    response = client.post("/validate_token", json={"token": token})
    assert response.status_code == 200
    assert response.json() == {"is_valid": False}

def test_validate_token_invalid_seed():
    # Token com Seed não primo
    import jwt

    payload = {
        "Name": "UsuarioValido",
        "Role": "Member",
        "Seed": 16  # 16 não é primo
    }

    token = jwt.encode(payload, key=None, algorithm=None)

    response = client.post("/validate_token", json={"token": token})
    assert response.status_code == 200
    assert response.json() == {"is_valid": False}

def test_validate_token_missing_claims():
    # Token com claims faltando
    import jwt

    payload = {
        "Name": "UsuarioValido",
        "Role": "Member"
        # "Seed" está faltando
    }

    token = jwt.encode(payload, key=None, algorithm=None)

    response = client.post("/validate_token", json={"token": token})
    assert response.status_code == 200
    assert response.json() == {"is_valid": False}

def test_validate_token_extra_claims():
    # Token com claims extras
    import jwt

    payload = {
        "Name": "UsuarioValido",
        "Role": "Member",
        "Seed": 17,
        "ExtraClaim": "ExtraValue"
    }

    token = jwt.encode(payload, key=None, algorithm=None)

    response = client.post("/validate_token", json={"token": token})
    assert response.status_code == 200
    assert response.json() == {"is_valid": False}

def test_validate_token_invalid_token():
    # Token inválido (não é um JWT)
    token = "token_invalido"

    response = client.post("/validate_token", json={"token": token})
    assert response.status_code == 200
    assert response.json() == {"is_valid": False}