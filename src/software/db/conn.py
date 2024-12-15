import psycopg2
import json
from model.OciVault import OciVault

def get_conexao():
    vault_manager = OciVault()
    
    DB_CREDENTIALS_SECRET_ID = "<seu_OCI_secret>" # Substitua pelo seu secret vault OCID
    
    db_credentials = vault_manager.get_secret(DB_CREDENTIALS_SECRET_ID)

    print(f"Conteúdo bruto do vault: '{db_credentials}'")

    db_config = json.loads(db_credentials)
    
    conexao = psycopg2.connect(
        host=db_config['host'],
        port=db_config['port'],
        database=db_config['database'],
        user=db_config['user'],
        password=db_config['password']
    )

    return conexao

def create_database_and_table():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute(open('db/script.sql', 'r').read())
    conexao.commit()
    cursor.close()
    conexao.close()
