# instatus-bdd

## Sobre o projeto
Implementação dos testes automatizados de um sistema dentro do contexto BDD.
Os cenários são gerados automaticamente através do projeto [ready-to-use-skyfire](https://github.com/leokoike/ready-to-use-skyfire) que se utiliza da ferramenta [Skyfire](https://github.com/mdsol/skyfire). 
Os cenários dizem respeito a um modelo de maquina de estado, criado para representar o comportamento do sistema.

O sistema em questão é uma API, do sistema [Instatus](https://instatus.com/help/api).

## Pré requisitos
Foi utilizada a versão 3.10 do python.
Para instalar essa versão em um environment isolado, é recomendado o uso do [pyenv](https://github.com/pyenv/pyenv).

## Instalação
Execute o seguinte comando dentro do seu environment para instalar as dependências do projeto:

```sh
$ pip install -r requirements.txt
```

## Execução
Após executar a instalação das dependências, rode o seguinte comando para executar todos os testes automatizados:

```sh
$ behave
```

Caso queria executar um arquivo .feature específico, basta executar o seguinte comando:

```sh
$ behave -i features/nome_arquivo.feature
```

