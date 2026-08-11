import subprocess
import sys
from datetime import UTC, datetime


def create_migration(name, version):
    command = ["alembic", "revision", "--message", name, "--rev-id", version]

    subprocess.run(command, check=True)


if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("Create migration command: migration 'name'")
    sys.exit(1)
else:
    name = sys.argv[1]
    version = datetime.now(UTC).strftime("_%Y_%m_%d_%H%M%S")
    create_migration(name, version)
