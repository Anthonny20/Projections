import os
import shutil
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

#Caminho padrão do arquivo de destino
user_dir = os.path.expanduser('~')
kaggle_dir = os.path.join(user_dir, ".kaggle")
kaggle_json_path = os.path.join(kaggle_dir, 'kaggle.json')
downloads_path = os.path.join(user_dir, "Downloads")
kaggle_json_downloaded = os.path.join(downloads_path, 'kaggle.json')

# Passo 1: Garante que a pasta .kaggle existe
os.makedirs(kaggle_dir, exist_ok=True)

#Passo 2: Move o kaggle.json da pasta Downloads (se necessário)
if not os.path.exists(kaggle_json_path) and os.path.exists(kaggle_json_downloaded):
    shutil.move(kaggle_json_downloaded, kaggle_json_path)
    print(f'Arquivo kaggle.json movido para {kaggle_json_path}')

#Passo 3: Verifica se o arquivo agora está lá
if not os.path.exists(kaggle_json_path):
    raise FileNotFoundError('Arquivo kaggle.json não encontrado! ')

#Passo 4: Faz download dos dados da competição
api = KaggleApi()
api.authenticate()

competicao = "store-sales-time-series-forecasting"
pasta_destino = 'favorita-ruptura-estoque\\data'
os.makedirs(pasta_destino, exist_ok=True)

print(f"Baixando arquivos da competicao '{competicao}'...")
api.competition_download_files(competicao, path=pasta_destino)

#Passo 5: Descompacta os arquivos
zip_path = os.path.join(pasta_destino, f"{competicao}.zip")
if os.path.exists(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(pasta_destino)
    os.remove(zip_path)
    print(f"Arquivos extraídos para: {pasta_destino}")
else:
    print(f"Nenhum arquivo ZIP encontrado para extrair")