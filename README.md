# Comunidad Conectada

Este es un proyecto de Django diseñado para crear una plataforma de comunidad en línea. Proporciona características como autenticación de usuarios, una API RESTful, integración con PostgreSQL, integración de pagos con Transbank SDK y generación de informes con ReportLab.

## Instrucción para abrir el repositorio en VSCode

Sigue estos pasos para abrir el repositorio en VSCode:

1. **Clona el repositorio:** Abre tu terminal y ejecuta el siguiente comando para clonar el repositorio en tu máquina local:
    ```bash
    git clone https://github.com/Shiroyasha1997/comunidad_conectada.git
    ```

2. **Abre el repositorio en VSCode:** Navega hasta el directorio del repositorio clonado y abre VSCode desde la terminal usando el siguiente comando:
    ```bash
    code .
    ```

3. **Explora el proyecto:** Una vez abierto en VSCode, podrás explorar y editar el proyecto según sea necesario.

## Instalación desde Cero

Sigue estos pasos para configurar el entorno de desarrollo:

**Ejecutar este Script dentro de tu CMD para la creación de la base del proyecto:**
```bash
python -m pip install --upgrade pip
pip install --upgrade virtualenv
call cd /D "C:\ProyectosDjango"
call django-admin startproject comunidad_conectada
call cd comunidad_conectada
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install django
pip install pillow
pip install djangorestframework
pip install psycopg2-binary
pip install transbank-sdk
pip install reportlab
python manage.py startapp core
python manage.py startapp apirest
pip freeze > requirements.txt
call code .
```

## Contribución

¡Las contribuciones son bienvenidas! Si deseas contribuir a este proyecto, sigue estos pasos:

1. Hacer un fork del repositorio.
2. Crear una nueva rama (`git checkout -b feature/feature-name`).
3. Realizar tus cambios y hacer commits (`git commit -am 'Add new feature'`).
4. Hacer push a la rama (`git push origin feature/feature-name`).
5. Crear un nuevo Pull Request.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.