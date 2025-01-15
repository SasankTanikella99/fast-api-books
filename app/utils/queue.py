# app/utils/queue.py
import asyncio

# Single shared queue instance
book_updates_queue = asyncio.Queue()