import hashlib
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureEncryptionManager:
    def __init__(self, master_password: str, salt: bytes | None = None):
        """
        Initialize encryption manager with user's master password.
        If salt is None, generate a new one (for first-time setup).
        """
        if salt is None:
            self.salt = os.urandom(16)
        else:
            self.salt = salt
            
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        self.fernet = Fernet(key)
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext using derived key."""
        return self.fernet.encrypt(plaintext.encode()).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt ciphertext using derived key."""
        return self.fernet.decrypt(ciphertext.encode()).decode()
    
    def get_salt(self) -> bytes:
        """Get the salt for storage/retrieval."""
        return self.salt 