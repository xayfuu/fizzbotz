import aiohttp
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

    async def get_bestoftwitchchat_pasta(self, from_html=None):
        index = random.randint(1, 1104)  # TODO: programmatically discover max index
        url = 'http://www.thebestoftwitch.com/feeds/posts/summary?start-index={}&max-results=1'.format(index)
        text = await util.get_markup(url) if from_html is None else from_html

        raw_pasta = self._bestoftwitchchat_regex.search(text)
        pasta = raw_pasta.group(1)
        return html.unescape(pasta.strip())

    async def get_twitchquotes_pasta(self, from_html=None):
        url = 'http://www.twitchquotes.com/random'
        text = await util.get_markup(url) if from_html is None else from_html

        raw_quote = self._twitchquotes_regex.sub(r'\1', text)
        parsed_quote = bs4.BeautifulSoup(raw_quote, 'html.parser')
        pasta = parsed_quote.find('div', class_='show_quote_text_area')
        if pasta is None:
            pasta = parsed_quote.find('span', id="quote_content_")
            return pasta.string.replace(' ', '\n').strip(string.whitespace + "\"")

        return pasta.string.strip(string.whitespace + "\"")

    async def get(self):
        pasta_funcs = (self.get_bestoftwitchchat_pasta, self.get_twitchquotes_pasta)
        return await random.choice(pasta_funcs)()


class Joke:
    _joke_regex = re.compile('(.*?)\n{6}', re.DOTALL)

    async def get_oneliner(self, from_html=None):
        url = 'http://www.randomjoke.com/topic/oneliners.php'
        text = await util.get_markup(url) if from_html is None else from_html

        parsed_content = bs4.BeautifulSoup(text, 'html.parser')

        raw_joke = parsed_content.find_all('p')[6].get_text()
        match = self._joke_regex.search(raw_joke)
        return match.group(1).strip()

    async def get(self):
        return await self.get_oneliner()


class Square:
    @staticmethod
    async def get_square(string_literal):
        lookup_string = string_literal + string_literal[:-1][::-1]

        string_length = len(string_literal)
        string_list = []

        for idx in range(string_length):
            row_string = lookup_string[idx:string_length + idx]
            string_list.append(' '.join(row_string))

        return '\n'.join(string_list).upper()

    async def get(self, string_literal):
        if len(string_literal) > 31:
            raise StringLengthError

        if not string_literal:
            raise EmptyStringError

        square = await self.get_square(string_literal)
        return '```\n{}\n```'.format(square)


class Imgur:
    def __init__(self, id_length=5):
        self.id_length = id_length

        self._valid_characters = string.ascii_letters + string.digits
        self._removed_url = 'https://i.imgur.com/removed.png'
        self._base_url = 'https://i.imgur.com/{}.png'

    async def get(self):
        while True:
            image_id = ''.join(random.choice(self._valid_characters)
                               for _ in range(self.id_length))
            image_url = self._base_url.format(image_id)

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


class Insult:
    def __init__(self):
        self._insult_url = 'http://www.insultgenerator.org/'

    async def get(self, from_html=None):
        text = await util.get_markup(self._insult_url) if from_html is None else from_html

        parsed_insult = bs4.BeautifulSoup(text, 'html.parser')
        return parsed_insult.find('div', class_='wrap').get_text().lstrip()


class Roll:
    _DICE_LIMIT = 5000
    async def get(self, dice=None):
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
