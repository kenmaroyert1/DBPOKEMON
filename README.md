# � Pokémon ETL Project

Este proyecto implementa un proceso ETL (Extract, Transform, Load) especializado para datos de Pokémon. Extrae información desde un archivo CSV, realiza transformaciones y limpieza de datos, y finalmente los carga tanto en un nuevo CSV como en una base de datos MySQL.

## 📋 Estructura del Proyecto

```
DBPOKEMON/
├── Config/
│   ├── __init__.py
│   └── ConfigDB.py         # Configuración de rutas y conexión a BD
├── Extract/
│   ├── __init__.py
│   └── ExtractDB.py        # Extracción de datos del CSV
├── Transform/
│   ├── __init__.py
│   └── TransformDB.py      # Limpieza y transformación de datos
├── Load/
│   ├── __init__.py
│   └── LoadDB.py           # Carga de datos a CSV y MySQL
├── Test/
│   └── Test_DataBase.py    # Pruebas de conexión a la BD
├── output/
│   └── Pokemon_clean.csv   # Datos limpios en formato CSV
├── main.py                 # Script principal del ETL
├── Pokemon.csv             # Datos originales
├── requirements.txt        # Dependencias del proyecto
└── .env                    # Variables de entorno
```

## 🚀 Características

### Extract (Extracción)
- Lectura de datos desde archivo CSV
- Validación de existencia del archivo
- Carga en DataFrame de pandas

### Transform (Transformación)
- Eliminación de duplicados
- Limpieza de tipos de datos
- Eliminación de columnas innecesarias
- Manejo de valores nulos
- Conversión de tipos de datos

### Load (Carga)
- Exportación a CSV limpio
- Carga en base de datos MySQL
- Manejo automático de IDs duplicados
- Recreación de tabla en cada ejecución

## ⚙️ Requisitos y Configuración

### Requisitos Previos
- Python 3.x
- MySQL Server
- Pip (gestor de paquetes de Python)

### Dependencias Python
```bash
pip install -r requirements.txt
```

Contenido de requirements.txt:
```
pandas
python-dotenv
mysql-connector-python
```

### Configuración de Base de Datos
Crea un archivo `.env` en la raíz del proyecto con:
```env
DBUSER=tu_usuario
DBPASSWORD=tu_contraseña
DBHOST=tu_host
DBPORT=tu_puerto
DBDATABASE_NAME=nombre_base_datos
```

## 📊 Estructura de Datos

### Datos de Entrada (Pokemon.csv)
Columnas del archivo original:
- #: ID del Pokémon
- Name: Nombre del Pokémon
- Type 1: Tipo principal
- Total: Estadísticas totales
- HP: Puntos de vida
- Attack: Ataque
- Defense: Defensa
- Sp. Atk: Ataque especial
- Sp. Def: Defensa especial
- Speed: Velocidad
- Generation: Generación del Pokémon
- Legendary: Indicador si es legendario

### Estructura de la Base de Datos
```sql
CREATE TABLE pokemon (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type_1 VARCHAR(50) NOT NULL,
    total INT,
    hp INT,
    attack INT,
    defense INT,
    sp_atk INT,
    sp_def INT,
    speed INT,
    generation INT,
    legendary BOOLEAN
)
```

## 🚀 Uso

### Ejecutar el ETL Completo
```bash
python main.py
```

### Probar la Conexión a la Base de Datos
```bash
python Test/Test_DataBase.py
```

## 📝 Notas Importantes

- La tabla MySQL se elimina y recrea en cada ejecución
- Los IDs duplicados se manejan automáticamente asignando nuevos IDs (1000+)
- Los datos limpios se guardan en `output/Pokemon_clean.csv`
- El proceso muestra logs detallados con emojis para mejor seguimiento
- Se realiza validación de datos en cada paso del proceso

## ⚙️ Mantenimiento

Para mantener el proyecto:
1. Revisa regularmente las dependencias en requirements.txt
2. Ejecuta las pruebas de conexión antes de cada proceso ETL
3. Verifica los logs de salida para detectar posibles errores
4. Mantén actualizado el archivo .env con las credenciales correctas

## 👥 Contribuir

1. Haz un Fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

4. El resultado se guardará automáticamente en la carpeta `output/` como `cleaned_output.csv`.

---

## 📊 Ejemplo de salida

Si usamos el dataset de prueba `Pokemon.csv`, el flujo hará lo siguiente:

* Cargará todos los registros.
* Limpiará duplicados, valores faltantes y espacios.
* Normalizará las estadísticas (`HP`, `Attack`, `Defense`, etc.) entre 0 y 1.
* Guardará un archivo final en `output/cleaned_output.csv`.

---

## 📑 About Dataset

Este dataset incluye **721 Pokémon**, con su número, nombre, primer y segundo tipo, y estadísticas básicas: **HP, Attack, Defense, Special Attack, Special Defense y Speed**.
Ha sido usado como recurso educativo para enseñar estadística, y también puede servir como introducción geek a temas de machine learning.

📌 El dataset describe atributos del videojuego Pokémon (no cartas ni Pokémon Go).

Los atributos son:

* **#**: ID para cada Pokémon
* **Name**: Nombre de cada Pokémon
* **Type 1**: Tipo principal (determina debilidades y resistencias)
* **Type 2**: Tipo secundario (si aplica)
* **Total**: Suma de todas las estadísticas, indicador general de fuerza
* **HP**: Puntos de vida, resistencia antes de debilitarse
* **Attack**: Potencia base de ataques físicos
* **Defense**: Resistencia frente a ataques físicos
* **SP Atk**: Potencia base de ataques especiales (ej. Fire Blast, Bubble Beam)
* **SP Def**: Resistencia frente a ataques especiales
* **Speed**: Determina qué Pokémon ataca primero en cada turno

---

## 🔮 Conclusión

Este proyecto me permitió practicar la **arquitectura de un ETL real**, modularizar el código en Python y crear un sistema **universal** que pueda trabajar con cualquier dataset.
En el futuro se le pueden agregar más transformaciones y hasta conexión con bases de datos para automatizar todo el proceso.

