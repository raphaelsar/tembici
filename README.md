# TEMBICI

### Importante ###
Para os passos seguintes, estou considerando que a maquina onde serão executados os comandos tem o docker instalado,
caso não tenha, nesse link estão todos os passos para instalação: https://docs.docker.com/install/.
É importante usar docker, pois assim garantimos que independente do SO usado, o ambiente será exatamente igual.

### Preparando a imagem docker manualmente ###

```
git clone git@github.com:raphaelsar/tembici.git
cd tembici
  docker build -t tembici .
```

### Executando testes unitários ###
```
docker run -it tembici make run
```

