import yaml
import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from const import *
from utils import create_directory

# Caminho para os arquivos YAML
# path = 'data/metrics/'  # ajuste o caminho conforme necessário
files = glob.glob(os.path.join(dataDir + metricsDir, '*.yaml'))

create_directory(graphDir)

# Lista para armazenar os dados
data = []

# Ler todos os arquivos YAML
for file in files:
    with open(file, 'r') as f:
        metrics = yaml.safe_load(f)
        for metric in metrics['metrics']:
            metric_id = int(os.path.splitext(os.path.basename(file))[0].split('_')[1])
            metric['id'] = metric_id
            metric['implementation'] = metric['time']['implementation']
            metric['library'] = metric['time']['library']
            metric['accuracyAll'] = metric['time']['accuracyAll']
            metric['accuracy3'] = metric['time']['accuracy3']
            
            del metric['time']  # remover o dicionário 'time' original
        data.extend(metrics['metrics'])

# Converter os dados em um DataFrame do Pandas
df = pd.DataFrame(data)

# Configurar 'id' como índice
df.set_index('id', inplace=True)
# print(df)

df = df[df.index >= 7]
# print(df)

# Ordenar o DataFrame pelo eixo x (amount)
df = df.sort_values(by='amount')
df['accuracyAll'] = df['accuracyAll'] * 100 
df['accuracy3'] = df['accuracy3'] * 100 
# df['accuracy_3_first_Lib'] = df['accuracy_3_first_Lib'] * 100
# df['accuracy_all_Lib'] = df['accuracy_all_Lib'] * 100
# df['accuracy_3_first_Imp'] = df['accuracy_3_first_Imp'] * 100
# df['accuracy_all_Imp'] = df['accuracy_all_Imp'] * 100
# print(df)


# Calcular a média dos tempos de implementação e biblioteca por 'amount'
df_mean_time_I = df[['implementation', 'amount']].groupby('amount')['implementation'].mean().reset_index()
df_mean_time_I.columns = ['amount', 'mean_time']

df_mean_time_L = df[['library', 'amount']].groupby('amount')['library'].mean().reset_index()
df_mean_time_L.columns = ['amount', 'mean_time']
# print(df)


# Definir valores do eixo x
amount_labels = [ 5, 10, 50, 100, 500, 1000]
amount_ticks = range(len(amount_labels))

# # Mapear 'amount' para índices inteiros
amount_mapping = {amount: index for index, amount in enumerate(amount_labels)}
df['amount_mapped'] = df['amount'].map(amount_mapping)

y_percent_label = labels=[f'{val}%' for val in range(0,121,10)]

# # Criar o gráfico
# plt.figure(figsize=(10, 6))

# # Plotar as linhas
# plt.plot(amount_ticks, df_mean_time_I.set_index('amount').reindex(amount_labels)['mean_time'], linestyle='-', color='cornflowerblue', label='AHP implemented')
# plt.plot(amount_ticks, df_mean_time_L.set_index('amount').reindex(amount_labels)['mean_time'], linestyle='-', color='lightcoral', label='PyDecision')

# # Definir valores do eixo x uniformemente espaçados
# plt.xticks(ticks=amount_ticks, labels=amount_labels, rotation=45)

# # Definir rótulos e título
# plt.xlabel('Providers')
# plt.ylabel('Time (sec)')
# plt.title('Time (sec) AHP implemented x AHP PyDecision')
# plt.grid(True)
# plt.legend(loc='upper left')

# # Salvar o gráfico (comentado para evitar salvar durante o desenvolvimento)
# plt.savefig(graphDir + 'mean_time_vs_amount.png', dpi=300, bbox_inches='tight')

# # Mostrar o gráfico
# # plt.show()

# # Gráfico de Dispersão para 'accuracy_3_first' com 'amount_mapped' no eixo x e linha conectando os pontos
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x=df['amount_mapped'], y=df['accuracy3'], marker='o',color='blue')
# # sns.scatterplot(x='id', y='accuracy_3_first_Lib', data=df, marker='x',color='red', label='PyDecision')

# # plt.plot(df['amount_mapped'], df['accuracy3'], linestyle='-', color='cornflowerblue')

# # Definir valores do eixo x
# plt.xticks(ticks=range(len(amount_labels)), labels=amount_labels)
# # plt.yticks(ticks=range(0,121,20), labels=range(0,121,20))

# plt.xlabel('Number of Providers')
# plt.ylabel('Accuracy')
# plt.title('Accuracy of the first 3')
# plt.grid(True)

# plt.savefig(graphDir + 'accuracy_3_first_vs_amount.png', dpi=300, bbox_inches='tight')

# # plt.show()

# # Gráfico de Dispersão para 'accuracy_all' com 'amount_mapped' no eixo x e linha conectando os pontos
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x='amount_mapped', y='accuracyAll', data=df, marker='o',color='blue')
# # sns.scatterplot(x='id', y='accuracy_3_first_Lib', data=df, marker='x',color='red', label='PyDecision')

# # plt.plot(df['amount_mapped'], df['accuracy_all'], linestyle='-', color='cornflowerblue')

# # Definir valores do eixo x
# plt.xticks(ticks=range(len(amount_labels)), labels=amount_labels)

# # Definir valores do eixo y
# plt.yticks(ticks=range(0,101,20), labels=range(0,101,20))

# plt.xlabel('Number of Providers')
# plt.ylabel('Accuracy (%)')
# plt.title('Accuracy of all')
# plt.grid(True)

