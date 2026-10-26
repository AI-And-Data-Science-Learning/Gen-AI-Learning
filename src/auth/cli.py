"""Command-line demo for the auth module.

Usage:
    python -m src.auth.cli register alice
    python -m src.auth.cli login alice
"""

import argparse
import getpass
import sys

from src.auth import AuthError, AuthService


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m src.auth.cli")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("register", "login"):
        sub.add_parser(name).add_argument("username")
    args = parser.parse_args(argv)

    service = AuthService()
    password = getpass.getpass("Password: ")

    try:
        if args.command == "register":
            if getpass.getpass("Confirm password: ") != password:
                print("Passwords do not match.")
                return 1
            username = service.register(args.username, password)
            print(f"User '{username}' registered.")
        else:
            user = service.login(args.username, password)
            print(f"Login successful. Welcome, {user.username}!")
    except AuthError as error:
        print(f"Error: {error}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
