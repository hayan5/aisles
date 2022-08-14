import gzip
from tempfile import TemporaryFile

from requests import RequestException, Session

from aisles.logger import get_logger

logger = get_logger(__name__)


def fetch_data_uncompressed(
    url: str,
    session: Session,
    timeout: float = 3.0,
) -> bytes:

    logger.debug("Downloading Data from url: %s", url)
    try:
        with session.get(url, timeout=timeout) as response:
            response.raise_for_status()
            logger.debug(
                "Successfully Retrieved Data, Status Code: %s",
                str(response.status_code),
            )

            return response.content

    except RequestException as e:
        logger.error(
            "An error occurred downloading data from %s \n Cause of error: %s",
            url,
            e,
        )
        raise Exception(
            f"An error occurred downloading data from {url} \n \
            Cause of error:{e}",
        )


def fetch_data_compressed(
    url: str,
    session: Session,
    timeout: float = 3.0,
) -> bytes:

    logger.debug("Downloading Data from url: %s", url)
    try:
        with session.get(url, timeout=timeout, stream=True) as response:
            response.raise_for_status()
            logger.info("Decompressing Data from url: %s", url)
            with TemporaryFile("w+b") as temp_file:
                for chunk in response.raw.stream(1024, decode_content=False):
                    if chunk:
                        temp_file.write(chunk)

                temp_file.seek(0)
                data = gzip.decompress(temp_file.read())
                temp_file.close()

                logger.info(
                    "Successfully Retrieved Compressed Data, Status Code: %s",
                    str(response.status_code),
                )
                return data

    except RequestException as e:
        logger.error(
            "An error occurred downloading data from %s \n Cause of error: %s",
            url,
            e,
        )
        raise Exception(
            f"An error occurred downloading data from {url} \n \
            Cause of error:{e}",
        )
