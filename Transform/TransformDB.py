import pandas as pd

class TransformDB:
    """
    Clase para transformar y limpiar los datos extraídos.
    """
    def __init__(self, df):
        self.df = df

    def clean(self):
        """
        Realiza limpieza y transformación avanzada de los datos.
        """
        df = self.df.copy()
        
        print("\n🧹 Iniciando limpieza de datos...")

        # 1. Eliminar duplicados exactos
        num_duplicados = df.duplicated().sum()
        df = df.drop_duplicates()
        print(f"✓ Se eliminaron {num_duplicados} registros duplicados")

        # 2. Limpiar nombres (eliminar espacios extra y caracteres especiales)
        df['Name'] = df['Name'].str.strip().str.replace(r'[^\w\s-]', '', regex=True)
        print("✓ Nombres de Pokémon limpiados")

        # 3. Normalizar tipos (primera letra mayúscula, resto minúsculas)
        df['Type 1'] = df['Type 1'].str.strip().str.title()
        
        # 4. Limpiar y normalizar Type 2
        if "Type 2" in df.columns:
            # Rellenar valores nulos con 'None'
            df['Type 2'] = df['Type 2'].fillna('None')
            # Limpiar y normalizar al igual que Type 1
            df['Type 2'] = df['Type 2'].str.strip().str.title()
            print("✓ Tipos de Pokémon (Type 1 y Type 2) normalizados")

        # 5. Validar y corregir valores numéricos
        num_cols = ["Total", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
        for col in num_cols:
            if col in df.columns:
                # Convertir a numérico y reemplazar valores negativos por 0
                df[col] = pd.to_numeric(df[col], errors="coerce")
                neg_count = (df[col] < 0).sum()
                if neg_count > 0:
                    df[col] = df[col].clip(lower=0)
                    print(f"✓ Se corrigieron {neg_count} valores negativos en {col}")
                
                # Reemplazar valores nulos con la mediana de la columna
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    df[col] = df[col].fillna(df[col].median())
                    print(f"✓ Se corrigieron {null_count} valores nulos en {col}")
                
                # Redondear valores a enteros
                df[col] = df[col].round().astype(int)

        # 6. Validar generación (debe estar entre 1 y 7)
        invalid_gen = (df['Generation'] < 1) | (df['Generation'] > 7)
        if invalid_gen.any():
            df.loc[invalid_gen, 'Generation'] = 1
            print(f"✓ Se corrigieron {invalid_gen.sum()} valores inválidos en Generation")

        # 7. Asegurar que Legendary sea booleano
        df['Legendary'] = df['Legendary'].astype(bool)
        print("✓ Campo Legendary convertido a booleano")

        # 8. Validar IDs
        df['#'] = pd.to_numeric(df['#'], errors='coerce').fillna(999999).astype(int)
        invalid_ids = (df['#'] <= 0).sum()
        if invalid_ids > 0:
            print(f"✓ Se corrigieron {invalid_ids} IDs inválidos")

        # 9. Añadir columna de fecha de procesamiento
        df['ProcessedDate'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        print("✓ Se agregó columna de fecha de procesamiento")

        # 10. Ordenar por ID
        df = df.sort_values(by='#')
        print("✓ Datos ordenados por ID")

        print(f"\n📊 Resumen de limpieza:")
        print(f"- Registros iniciales: {len(self.df)}")
        print(f"- Registros finales: {len(df)}")
        print(f"- Columnas procesadas: {', '.join(df.columns)}")

        self.df = df
        return self.df
