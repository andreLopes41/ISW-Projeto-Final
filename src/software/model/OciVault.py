import oci
import base64
from pathlib import Path

class OciVault:
    def __init__(self):
        self.config = oci.config.from_file("config", "DEFAULT")
        self.secrets_client = oci.secrets.SecretsClient(self.config)
        self.vault_client = oci.vault.VaultsClient(self.config)
        
    def get_secret(self, secret_id: str) -> str:
        """Recupera um segredo do OCI Vault"""
        try:
            response = self.secrets_client.get_secret_bundle(secret_id)
            base64_content = response.data.secret_bundle_content.content
            decoded_content = base64.b64decode(base64_content).decode()
            return decoded_content
        except Exception as e:
            raise Exception(f"Erro ao recuperar segredo: {str(e)}")