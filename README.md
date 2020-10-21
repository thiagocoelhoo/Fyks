# Fyks
O projeto Fyks é um software desenvolvido com foco em simulação de fenômenos físicos para sala de aula.
## Downloads
Os links para download estão disponíveis no site do projeto: https://rabbithy.github.io/Fyks/.
## Dependências 
- numpy
- pyglet
## Build (Windows)
1. Primeiro é necessário criar um clone do repositório. Clique no botão verde escrito "code" e baixe o arquivo .zip.
2. O segundo passo é instalar as dependencias do projeto. Para isto, execute o seguinte comando:
  ```
  pip install -r requirements.txt
  ```
3. Para realizar o build da aplicação, é necessário a instalação do pyinstaller executando o commando abaixo:
  ```
  pip install pyinstaller
  ```
4. Após a instalação do pyinstaller é necessário configurar as dependencias que serão usadas, caso haja alguma alteração. Para isso você deve alterar o aquivo "fyks.spec"
5. Depois de configurar todo o ambiente, rode o seguinte comando no cmd no diretório raiz do projeto:
  ```
  pyinstaller fyks.spec
  ```
