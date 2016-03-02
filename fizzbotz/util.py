import aiohttp
import asyncio


@asyncio.coroutine
def get_markup(url):
    response = yield from aiohttp.get(url)
    markup = yield from response.text()
    return markup


class Buffer:
    def __init__(self, get_item_class, queue_size=20):
        self.queue_size = queue_size
        self.queue = asyncio.Queue(maxsize=self.queue_size)
        self.get_item_class = get_item_class

    @asyncio.coroutine
    def populate(self):
        for _ in range(self.queue_size):
            yield from asyncio.ensure_future(self._put_new_entry())

    @asyncio.coroutine
    def get(self):
        item = yield from self.queue.get()
        yield from asyncio.ensure_future(self._put_new_entry())
        return item

    @asyncio.coroutine
    def _put_new_entry(self):
        item = yield from self.get_item_class.get()
        self.queue.put_nowait(item)
