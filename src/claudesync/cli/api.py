import click

from claudesync.provider_factory import get_provider
from ..config_manager import ConfigManager
from ..utils import handle_errors


@click.group()
def api():
    """Manage api."""
    pass


@api.command()
@click.argument("provider", required=False)
@click.pass_obj
@handle_errors
def login(config: ConfigManager, provider):
    """Authenticate with an AI provider."""
    providers = get_provider()
    if not provider:
        click.echo("Available providers:\n" + "\n".join(f"  - {p}" for p in providers))
        return
    if provider not in providers:
        click.echo(
            f"Error: Unknown provider '{provider}'. Available: {', '.join(providers)}"
        )
        return
    provider_instance = get_provider(provider)
    session = provider_instance.login()
    config.set_session_key(session[0], session[1])
    config.set("active_provider", provider)
    click.echo("Logged in successfully.")


@api.command()
@click.pass_obj
def logout(config):
    """Log out from the current AI provider."""
    for key in [
        "session_key",
        "session_key_expiry",
        "active_provider",
        "active_organization_id",
        "active_project_id",
        "active_project_name",
        "local_path",
    ]:
        config.set(key, None)
    click.echo("Logged out successfully.")


@api.command()
@click.option("--delay", type=float, required=True, help="Upload delay in seconds")
@click.pass_obj
@handle_errors
def ratelimit(config, delay):
    """Set the delay between file uploads during sync."""
    if delay < 0:
        click.echo("Error: Upload delay must be a non-negative number.")
        return
    config.set("upload_delay", delay)
    click.echo(f"Upload delay set to {delay} seconds.")


@api.command()
@click.option("--size", type=int, required=True, help="Maximum file size in bytes")
@click.pass_obj
@handle_errors
def max_filesize(config, size):
    """Set the maximum file size for syncing."""
    if size < 0:
        click.echo("Error: Maximum file size must be a non-negative number.")
        return
    config.set("max_file_size", size)
    click.echo(f"Maximum file size set to {size} bytes.")
