import os
import subprocess
from rich.console import Console
from rich.table import Table

console = Console()

def analyze_system():
    console.print("[bold yellow]Analyzing system security...[/bold yellow]\n")

    # SELinux Status
    try:
        selinux_status = subprocess.check_output(["getenforce"], text=True).strip()
        console.print(f"[cyan]SELinux Status:[/cyan] {selinux_status}")
    except FileNotFoundError:
        console.print("[red]SELinux: Not installed or not found.[/red]")

    # Open Ports
    console.print("\n[cyan]Open Ports:[/cyan]")
    try:
        result = subprocess.check_output(["ss", "-tuln"], text=True).splitlines()
        table = Table(title="Open Ports")
        table.add_column("Protocol", style="cyan")
        table.add_column("State", style="green")
        table.add_column("Local Address:Port", style="magenta")
        table.add_column("Peer Address:Port", style="magenta")

        for line in result[1:]:
            parts = line.split()
            if len(parts) >= 5:
                table.add_row(parts[0], parts[1], parts[4], parts[5] if len(parts) > 5 else "-")

        console.print(table)
    except FileNotFoundError:
        console.print("[red]Unable to detect open ports (ss command not found).[/red]")

    # SSH Configuration
    console.print("\n[cyan]SSH Configuration:[/cyan]")
    ssh_config = "/etc/ssh/sshd_config"
    if os.path.exists(ssh_config):
        try:
            with open(ssh_config, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip().startswith("PermitRootLogin"):
                        console.print(f" - {line.strip()}")
        except PermissionError:
            console.print("[red]Permission denied: Cannot read SSH configuration. Run with 'sudo'.[/red]")
    else:
        console.print("[red]SSH configuration file not found.[/red]")

    # Outdated Packages
    console.print("\n[cyan]Outdated Packages:[/cyan]")
    try:
        distro = subprocess.check_output(["lsb_release", "-is"], text=True).strip().lower()
        if "ubuntu" in distro or "debian" in distro:
            subprocess.run(["apt", "list", "--upgradable"])
        elif "fedora" in distro or "centos" in distro:
            subprocess.run(["dnf", "check-update"])
        else:
            console.print("[red]Package manager not supported for this operation.[/red]")
    except Exception as e:
        console.print(f"[red]Error checking for outdated packages:[/red] {e}")
