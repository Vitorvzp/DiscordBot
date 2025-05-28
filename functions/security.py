import json
from cryptography.fernet import Fernet

# Caminhos dos arquivos
CAMINHO_CHAVE = "functions\key.key"
CAMINHO_CRIPTO = "functions\cripto.enc"
CAMINHO_DESCRIPTO = "functions\descripto.enc"

def carregar_dicionario(caminho_arquivo: str, chave: bytes) -> dict:
    fernet = Fernet(chave)
    with open(caminho_arquivo, "rb") as f:
        dados_encriptados = f.read()
    dados_json = fernet.decrypt(dados_encriptados)
    return json.loads(dados_json.decode())

# Carregar a chave
with open(CAMINHO_CHAVE, "rb") as f:
    chave = f.read()

# Carregar dicionários criptografado e descriptografado
DIC_CRIPTO = carregar_dicionario(CAMINHO_CRIPTO, chave)
DIC_DESCRIPTO = carregar_dicionario(CAMINHO_DESCRIPTO, chave)

# Função de criptografia
def criptografar(mensagem: str) -> str:
    return ''.join(DIC_CRIPTO.get(letra, letra) for letra in mensagem)

# Função de descriptografia
def descriptografar(mensagem: str) -> str:
    return ''.join(DIC_DESCRIPTO.get(letra, letra) for letra in mensagem)
