# Airpeek

AirPeek es una aplicación desarrollada en grupo como proyecto del ciclo de **Desarrollo de Aplicaciones Multiplataforma (DAM)**. Permite buscar vuelos económicos comparando múltiples aerolíneas y rutas, guardar itinerarios y configurar alertas de vuelo. Este repositorio recopila y organiza todo el código del proyecto realizado de forma colaborativa.

<p align="left">
  <img src="https://img.shields.io/badge/Backend-Django-green">
  <img src="https://img.shields.io/badge/Language-Python-yellow">
  <img src="https://img.shields.io/badge/Frontend-Android-brightgreen">
  <img src="https://img.shields.io/badge/Build-Gradle-02303A">
  <img src="https://img.shields.io/badge/Database-SQLite-blue">
</p>


## Índice

1. [Apuntes y requisitos previos](#apuntes-y-requisitos-previos)
2. [Características del proyecto](#caracteristicas)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Detalles técnicos](#detalles-tecnicos)
5. [Guía de uso del proyecto](#guia-de-uso-del-proyecto)


## Apuntes y requisitos previos

* El backend está pensado para ejecutarse en **entorno de desarrollo local**.
* Cada parte del proyecto (backend y frontend) gestiona sus dependencias de forma independiente.
* Para ejecutar el proyecto, se requiere de tener instaladas las siguientes herramientas:
    * **Android Studio** junto al **JDK 17**; que suele venir incluído.
    * **Python ver.3.11+**
    * **Git**


## Características

* Comparación de vuelos entre múltiples aerolíneas, con visualización de resultados y redirección a plataformas externas para la compra de billetes.
* Gestión de itinerarios y sistema de alertas de vuelo.
* Backend basado en una API REST desarrollada con Django.
* Frontend implementado como aplicación Android nativa.
* Arquitectura modular con separación frontend/backend, desarrollada de forma colaborativa en el ciclo DAM.


## Estructura del proyecto

```
airpeek/
├── code/
│   ├── backend/                  # API REST desarrollada con Django
│   │   ├── airpeek/              # Configuración principal del proyecto
│   │   ├── airpeek_api/          # Lógica de negocio y endpoints
│   │   ├── db.sqlite3            # Base de datos SQLite
│   │   ├── manage.py             # Punto de entrada del backend
│   │   └── requirements.txt      # Dependencias del backend
│   │
│   └── frontend/                 # Aplicación Android
│       ├── app/                  # Código fuente de la app
│       └── gradle/               # Configuración de Gradle
├── doc/
├── logo/
└── README.md
```

La estructura del proyecto está organizada de forma modular, separando de forma clara el backend y el frontend para facilitar el desarrollo y mantenimiento del mismo.
El directorio **code** concentra el núcleo de la aplicación, y los directorios **doc** y **logo** se destinan a la documentación y al logo del proyecto respectivamente.


## Detalles técnicos

**Lenguajes:** Python, Java y XML.

**Tecnologías y herramientas:** Django, Android SDK, Gradle y SQLite.

**Arquitectura:** API REST con separación frontend/backend y comunicación HTTP.

**Entorno:** Desarrollo local con emulador Android y gestión independiente de dependencias.


## Guía de uso del proyecto

### Backend (Django)

---

### 1.1 Acceso al backend del proyecto:

```sh
cd code/backend
```

### 1.2 Creado y activación del entorno virtual (opcional):

```sh
python -m venv .venv
```

- **Windows (PowerShell):**

```sh
source .venv/bin/activate
```

- **Linux / macOS (bash o zsh):**

```sh
source .venv/bin/activate
```

### 1.3 Instalación de las dependencias:

```sh
pip install -r requirements.txt
```

### 1.4 Aplicación de las migraciones:

```sh
python manage.py migrate
```

### 1.5 Ejecución del servidor:

```sh
python manage.py runserver
```

* El backend quedará disponible en: http://127.0.0.1:8000


---

### Frontend (Android)

### 2.1 Abrir el proyecto en Android Studio:

  1. Abrir **Android Studio**
  2. Seleccionar **Open**
  3. Abrir la carpeta: airpeek/code/frontend
  4. Esperar a que **Gradle sincronice** el proyecto


### 2.2 Configuración del Android SDK:

  En Android Studio:

  * **File → Settings → Android SDK**
  * Instalar:
    * Android SDK Platform (API 33 o superior)
    * Android SDK Build-Tools
    * Android Emulator


### 2.3 Creación y ejecución de un emulador:

  1. **Tools → Device Manager**
  2. Crear un dispositivo virtual (Pixel recomendado)
  3. Seleccionar Android API 33+
  4. Iniciar el emulador

---

### Conexión del entre backend y frontend:

### 3.3 Configurar la URL de la API

En el frontend Android, configura la URL base de la API:

```java
const val BASE_URL = "http://10.0.2.2:8000/"
```
  - __Anotaciones:__
    - `10.0.2.2` es obligatorio para emuladores Android.
    - No usar `localhost` ni `127.0.0.1`.
  <br/>
  - **__Asegurarse de que el archivo `AndroidManifest.xml` contiene la siguiente línea:__**

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

## 4. Ejecución de la aplicación:

1. Comprobar que el server está siendo ejecutado (`python manage.py runserver`)
2. Tener el emulador de Android Studio iniciado.
3. Pulsar **Run ▶️** en Android Studio.
