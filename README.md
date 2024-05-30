# Comunidad Conectada

Este es un proyecto de Django diseñado para crear una plataforma de comunidad en línea. Proporciona características como autenticación de usuarios, una API RESTful, integración con PostgreSQL, integración de pagos con Transbank SDK y generación de informes con ReportLab.

## Instalación

Sigue estos pasos para configurar el entorno de desarrollo:

1. **Actualizar pip:**
    ```bash
    python -m pip install --upgrade pip
    ```

2. **Instalar o actualizar virtualenv:**
    ```bash
    pip install --upgrade virtualenv
    ```

3. **Navegar al directorio de proyectos Django:**
    ```bash
    cd /D "C:\ProyectosDjango"
    ```

4. **Crear un nuevo proyecto Django llamado `comunidad_conectada`:**
    ```bash
    django-admin startproject comunidad_conectada
    ```

5. **Ingresar al directorio del proyecto:**
    ```bash
    cd comunidad_conectada
    ```

6. **Crear un entorno virtual llamado `venv`:**
    ```bash
    python -m venv venv
    ```

7. **Activar el entorno virtual:**
    ```bash
    venv\Scripts\activate.bat
    ```

8. **Actualizar pip dentro del entorno virtual:**
    ```bash
    python -m pip install --upgrade pip
    ```

9. **Instalar los paquetes necesarios:**
    ```bash
    pip install django pillow djangorestframework psycopg2-binary transbank-sdk reportlab
    ```

10. **Crear dos nuevas aplicaciones Django llamadas `core` y `apirest`:**
    ```bash
    python manage.py startapp core
    python manage.py startapp apirest
    ```

11. **Guardar los requisitos instalados en un archivo `requirements.txt`:**
    ```bash
    pip freeze > requirements.txt
    ```

12. **Abrir el proyecto en tu editor de código preferido:**
    ```bash
    code .
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