import oci

config = oci.config.from_file("config", "DEFAULT")
identity = oci.identity.IdentityClient(config)
user = identity.get_user(config["user"]).data

# Cliente do Oracle Cloud Object Storage
object_storage_client = oci.object_storage.ObjectStorageClient(config)

# Nome do namespace
namespace = object_storage_client.get_namespace().data

# Nome do bucket que você deseja listar
bucket_name = "secure-password"

# Lista os objetos no bucket
list_objects_response = object_storage_client.list_objects(namespace, bucket_name)

# Exibe os nomes dos objetos no bucket
for obj in list_objects_response.data.objects:
    print(obj.name)