from fastapi import FastAPI
from pydantic import BaseModel
import jwt
import logging

# Configuração básica do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# Logger para o aplicativo
logger = logging.getLogger("app")

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
        logger.debug(f"Payload decodificado: {payload}")

        # Verifica se há mais de 3 claims
        if len(payload) > 3:
            logger.warning("Abrindo o JWT, foi encontrado mais de 3 claims.")
            return {"is_valid": "falso"}

        # Verifica se há exatamente 3 claims
        if set(payload.keys()) != {"Name", "Role", "Seed"}:
            return {"is_valid": "falso"}
    
        #Valida o tamanho da claim Name
        name = payload.get("Name")
        if not isinstance(name, str) or len(name) > 256:
            logger.warning("A claim 'Name é inválida' verificar tipo ou tamanho).")
            return {"is_valid": "falso"}
        if any(char.isdigit() for char in name):
            logger.warning("Abrindo o JWT, a Claim Name possui caracter de números.")
            return {"is_valid": "falso"}        
        
        # Valida a claim Seed
        seed = payload.get("Seed")

        # Valida a claim Role
        role = payload.get("Role")
        if role not in ["Admin", "Member", "External"]:
            logger.warning("A claim 'Role' contém um valor inválido.")
            return {"is_valid": "falso"}
        
        # Converter seed para inteiro
        try:
            seed = int(seed)
            logger.debug(f"Claim 'Seed' convertida para inteiro: {seed}")
        except (ValueError, TypeError):
            logger.warning("A claim 'Seed' não pôde ser convertida para inteiro.")
            return {"is_valid": "falso"}
        
        if not is_prime(seed):
            logger.warning("A claim 'Seed' não é um número primo.")
            return {"is_valid": "falso"}
        
        logger.info("Token válido.")
        # Se todas as validações passarem, retorna "verdadeiro"
        return {"is_valid": "verdadeiro"}
    
    except jwt.DecodeError:
        logger.error("JWT invalido.")
        return {"is_valid": "falso"}
    except Exception as e:
        logger.exception(f"Ocorreu um erro inesperado: {e}")
        return {"is_valid": "falso"}
