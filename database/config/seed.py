import os
import sys
import inspect
sys.path.append(os.getcwd())
from dotenv import load_dotenv
from database.seeders import *

load_dotenv()

if len(sys.argv) < 2:
    print("Seed command: seed <seeder_class or all>")
    sys.exit(1)
else:
    seeder_name = sys.argv[1]

    if seeder_name == 'all':
        seeders = [cls for name, cls in globals().items() if inspect.isclass(cls)]
        sorted_seeders = sorted(seeders, key=lambda cls: cls.revision)
        
        for seeder in sorted_seeders:
            print(f'INFO  Running {seeder.__name__} seeder')
            seeder()
    else:
        seeder = globals().get(seeder_name)
        print(f'INFO  Running {seeder.__name__} seeder')
        seeder()