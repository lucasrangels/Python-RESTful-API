# Python RESTful API - Star Wars

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Exemplo de uma API RESTFul, com a inclusão de algumas operações de CRUD.
O serviço tem como objetivo guardar informações de planetas, buscando de forma dinâmica o número de aparições dos mesmos através de uma API dedicada para filmes de Star Wars (https://swapi.dev/).

# EndPoints

POST /api/v1/planetas - Cria um planeta(CREATE)

GET /api/v1/planetas - Buscar todos os planetas cadastrados(READ)

GET /api/v1/planetas/<nome> - Buscar um planeta por nome(READ)
    
PUT /api/v1/planetas - Atualiza informações de um planeta já cadastrado(UPDATE)

DELETE /api/v1/planetas - Exclui o cadastro de um planeta(DELETE)

# Pré-Requisitos

Python3.x - Linguagem padrão do projeto.

PostgreSQL - Banco de dados relacional.

# Deploy

Inicialmente certifique-se que o sistema possui os pré-requisitos instalados e, no caso do Python, com seus PATHS preenchidos corretamente.

### Crie uma base de dados
Crie uma base de dados com o nome starwars_api_db através de um gerenciador de banco de dados (PgAdmin, DBeaver, etc...).
Também é possível criar a partir de um terminal com o seguinte comando:

```sh
$ createdb starwars_api_db
```

# Iniciando a API
O projeto conta com um arquivo batch dedicado para iniciar o serviço, não necessitando de instalação de dependências ou migrações de banco de forma manual.
Inicie através do arquivo 'iniciar.bat' localizado na pasta raiz do projeto.


# Exemplos de Uso

As operações UPDATE, GET (por nome) e DELETE necessitam de uma entrada em formato JSON para realizar as alterações locais.

É necessário que o planeta exista no universo de Star Wars para que sua inserção seja possível através da API. Caso tenha dúvidas sobre
o nome dos planetas ou queira mais informações sobre os mesmos consulte o link abaixo:
```sh
https://pt.qwe.wiki/wiki/List_of_Star_Wars_planets_and_moons
```

Seguem abaixo exemplos de uso:

### Inserção 
```sh
{
    "nome": "Alderaan",
    "clima": "Temperado",
    "terreno": "Montanhoso"
}
```
Caso o planeta em questão já tenha sido cadastrado previamente no banco de dados o sistema retornará a seguinte mensagem:
```sh
{'Erro': 'Planeta inserido já está cadastrado'}
```
No entanto, caso a operação seja um sucesso o retorno será:
```sh
 {'Mensagem': 'Planeta cadastrado com sucesso!'}
 ```
 
### Exclusão
 A exclusão utiliza os mesmos parâmetros da inserção, tendo sua identificação a partir do nome do planeta.
```sh
{
    "nome": "Alderaan",
    "clima": "Temperado",
    "terreno": "Montanhoso"
}
```
Caso o planeta em questão não exista no banco de dados a mensagem será a seguinte:
```sh
'Erro': 'Não foi possível excluir o planeta pois o mesmo não está cadastrado.'}
```
No entanto, caso a operação seja um sucesso o retorno será:
```sh
{'Mensagem': 'Planeta excluído com sucesso!'}
 ```

### Buscar todos os planetas cadastrados
```sh
http://127.0.0.1:5000/api/v1/planetas/
```
 
### Busca por Nome e ID
A API possui busca de planetas cadastrados a partir de seu nome ou ID. A busca ocorre a partir da URL não sendo necessário uma entrada.
```sh
http://127.0.0.1:5000/api/v1/planetas/Tatooine
```
Ou no caso de uma ID:
```sh
http://127.0.0.1:5000/api/v1/planetas/7
```

### Atualização
A atualização utiliza o mesmo formato da inserção, porém a mesma realiza uma validação do nome para garantir que o planeta exista.
```sh
{
    "nome": "Alderaan",
    "clima": "Temperado",
    "terreno": "Montanhoso"
}
```
Caso o planeta em questão não exista no banco de dados a mensagem será a seguinte:
```sh
{'Erro': 'Não foi possível atualizar informações do planeta pois o mesmo não está cadastrado.'}
```
O retorno da operação será a própria entrada.


# Reiniciando o deploy
O deploy pode ser reiniciado em caso de inconsistências ou inputs errados por parte do usuário. Execute o passo a passo abaixo para fazê-lo:

- Exclusão da pasta MIGRATIONS e VENV no diretório raiz do projeto.
- Exclusão de todas as tabelas do banco de dados criado ou do próprio banco.
- Executar o arquivo 'iniciar.bat'.

Após as etapas explicitadas o serviço buscará novamente as dependências, realizando a migração e upgrade do banco de dados.
