from Config.ConfigDB import ConfigDB
from Extract.ExtractDB import ExtractDB
from Transform.TransformDB import TransformDB
from Load.LoadDB import LoadDB
import time

def main():
    try:
        print("\n🚀 Iniciando proceso ETL para datos Pokemon...")
        start_time = time.time()

        # Extract
        print("\n📥 Fase de Extracción:")
        print(f"Leyendo datos desde: {ConfigDB.INPUT_PATH}")
        extractor = ExtractDB(ConfigDB.INPUT_PATH)
        df = extractor.extract()

        if df is not None:
            print(f"✅ Datos extraídos exitosamente. Registros encontrados: {len(df)}")

            # Transform
            print("\n🔄 Fase de Transformación:")
            print("Limpiando y preparando los datos...")
            transformer = TransformDB(df)
            df_clean = transformer.clean()
            
            print("\n📊 Resumen de datos limpios:")
            print(f"- Total de registros: {len(df_clean)}")
            print(f"- Columnas: {', '.join(df_clean.columns)}")
            print("\nPrimeros 5 registros:")
            print(df_clean.head())

            # Load
            print("\n📤 Fase de Carga:")
            loader = LoadDB(df_clean)
            
            # Guardar en CSV
            print("\n💾 Guardando datos en CSV...")
            loader.to_csv(ConfigDB.OUTPUT_PATH)
            
            # Cargar en MySQL
            print("\n🗄️ Cargando datos en MySQL...")
            loader.to_mysql()

            # Resumen final
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            print(f"\n✨ Proceso ETL completado exitosamente en {duration} segundos")
            print(f"📁 CSV guardado en: {ConfigDB.OUTPUT_PATH}")
            print(f"🗃️ Datos cargados en la tabla: {ConfigDB.MYSQL_TABLE}")

        else:
            print("❌ Error: No se pudieron extraer los datos")

    except Exception as e:
        print(f"\n❌ Error en el proceso ETL: {str(e)}")
        raise

if __name__ == "__main__":
    main()
