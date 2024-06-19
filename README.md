# Comunidad Conectada

## Introducción
"Comunidad Conectada" es un proyecto de Django para crear una plataforma de comunidad en línea. Ofrece autenticación de usuarios, una API RESTful, integración de pagos con Transbank SDK y generación de informes con ReportLab.

## Requisitos
- Python 3.12 (o superior)
- pip
- virtualenv (opcional)
- Git
- Editor de código (VSCode recomendado)

## Configuración del Entorno de Desarrollo

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Shiroyasha1997/comunidad_conectada.git
cd comunidad_conectada
code .
```

### 2. Crear y Activar un Entorno Virtual (Opcional)
```bash
python -m venv env
source env/bin/activate  # En Windows use `env\Scripts\activate`
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos

La configuración predeterminada usa SQLite. Asegúrese de que settings.py tenga la siguiente configuración:

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 5. Aplicar Migraciones y Crear Superusuario
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Aplicar Migraciones y Crear Superusuario
```bash
python manage.py runserver
```

Abra http://127.0.0.1:8000/ en su navegador.

## Conclusion

Este README proporciona los pasos necesarios para configurar el entorno de desarrollo para "Comunidad Conectada" usando SQLite. Siguiendo estos pasos, podrá preparar su entorno y contribuir al proyecto.