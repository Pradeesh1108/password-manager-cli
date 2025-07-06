# 🔐 Secure Password Manager CLI

A production-ready, secure password manager built with Python, featuring PBKDF2 key derivation, SQLite3 storage, and Fernet encryption. This project demonstrates advanced security practices, OOP principles, and design patterns.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- macOS/Linux/Windows

### Installation

1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   python3 -m pip install --break-system-packages -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python3 main.py
   ```
4. **Set your master password** when prompted (first time only)

### First-Time Setup
When you run the password manager for the first time, you will be prompted to create your own master password. This password is never stored anywhere—if you forget it, you cannot recover your vault.

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `add` | Add a new password entry |
| `view` | View a password for a service |
| `delete` | Delete an entry for a service |
| `list` | List all saved services |
| `search` | Search for a service by name |
| `change-password` | Change master password |
| `exit` | Exit the program |

## 🔒 Security Features

### 🔐 Cryptographic Security
- **PBKDF2 Key Derivation**: 100,000 iterations with SHA-256
- **Random Salt**: 16-byte unique salt per vault prevents rainbow table attacks
- **Fernet Encryption**: AES-128-CBC with HMAC-SHA256 authentication
- **No Hardcoded Secrets**: Master password never stored, only used for key derivation

### 🛡️ Security Practices
- **Secure Input**: Hidden password input using `getpass`
- **Atomic Operations**: Database transactions ensure data integrity
- **Error Handling**: Graceful handling of cryptographic failures
- **Re-encryption**: All passwords re-encrypted when master password changes

### 🔄 Master Password Management
- **User-Defined**: Set your own master password (no hardcoded defaults)
- **Changeable**: Built-in command to change master password
- **Secure Storage**: Only derived keys and salts are stored

## 🏗️ Architecture

### 📁 Project Structure
```
passwordProject/
├── main.py                 # CLI interface and user interaction
├── secure_vault.py         # Database operations and vault management
├── secure_encryption.py    # PBKDF2 key derivation and Fernet encryption
├── database.py            # Legacy singleton database connection
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
└── .vscode/
    └── settings.json     # VSCode configuration
```

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `cryptography` | Latest | Fernet encryption and PBKDF2 key derivation |
| `sqlite3` | Built-in | Database operations |
| `getpass` | Built-in | Secure password input |
| `base64` | Built-in | Binary data encoding |
| `os` | Built-in | Random salt generation |

## 🛠️ Development Setup

### VSCode Configuration
The `.vscode/settings.json` file configures:
- Python interpreter path
- Site-packages inclusion
- Type checking settings

### Running Tests
```bash
# Test encryption
python3 -c "from secure_encryption import SecureEncryptionManager; print('Encryption works!')"

# Test database
python3 -c "from secure_vault import SecureVault; print('Database works!')"
```

## 🔍 Troubleshooting

### Common Issues

#### Import Errors
- **Problem**: "Import cryptography could not be resolved"
- **Solution**: Install dependencies with `--break-system-packages` flag
- **Alternative**: Use virtual environment

#### Password Input Issues
- **Problem**: Can't type password in terminal
- **Solution**: Use native terminal (not IDE terminal)
- **Alternative**: Use `input()` instead of `getpass()` for development

#### Database Errors
- **Problem**: "Failed to unlock vault"
- **Solution**: Check if master password is correct
- **Alternative**: Delete `secure_vault.db` to start fresh

### Performance Notes
- **PBKDF2 iterations**: 100,000 iterations may take 1-2 seconds
- **Database size**: Minimal, encrypted passwords are compact
- **Memory usage**: Low, only loads requested data

## 🚨 Security Considerations

### Production Use
- ✅ **Suitable for personal use**
- ✅ **Industry-standard cryptography**
- ✅ **No known vulnerabilities**

### Limitations
- ⚠️ **Single-user only** (no multi-user support)
- ⚠️ **Local storage only** (no cloud sync)
- ⚠️ **No backup features** (manual database backup required)

### Best Practices
1. **Strong Master Password**: Use 16+ characters with mixed types
2. **Regular Backups**: Copy `secure_vault.db` to safe location
3. **Secure Environment**: Run on trusted machine only
4. **Regular Updates**: Keep cryptography package updated

## 📈 Future Enhancements

### Potential Features
- [ ] Cloud synchronization
- [ ] Multi-user support
- [ ] Password strength analysis
- [ ] Automatic backups
- [ ] Browser integration
- [ ] Mobile app companion

### Security Improvements
- [ ] Argon2 key derivation (more memory-hard)
- [ ] Hardware security module (HSM) support
- [ ] Zero-knowledge architecture
- [ ] Audit logging

## 📄 License

This project is for educational and personal use. The cryptography library is licensed under Apache 2.0.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review security considerations
3. Test with minimal example
4. Report detailed error messages

---

**🔐 Remember**: Your master password is the key to all your stored passwords. Keep it secure and never share it! 