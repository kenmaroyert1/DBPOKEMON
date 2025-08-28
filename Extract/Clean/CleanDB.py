import pandas as pd
from Config.ConfigBig import Config

class CleanDB:
    """
    Limpieza universal (aplica a cualquier CSV, optimizado para Pokémon).
    Incluye:
    - Eliminación de duplicados
    - Manejo de NA
    - Valores no deseados
    - Datos ausentes (numéricos)
    - QA de tipos de datos
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # --- pasos atómicos (encadenables) ---

    def remove_duplicates(self):
        if Config.DROP_DUPLICATES:
            self.df = self.df.drop_duplicates()
        return self

    def handle_na_text(self):
        # Si existen estas columnas, aplicar defaults razonables
        if "Type 2" in self.df.columns:
            self.df["Type 2"] = self.df["Type 2"].fillna(Config.TYPE2_DEFAULT)

        # Relleno genérico para textos
        text_cols = self.df.select_dtypes(include=["object"]).columns
        if len(text_cols) > 0:
            self.df[text_cols] = self.df[text_cols].fillna(Config.FILL_TEXT_DEFAULT)
        return self

    def remove_unwanted_values(self):
        # Limpieza de caracteres no deseados en columnas de texto
        text_cols = self.df.select_dtypes(include=["object"]).columns
        for col in text_cols:
            self.df[col] = (
                self.df[col]
                .astype(str)
                .str.strip()
                .str.replace(Config.UNWANTED_PATTERN, "", regex=True)
            )
        return self

    def fill_missing_numeric(self):
        # Convertir a numérico lo que se pueda y rellenar NA
        num_candidates = self.df.columns.difference(
            self.df.select_dtypes(include=["object", "bool", "datetime64[ns]"]).columns
        )
        # Asegurar coerción numérica en columnas que parecen numéricas con ruido
        for col in num_candidates:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        num_cols = self.df.select_dtypes(include=["number"]).columns
        if len(num_cols) == 0:
            return self

        strat = Config.NUMERIC_MISSING_STRATEGY
        if strat == "zero":
            self.df[num_cols] = self.df[num_cols].fillna(0)
        elif strat == "mean":
            self.df[num_cols] = self.df[num_cols].fillna(self.df[num_cols].mean())
        elif strat == "median":
            self.df[num_cols] = self.df[num_cols].fillna(self.df[num_cols].median())
        elif strat == "mode":
            self.df[num_cols] = self.df[num_cols].fillna(self.df[num_cols].mode().iloc[0])
        else:
            # por defecto zero
            self.df[num_cols] = self.df[num_cols].fillna(0)
        return self

    def qa_types(self):
        # Tipos razonables en Pokémon si existen
        if "#" in self.df.columns:
            self.df["#"] = pd.to_numeric(self.df["#"], errors="coerce").fillna(0).astype(int)

        # Fuerza strings en columnas clave si existen
        for col in ["Name", "Type 1", "Type 2", "Generation", "Legendary"]:
            if col in self.df.columns:
                if col == "Legendary":
                    # intentar convertir booleano
                    self.df[col] = (
                        self.df[col]
                        .astype(str)
                        .str.strip()
                        .str.lower()
                        .map({"true": True, "false": False})
                        .fillna(False)
                        .astype(bool)
                    )
                else:
                    self.df[col] = self.df[col].astype(str).str.strip()
        return self

    # --- pipeline principal ---

    def universal_clean(self) -> pd.DataFrame:
        """
        Ejecuta todos los pasos de limpieza (universal).
        """
        return (
            self.remove_duplicates()
                .handle_na_text()
                .remove_unwanted_values()
                .fill_missing_numeric()
                .qa_types()
                .df
        )
