#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import aiohttp
import asyncio
import random
import string


async def get_markup(url):
    response = await aiohttp.get(url)
    markup = await response.text()
    return markup


class Buffer:
    def __init__(self, queue_size=20):
        """

        Args:
            queue_size:
        """
        self.queue_size = queue_size
        self.queue = asyncio.Queue(maxsize=self.queue_size)

    async def populate(self):
        for _ in range(self.queue_size):
            await asyncio.ensure_future(self._put_new_entry())

    async def get(self):
        item = await self.queue.get()
        await asyncio.ensure_future(self._put_new_entry())
        return item

    async def _put_new_entry(self):
        item = await self._get_item()
        self.queue.put_nowait(item)

    @abc.abstractmethod
    async def _get_item(self):
        return NotImplementedError  # pragma: no cover


class ImageBuffer(Buffer):
    _imgur_url = 'https://i.imgur.com/{}.png'
    _removed_url = 'https://i.imgur.com/removed.png'
    _valid_characters = string.ascii_letters + string.digits
    _id_length = 5

    async def _get_item(self):
        """

        Returns:

        """
        while True:
            image_id = ''.join(random.choice(self._valid_characters) for _ in range(self._id_length))
            image_url = self._imgur_url.format(image_id)

            r = None
            try:
                r = await aiohttp.get(image_url)
            except aiohttp.errors.ClientResponseError:
                continue
            finally:
                if r is not None:
                    r.close()

            if r.url != self._removed_url:
                return image_url
