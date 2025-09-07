import pandas as pd

class TransformDB:
    """
    Clase para transformar y limpiar los datos extraídos.
    """
    def __init__(self, df):
        self.df = df

    def clean(self):
        """
        Realiza limpieza y transformación de los datos.
        """
        df = self.df.copy()

        # Eliminar duplicados
        df = df.drop_duplicates()

        # Eliminar la columna Type 2
        if "Type 2" in df.columns:
            df = df.drop(columns=["Type 2"])

        # Asegurar que las columnas numéricas no tengan nulos
        num_cols = ["Total", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Convertir columna Legendary a boolean
        if "Legendary" in df.columns:
            df["Legendary"] = df["Legendary"].astype(bool)

        self.df = df
        return self.df
