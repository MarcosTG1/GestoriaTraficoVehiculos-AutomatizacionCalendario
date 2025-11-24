# 📅 Gestoría - Actualizaciones de Calendario

Sistema automatizado para la gestión de eventos recurrentes en Google Calendar basado en datos de CSV. Diseñado para gestorías que necesitan hacer seguimiento automático de justificantes, incidencias y rechazos de tráfico.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Uso](#-uso)
- [Formato de Datos CSV](#-formato-de-datos-csv)
- [Solución de Problemas](#-solución-de-problemas)

## ✨ Características

- **Autenticación OAuth2** con Google Calendar API
- **Gestión automatizada de eventos** desde archivos CSV
- **Eventos recurrentes configurables** con intervalos personalizables
- **Tres tipos de eventos**:
  - 📄 **Justificantes**: Seguimiento de documentación pendiente
  - ⚠️ **Incidencias**: Estados y actualizaciones periódicas
  - 🚗 **Tráfico**: Rechazos y seguimientos de tráfico
- **Eliminación masiva de eventos** con confirmación de seguridad
- **Configuración mediante variables de entorno** para mayor seguridad
- **Manejo robusto de errores** con reportes detallados

## 🔧 Requisitos Previos

- **Python 3.8+**
- **Cuenta de Google** con acceso a Google Calendar
- **Proyecto en Google Cloud Console** con Calendar API habilitada
- **Archivo `credentials.json`** descargado desde Google Cloud Console

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/Gestoria-Trafico-Vehiculos-Automatizacion-Calendario.git
cd Gestoria-Trafico-Vehiculos-Automatizacion-Calendario
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Configurar Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la **Google Calendar API**
4. Ve a **Credenciales** → **Crear credenciales** → **ID de cliente de OAuth 2.0**
5. Configura el tipo de aplicación como **Aplicación de escritorio**
6. Descarga el archivo JSON y guárdalo como `secrets/credentials.json`

### 2. Configurar variables de entorno

Copia el archivo de ejemplo y edítalo con tus valores:

```bash
copy .env.example .env
```

Edita el archivo `.env` con tus configuraciones:

```env
# Rutas de autenticación de Google
GOOGLE_CREDENTIALS_PATH=secrets/credentials.json
GOOGLE_TOKEN_PATH=secrets/token.json
CALENDAR_ID=primary

# Rutas de archivos CSV
PATH_INCIDENCIAS=./data/LISTADO_INCIDENCIAS.csv
PATH_JUSTIFICANTES=./data/LISTADO_JUSTIFICANTES.csv
PATH_TRAFICO=./data/LISTADO_TRAFICO.csv

# Configuración de recurrencia para Justificantes
DIAS_RECURRENCIA_JUSTIFICANTE=28
VECES_REPETICION_JUSTIFICANTE=3

# Configuración de recurrencia para Incidencias
DIAS_RECURRENCIA_INCIDENCIA=15
VECES_REPETICION_INCIDENCIA=6

# Configuración de recurrencia para Tráfico
DIAS_RECURRENCIA_TRAFICO=15
VECES_REPETICION_TRAFICO=6
```

### 3. Preparar archivos CSV

Coloca tus archivos CSV en la carpeta `data/` con el siguiente formato:

**Columnas requeridas:**
- `BASTIDOR`: Identificador único del vehículo
- `FECHA DE CREACIÓN`: Fecha en formato ISO (YYYY-MM-DD) o compatible con pandas

Ejemplo:
```csv
BASTIDOR,FECHA DE CREACIÓN
VF1RFB0F0123456,2024-01-15
WBA1234567890ABC,2024-01-20
```

## 📁 Estructura del Proyecto

```
GestoríaActualizaciónesCalendario/
├── data/                           # Archivos CSV de datos
│   ├── LISTADO_INCIDENCIAS.csv
│   ├── LISTADO_JUSTIFICANTES.csv
│   └── LISTADO_TRAFICO.csv
├── scripts/                        # Scripts ejecutables
│   ├── auth_script.py              # Script de autenticación
│   └── BorrarEventos.py            # Script para eliminar eventos
├── src/                            # Código fuente principal
│   ├── __init__.py
│   ├── config.py                   # Configuración centralizada
│   ├── main.py                     # Punto de entrada principal
│   └── services/                   # Servicios de lógica de negocio
│       ├── __init__.py
│       ├── ManejoDeEventos.py      # Gestión de eventos del calendario
│       └── ManejoGoogleCalendar.py # API de Google Calendar
├── secrets/                        # Credenciales (NO subir a Git)
│   ├── credentials.json            # Credenciales de OAuth2
│   └── token.json                  # Token de acceso (generado automáticamente)
├── .env                            # Variables de entorno (NO subir a Git)
├── .env.example                    # Plantilla de variables de entorno
├── .gitignore                      # Archivos ignorados por Git
├── requirements.txt                # Dependencias de Python
└── README.md                       # Este archivo
```

## 🚀 Uso

### Primera vez: Autenticación

Antes de usar el sistema, debes autenticarte con Google:

```bash
python scripts/auth_script.py
```

Este comando:
1. Abrirá tu navegador
2. Te pedirá que inicies sesión en Google
3. Solicitará permisos para gestionar tu calendario
4. Guardará un token en `secrets/token.json` para futuros usos

### Ejecución completa del sistema

Para ejecutar todo el flujo de actualización:

```bash
python src/main.py
```

Este comando ejecutará en orden:
1. ✅ Autenticación
2. 🗑️ Eliminación de eventos existentes (con confirmación)
3. 📄 Creación de eventos de Justificantes
4. ⚠️ Creación de eventos de Incidencias
5. 🚗 Creación de eventos de Tráfico

### Scripts individuales

#### Eliminar eventos existentes

```bash
python scripts/BorrarEventos.py
```

> ⚠️ **Advertencia**: Este script eliminará todos los eventos en el rango del año anterior, actual y siguiente. Se solicitará confirmación antes de proceder.

## 📊 Formato de Datos CSV

Cada archivo CSV debe contener las siguientes columnas:

| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| `BASTIDOR` | String | Número de bastidor/matrícula del vehículo | `P0079BDP 1XGK79 VOLVO XC60` |
| `ESTADO` | String | Tipo de evento (Incidencia, Justificante, Tráfico) | `Incidencia` |
| `FECHA DE CREACIÓN` | DateTime | Fecha y hora de creación del registro | `2025-10-20 09:30:20` |
| `FECHA DE MODIFICACIÓN` | DateTime | Fecha y hora de última modificación | `2025-11-24 08:52:35` |

### Ejemplo de archivo CSV

```csv
BASTIDOR,ESTADO,FECHA DE CREACIÓN,FECHA DE MODIFICACIÓN
P0079BDP 1XGK79 VOLVO XC60,Incidencia,2025-10-20 09:30:20,2025-11-24 08:52:35
1657NFG,Incidencia,2025-11-21 18:28:46,2025-11-24 08:20:28
TF896L mazda,Incidencia,2025-11-21 20:26:10,2025-11-24 07:02:47
9426 JHV,Incidencia,2025-11-21 11:59:52,2025-11-21 12:17:51
A6781BF LUIS SERRA,Incidencia,2025-11-13 11:45:02,2025-11-19 17:53:49
```

> 💡 **Nota**: El campo `BASTIDOR` puede contener información adicional como modelo del vehículo o nombre del cliente. La aplicación procesará automáticamente la columna `FECHA DE CREACIÓN` para programar los eventos recurrentes.

## 🔍 Solución de Problemas

### Error: "Credentials file not found"

**Solución**: Asegúrate de haber descargado `credentials.json` desde Google Cloud Console y haberlo colocado en `secrets/credentials.json`.

### Error: "Variable 'XXX' NO está definida en el archivo .env"

**Solución**: Verifica que tu archivo `.env` contenga todas las variables requeridas. Usa `.env.example` como referencia.

### Error: "No se encontró el archivo CSV"

**Solución**: Verifica que:
1. Los archivos CSV existan en la ruta especificada
2. Las rutas en `.env` sean correctas
3. Los nombres de archivo coincidan exactamente

### Los eventos no se crean

**Solución**: 
1. Ejecuta `python scripts/auth_script.py` para verificar la autenticación
2. Verifica que el archivo CSV tenga el formato correcto
3. Revisa los mensajes de error en la consola

### Token expirado

**Solución**: Elimina `secrets/token.json` y vuelve a ejecutar `python scripts/auth_script.py`.

## 🔒 Seguridad

- ❌ **NO** subas `secrets/` ni `.env` a Git
- ✅ Usa `.gitignore` para excluir archivos sensibles
- ✅ Comparte `.env.example` como plantilla
- ✅ Revoca tokens desde Google Cloud Console si se comprometen

## 📝 Licencia

Este proyecto es de uso interno. Todos los derechos reservados.

## 👤 Autor

Desarrollado para la gestión automatizada de calendarios en entornos de gestoría.

---

**¿Necesitas ayuda?** Revisa la sección de [Solución de Problemas](#-solución-de-problemas) o contacta al administrador del sistema.
