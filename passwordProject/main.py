import sys
from getpass import getpass
from secure_vault import SecureVault

WELCOME = """
============================
  Secure Password Manager CLI
============================
Commands:
  add      - Add a new password entry
  view     - View a password for a service
  delete   - Delete an entry for a service
  list     - List all saved services
  search   - Search for a service by name
  change-password - Change master password
  exit     - Exit the program
============================
"""

def main():
    print("Welcome to the Secure Password Manager!")
    print("Enter your master password to unlock the vault:")
    
    master_password = getpass("Master password: ")
    if not master_password:
        print("[!] Master password cannot be empty.")
        sys.exit(1)
    
    try:
        vault = SecureVault(master_password)
        print("[+] Vault unlocked successfully!")
    except Exception as e:
        print(f"[!] Failed to unlock vault: {e}")
        print("[!] This might be due to incorrect master password.")
        sys.exit(1)
    
    print(WELCOME)
    
    while True:
        try:
            cmd = input("secure-vault> ").strip().lower()
            
            if cmd == 'add':
                service = input("Service: ").strip()
                username = input("Username: ").strip()
                password = getpass("Password: ")
                vault.add_entry(service, username, password)
                print(f"[+] Entry added for service: {service}")
                
            elif cmd == 'view':
                service = input("Service: ").strip()
                entry = vault.get_entry(service)
                if entry:
                    username, password = entry
                    print(f"Service: {service}")
                    print(f"Username: {username}")
                    print(f"Password: {password}")
                else:
                    print(f"[!] No entry found for service: {service}")
                    
            elif cmd == 'delete':
                service = input("Service: ").strip()
                vault.delete_entry(service)
                print(f"[-] Entry deleted for service: {service}")
                
            elif cmd == 'list':
                services = vault.list_services()
                if services:
                    print("Saved services:")
                    for service in services:
                        print(f"- {service}")
                else:
                    print("[!] No services found.")
                    
            elif cmd == 'search':
                query = input("Search query: ").strip()
                results = vault.search_services(query)
                if results:
                    print("Search results:")
                    for service in results:
                        print(f"- {service}")
                else:
                    print(f"[!] No services found matching: {query}")
                    
            elif cmd == 'change-password':
                print("Change Master Password")
                print("===================")
                new_password = getpass("Enter new master password: ")
                confirm_password = getpass("Confirm new master password: ")
                
                if new_password != confirm_password:
                    print("[!] Passwords do not match. Try again.")
                    continue
                
                if not new_password:
                    print("[!] New password cannot be empty.")
                    continue
                
                try:
                    vault.change_master_password(new_password)
                    print("[+] Master password changed successfully!")
                    print("[!] All stored passwords have been re-encrypted.")
                except Exception as e:
                    print(f"[!] Failed to change master password: {e}")
                    
            elif cmd == 'exit':
                vault.close()
                print("Goodbye!")
                break
                
            else:
                print("[!] Unknown command. Type one of: add, view, delete, list, search, change-password, exit.")
                
        except KeyboardInterrupt:
            print("\n[!] Exiting.")
            vault.close()
            break
        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    main() 