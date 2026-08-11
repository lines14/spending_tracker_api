import asyncio
import inspect
import sys

from dotenv import load_dotenv

import db.seeders as seeders

load_dotenv()


async def main():
    if len(sys.argv) < 2:
        print("Seed command: seed <seeder_class or all>")
        sys.exit(1)
    else:
        seeder_name = sys.argv[1]

        if seeder_name == "all":
            seeders_list = [
                cls for name, cls in inspect.getmembers(seeders, inspect.isclass) if hasattr(cls, "revision")
            ]

            sorted_seeders = sorted(seeders_list, key=lambda cls: cls.revision)

            for seeder in sorted_seeders:
                print(f"INFO  Running {seeder.__name__} seeder")
                await seeder().run()
        else:
            seeder = getattr(seeders, seeder_name, None)

            if not seeder:
                print(f"ERROR  Seeder '{seeder_name}' not found")
                sys.exit(1)

            print(f"INFO  Running {seeder.__name__} seeder")
            await seeder().run()


if __name__ == "__main__":
    asyncio.run(main())
