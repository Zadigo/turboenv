import argparse
import pathlib
import os

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='TurboEnv: A tool for managing environment variables.')

    argparser.add_argument(
        '-l',
        '--list-files',
        action='store_true',
        help='List all the files in the current directory that end with .env'
    )

    namespace = argparser.parse_args()

    if namespace.list_files:
        current_dir = pathlib.Path(os.getcwd())
        files = current_dir.glob('*.env')
        for file in files:
            print(f'  * {file}')
