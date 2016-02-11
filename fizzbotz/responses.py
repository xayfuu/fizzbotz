import html
import random
import re
import string

import bs4

import fizzbotz.util as util


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
            raise ValueError('String is too long')

        if not string_literal:
            raise ValueError("Can't generate square from empty string")

        square = await self.get_square(string_literal)
        return '```\n{}\n```'.format(square)


class Imgur:
    def __init__(self, queue_size=20):
        self._image_queue = util.ImageQueue(queue_size)

    async def get(self):
        if self._image_queue.queue.empty():
            await self._image_queue.populate()

        return await self._image_queue.get_image()
