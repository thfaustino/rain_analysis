import pandas as pd


## CARREGA DADOS
mco = pd.read_csv('db\\mco_final.csv',sep=";")
rain = pd.read_excel('db\\rain_final.xlsx')


rain['hora'] = rain['hora'].astype(str).str[:2]
rain['key'] = rain['data'].astype(str) +'-'+ rain['hora'].astype(int).astype(str)


mco['data'] = pd.to_datetime(mco['data'], format='%d/%m/%Y')
mco['key'] = mco['data'].dt.strftime('%Y-%m-%d') +'-'+ mco['faixa_horaria'].astype(int).astype(str)


# merge mco with rain on the 'key' column, using only classificacao and rain_mm columns from rain
mco = mco.merge(rain[['key', 'classificacao', 'rain_mm']], on='key', how='left')
mco['linha'].unique()


mco['sublinha'].unique()
mco = mco[(mco['linha'] == '3302A') & (mco['sublinha'] == 1) & (mco['pc'] == 1)]
mco['data_hora'] = pd.to_datetime(mco['data'].dt.strftime('%Y-%m-%d') + ' ' + mco['faixa_horaria'].astype(str) + ':00:00', format='%Y-%m-%d %H:%M:%S')
mco = mco[mco['tempo_min'] > 60]
mco['tempo_min'].quantile(.005)
mco['tempo_min'] = mco['tempo_min']>=mco['tempo_min'].quantile(.005) # remove outliers



import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(mco['rain_mm'], mco['tempo_mean'], alpha=0.6)
ax.set_xlabel('rain_mm (mm)')
ax.set_ylabel('tempo_mean (minutes)')
ax.set_title('Tempo Médio vs Chuva')
plt.tight_layout()
plt.show()




mco.describe()

ax = mco['tempo_min'].hist(bins=10, figsize=(10, 6), edgecolor='black')
ax.set_xlabel('tempo_min (minutes)')
ax.set_ylabel('Frequency')
ax.set_title('Distribuição de Tempo Mínimo')
plt.tight_layout()
plt.show()

# Agrupa por data_hora e calcula demanda e máximo de rain_mm
ts_data = mco.groupby('data_hora').agg({'tempo_mean': 'mean', 'rain_mm': 'max', 'classificacao': 'first'}).reset_index()
ts_data.columns = ['data_hora', 'tempo_mean', 'rain_mm_max', 'classificacao']

# Agrupa por hora e classifica por dias com chuva
ts_data['hora'] = ts_data['data_hora'].dt.hour
ts_data['data'] = ts_data['data_hora'].dt.date

# Identifica dias com chuva
dias_chuva = ts_data[ts_data['rain_mm_max'] > 0]['data'].unique()
ts_data['tem_chuva'] = ts_data['data'].isin(dias_chuva)

# Agrupa por hora e classificação
hourly_data = ts_data.groupby(['hora', 'classificacao']).agg({'tempo_mean': 'mean', 'rain_mm_max': 'mean'}).reset_index()

fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot cada classificação com uma cor diferente
for classificacao in hourly_data['classificacao'].unique():
    data = hourly_data[hourly_data['classificacao'] == classificacao]
    ax1.plot(data['hora'], data['tempo_mean'], linewidth=2, label=f'Tempo Médio - {classificacao}', marker='o')

ax1.set_xlabel('Hora do Dia')
ax1.set_ylabel('Tempo Médio (min)')
ax1.legend(loc='upper left')

fig.suptitle(f'Série Temporal por Hora: Tempo Médio vs Chuva\n(Dias com Chuva: {len(dias_chuva)})')
plt.tight_layout()
plt.show()

mco.head()




# Agrupa por data_hora e calcula demanda e máximo de rain_mm
ts_data = mco.groupby('data_hora').agg({'n_vrread': 'mean', 'rain_mm': 'max', 'classificacao': 'first'}).reset_index()
ts_data.columns = ['data_hora', 'n_vrread', 'rain_mm_max', 'classificacao']

# Agrupa por hora e classifica por dias com chuva
ts_data['hora'] = ts_data['data_hora'].dt.hour
ts_data['data'] = ts_data['data_hora'].dt.date

# Identifica dias com chuva
dias_chuva = ts_data[ts_data['rain_mm_max'] > 0]['data'].unique()
ts_data['tem_chuva'] = ts_data['data'].isin(dias_chuva)

# Agrupa por hora e classificação
hourly_data = ts_data.groupby(['hora', 'classificacao']).agg({'n_vrread': 'mean', 'rain_mm_max': 'mean'}).reset_index()

fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot cada classificação com uma cor diferente
for classificacao in hourly_data['classificacao'].unique():
    data = hourly_data[hourly_data['classificacao'] == classificacao]
    ax1.plot(data['hora'], data['n_vrread'], linewidth=2, label=f'Número de VRRead - {classificacao}', marker='o')

ax1.set_xlabel('Hora do Dia')
ax1.set_ylabel('Número de VRRead')
ax1.legend(loc='upper left')

fig.suptitle(f'Série Temporal por Hora: Tempo Médio vs Chuva\n(Dias com Chuva: {len(dias_chuva)})')
plt.tight_layout()
plt.show()



# Agrupa por data_hora e calcula demanda e máximo de rain_mm
ts_data = mco.groupby('data_hora').agg({'usuarios_mean': 'mean', 'rain_mm': 'max', 'classificacao': 'first'}).reset_index()
ts_data.columns = ['data_hora', 'usuarios_mean', 'rain_mm_max', 'classificacao']

# Agrupa por hora e classifica por dias com chuva
ts_data['hora'] = ts_data['data_hora'].dt.hour
ts_data['data'] = ts_data['data_hora'].dt.date

# Identifica dias com chuva
dias_chuva = ts_data[ts_data['rain_mm_max'] > 0]['data'].unique()
ts_data['tem_chuva'] = ts_data['data'].isin(dias_chuva)

# Agrupa por hora e classificação
hourly_data = ts_data.groupby(['hora', 'classificacao']).agg({'usuarios_mean': 'mean', 'rain_mm_max': 'mean'}).reset_index()

fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot cada classificação com uma cor diferente
for classificacao in hourly_data['classificacao'].unique():
    data = hourly_data[hourly_data['classificacao'] == classificacao]
    ax1.plot(data['hora'], data['usuarios_mean'], linewidth=2, label=f'Número de Usuários - {classificacao}', marker='o')

ax1.set_xlabel('Hora do Dia')
ax1.set_ylabel('Número de Usuários')
ax1.legend(loc='upper left')

fig.suptitle(f'Série Temporal por Hora: Número de Usuários vs Chuva\n(Dias com Chuva: {len(dias_chuva)})')
plt.tight_layout()
plt.show()