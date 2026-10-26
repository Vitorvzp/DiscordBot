# DiscordBot · Python

> **Escopo deste rascunho:** este PR inclui somente código, documentação e testes. As remoções de arquivos privados do índice foram preparadas apenas no commit local e não estão incluídas aqui, para evitar sua exposição no diff. Os arquivos legados continuam rastreados nesta branch remota e no histórico até uma etapa específica.

Bot Discord com comandos de chat, integração com Gemini, consultas a uma API e dicionários legados de substituição de caracteres. Usa discord.py, Google Gen AI, SQLModel/SQLite e requests. O comportamento e as permissões dos comandos estão em `main.py`.

## Estrutura

- `main.py`: comandos e inicialização do bot.
- `database.py`: armazenamento do histórico de chat.
- `functions/connect.py`: integração HTTP e arquivos de resposta.
- `functions/security.py`: carregamento sob demanda dos dicionários privados.
- `runtime_paths.py`: caminhos externos de dados e chaves.
- `tests/`: testes isolados com dados sintéticos e HTTP simulado.

## Desenvolvimento local

Crie um ambiente virtual e instale `requirements.txt`. Antes de executar `python main.py`, configure estas variáveis no ambiente ou em um `.env` local ignorado pelo Git:

| Variável | Uso |
| --- | --- |
| `DISCORDBOT_DATA_DIR` | Diretório absoluto fora do checkout para SQLite e respostas. Obrigatório para iniciar. |
| `DISCORDBOT_KEY_FILE` | Chave Fernet em arquivo absoluto fora do checkout. Obrigatória para usar os dicionários. |
| `DISCORDBOT_CRIPTO_FILE` | Dicionário cifrado de substituição em arquivo externo. |
| `DISCORDBOT_DESCRIPTO_FILE` | Dicionário inverso cifrado em arquivo externo. |
| `TOKEN` | Token do bot Discord. |
| `API_GEMINI` | Chave da integração Gemini. |

O banco fica em `DISCORDBOT_DATA_DIR/database.db`; respostas recebidas e formatadas ficam nos subdiretórios `recived/` e `result/` desse diretório. Os diretórios necessários são criados sob o caminho configurado; arquivos privados existentes não são copiados nem migrados automaticamente. Caminhos relativos ou dentro deste checkout são recusados. Configuração ausente interrompe a operação correspondente, sem usar arquivos antigos do repositório.

Os dicionários são carregados somente na primeira operação e mantidos em memória até reiniciar. A substituição de caracteres é um mecanismo legado e não equivale à criptografia adequada de dados ou ao hashing de senhas.

## Testes sem serviços externos

Com `cryptography`, `sqlmodel` e `requests` instalados no ambiente virtual:

```sh
python -m unittest discover -s tests -v
```

Os testes usam chave efêmera, dicionários inventados, SQLite temporário e HTTP simulado. Não executam o bot, não conectam a Discord/Gemini/API e não usam arquivos pessoais.

## Estado de segurança

No preparo local, chave, dicionários cifrados, SQLite, respostas e caches foram retirados apenas do índice Git, com as cópias em disco preservadas. Esta branch remota contém somente código, documentação e testes: os arquivos legados continuam rastreados nela e no histórico. O .gitignore cobre esses padrões, mas não remove entradas já rastreadas. Isso não apaga o histórico nem invalida material já exposto. Rotação de chaves, avaliação de dados expostos, migração e eventual limpeza de histórico exigem uma etapa específica; não foram executadas por esta alteração.

Os comandos ainda podem solicitar dados sensíveis à API e enviá-los a canais Discord; a configuração dos canais, as permissões e o tratamento desses dados precisam de revisão separada antes de uso real. Esta alteração trata o armazenamento local e não altera servidores, chaves, permissões, configurações de acesso ou produção.

## Autoria e licença

A autoria e o histórico existentes foram preservados. O checkout atual não contém arquivo `LICENSE`; este README não atribui uma licença ausente.
