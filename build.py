import os
import subprocess
import sys
import shutil
import platform

def build_app():
    print("Iniciando o processo de build do Catálogo de Filmes...")
    
    # Detecta o sistema operacional
    sistema = platform.system()
    print(f"Sistema operacional detectado: {sistema}")
    
    # 1. Instala as dependências
    print("Instalando dependências...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # 2. Define o nome do executável conforme o sistema
    if sistema == "Windows":
        exe_name = "catalogo_app.exe"
    else:
        exe_name = "catalogo_app"
    
    # 3. Executa o PyInstaller
    print("Empacotando com PyInstaller (Isso pode levar alguns minutos)...")
    # --onefile: cria um único executável
    # --noconsole: não abre a janela preta do terminal (opcional, remova se quiser ver os logs)
    # --add-data: garante que a pasta templates vá junto
    # --name: define o nome do executável
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller", "--onefile", "--noconsole",
        "--name", "catalogo_app",
        "--add-data", f"templates{os.pathsep}templates",
        "app.py"
    ])
    
    # 4. Renomeia no Windows para .exe (PyInstaller adiciona extensão automaticamente em Windows)
    if sistema == "Windows":
        exe_final = os.path.join("dist", exe_name)
    else:
        exe_final = os.path.join("dist", "catalogo_app")
    
    # 5. Limpa arquivos temporários desnecessários
    print("Limpando arquivos temporários...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("catalogo_app.spec"):
        os.remove("catalogo_app.spec")
        
    print("\n" + "="*50)
    print("BUILD CONCLUÍDO COM SUCESSO!")
    print(f"O executável está na pasta: {os.path.abspath(exe_final)}")
    if sistema == "Windows":
        print("Você pode mover esse 'catalogo_app.exe' para qualquer computador Windows e dar dois cliques para abrir!")
    elif sistema == "Darwin":
        print("Você pode mover esse 'catalogo_app' para qualquer Mac e dar dois cliques para abrir!")
    else:
        print("Você pode mover esse 'catalogo_app' para qualquer Linux e executar via terminal: ./catalogo_app")
    print("="*50)

if __name__ == '__main__':
    build_app()
