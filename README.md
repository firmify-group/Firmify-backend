# Firmify

## Clonar repositorio

1) Clonar repositorio

```
git clon https://github.com/DaniAlejandro1/Firmify.git
```

2) Entrar en directorio /Firmify
3) Iniciar gitflow
```
git flow init
```

## Instalar entorno

1) Crear un entorno virtual
En este paso se presupone que cuenta con las dependecias de python instaladas en su maquina.:
```
python3 -m venv .venv
```

2) Activar el entorno virtual
Linux (bash):
```
source .venv/bin/activate
```
3)   Windows (PowerShell):

```
.\.venv\Scripts\activate
```

4) Instalar las dependencias necesarias
Linux y Windows:
```
pip install -r requirements.txt
```

5) Ejecutar el servidor del backend
Linux y Windows:
```
uvicorn main:app --reload
```