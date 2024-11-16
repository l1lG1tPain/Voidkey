import os
from cryptography.fernet import Fernet
from rich.console import Console

console = Console()

def encrypt_file(file_path, password=None):
    if not os.path.exists(file_path):
        console.print("[red]File does not exist.[/red]")
        return

    key = Fernet.generate_key() if not password else Fernet(password.encode())
    cipher = Fernet(key)

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted_data = cipher.encrypt(data)

    with open(file_path + ".enc", "wb") as f:
        f.write(encrypted_data)

    console.print(f"[green]File encrypted successfully:[/green] {file_path}.enc")

    if not password:
        console.print(f"[blue]Encryption key:[/blue] {key.decode()}")
        console.print("[red]Save this key securely to decrypt the file later.[/red]")

def decrypt_file(file_path, password):
    if not os.path.exists(file_path):
        console.print("[red]File does not exist.[/red]")
        return

    if not password:
        console.print("[red]Password is required for decryption.[/red]")
        return

    cipher = Fernet(password.encode())

    try:
        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = cipher.decrypt(encrypted_data)
        original_file_path = file_path.replace(".enc", "")

        with open(original_file_path, "wb") as f:
            f.write(decrypted_data)

        console.print(f"[green]File decrypted successfully:[/green] {original_file_path}")
    except Exception as e:
        console.print(f"[red]Decryption failed:[/red] {e}")

def encrypt_folder(folder_path, password=None):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        console.print("[red]Folder does not exist or is not a directory.[/red]")
        return

    for root, _, files in os.walk(folder_path):
        for file in files:
            encrypt_file(os.path.join(root, file), password)
    console.print("[green]All files in the folder have been encrypted successfully![/green]")

def decrypt_folder(folder_path, password):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        console.print("[red]Folder does not exist or is not a directory.[/red]")
        return

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".enc"):
                decrypt_file(os.path.join(root, file), password)
    console.print("[green]All encrypted files in the folder have been decrypted successfully![/green]")
