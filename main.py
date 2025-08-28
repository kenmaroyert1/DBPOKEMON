from Config.ConfigBig import Config
from Extract.BigDataExtract import BigDataExtract
from Transform.BigDataTransform import BigDataTransform
from Load.BigDataLoad import BigDataLoad

def main():
    # Extract
    extractor = BigDataExtract(Config.INPUT_PATH)
    df = extractor.extract()

    if df is not None:
        # Transform
        transformer = BigDataTransform(df)
        df_clean = transformer.clean()

        # Mostrar algunos resultados
        print("Primeros registros limpios:")
        print(df_clean.head())
        print("\nEstadísticas generales:")
        print(df_clean.describe())

        # Load
        loader = BigDataLoad(df_clean)
        loader.to_csv(Config.OUTPUT_PATH)

if __name__ == "__main__":
    main()
