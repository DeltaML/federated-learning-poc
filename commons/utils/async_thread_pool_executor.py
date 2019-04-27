import asyncio
import concurrent.futures
import logging

MAX_WORKERS = 5


class AsyncThreadPoolExecutor:

    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)

    async def _main(self, executable, args):
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(self.executor, executable, arg)
            for arg in args
            ]
        return await asyncio.gather(*futures)

    def run(self, executable, args):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(self._main(executable, args))
        loop.close()
        return results
