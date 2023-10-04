#### GUIA DE SET UP

#### Crear entorno virtual (1° vez):

```bash
python -m venv env
```


### ACTIVAR ENTORNO VIRTUAL (1° Y CADA VEZ QUE SE INICIE EL SERVIDOR):
en linux o git bash:
```bash
source env/Scripts/activate
```

### INSTALAR DEPENDENCIAS (1° vez):
``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### REALIZAR MIGRACIONES EN LA BASE DE DATOS (1° vez):
```bash
py manage.py makemigrations users ecommerce
py manage.py migrate
```

### CREAR SUPER USUARIO (1° vez)
``` bash
py manage.py createsuperuser
```




### INICIAR EL SERVIDOR
``` bash
py manage.py runserver
```


### ACCEDER AL PANEL DE ADMINISTRACIÓN EN EL NAVEGADOR: 
http://127.0.0.1:8000/admin/






