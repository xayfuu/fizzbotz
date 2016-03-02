#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import pytest
from os import path

import fizzbotz


@pytest.mark.asyncio
async def test_get_html():
    file_path = path.join(path.dirname(__file__), 'test_files', 'httpbin_html.html')
    with codecs.open(file_path, 'r', 'utf-8') as test_file:
        expected_html = test_file.read()[:-1]  # strip \n from end of file

    assert await fizzbotz.util.get_markup('http://httpbin.org/html') == expected_html


@pytest.mark.asyncio
async def test_buffer():
    class MockItemClass:
        async def get(self):
            return 'foo'

    buffer = fizzbotz.Buffer(MockItemClass(), 3)

    await buffer.populate()
    assert buffer.queue.qsize() == 3

    await buffer.get()
    assert buffer.queue.qsize() == 3
