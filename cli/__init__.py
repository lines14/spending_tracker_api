import argparse
import asyncio
import sys

from db.base.base_db import BaseDB
from .currency_rates import CurrencyRates

async def currency_rates_update():
    try:
        await CurrencyRates().update()
    finally:
        await BaseDB.dispose_engine()

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    args = parser.parse_args()
    func = getattr(sys.modules[__name__], args.command, None)

    if not func or not asyncio.iscoroutinefunction(func):
        print(f"ERROR:     Command '{args.command}' not found")
        sys.exit(1)

    asyncio.run(func())