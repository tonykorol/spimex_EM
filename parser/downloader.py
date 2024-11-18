import asyncio
import os
from datetime import datetime

import aiohttp



class Downloader:
    def __init__(self, urls: list) -> None:
        """
        Функция для инициализации загрузчика.

        Создает папку для загрузки файлов.
        """
        self.filename = None
        self.urls = urls
        download_directory = os.path.join(os.getcwd(), "parser")
        self.download_folder = os.path.join(download_directory, "downloaded_files")
        os.makedirs(self.download_folder, exist_ok=True)

    async def download(self) -> None:
        """
        Функция для загрузки файлов.

        Выполняет асинхронные запросы по ссылкам из списка urls.
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in self.urls:
                task = asyncio.create_task(self.fetch(session, url))
                tasks.append(task)
            await asyncio.gather(*tasks)

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> None:
        """
        Функция для загрузки файла.

        Выполняет асинхронный запрос по ссылке.

        Если запрос успешный, то сохраняет файл в папку вызывая метод save_file
        передавая в качестве аргументов имя файла, созданное функцией filename_creator
        и content - файл.
        """
        async with session.get(f"https://spimex.com{url}") as response:
            if response.status == 200:
                content = await response.read()
                await self.save_file(self.filename_creator(), content)

    async def save_file(self, filename: str, content) -> None:
        """
        Функция для сохранения файлов.

        Сохраняет файл в папку self.download_folder.
        """
        filepath = os.path.join(self.download_folder, filename)
        with open(filepath, "wb") as file:
            file.write(content)

    @staticmethod
    def filename_creator() -> str:
        """
        Функция для создания имени файла.

        Генерирует имя файла с текущей датой и временем.

        Возвращает строку вида "file_2021-06-01_12.00.00.xls
        """
        now = datetime.now()
        return f"file_{now.date()}_{str(now.time()).replace(':', '.')}.xls"

    async def delete_downloaded_files(self) -> None:
        """
        Функция для удаления файлов.

        Удаляет все файлы из папки self.download_folder.
        """
        for filename in os.listdir(self.download_folder):
            try:
                os.remove(os.path.join(self.download_folder, filename))
            except Exception as e:
                print(f"Ошибка удаления файла {filename}\n{e}")
