"""Script to manage users for the SmartHub auth provider."""

import argparse
import asyncio
from collections.abc import Sequence
import logging
import os
from typing import TYPE_CHECKING

from smarthub import runner
from smarthub.auth import auth_manager_from_config
from smarthub.auth.providers import smarthub as hass_auth
from smarthub.config import get_default_config_dir
from smarthub.core import SmartHub
from smarthub.helpers import device_registry as dr, entity_registry as er

# mypy: allow-untyped-calls, allow-untyped-defs


def run(args: Sequence[str] | None) -> None:
    """Handle SmartHub auth provider script."""
    parser = argparse.ArgumentParser(description="Manage SmartHub users")
    parser.add_argument("--script", choices=["auth"])
    parser.add_argument(
        "-c",
        "--config",
        default=get_default_config_dir(),
        help="Directory that contains the SmartHub configuration",
    )

    subparsers = parser.add_subparsers(dest="func")
    subparsers.required = True
    parser_list = subparsers.add_parser("list")
    parser_list.set_defaults(func=list_users)

    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("username", type=str)
    parser_add.add_argument("password", type=str)
    parser_add.set_defaults(func=add_user)

    parser_validate_login = subparsers.add_parser("validate")
    parser_validate_login.add_argument("username", type=str)
    parser_validate_login.add_argument("password", type=str)
    parser_validate_login.set_defaults(func=validate_login)

    parser_change_pw = subparsers.add_parser("change_password")
    parser_change_pw.add_argument("username", type=str)
    parser_change_pw.add_argument("new_password", type=str)
    parser_change_pw.set_defaults(func=change_password)

    asyncio.set_event_loop_policy(runner.HassEventLoopPolicy(False))
    asyncio.run(run_command(parser.parse_args(args)))


async def run_command(args: argparse.Namespace) -> None:
    """Run the command."""
    hass = SmartHub(os.path.join(os.getcwd(), args.config))
    await asyncio.gather(dr.async_load(hass), er.async_load(hass))
    hass.auth = await auth_manager_from_config(hass, [{"type": "smarthub"}], [])
    provider = hass.auth.auth_providers[0]
    await provider.async_initialize()
    await args.func(hass, provider, args)

    # Triggers save on used storage helpers with delay (core auth)
    logging.getLogger("smarthub.core").setLevel(logging.WARNING)

    await hass.async_stop()


async def list_users(
    hass: SmartHub, provider: hass_auth.HassAuthProvider, args: argparse.Namespace
) -> None:
    """List the users."""
    count = 0
    if TYPE_CHECKING:
        assert provider.data
    for user in provider.data.users:
        count += 1
        print(user["username"])

    print()
    print("Total users:", count)


async def add_user(
    hass: SmartHub, provider: hass_auth.HassAuthProvider, args: argparse.Namespace
) -> None:
    """Create a user."""
    if TYPE_CHECKING:
        assert provider.data
    try:
        provider.data.add_auth(args.username, args.password)
    except hass_auth.InvalidUser:
        print("Username already exists!")
        return

    # Save username/password
    await provider.data.async_save()
    print("Auth created")


async def validate_login(
    hass: SmartHub, provider: hass_auth.HassAuthProvider, args: argparse.Namespace
) -> None:
    """Validate a login."""
    if TYPE_CHECKING:
        assert provider.data
    try:
        provider.data.validate_login(args.username, args.password)
        print("Auth valid")
    except hass_auth.InvalidAuth:
        print("Auth invalid")


async def change_password(
    hass: SmartHub, provider: hass_auth.HassAuthProvider, args: argparse.Namespace
) -> None:
    """Change password."""
    if TYPE_CHECKING:
        assert provider.data
    try:
        provider.data.change_password(args.username, args.new_password)
        await provider.data.async_save()
        print("Password changed")
    except hass_auth.InvalidUser:
        print("User not found")
