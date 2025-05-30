import requests
from os import path
import functions.security
from datetime import datetime
from time import sleep, time

paths = ["result", "recived"]

def conectar_api(link):
  requisition = requests.get(link)
  if str(requisition) == '<Response [200]>':
    with open(path.join(paths[1], "recived.txt"), 'w', encoding='utf-8') as escrever:
     escrever.write(f'{requisition.json()}')
    if link == 'https://api-c783.onrender.com/Usuarios':
      with open(path.join(paths[0], "result.txt"), 'w', encoding='utf-8') as escrever:
        lines = requisition.json().split('\n')
        for linha in lines:
          campos = linha.split(',')
          id = campos[0].strip()
          nome = campos[1].strip()
          idade = campos[2].strip()
          gmail = campos[3].strip()
          escrever.write(f'{id},{functions.security.descriptografar(nome)},{idade},{functions.security.descriptografar(gmail)}\n')
    else:
      with open(path.join(paths[0], "result.txt"), 'w', encoding='utf-8') as escrever:
        lines = requisition.json().split('\n')
        id = 0
        for linha in lines:
          id += 1
          campos = linha.split(',')
          nome = campos[0].strip()
          escrever.write(f'ID:{id}, NOME: {functions.security.descriptografar(nome)}\n')
    return 'API CONECTADA'
  else:
    return 'API NÃO CONECTADA'

if __name__ == '__main__':
  pass