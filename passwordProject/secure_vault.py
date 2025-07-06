import sqlite3
import base64
from secure_encryption import SecureEncryptionManager

class SecureVault:
    def __init__(self, master_password: str):
        self.master_password = master_password
        self.db = sqlite3.connect('secure_vault.db')
        self.cursor = self.db.cursor()
        self._create_tables()
        self._init_encryption()
    
    def _create_tables(self):
        """Create tables for passwords and salt storage."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vault_meta (
                id INTEGER PRIMARY KEY,
                salt TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.db.commit()
    
    def _init_encryption(self):
        """Initialize encryption with stored salt or create new one."""
        self.cursor.execute('SELECT salt FROM vault_meta LIMIT 1')
        result = self.cursor.fetchone()
        
        if result:
            salt = base64.b64decode(result[0])
            self.encryption = SecureEncryptionManager(self.master_password, salt)
        else:
            self.encryption = SecureEncryptionManager(self.master_password)
            salt_b64 = base64.b64encode(self.encryption.get_salt()).decode()
            self.cursor.execute('INSERT INTO vault_meta (salt) VALUES (?)', (salt_b64,))
            self.db.commit()
    
    def change_master_password(self, new_master_password: str):
        """Change the master password and re-encrypt all passwords."""
        if not new_master_password:
            raise ValueError("New master password cannot be empty")
        
        self.cursor.execute('SELECT id, service, username, password FROM passwords')
        entries = self.cursor.fetchall()
        
        if not entries:
            new_encryption = SecureEncryptionManager(new_master_password)
            new_salt_b64 = base64.b64encode(new_encryption.get_salt()).decode()
            self.cursor.execute('UPDATE vault_meta SET salt = ?', (new_salt_b64,))
            self.encryption = new_encryption
            self.master_password = new_master_password
            self.db.commit()
            return
        
        new_encryption = SecureEncryptionManager(new_master_password)
        
        for entry_id, service, username, encrypted_password in entries:
            old_password = self.encryption.decrypt(encrypted_password)
            new_encrypted_password = new_encryption.encrypt(old_password)
            self.cursor.execute(
                'UPDATE passwords SET password = ? WHERE id = ?',
                (new_encrypted_password, entry_id)
            )
        
        new_salt_b64 = base64.b64encode(new_encryption.get_salt()).decode()
        self.cursor.execute('UPDATE vault_meta SET salt = ?', (new_salt_b64,))
        
        self.encryption = new_encryption
        self.master_password = new_master_password
        
        self.db.commit()
    
    def add_entry(self, service: str, username: str, password: str):
        """Add a new password entry."""
        encrypted_password = self.encryption.encrypt(password)
        self.cursor.execute(
            'INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)',
            (service, username, encrypted_password)
        )
        self.db.commit()
    
    def get_entry(self, service: str):
        """Get a password entry."""
        self.cursor.execute('SELECT username, password FROM passwords WHERE service = ?', (service,))
        row = self.cursor.fetchone()
        if row:
            username, encrypted_password = row
            password = self.encryption.decrypt(encrypted_password)
            return username, password
        return None
    
    def delete_entry(self, service: str):
        """Delete a password entry."""
        self.cursor.execute('DELETE FROM passwords WHERE service = ?', (service,))
        self.db.commit()
    
    def list_services(self):
        """List all services."""
        self.cursor.execute('SELECT service FROM passwords')
        return [row[0] for row in self.cursor.fetchall()]
    
    def search_services(self, query: str):
        """Search services by name."""
        self.cursor.execute('SELECT service FROM passwords WHERE service LIKE ?', (f'%{query}%',))
        return [row[0] for row in self.cursor.fetchall()]
    
    def close(self):
        """Close database connection."""
        self.db.close() 