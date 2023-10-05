#### TODO: details on FE. add qantity into product




#### SETUP


#### crear entorno virtual (1° vez):


```bash
python -m venv env
```




#### activar entorno virtual (1° y cada vez que se inicie el servidor):
```bash
source env/Scripts/activate
```


#### instalar dependencias (1° vez):
``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```


#### realizar migraciones en la base de datos (1° vez):
```bash
py manage.py makemigrations users ecommerce
py manage.py migrate
```


#### crear super usuario (1° vez)
``` bash
py manage.py createsuperuser
```








#### iniciar el servidor
``` bash
py manage.py runserver
```




#### acceder al panel de administración en el navegador:
http://127.0.0.1:8000/admin/















