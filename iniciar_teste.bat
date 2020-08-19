:: Insira abaixo a URL de seu banco de dados
:: Exemplo: postgres://usuario:senha@host:porta/starwars_api_db


@SET DATABASE_URL=postgres://postgres:postgres@localhost:5432/starwars_api_db



@SET PYTHONPATH=%CD%\src

@IF EXIST venv (
  @CALL "%CD%\venv\Scripts\"deactivate.bat
)

@ECHO ##### Criando o ambiente virtual #####

@python -m venv --clear venv

@ECHO ##### Iniciando variaveis de API #####

@CALL "%CD%\venv\Scripts\"activate.bat

@pip3 install wheel && @pip install -r requirements.txt 

@IF NOT EXIST migrations (

  @ECHO ##### Realizando migracoes de banco de dados #####

  @python manage.py db init && @python manage.py db migrate && @python manage.py db upgrade
)

@ECHO ##### Iniciando Testes #####

@python test.py

@CALL "%CD%\venv\Scripts\"deactivate.bat

@ECHO ##### Testes Concluidos #####