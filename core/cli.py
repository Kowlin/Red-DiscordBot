import argparse
import asyncio

from core.bot import Red


def confirm(m=""):
    return input(m).lower().strip() in ("y", "yes")


def interactive_config(red, token_set, prefix_set):
    loop = asyncio.get_event_loop()
    token = ""

    print("Red - Discord Bot | Configuration process\n")

    if not token_set:
        print("Please enter a valid token:")
        while not token:
            token = input("> ")
            if not len(token) >= 50:
                print("That doesn't look like a valid token.")
                token = ""
            if token:
                loop.run_until_complete(red.db.token.set(token))

    if not prefix_set:
        prefix = ""
        print("\nPick a prefix. A prefix is what you type before a "
              "command. Example:\n"
              "!help\n^ The exclamation mark is the prefix in this case.\n"
              "Can be multiple characters. You will be able to change it "
              "later and add more of them.\nChoose your prefix:\n")
        while not prefix:
            prefix = input("Prefix> ")
            if len(prefix) > 10:
                print("Your prefix seems overly long. Are you sure it "
                      "is correct? (y/n)")
                if not confirm("> "):
                    prefix = ""
            if prefix:
                loop.run_until_complete(red.db.prefix.set([prefix]))

    ask_sentry(red)

    return token


def ask_sentry(red: Red):
    loop = asyncio.get_event_loop()
    print("\nThank you for installing Red V3 alpha! The current version\n"
          " is not suited for production use and is aimed at testing\n"
          " the current and upcoming featureset, that's why we will\n"
          " also collect the fatal error logs to help us fix any new\n"
          " found issues in a timely manner. If you wish to opt in\n"
          " the process please type \"yes\":\n")
    if not confirm("> "):
        loop.run_until_complete(red.db.enable_sentry.set(False))
    else:
        loop.run_until_complete(red.db.enable_sentry.set(True))
        print("\nThank you for helping us with the development process!")


def parse_cli_flags():
    parser = argparse.ArgumentParser(description="Red - Discord Bot")
    parser.add_argument("--owner", type=int,
                        help="ID of the owner. Only who hosts "
                             "Red should be owner, this has "
                             "serious security implications.")
    parser.add_argument("--co-owner", type=int, action="append", default=[],
                        help="ID of a co-owner. Only people who have access "
                             "to the system that is hosting Red should be  "
                             "co-owners, as this gives them complete access "
                             "to the system's data. This has serious "
                             "security implications if misused. Can be "
                             "multiple.")
    parser.add_argument("--prefix", "-p", action="append",
                        help="Global prefix. Can be multiple")
    parser.add_argument("--no-prompt",
                        action="store_true",
                        help="Disables console inputs. Features requiring "
                             "console interaction could be disabled as a "
                             "result")
    parser.add_argument("--no-cogs",
                        action="store_true",
                        help="Starts Red with no cogs loaded, only core")
    parser.add_argument("--self-bot",
                        action='store_true',
                        help="Specifies if Red should log in as selfbot")
    parser.add_argument("--not-bot",
                        action='store_true',
                        help="Specifies if the token used belongs to a bot "
                             "account.")
    parser.add_argument("--dry-run",
                        action="store_true",
                        help="Makes Red quit with code 0 just before the "
                             "login. This is useful for testing the boot "
                             "process.")
    parser.add_argument("--debug",
                        action="store_true",
                        help="Sets the loggers level as debug")
    parser.add_argument("--dev",
                        action="store_true",
                        help="Enables developer mode")

    args = parser.parse_args()

    if args.prefix:
        args.prefix = sorted(args.prefix, reverse=True)
    else:
        args.prefix = []

    return args
