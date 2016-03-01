import aiohttp
import asyncio
import html
import random
import re
import string

import bs4

import fizzbotz.util as util
from fizzbotz.exceptions import StringLengthError, EmptyStringError


class TwitchChat:
    _bestoftwitchchat_regex = re.compile('<summary type="text">(.*)</summary>', re.DOTALL)
    _twitchquotes_regex = re.compile('<img class="emoticon" data-emote="(.*?)" src=".*?"/>', re.DOTALL)

    @asyncio.coroutine
    def get_bestoftwitchchat_pasta(self, from_html=None):
        index = random.randint(1, 1104)  # TODO: programmatically discover max index
        url = 'http://www.thebestoftwitch.com/feeds/posts/summary?start-index={}&max-results=1'.format(index)
        if from_html is None:
            text = yield from util.get_markup(url)
        else:
            text = from_html

        raw_pasta = self._bestoftwitchchat_regex.search(text)
        pasta = raw_pasta.group(1)
        return html.unescape(pasta.strip())

    @asyncio.coroutine
    def get_twitchquotes_pasta(self, from_html=None):
        url = 'http://www.twitchquotes.com/random'
        if from_html is None:
            text = yield from util.get_markup(url)
        else:
            text = from_html

        raw_quote = self._twitchquotes_regex.sub(r'\1', text)
        parsed_quote = bs4.BeautifulSoup(raw_quote, 'html.parser')
        pasta = parsed_quote.find('div', class_='show_quote_text_area')
        if pasta is None:
            pasta = parsed_quote.find('span', id="quote_content_")
            return pasta.string.replace(' ', '\n').strip(string.whitespace + "\"")

        return pasta.string.strip(string.whitespace + "\"")

    @asyncio.coroutine
    def get(self):
        pasta_funcs = (self.get_bestoftwitchchat_pasta, self.get_twitchquotes_pasta)
        result = yield from random.choice(pasta_funcs)()
        return result


class Joke:
    _joke_regex = re.compile('(.*?)\n{6}', re.DOTALL)

    @asyncio.coroutine
    def get_oneliner(self, from_html=None):
        url = 'http://www.randomjoke.com/topic/oneliners.php'
        if from_html is None:
            text = yield from util.get_markup(url)
        else:
            text = from_html

        parsed_content = bs4.BeautifulSoup(text, 'html.parser')

        raw_joke = parsed_content.find_all('p')[6].get_text()
        match = self._joke_regex.search(raw_joke)
        return match.group(1).strip()

    @asyncio.coroutine
    def get(self):
        result = yield from self.get_oneliner()
        return result


class Square:
    @staticmethod
    @asyncio.coroutine
    def get_square(string_literal):
        lookup_string = string_literal + string_literal[:-1][::-1]

        string_length = len(string_literal)
        string_list = []

        for idx in range(string_length):
            row_string = lookup_string[idx:string_length + idx]
            string_list.append(' '.join(row_string))

        return '\n'.join(string_list).upper()

    @asyncio.coroutine
    def get(self, string_literal):
        if len(string_literal) > 31:
            raise StringLengthError

        if not string_literal:
            raise EmptyStringError

        square = yield from self.get_square(string_literal)
        return '```\n{}\n```'.format(square)


class Imgur:
    def __init__(self, id_length=5):
        self.id_length = id_length

        self._valid_characters = string.ascii_letters + string.digits
        self._removed_url = 'https://i.imgur.com/removed.png'
        self._base_url = 'https://i.imgur.com/{}.png'

    @asyncio.coroutine
    def get(self):
        while True:
            image_id = ''.join(random.choice(self._valid_characters)
                               for _ in range(self.id_length))
            image_url = self._base_url.format(image_id)

            r = None
            try:
                r = yield from aiohttp.get(image_url)
            except aiohttp.errors.ClientResponseError:
                continue
            finally:
                if r is not None:
                    r.close()

            if r.url != self._removed_url:
                return image_url


class Insult:
    def __init__(self):
        self._insult_url = 'http://www.insultgenerator.org/'

    @asyncio.coroutine
    def get(self, from_html=None):
        if from_html is None:
            text = yield from util.get_markup(self._insult_url)
        else:
            text = from_html

        parsed_insult = bs4.BeautifulSoup(text, 'html.parser')
        return parsed_insult.find('div', class_='wrap').get_text().lstrip()


class Roll:
    _DICE_LIMIT = 5000

    @asyncio.coroutine
    def get(self, dice=None):
        if not dice:
            return str(random.randint(1, 6))

        dice = dice.lower()

        try:
            rolls, limit = map(int, dice.split('d'))
            num_limit_digits = int(len(str(abs(limit))))
            if rolls * num_limit_digits > self._DICE_LIMIT:
                raise StringLengthError

            return ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        except ValueError:
            try:
                return str(random.randint(1, int(dice)))
            except ValueError:
                raise
