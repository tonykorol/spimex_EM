import asyncio
import logging
import time

from parser.database_saver import save_to_database
from parser.downloader import Downloader
from parser.file_parser import get_products
from parser.logging_config import setup_logging
from parser.site_parser import SiteParser

setup_logging()

async def main():
    downloader = None
    try:
        start_time = time.time()
        logging.debug(f"Start at {str(start_time)}")

        parser = SiteParser()
        logging.debug(f"Run parser")
        urls = await parser.start()

        downloader = Downloader(urls)
        logging.debug(f"Run downloader")
        await downloader.download()
        logging.debug(f"download time {time.time() - start_time}")

        products = get_products()
        logging.debug(f"Run save to database")
        await save_to_database(products)


    except Exception as e:
        logging.error(f"{e}")
    finally:
        if downloader is not None:  # Проверяем, чтобы избежать ошибки при отсутствии downloader
            logging.debug(f"Delete files")
            await downloader.delete_downloaded_files()
        end_time = time.time()
        logging.debug(f"Сompleted in {end_time - start_time}")



if __name__ == "__main__":
    asyncio.run(main())
