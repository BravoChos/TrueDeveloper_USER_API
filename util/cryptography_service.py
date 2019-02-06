import logging
import aws_encryption_sdk as aws

class CryptographyService:
    def __init__(self, customer_master_key):
        self.kms_key_provider = aws.KMSMasterKeyProvider(
            key_ids = [customer_master_key]
        )
    
    def encrypt(self, data, encryption_context = { }):
        encrypted_data, encryptor_header = aws.encrypt(
            source             = data,
            key_provider       = self.kms_key_provider,
            encryption_context = encryption_context
        )

        return encrypted_data

    def decrypt(self, encrypted_data):
        decrypted_data, decryptor_header = aws.decrypt(
            source       = encrypted_data,
            key_provider = self.kms_key_provider
        )

        return decrypted_data
