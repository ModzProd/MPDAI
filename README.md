# Catálogo de Filmes e Séries — Software Desktop Offline

Aplicação desktop 100% offline para gerenciar seu catálogo pessoal de filmes, séries e documentários. Funciona no Windows, macOS e Linux.

## Recursos

- Cadastro de obras com título, tipo, ano, sinopse, status e URL da capa
- Múltiplos gêneros por obra (8 gêneros padrão pré-cadastrados)
- Busca por título em tempo real
- Edição e exclusão de obras
- Banco de dados SQLite embutido (sem servidor)
- Gera um único executável portável

## Stack

- Python 3
- Flask (servidor web local)
- SQLite (banco offline)
- PyInstaller (empacotamento)
- Bootstrap 5 (interface)

## Como rodar o projeto em modo desenvolvimento

```bash
cd catalogo_app
pip install -r requirements.txt
python app.py
```

Acesse no navegador: http://127.0.0.1:5000

## Como gerar o executável portável

```bash
cd catalogo_app
python build.py
```

O executável final será gerado em `catalogo_app/dist/catalogo_app` (Linux/Mac) ou `catalogo_app/dist/catalogo_app.exe` (Windows).

## Como usar o executável final

1. Copie o arquivo gerado para qualquer computador com Windows/Mac/Linux
2. Dê dois cliques (ou execute `./catalogo_app` no Linux/Mac via terminal)
3. O navegador padrão abrirá automaticamente em http://127.0.0.1:5000
4. O banco de dados SQLite será criado automaticamente na mesma pasta do executável

**Observação:** O executável só funciona no mesmo sistema operacional onde foi gerado. Para gerar `.exe` Windows, rode o `build.py` em um Windows com Python 3 instalado, ou use o workflow do GitHub Actions incluído (`.github/workflows/build-windows.yml`).

## Estrutura do projeto

```
catalogo_app/
├── app.py                     # Backend Flask + SQLite
├── build.py                   # Script PyInstaller para gerar executável
├── requirements.txt           # Dependências
├── README.md                  # Este arquivo
├── .github/
│   └── workflows/
│       └── build-windows.yml  # CI para gerar .exe Windows automaticamente
└── templates/
    ├── index.html             # Página principal (lista + adicionar)
    └── editar.html            # Tela de edição
```

## Gerar .exe Windows via GitHub Actions (sem precisar de Windows)

1. Crie um repositório no GitHub e suba toda a pasta `catalogo_app/`
2. Vá em Actions → "Build Windows EXE" → Run workflow
3. Quando terminar, faça download do artefato `catalogo_app-windows-exe.zip`
4. Descompacte e use o `catalogo_app.exe` em qualquer Windows

## Persistência de dados

O banco SQLite (`catalogo_database.db`) é criado automaticamente na mesma pasta do executável ao rodar pela primeira vez. Para backup, basta copiar esse arquivo. Para resetar, basta apagá-lo — o sistema recriará com os gêneros padrão na próxima execução.
