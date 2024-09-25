## Projeto backend-challenge: Validador de Tokens JWT com FastAPI
## Descrição
Este projeto é uma API desenvolvida com FastAPI para validar tokens JWT. A API verifica a estrutura e o conteúdo do token, garantindo que ele contenha exatamente três claims: Name, Role e Seed. Além disso, realiza validações específicas para cada claim, como o tamanho do nome de ate 256 caracteres e formato do Name no qual não pode ter números, a integridade do Role e a Seed no qual valida se é número Primo.
Recomendando esta na versão do Python 3.9 ou seperior [Link da biblioteca python](https://docs.python.org/3.9/)

## Instalação e Execução de aplicação

1 - Clone o Repositório:
```bash
git clone https://github.com/gustavorsilva/application-backend-challenge
cd application-backend-challenge
```
2 - Ambiente Linux:
```bash
cd application-backend-challenge/backendchallenge
```
execute os seguinte comandos:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
em seguida a aplicação esta disponivel no browser no endereço:http://127.0.0.1:8000/docs ou prompt de comando: 
curl -X POST "http://127.0.0.1:80/validate_token" \
-H "Content-Type: application/json" \
-d '{"token": "insira deu token"}'