# markov.law

## Links
* https://github.com/fasfsfgs/cnj-inova.git
* https://www.youtube.com/watch?v=LJ4-jOPDdG8

## Arquivos do projeto
* `docs/logo_marcovlaw.jpeg`
* `docs/metodologia_markovlaw.pdf`

## Descrição do projeto
Sistema basedo nas cadeias de Markov que melhora eficiência na identificação e gestão de potenciais anomalias das movimentações processuais.

É essencial a leitura da metodologia `docs/metodologia_markovlaw.pdf`.

## Instruções para execução da aplicação
A solução utiliza a linguagem Python.
As dependências estão explicitadas no arquivo `requirements.txt` conforme boas práticas.

Obs.: os arquivos JSONs fornecidos para o desafio não foram salvos no GitHub.

1. Baixar os arquivos fornecidos no GitHub;

2. Instalar as dependências explicitadas no `requirements.txt`;

3. Colocar na pasta `data` os JSONs contendo os processos que devem ser analisados;
Esse passo pode demorar dependendo do volume de dados analisados.

4. Executar o arquivo `src/processar_dados.py`;
A análise dos processos fornecidos em JSON é realizada nesse passo.
Ao final, os arquivos `lista_movimentos.csv` e `lista_movimentos.json` são criados na pasta raíz do projeto para ser utilizado pelo frontend.

5. Executar o arquivo `application.py`;
Uma aplicação web (utilizando Flask) é executada.

6. Abrir o endereço `http://localhost:5000/` para entrar na aplicação.
