from fastapi import FastAPI
from pydantic import BaseModel
import jwt

app = FastAPI()

# Modelo de dados para receber o token
class TokenValidationResponse(BaseModel):
    token: str

# Função para verificar se um número é primo
def is_prime(n):
    """Função para verificar se um número é primo."""
    if n <= 1:
        return "falso"
    if n <= 3:
        return "verdadeiro"
    if n % 2 == 0 or n % 3 == 0:
        return "falso"
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return "falso"
        i += 6
    return "verdadeiro"

# Endpoint
@app.post("/validate_token", response_model=TokenValidationResponse)
def validate_token_endpoint(token: str):
    response = validar_token(token)
    return response

def validar_token(token):
    try:
        # Decodifica o token JWT sem verificar a assinatura
        payload = jwt.decode(token, options={"verify_signature": False})
        
        # Verifica se há exatamente 3 claims
        if set(payload.keys()) != {"Name", "Role", "Seed"}:
            return {"is_valid": "falso"}
        
        # Valida o tamanho da claim Name
        name = payload.get("Name")
        if not isinstance(name, str) or len(name) > 256:
            return {"is_valid": "falso"}
        if any(char.isdigit() for char in name):
            return {"is_valid": "falso"}
        
        # Valida a claim Role
        role = payload.get("Role")
        if role not in ["Admin", "Member", "External"]:
            return {"is_valid": "falso"}
        
        # Valida a claim Seed
        seed = payload.get("Seed")
        
        # Converter seed para inteiro
        try:
            seed = int(seed)
        except (ValueError, TypeError):
            return {"is_valid": "falso"}
        
        if not is_prime(seed):
            return {"is_valid": "falso"}
        
        # Se todas as validações passarem, retorna "verdadeiro"
        return {"is_valid": "verdadeiro"}
    except jwt.DecodeError:
        # Se o token não puder ser decodificado
        return {"is_valid": "falso"}
    except Exception as e:
        # Captura outras exceções
        return {"is_valid": "falso"}
