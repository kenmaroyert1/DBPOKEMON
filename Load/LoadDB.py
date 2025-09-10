import os
import mysql.connector
import time
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

    def _get_connection(self, max_retries=3, delay=5):
        """Intenta establecer una conexión con reintentos"""
        for attempt in range(max_retries):
            try:
                config = ConfigDB.MYSQL_CONFIG.copy()
                # Agregar timeouts y configuración adicional
                config.update({
                    'connect_timeout': 60,
                    'connection_timeout': 60,
                    'pool_size': 5,
                    'pool_reset_session': True,
                    'autocommit': True,  # Activar autocommit para evitar transacciones largas
                    'buffered': True     # Usar cursores con buffer
                })
                return mysql.connector.connect(**config)
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⚠️ Intento {attempt + 1} fallido. Reintentando en {delay} segundos...")
                    time.sleep(delay)
                else:
                    raise e

    def to_mysql(self, batch_size=50):
        conn = None
        cursor = None
        
        try:
            # Conectar a la base de datos con reintentos
            print("🔄 Conectando a la base de datos...")
            conn = self._get_connection()
            cursor = conn.cursor()

            print("🗑️ Eliminando tabla anterior si existe...")
            cursor.execute("DROP TABLE IF EXISTS pokemon")
            conn.commit()
            
            print("📝 Creando nueva tabla...")
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
            conn.commit()

            # Preparar los datos para inserción
            seen_ids = {}
            next_id = 1000
            total_rows = len(self.df)
            processed_rows = 0
            batch_data = []

            print("📥 Iniciando carga de datos por lotes...")
            for _, row in self.df.iterrows():
                pokemon_id = int(row['#'])
                if pokemon_id in seen_ids:
                    pokemon_id = next_id
                    next_id += 1
                else:
                    seen_ids[pokemon_id] = True

                batch_data.append((
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

                # Insertar cuando el lote está completo o es el último registro
                if len(batch_data) >= batch_size or processed_rows == total_rows - 1:
                    retry_count = 0
                    max_retries = 3
                    
                    while retry_count < max_retries:
                        try:
                            if not conn.is_connected():
                                print("⚠️ Reconectando a la base de datos...")
                                conn = self._get_connection()
                                cursor = conn.cursor()

                            cursor.executemany("""
                                INSERT INTO pokemon (id, name, type_1, total, hp, attack, defense, 
                                                  sp_atk, sp_def, speed, generation, legendary)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, batch_data)
                            conn.commit()
                            processed_rows += len(batch_data)
                            print(f"📊 Progreso: {processed_rows}/{total_rows} registros procesados")
                            batch_data = []
                            break
                        except mysql.connector.Error as err:
                            retry_count += 1
                            if retry_count < max_retries:
                                print(f"⚠️ Error en lote, reintento {retry_count} de {max_retries}...")
                                time.sleep(5)  # Esperar antes de reintentar
                            else:
                                raise err

            print(f"✅ Datos cargados exitosamente en la tabla {ConfigDB.MYSQL_TABLE}")

        except Exception as e:
            print(f"❌ Error al cargar datos en MySQL: {str(e)}")
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass
            if conn:
                try:
                    conn.close()
                except:
                    pass
