import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from Config.ConfigDB import ConfigDB

class PokemonVisualizer:
    def __init__(self, csv_path=ConfigDB.OUTPUT_PATH):
        self.df = pd.read_csv(csv_path)
        # Configurar el estilo de las gráficas
        plt.style.use('default')
        sns.set_theme()  # Usar el tema por defecto de seaborn

    def plot_pokemon_by_generation(self):
        """Gráfica de cantidad de Pokémon por generación"""
        plt.figure(figsize=(10, 6))
        gen_counts = self.df['Generation'].value_counts().sort_index()
        
        ax = gen_counts.plot(kind='bar')
        plt.title('Cantidad de Pokémon por Generación', pad=20)
        plt.xlabel('Generación')
        plt.ylabel('Cantidad de Pokémon')
        
        # Agregar valores sobre las barras
        for i, v in enumerate(gen_counts):
            ax.text(i, v + 1, str(v), ha='center')
        
        plt.tight_layout()
        plt.savefig('output/pokemon_by_generation.png')
        plt.close()

    def plot_type_distribution(self):
        """Gráfica de distribución de tipos primarios"""
        plt.figure(figsize=(12, 6))
        type_counts = self.df['Type 1'].value_counts()
        
        ax = type_counts.plot(kind='bar')
        plt.title('Distribución de Tipos Primarios de Pokémon', pad=20)
        plt.xlabel('Tipo')
        plt.ylabel('Cantidad')
        plt.xticks(rotation=45)
        
        # Agregar valores sobre las barras
        for i, v in enumerate(type_counts):
            ax.text(i, v + 1, str(v), ha='center')
        
        plt.tight_layout()
        plt.savefig('output/type_distribution.png')
        plt.close()

    def plot_stats_by_generation(self):
        """Gráfica de estadísticas promedio por generación"""
        stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        avg_stats = self.df.groupby('Generation')[stats].mean()
        
        plt.figure(figsize=(12, 6))
        ax = avg_stats.plot(kind='bar', width=0.8)
        plt.title('Estadísticas Promedio por Generación', pad=20)
        plt.xlabel('Generación')
        plt.ylabel('Valor Promedio')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig('output/stats_by_generation.png')
        plt.close()

    def plot_legendary_distribution(self):
        """Gráfica de Pokémon legendarios vs no legendarios por generación"""
        plt.figure(figsize=(10, 6))
        legendary_by_gen = self.df.groupby(['Generation', 'Legendary']).size().unstack()
        
        ax = legendary_by_gen.plot(kind='bar', stacked=True)
        plt.title('Distribución de Pokémon Legendarios por Generación', pad=20)
        plt.xlabel('Generación')
        plt.ylabel('Cantidad de Pokémon')
        plt.legend(title='Legendario', labels=['No', 'Sí'])
        
        # Agregar valores sobre las barras
        for c in ax.containers:
            ax.bar_label(c, label_type='center')
        
        plt.tight_layout()
        plt.savefig('output/legendary_distribution.png')
        plt.close()

    def plot_type_stats_radar(self):
        """Gráfica de radar para estadísticas promedio por tipo"""
        stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        avg_stats_by_type = self.df.groupby('Type 1')[stats].mean()
        
        # Crear una gráfica para cada tipo
        for pokemon_type in avg_stats_by_type.index:
            values = avg_stats_by_type.loc[pokemon_type].values
            values = np.append(values, values[0])  # Completar el círculo
            
            angles = np.linspace(0, 2*np.pi, len(stats), endpoint=False)
            angles = np.concatenate((angles, [angles[0]]))  # Completar el círculo
            
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
            ax.plot(angles, values)
            ax.fill(angles, values, alpha=0.25)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(stats)
            plt.title(f'Estadísticas del tipo {pokemon_type}')
            
            plt.tight_layout()
            plt.savefig(f'output/type_stats_{pokemon_type.lower()}.png')
            plt.close()

    def create_type_heatmap(self):
        """Crear un mapa de calor de las estadísticas por tipo"""
        stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total']
        avg_stats = self.df.groupby('Type 1')[stats].mean()
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(avg_stats, annot=True, fmt='.0f', cmap='coolwarm', center=0)
        plt.title('Mapa de Calor: Estadísticas Promedio por Tipo', pad=20)
        plt.tight_layout()
        plt.savefig('output/type_stats_heatmap.png')
        plt.close()

def main():
    print("\n🎨 Iniciando generación de visualizaciones...")
    
    try:
        visualizer = PokemonVisualizer()
        
        print("\n📊 Generando gráficas...")
        
        print("1. Generando gráfica de Pokémon por generación...")
        visualizer.plot_pokemon_by_generation()
        
        print("2. Generando gráfica de distribución de tipos...")
        visualizer.plot_type_distribution()
        
        print("3. Generando gráfica de estadísticas por generación...")
        visualizer.plot_stats_by_generation()
        
        print("4. Generando gráfica de distribución de legendarios...")
        visualizer.plot_legendary_distribution()
        
        print("5. Generando mapa de calor de estadísticas por tipo...")
        visualizer.create_type_heatmap()
        
        print("\n✨ Visualizaciones generadas exitosamente!")
        print("📁 Las gráficas han sido guardadas en la carpeta 'output'")
        
    except Exception as e:
        print(f"\n❌ Error al generar visualizaciones: {str(e)}")
        raise

if __name__ == "__main__":
    main()