# plt.savefig(graphDir + 'accuracy_all_vs_amount.png', dpi=300, bbox_inches='tight')

# # plt.show()

# # Gráfico de Dispersão para 'MSE' com 'amount_mapped' no eixo x e linha conectando os pontos
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x='amount_mapped', y='mse', data=df, marker='o')
# # plt.plot(df['amount_mapped'], df['mse'], linestyle='-', color='cornflowerblue')

# # Warinig: eixo 5 está errado
# # Definir valores do eixo x
# plt.xticks(ticks=range(len(amount_labels)), labels=amount_labels)

# plt.xlabel('Provedores')
# plt.ylabel('Mean Squared Error')
# plt.title('Mean Squared Error x Provedores')
# plt.grid(True)
# # plt.savefig(graphDir + 'Mean_Squared_Error_vs_amount.png', dpi=300, bbox_inches='tight')

# plt.show()

# # Boxplot MSE
# plt.figure(figsize=(10, 6))  # Define o tamanho da figura
# sns.boxplot(x='amount', y='mse', data=df, palette="Set3")  # Cria o boxplot
# plt.title('MSE / Provedores')  # Título do gráfico
# plt.xlabel('Provedores')  # Rótulo do eixo x
# plt.ylabel('MSE')  # Rótulo do eixo y
# # plt.savefig(graphDir + 'boxspot_Mean_Squared_Error_vs_amount.png', dpi=300, bbox_inches='tight')

# plt.show()  # Exibe o gráfico

# # Boxplot Accuracy 3
# # df_melted = pd.melt(df.reset_index(), id_vars='id', value_vars=['accuracy_3_first_Imp', 'accuracy_3_first_Lib'],
#                     # var_name='Provider', value_name='Accuracy')
# plt.figure(figsize=(10, 6))  # Define o tamanho da figura
# sns.boxplot(x='amount_mapped', y='accuracy3', data=df,color='blue')
# # sns.boxplot(x='id', y='accuracy_3_first_Lib', data=df,color='red', label='PyDecision')
# plt.title('Accuracy of the first 3 / Number of Providers')  # Título do gráfico
# plt.xticks(ticks=range(len(amount_labels)), labels=amount_labels)
# plt.xlabel('Number of Providers')
# plt.ylabel('Accuracy')
# plt.grid(True)

# plt.savefig(graphDir + 'boxspot_accuracy_3_vs_amount.png', dpi=300, bbox_inches='tight')

# # plt.show()  # Exibe o gráfico

# Boxplot Accuracy all

# plt.figure(figsize=(10, 6))  # Define o tamanho da figura
# sns.boxplot(x=df.index, y=df['accuracyAll'], data=df,hue='amount')
# plt.title('Accuracy of all / Number of Providers')  # Título do gráfico
# plt.xticks(ticks=range(6), labels=range(1,7))
# # plt.yticks(ticks=range(0,101,10), labels=range(0,101,10))
# plt.xlabel('Number of Providers')  # Rótulo do eixo x
# plt.ylabel('Accuracy (%)')  # Rótulo do eixo y
# plt.grid(True)

# plt.savefig(graphDir + 'boxspot_accuracy_all_vs_amount.png', dpi=300, bbox_inches='tight')
# plt.show()  # Exibe o gráfico

# Boxplot Time
# Criando a figura e os eixos
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

# Boxplot para 'library'
sns.boxplot(x='amount', y='library', data=df, palette="Set3", ax=ax1)
ax1.set_title('Average Time (sec) of PyDecision Library vs Providers')
ax1.set_xlabel('Providers')
ax1.set_ylabel('Time (sec)')

# ticks = np.arange(0, 0.013, 0.002)
# ax1.set_yticks(ticks)
# ax1.set_yticklabels([f'{x:.3f}' for x in ticks])
ax1.grid(True)

# Boxplot para 'implementation'
sns.boxplot(x='amount', y='implementation', data=df, palette="Set3", ax=ax2)
ax2.set_title('Average AHP Implemented Time (sec) x Providers')
ax2.set_xlabel('Providers')
ax2.set_ylabel('Time (sec)')
ax2.grid(True)

# Mostrando o gráfico
ax2.set_yticks(np.arange(0, 0.013, 0.002))
ax2.set_yticklabels([f'{x:.3f}' for x in np.arange(0, 0.013, 0.002)])

# plt.grid(True)
plt.tight_layout()  # Ajusta o layout para evitar sobreposição de rótulos
plt.savefig(graphDir + 'boxspot_library_vs_implementation_vs_amount.png', dpi=300, bbox_inches='tight')

# plt.show()






# Gráfico de Dispersão
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x=df.index, y='accuracy_3_first', data=df, label='Accuracy 3 First')
# sns.scatterplot(x=df.index, y='accuracy_all', data=df, label='Accuracy All')
# sns.scatterplot(x=df.index, y='mse', data=df, label='MSE')
# plt.xlabel('Index')
# plt.ylabel('Values')
# plt.title('Scatter Plot of Metrics')
# plt.legend()
# plt.show()

# Gráfico de Linha
# plt.figure(figsize=(10, 6))
# plt.plot(df.amount, df['accuracy_3_first'], label='Accuracy 3 First')
# # plt.plot(df.index, df['accuracy_all'], label='Accuracy All')
# # plt.plot(df.index, df['mse'], label='MSE')
# plt.xlabel('Index')
# plt.ylabel('Values')
# plt.title('Line Plot of Metrics')
# plt.legend()
# plt.show()