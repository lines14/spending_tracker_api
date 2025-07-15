# from datetime import datetime
# import asyncio

# def after_update(mapper, connection, target):
#     print(f"[after_update] {target} updated at {datetime.utcnow()}")

#     asyncio.create_task(async_cache_invalidate(target))

# def after_delete(mapper, connection, target):
#     print(f"[after_delete] {target} deleted at {datetime.utcnow()}")

#     asyncio.create_task(async_cleanup(target))

# async def async_cache_invalidate(instance):
#     print(f"Invalidate cache for {instance}")

# async def async_cleanup(instance):
#     print(f"Cleanup for {instance}")

# def after_insert(mapper, connection, target):
#     print(f"[after_insert] New {target} added at {datetime.utcnow()}")

#     asyncio.create_task(async_post_insert_tasks(target))


# async def async_post_insert_tasks(instance):
#     print(f"Running async post-insert tasks for {instance}")