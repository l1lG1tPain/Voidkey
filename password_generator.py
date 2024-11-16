import secrets
import string
from cryptography.fernet import Fernet
from rich.console import Console

console = Console()

def generate_password(length=12, save=False, exclude_similar=False, mnemonic=False):
    if mnemonic:
        # Мнемоническая генерация пароля
        words = ["apple", "orange", "banana", "grape", "kiwi", "peach"]
        password = "-".join(secrets.choice(words) for _ in range(length // 6))
    else:
        characters = string.ascii_letters + string.digits + string.punctuation
        if exclude_similar:
            characters = characters.translate(str.maketrans("", "", "l1IO0"))
        password = ''.join(secrets.choice(characters) for _ in range(length))
    
    console.print(f"[green]Generated Password:[/green] {password}")

    if save:
        key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted_password = cipher.encrypt(password.encode())

        with open("passwords.txt", "wb") as f:
            f.write(key + b"\n" + encrypted_password)

        console.print("[blue]Password saved to 'passwords.txt' (encrypted).[/blue]")
