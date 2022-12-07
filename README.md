# instatus-bdd

## Sobre o projeto
Implementação dos testes automatizados de um sistema dentro do contexto BDD.
Os cenários são gerados automaticamente através de software, chamado [Skyfire](https://github.com/mdsol/skyfire). 
Os cenários dizem respeito a um modelo de maquina de estado, criado para representar o comportamento do sistema.

O sistema em questão é uma API, do sistema [Instatus](https://instatus.com/help/api).

## Instalação
Execute o seguinte comando para instalar as dependências do projeto:

```sh
$ pip install -r requirements.txt
```

## Execução
Após executar a instalação das dependências, rode o seguinte comando para executar os testes automatizados:

```sh
$ behave
```