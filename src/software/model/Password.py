from datetime import datetime
from db.conn import get_conexao, create_database_and_table
from psycopg2 import IntegrityError
import oci
import json
from datetime import datetime, date


class Password:
    def __init__(self, domain=None, password=None, create_at=None):
        self.domain = domain
        self.password = password
        self.create_at = create_at if create_at else datetime.now().date()

    def save(self):
        create_database_and_table()
        conexao = get_conexao()
        cursor = conexao.cursor()
        
        sql = '''
        INSERT INTO records (domain, password, create_at)
        VALUES (%s, %s, %s)
        '''
        
        valores = (self.domain, self.password, self.create_at)
        
        try:
            cursor.execute(sql, valores)
            conexao.commit()
        except IntegrityError:
            cursor.close()
            conexao.close()
            raise ValueError("Domínio já cadastrado no sistema")
        except Exception as e:
            cursor.close()
            conexao.close()
            raise Exception(f"Erro ao salvar senha: {str(e)}")
            
        cursor.close()
        conexao.close()
    
    @staticmethod
    def get():
        conexao = get_conexao()
        cursor = conexao.cursor()
        
        sql = "SELECT * FROM records"
        cursor.execute(sql)
        
        resultados = cursor.fetchall()
        
        passwords = []
        for resultado in resultados:
            password = {
                'id': resultado[0],
                'domain': resultado[1],
                'password': resultado[2],
                'create_at': resultado[3]
            }
            passwords.append(password)
        
        cursor.close()
        conexao.close()
        
        return passwords

    @staticmethod
    def get_by_domain(domain):
        conexao = get_conexao()
        cursor = conexao.cursor()
        
        sql = "SELECT * FROM records WHERE domain = %s"
        cursor.execute(sql, (domain,))
        
        resultado = cursor.fetchone()
        
        if resultado:
            password = {
                'id': resultado[0],
                'domain': resultado[1],
                'password': resultado[2],
                'create_at': resultado[3]
            }
        else:
            password = None
        
        cursor.close()
        conexao.close()
        
        return password
    
    @staticmethod
    def backup_to_bucket():
        
        class DateEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, (date, datetime)):
                    return obj.isoformat()
                return super().default(obj)
        
        config = oci.config.from_file("config", "DEFAULT")
        object_storage_client = oci.object_storage.ObjectStorageClient(config)
        
        namespace = object_storage_client.get_namespace().data
        
        bucket_name = "secure-password"
        
        passwords = Password.get()
        
        backup_data = json.dumps(passwords, cls=DateEncoder)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        object_name = f"senhas_{timestamp}.json"
        
        try:
            object_storage_client.put_object(
                namespace,
                bucket_name,
                object_name,
                bytes(backup_data, 'utf-8')
            )
            return f"Backup realizado com sucesso: {object_name}"
        except Exception as e:
            raise Exception(f"Erro ao realizar backup: {str(e)}")