import logging
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup


class SiteParser:
    PAGE_URL = "https://spimex.com/markets/oil_products/trades/results/?page=page-{0}&bxajaxid=d609bce6ada86eff0b6f7e49e6bae904"

    def __init__(self, date_cutoff: datetime = datetime(2022, 12, 31)):
        """
        Инициализирует SiteParser с заданной датой отсечения.

        Args:
            date_cutoff (datetime): Дата, до которой ссылки не будут извлекаться.
        """
        self.date_cutoff = date_cutoff

    async def start(self) -> list:
        """
        Запускает процесс получения ссылок на файлы.

        Эта функция инициирует процесс получения всех ссылок на файлы,
        вызывая метод get_file_links.
        """
        file_links = await self.get_file_links()
        return file_links

    async def fetch_page(self, session: aiohttp.ClientSession, n: int = 1) -> str:
        """
        Получает HTML страницы по заданному номеру страницы
        """
        url = self.PAGE_URL.format(n)
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                raise ValueError(f"Request failed with status code {response.status}")

    def parse_blocks(self, page_html: str) -> list:
        """
        Парсит HTML-код страницы и извлекает ссылки на файлы.
        """
        file_date_block_selector = "div.accordeon-inner__item-inner > div > p > span"
        file_link_block_selector = "div.accordeon-inner__header > a"
        soup = BeautifulSoup(page_html, 'html.parser')
        blocks = soup.find_all(class_="accordeon-inner__item")
        file_links = []
        for block in blocks:
            file_date_str = block.select_one(file_date_block_selector)
            if not file_date_str:
                continue

            file_date_str = file_date_str.text

            try:
                file_date = datetime.strptime(file_date_str, "%d.%m.%Y")
            except ValueError as e:
                logging.error(f"Date parsing error for date '{file_date_str}': {e}")
                continue

            if file_date > self.date_cutoff:
                file_link = block.select_one(file_link_block_selector)["href"]
                file_links.append(file_link)
            else:
                break
        # logging.debug(f"Parsed {len(file_links)} links from the page.")
        return file_links

    async def get_file_links(self) -> list:
        """
        Функция для получения ссылок на файлы.

        Эта функция инициирует процесс получения всех ссылок на файлы,
        вызывая метод fetch_page и parse_blocks.

        Если на странице нет новых ссылок, то процесс завершается и возвращается список
        полученных ссылок.
        """
        async with aiohttp.ClientSession() as session:
            file_links = []
            page_number = 1
            while True:
                page_html = await self.fetch_page(session, page_number)
                new_links = self.parse_blocks(page_html)
                if not new_links:
                    break
                file_links.extend(new_links)
                page_number += 1
            return file_links
