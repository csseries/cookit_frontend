from os.path import isfile, dirname, join
from dotenv import load_dotenv

env_path = join(dirname(dirname(__file__)), '.env') # ../.env
load_dotenv(dotenv_path=env_path)
print('Tying to load dotenv from: ', env_path)


version_file = '{}/version.txt'.format(dirname(__file__))

if isfile(version_file):
    with open(version_file) as version_file:
        __version__ = version_file.read().strip()
