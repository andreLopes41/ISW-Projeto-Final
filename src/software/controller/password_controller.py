from model.Password import Password
from pathlib import Path
from model.FernetHasher import FernetHasher

class PasswordController:
    def __init__(self):
        self.key_path = Path(FernetHasher.KEY_DIR / 'key.key')
        self.is_first_password = not self.key_path.exists()
        
        if self.is_first_password:
            self.key, _ = FernetHasher.create_key()
            self.key_path = FernetHasher.archive_key(self.key)
        else:
            with open(self.key_path, 'rb') as arq:
                self.key = arq.read()
        
        self.hasher = FernetHasher(self.key)
    
    def create_password(self, domain: str, password: str) -> tuple[bool, str]:
        """Cria uma nova senha criptografada no banco de dados"""
        try:
            encrypted_password = self.hasher.encrypt(password)
            password_obj = Password(
                domain=domain,
                password=encrypted_password.decode()
            )
            password_obj.save()

            Password.backup_to_bucket()
            
            if self.is_first_password:
                return True, self.key.decode()
            return False, ""
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Erro ao criar senha: {str(e)}")
    
    def get_password(self, domain: str, access_key: str) -> str:
        """Recupera e descriptografa a senha de um domínio específico"""
        try:
            with open(self.key_path, 'rb') as arq:
                stored_key = arq.read()
            
            if access_key.encode() != stored_key:
                return "Chave de acesso inválida"
            
            password_data = Password.get_by_domain(domain)
            if password_data:
                decrypted_password = self.hasher.decrypt(password_data['password'])
                return decrypted_password
            return "Senha não encontrada"
            
        except Exception as e:
            return f"Erro ao recuperar senha: {str(e)}"
    
    def list_passwords(self) -> list:
        """Lista todas as senhas com seus domínios"""
        passwords = Password.get()
        decrypted_passwords = []
        
        for pwd in passwords:
            decrypted_pwd = pwd.copy()
            decrypted_pwd['password'] = self.hasher.decrypt(pwd['password'])
            decrypted_passwords.append(decrypted_pwd)
        
        return decrypted_passwords