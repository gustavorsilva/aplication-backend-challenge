## Projeto backend-challenge: Validador de Tokens JWT com FastAPI
## Descrição
Este projeto é uma API desenvolvida com FastAPI para validar tokens JWT. A API verifica a estrutura e o conteúdo do token, garantindo que ele contenha exatamente três claims: Name, Role e Seed. Além disso, realiza validações específicas para cada claim, como o tamanho do nome de ate 256 caracteres e formato do Name no qual não pode ter números e por final o seed no qual deve ser um número primo.
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
## Uso
em seguida a aplicação esta disponivel no browser no endereço:
```bash 
Swagger UI
http://127.0.0.1:8000/docs
```
 ou prompt de comando:
 ```bash  
curl -X POST "http://127.0.0.1:8000/validate_token" \ -H "Content-Type: application/json" \ -d '{"token": "insira deu token"}'
```
tambem pode ser validado utlizando ferramentas como (insomnia ou postman).

2.1 - Ambiente Windows:
Recomendações: Instalação do Docker Desktop para execução do codigo.[Link para instalação do docker desktop](https://docs.docker.com/desktop/install/windows-install/)
Abra o arquivo com seu IDE de preferencia
```bash
cd application-backend-challenge/backendchallenge
```
Abra um terminal e execute os seguinte comandos:
Primeiro sera executado o build da aplicação
```bash
docker build -t jwt-api .
```
em seguida execute o comando sera montado a imagem no docker desktop:
```bash
docker run -d --name jwt-api -p 80:80 jwt-api 
```
## Uso
Com sua imagem ja sendo executado localmente, pode ser acessada localmente utilizando no browser no endereço:
```bash 
Swagger UI
http://127.0.0.1:80/docs
```
ou prompt de comando:
 ```bash  
curl -X POST "http://127.0.0.1:80/validate_token" \ -H "Content-Type: application/json" \ -d '{"token": "insira deu token"}'
```
tambem pode ser validado utlizando ferramentas como (insomnia ou postman).

## Como Utilizar localmente Insomnia ou outras ferramentas para execução de teste de api
- Insira o Curl completo na na URL clique em import, em seguida clique em send. Sua aplicação vai responder ao token
![Animação](https://github.com/user-attachments/assets/77b5fc61-e4ee-4e31-b842-d6af97d1b786)

## Endpoints da API
 ```bash
POST /validate_token
```
Valida um token JWT enviado no corpo da requisição.

Parâmetros
- Body: JSON contendo o token a ser validado.
```bash
{
  "token": "seu_token_jwt_aqui"
}
```
# Respostas
- Status Code:200(OK)  quando para verdadeiro ou para falso. O restante das informações estão no log da aplicação.
```json
{
  "is_valid": "verdadeiro"
}
```
ou
```json
{
  "is_valid": "falso"
}
```
## Exemplo de Requisição Válida
```bash
curl -X POST "http://127.0.0.1:80/validate_token" \
-H "Content-Type: application/json" \
-d '{"token": "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJTZWVkIjoiNzg0MSIsIk5hbWUiOiJUb25pbmhvIEFyYXVqbyJ9.QY05sIjtrcJnP533kQNk8QXcaleJ1Q01jWY_ZzIZuAg"}'
```
- Resposta
```bash
{
  "is_valid": "verdadeiro"
}
```
- Log
![alt text](imagereadme/imagem-2.png)

## Exemplo de Requisição Invalida
```bash
curl -X POST "http://127.0.0.1:80/validate_token" \
-H "Content-Type: application/json" \
-d '{"token": "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiTWVtYmVyIiwiT3JnIjoiQlIiLCJTZWVkIjoiMTQ2MjciLCJOYW1lIjoiVmFsZGlyIEFyYW5oYSJ9.cmrXV_Flm5mfdpfNUVopY_I2zeJUy4EZ4i3Fea98zvY"}'
```
- Resposta
```bash
{
  "is_valid": "falso"
}
```
- Log
![alt text](imagereadme/image-1.png)

## Níveis de log utilizados:
- INFO: Informações gerais sobre o funcionamento da aplicação.
- ERROR: Erros na validação do token.

## LOGS
- Foi utlizado o EKL (Elasticsearch, Kibana & Logstash) para coletar os Logging da aplicação e Monitoring
![alt text](imagereadme/ekl.png)


## CI/CD
Este repositório utiliza uma pipeline de CI/CD implementada com GitHub Actions para automatizar o processo de integração, teste, construção e implantação da aplicação. A seguir, descrevemos detalhadamente como a pipeline está configurada e como cada etapa funciona.

# Configuração Manifesto Kubernetes
Na rota infra/deployeks.yaml construido o manifesto Kubernetes que tem o deplolyment e o service.

# Jobs Pipeline
![alt text](imagereadme/esteira.png)

1. Build and Test:
Este job é responsável por compilar o código, instalar as dependências e executar os testes automatizados.

2. Build and Push to ECR:
Este job constrói a imagem Docker da aplicação e a envia para o Amazon Elastic Container Registry (ECR).

3. Deploy to Kubernetes:
Este job realiza a implantação da aplicação no cluster Kubernetes utilizando o Amazon EKS.
- Dentro dos steps vc consegue recuperar os valores dos Load Balancer quanto aplicação e Kibana, no campo *** informe a região
us-east-1 exemplo:
![alt text](imagereadme/loadbalancerurl.png)


# Segredos e Configurações
Para que a pipeline funcione corretamente, é necessário configurar os seguintes segredos no repositório do GitHub:

- AWS_ACCESS_KEY_ID:.
- AWS_SECRET_ACCESS_KEY:
- AWS_REGION:
- ECR_REPOSITORY: Nome do repositório no Amazon ECR onde as imagens Docker serão armazenadas.
- ECR_REGISTRY: URI do Amazon ECR. Exemplo: numerodacontaaws.dkr.ecr.regiao.amazonaws.com
- EKS_CLUSTER_NAME: Nome do cluster Amazon EKS onde a aplicação será implantada.

# Acessando a API após publicação no Kubernetes
- Acessando a pipeline acessando o workflow Deploy-To-Kubernetes no step "Endereço Load Balancar e Endereço Kibana" você tera
acesso as URL para testa API e outra para acessar os logs da API.

# Como realizar as chamadas:
- Via Browser vc pode jogar a URL do Load Balancar com a porta configurada. Exemplo:
```bash 
Swagger UI
http://http://a3cd5c4765f8a41399d1769fa1ca78b3-112773827.us-east-1.elb.amazonaws.com/docs
```
Acessando a URL no parametro { "token": "informe sua chave"} exemplo:
![alt text](imagereadme/urlexterno.png)

- Via Insomnia ou outras Ferramentas voce pode executar seguindo o Exemplo:
```bash
curl -X POST "http://http://http://a3cd5c4765f8a41399d1769fa1ca78b3-112773827.us-east-1.elb.amazonaws.com/validate_token" \
-H "Content-Type: application/json" \
-d '{"token": "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiTWVtYmVyIiwiT3JnIjoiQlIiLCJTZWVkIjoiMTQ2MjciLCJOYW1lIjoiVmFsZGlyIEFyYW5oYSJ9.cmrXV_Flm5mfdpfNUVopY_I2zeJUy4EZ4i3Fea98zvY"}'
```
Acessando a Insomnia no parametro { "token": "informe sua chave"} exemplo:



## Repositorios Infraestrutura
# Criação do EKS: [Link do Repositorio](https://github.com/gustavorsilva/backend-challenge-infra)

# Criação do ECR: [Link do Repositorio](https://github.com/gustavorsilva/backend-challenge-infra/tree/OpenTerraform)

