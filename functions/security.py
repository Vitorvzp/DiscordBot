"""Legacy substitution dictionaries; private material is loaded only on use."""

from functools import lru_cache
import json

from cryptography.fernet import Fernet, InvalidToken

from runtime_paths import ENV_PREFIX, private_file


def carregar_dicionario(caminho_arquivo, chave: bytes) -> dict:
    dados_json = Fernet(chave).decrypt(caminho_arquivo.read_bytes())
    dicionario = json.loads(dados_json.decode("utf-8"))
    if not isinstance(dicionario, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in dicionario.items()
    ):
        raise ValueError("Invalid dictionary format.")
    return dicionario


@lru_cache(maxsize=1)
def _dicionarios():
    # Validate every path before opening any private material.
    chave_path = private_file(f"{ENV_PREFIX}_KEY_FILE")
    cripto_path = private_file(f"{ENV_PREFIX}_CRIPTO_FILE")
    descripto_path = private_file(f"{ENV_PREFIX}_DESCRIPTO_FILE")
    try:
        chave = chave_path.read_bytes()
        return (
            carregar_dicionario(cripto_path, chave),
            carregar_dicionario(descripto_path, chave),
        )
    except (OSError, ValueError, InvalidToken):
        raise RuntimeError("Unable to load configured private dictionaries.") from None


def criptografar(mensagem: str) -> str:
    dicionario, _ = _dicionarios()
    return ''.join(dicionario.get(letra, letra) for letra in mensagem)


def descriptografar(mensagem: str) -> str:
    _, dicionario = _dicionarios()
    return ''.join(dicionario.get(letra, letra) for letra in mensagem)
