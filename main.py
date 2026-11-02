import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar el dataset original
csv_file = 'living (6) (3).csv'
df = pd.read_csv(csv_file)

# 2. Generar el archivo costo_vida.sql automáticamente desde los datos
sql_statements = [
    """CREATE TABLE IF NOT EXISTS costo_vida (
    id INT PRIMARY KEY,
    pais VARCHAR(100) NOT NULL,
    costo_vida_2017 DECIMAL(5,2) NOT NULL,
    ranking_global INT NOT NULL,
    datos_disponibles VARCHAR(50),
    continente VARCHAR(50)
);"""
]

for idx, row in df.iterrows():
    country = str(row['Countries']).replace("'", "''")
    continent = str(row['Continent']).replace("'", "''")
    avail = str(row['Available data']).replace("'", "''")
    sql = f"INSERT INTO costo_vida (id, pais, costo_vida_2017, ranking_global, datos_disponibles, continente) VALUES ({int(row['Unnamed: 0']) + 1}, '{country}', {row['Cost of living, 2017']}, {int(row['Global rank'])}, '{avail}', '{continent}');"
    sql_statements.append(sql)

with open('costo_vida.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(sql_statements))
print("[OK] Archivo 'costo_vida.sql' generado exitosamente.")

# 3. Conectar a una base de database SQLite local y cargar el script .sql creado
conn = sqlite3.connect('costo_vida.db')
cursor = conn.cursor()

# Ejecutar el archivo SQL para poblar la base de datos relacional
with open('costo_vida.sql', 'r', encoding='utf-8') as f:
    conn.executescript(f.read())

# 4. Consulta SQL analítica correcta (usando los nombres reales de la tabla SQL: 'pais')
query_peru = "SELECT pais, costo_vida_2017, ranking_global, continente FROM costo_vida WHERE pais LIKE '%Peru%'"
print("\n--- Resultado de Consulta SQL para Perú ---")
print(pd.read_sql(query_peru, conn))

# 5. Generación de Visualizaciones (Gráficos)
sns.set_theme(style="whitegrid")

# Gráfica 1: Top 10 países con mayor costo de vida
top_10_high = df.nlargest(10, 'Cost of living, 2017')
plt.figure(figsize=(10, 6))
sns.barplot(x='Cost of living, 2017', y='Countries', data=top_10_high, palette='Reds_r')
plt.title('Top 10 Países con Mayor Costo de Vida (2017)')
plt.xlabel('Índice de Costo de Vida')
plt.ylabel('País')
plt.tight_layout()
plt.savefig('top_10_highest.png')
plt.close()

# Gráfica 2: Top 10 países con menor costo de vida
top_10_low = df.nsmallest(10, 'Cost of living, 2017')
plt.figure(figsize=(10, 6))
sns.barplot(x='Cost of living, 2017', y='Countries', data=top_10_low, palette='Blues_r')
plt.title('Top 10 Países con Menor Costo de Vida (2017)')
plt.xlabel('Índice de Costo de Vida')
plt.ylabel('País')
plt.tight_layout()
plt.savefig('top_10_lowest.png')
plt.close()

# Gráfica 3: Costo de vida en los países de América
americas = df[df['Continent'].str.contains('America', case=False, na=False)].sort_values(by='Cost of living, 2017', ascending=False)
plt.figure(figsize=(12, 8))
sns.barplot(x='Cost of living, 2017', y='Countries', data=americas, palette='viridis')
plt.title('Costo de Vida en Países de América (2017)')
plt.xlabel('Índice de Costo de Vida')
plt.ylabel('País')
plt.tight_layout()
plt.savefig('americas_cost_of_living.png')
plt.close()

# Cerrar conexión a la base de datos
conn.close()

print("\n[OK] ¡Todas las consultas SQL y gráficas (.png) se han generado y guardado correctamente!")