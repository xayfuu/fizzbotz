#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aiohttp
import asyncio

async def get_markup(url):
    response = await aiohttp.get(url)
    markup = await response.text()
    return markup


class Buffer:
    def __init__(self, get_item_class, queue_size=20):
        self.queue_size = queue_size
        self.queue = asyncio.Queue(maxsize=self.queue_size)
        self.get_item_class = get_item_class

    async def populate(self):
        for _ in range(self.queue_size):
            await asyncio.ensure_future(self._put_new_entry())

    async def get(self):
        item = await self.queue.get()
        await asyncio.ensure_future(self._put_new_entry())
        return item

    async def _put_new_entry(self):
        item = await self.get_item_class.get()
        self.queue.put_nowait(item)
