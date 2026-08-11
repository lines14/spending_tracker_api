import os
import sys
from datetime import UTC, datetime

cwd = os.getcwd()

if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("Create seeder command: seeder 'name'")
    sys.exit(1)
else:
    name = sys.argv[1]
    file_name = name.replace(" ", "_")
    class_name = "".join([word.capitalize() for word in name.split()])
    version = datetime.now(UTC).strftime("_%Y_%m_%d_%H%M%S")

    print(f"  Generating /app/db/seeders/{version}_{file_name}.py ...  done")

    content = f"""from db.seeders.base.base_seeder import BaseSeeder
from repositories.base.base_repository import BaseRepository\n
class {class_name}(BaseSeeder):
    revision: str = '{version}'\n
    def __init__(self):
    # Initialize in superconstructor your seeder model
    async def run(self):
        # Get your list of related instances here
        data_list = [
            # Add your seed data here
        ]

        await self.seed(data_list)
"""

    with open(os.path.join(cwd, "db/seeders", version + "_" + file_name + ".py"), "w") as file:
        file.write(content)
