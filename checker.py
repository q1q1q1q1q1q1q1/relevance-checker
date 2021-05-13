import docx
import aiohttp
import asyncio
import loguru


#
# class __SearchEngine:
#     def __init__(self, sentence: str):
#         self._sentence = sentence
#
#
# class GoogleSearch(__SearchEngine):
#     def __init__(self, sentence: str):
#         super().__init__(sentence)

class __Parser:
    def __init__(self, _path: str):
        self._path = _path
        self._full_text = ""
        self._phrases_for_analysis = []
        self._stolen_text = []

    @loguru.logger.catch
    async def analyze(self):
        assert len(self._full_text) > 3, "[ERROR] too little text to analyze"
        tasks = []
        for sentence in self._full_text.split("."):
            if len(sentence.split(" ")) > 4:
                self._phrases_for_analysis.append(sentence)
                tasks.append(asyncio.create_task(self.searcher(sentence)))

        await asyncio.gather(*tasks)

        print(str(len(self._phrases_for_analysis) / len(self._stolen_text)) + "% originality ^^")

    @loguru.logger.catch
    async def searcher(self, sentence: str):
        if await self.googleSearch(sentence):
            self._stolen_text.append(sentence)

    @loguru.logger.catch
    async def googleSearch(self, sentence: str) -> bool:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.google.com/search?q={sentence}", headers=headers) as response:
                if sentence in response.text:
                    return True
            return False

    def __str__(self):
        return self._path

    def __add__(self, other):
        return self._path + "\n" + other


class WordPars(__Parser):
    def __init__(self, _path: str):
        super().__init__(_path)
        doc_x = docx.Document(_path)
        for paragraph in doc_x.paragraphs:
            self._full_text += paragraph.text


class TxtPars(__Parser):
    def __init__(self, _path: str):
        super().__init__(_path)
        with open(_path, 'r', encoding='utf-8') as text:
            self.text = text
