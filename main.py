from Config.ConfigDB import ConfigDB
from Extract.ExtractDB import ExtractDB
from Transform.TransformDB import TransformDB
from Load.LoadDB import LoadDB

def main():
    # Extract
    extractor = ExtractDB(ConfigDB.INPUT_PATH)
    df = extractor.extract()

    if df is not None:
        # Transform
        transformer = TransformDB(df)
        df_clean = transformer.clean()

        # Mostrar algunos resultados
        print("Primeros registros limpios:")
        print(df_clean.head())
        print("\nEstadísticas generales:")
        print(df_clean.describe())

        # Load
        loader = LoadDB(df_clean)
        loader.to_csv(ConfigDB.OUTPUT_PATH)

if __name__ == "__main__":
    main()
