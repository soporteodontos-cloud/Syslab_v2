# Syslab

Sistema web de gestión para laboratorio dental (órdenes de trabajo, pacientes, insumos, informes y usuarios) construido con Django.

## Stack

- **Backend:** Django 3.2 / Python 3
- **API:** Django REST Framework + DRF Datatables
- **Async / Tasks:** Celery + Redis, Django Channels + Daphne
- **Frontend:** Django Templates + Bootstrap 4 + Crispy Forms + DataTables + Select2 (django-autocomplete-light)
- **Auth:** Modelo custom (`users.CustomUsers`)
- **Otros:** django-simple-history, django-filter, django-multiselectfield, Firebase Admin, Google Cloud Storage

## Estructura del proyecto

```
syslab/
├── syslab/          # Configuración (settings, urls, wsgi, asgi, celery)
├── core/            # Catálogos (pacientes, insumos, marcas, categorías, ciudades, etc.)
├── ordenes/         # Órdenes de trabajo y retiros
├── informes/        # Reportes
├── users/           # Usuarios y autenticación
├── templates/       # Templates globales (menú, 403, registration)
├── static/          # Assets (bootstrap, jquery, datatables, select2, sb-admin-2)
├── media/           # Archivos subidos (ignorado en git)
├── manage.py
└── req.txt          # Dependencias
```

## Requisitos

- Python 3.8+
- Redis (para Celery y Channels)
- Base de datos configurada en `.env` (Django soporta PostgreSQL, MySQL, SQLite)

## Instalación

```powershell
# 1. Clonar
git clone https://github.com/soporteodontos-cloud/Syslab_v2.git
cd Syslab_v2

# 2. Entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Dependencias
pip install -r req.txt

# 4. Variables de entorno
# Editar el archivo .env con las credenciales locales

# 5. Migraciones
python manage.py migrate

# 6. Superusuario
python manage.py createsuperuser

# 7. Servidor de desarrollo
python manage.py runserver
```

## Servicios auxiliares

**Celery worker:**
```powershell
celery -A syslab worker -l info
```

**Celery beat (tareas programadas):**
```powershell
celery -A syslab beat -l info
```

## Aplicaciones

| App | Responsabilidad |
|---|---|
| `core` | Catálogos base: pacientes, insumos, marcas, categorías, materiales, ciudades, especialidades, sucursales, tareas, tipos de trabajo, vendedores |
| `ordenes` | Gestión de órdenes de trabajo y movimientos de retiro |
| `informes` | Reportes del sistema |
| `users` | Modelo custom de usuarios y autenticación |

## Notas

- Al iniciar sesión se redirige a `/ordenes/`.
- Historial de cambios en modelos vía `django-simple-history`.
- Autocompletes con `django-autocomplete-light` (dal + select2).
