from django.test import TestCase


# Create your tests here.

from dotenv import load_dotenv
import os


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(script_dir, "dev.env")
    load_dotenv(dotenv_path=dotenv_path)

    user = os.getenv('UserID')
    print(f'User ID: {user}, {type(user)}')

if __name__ == '__main__':
    main()