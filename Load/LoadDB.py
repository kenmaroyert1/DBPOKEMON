import os
import mysql.connector
from Config.ConfigDB import ConfigDB

class LoadDB:
    def __init__(self, df):
        self.df = df

    def to_csv(self, output_path):
        try:
            # Obtener la carpeta (por ejemplo, 'output' de 'output/archivo.csv')
            output_dir = os.path.dirname(output_path)

            # Crear la carpeta si no existe
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Guardar el archivo CSV
            self.df.to_csv(output_path, index=False)
            print(f"✅ Datos guardados en: {output_path}")
        except Exception as e:
            print(f"❌ Error al guardar datos en CSV: {e}")

    def to_mysql(self):
        try:
            # Conectar a la base de datos
            conn = mysql.connector.connect(**ConfigDB.MYSQL_CONFIG)
            cursor = conn.cursor()

            # Eliminar la tabla si existe
            cursor.execute("DROP TABLE IF EXISTS pokemon")
            
            # Crear la tabla desde cero
            cursor.execute("""
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
            """)

            # Preparar los datos para inserción
            seen_ids = {}
            next_id = 1000

            # Insertar los datos
            for _, row in self.df.iterrows():
                pokemon_id = int(row['#'])
                if pokemon_id in seen_ids:
                    pokemon_id = next_id
                    next_id += 1
                else:
                    seen_ids[pokemon_id] = True

                cursor.execute("""
                    INSERT INTO pokemon (id, name, type_1, total, hp, attack, defense, 
                                      sp_atk, sp_def, speed, generation, legendary)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    pokemon_id,
                    row['Name'],
                    row['Type 1'],
                    row['Total'],
                    row['HP'],
                    row['Attack'],
                    row['Defense'],
                    row['Sp. Atk'],
                    row['Sp. Def'],
                    row['Speed'],
                    row['Generation'],
                    row['Legendary']
                ))

            # Confirmar los cambios
            conn.commit()
            print(f"✅ Datos cargados exitosamente en la tabla {ConfigDB.MYSQL_TABLE}")

        except Exception as e:
            print(f"❌ Error al cargar datos en MySQL: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
