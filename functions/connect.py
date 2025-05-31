import requests
from os import path
import functions.security as descriptografar
from datetime import datetime
from time import sleep, time

paths = ["recived","result" ]

def conectar_api(link, id):
  link = f'{link}/{id}'
  links = [f'https://api-c783.onrender.com/Usuarios/{id}', f'https://api-c783.onrender.com/Produtos/{id}', f'https://api-c783.onrender.com/Funcionarios/{id}']
  if link in links:
    requisition = requests.get(link)
    if link == links[0]:
      with open(path.join(paths[0], "recived.txt"), 'w', encoding='utf-8') as arquivo:
        arquivo.write(f'{requisition.json()}')
      with open(path.join(paths[1], "result.txt"), 'w', encoding='utf-8') as arquivo:
        dicionario = requisition.json()
        arquivo.write(f'''```
ID: {dicionario['id']}
NOME: {descriptografar.descriptografar(dicionario['nome'])}
IDADE: {dicionario['idade']}
CPF: {descriptografar.descriptografar(dicionario['cpf'])}
GMAIL: {descriptografar.descriptografar(dicionario['gmail'])}
ANO DE NASCIMENTO: {dicionario['ano']}
```''')
        return 'CONECTADO'
    if link == links[2]:
      with open(path.join(paths[0], "recived.txt"), 'w', encoding='utf-8') as arquivo:
        arquivo.write(f'{requisition.json()}')
      with open(path.join(paths[1], "result.txt"), 'w', encoding='utf-8') as arquivo:
        dicionario = requisition.json()
        arquivo.write(f'''```
ID: {dicionario['id']}
NOME: {descriptografar.descriptografar(dicionario['nome'])}
SALÁRIO: R$:{dicionario['salário']}
SALDO: {dicionario['saldo']}
CPF: {descriptografar.descriptografar(dicionario['cpf'])}
USUÁRIO: {descriptografar.descriptografar(dicionario['usuario'])}
SENHA: {descriptografar.descriptografar(dicionario['senha'])}
```''')
        return 'CONECTADO'
    if link == links[1]:
      with open(path.join(paths[0], "recived.txt"), 'w', encoding='utf-8') as arquivo:
        arquivo.write(f'{requisition.json()}')
      with open(path.join(paths[1], "result.txt"), 'w', encoding='utf-8') as arquivo:
        dicionario = requisition.json()
        arquivo.write(f'''```
ID: {dicionario['id']}
NOME: {descriptografar.descriptografar(dicionario['nome'])}
PREÇO: R$:{dicionario['preço']}
```''')
        return 'CONECTADO'
  else:
    return "ERRO"