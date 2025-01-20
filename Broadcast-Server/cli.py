import urllib.request
import json
import argparse
import client
import server



def main():
    # Create the main parser
    parser = argparse.ArgumentParser(description="Broadcast Server")

    # Create a set of subcommands with 'required=True'
    subparsers = parser.add_subparsers(title='Commands',description='Available commands',dest='start or connect',required=True)

    # 'start' command
    parser_start = subparsers.add_parser('start',help='This command will start the server.')
    parser_start.set_defaults(func=server.start_command)

    # 'connect' command
    parser_connect = subparsers.add_parser('connect',help='This command will connect the client to the server.')
    parser_connect.set_defaults(func=client.connect_command)

    # Parse the arguments
    args = parser.parse_args()

    # Execute the function corresponding to the command
    args.func(args)


if __name__ == "__main__":
    main()
