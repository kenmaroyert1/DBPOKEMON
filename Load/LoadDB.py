import os

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
            print(f"❌ Error al guardar datos: {e}")
