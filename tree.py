import os


def listar_estructura(ruta, nivel=0, ignorar=None):
    if ignorar is None:
        ignorar = {'__pycache__', '.git', 'venv',
                   'env', 'migrations', '.idea', '.vscode'}

    for archivo in sorted(os.listdir(ruta)):
        if archivo in ignorar:
            continue
        ruta_completa = os.path.join(ruta, archivo)
        print("│   " * nivel + "├── " + archivo)
        if os.path.isdir(ruta_completa):
            listar_estructura(ruta_completa, nivel + 1, ignorar)


if __name__ == "__main__":
    ruta_proyecto = "."  # raíz del proyecto
    listar_estructura(ruta_proyecto)
