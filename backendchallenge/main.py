from fastapi import FastAPI
from pydantic import BaseModel
import jwt

app = FastAPI()

# Modelo de dados para receber o token
class Token(BaseModel):
    token: str

# Função para verificar se um número é primo
def is_prime(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

# Endpoint
@app.post("/validate_token")
def validate_token(token_data: Token):
    token = token_data.token
    try:
        # Decodifica o token JWT sem verificar a assinatura
        payload = jwt.decode(token, options={"verify_signature": False})
        
        # Verifica se há exatamente 3 claims
        if set(payload.keys()) != {"Name", "Role", "Seed"}:
            return {"is_valid": False}
        
        # Valida o tamanho da claim Name
        name = payload.get("Name")
        if not isinstance(name, str) or len(name) > 256:
            return {"is_valid": False}
        if any(char.isdigit() for char in name):
            return {"is_valid": False}
        
        # Valida a claim Role
        role = payload.get("Role")
        if role not in ["Admin", "Member", "External"]:
            return {"is_valid": False}
        
        # Valida a claim Seed
        seed = payload.get("Seed")
        
        # converter seed para inteiro
        try:
            seed = int(seed)
        except (ValueError, TypeError):
            return {"is_valid": False}
        
        if not is_prime(seed):
            return {"is_valid": False}
        
        # Se todas as validações passarem, retorna True
        return {"is_valid": True}
    except jwt.DecodeError:
        # Se o token não puder ser decodificado
        return {"is_valid": False}
    except Exception as e:
        # Captura outras exceções
        return {"is_valid": False}
