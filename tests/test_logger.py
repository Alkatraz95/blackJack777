from masks.masks import logger, apply_mask


def test_logger_creates_file():
    # Эта строка принудительно создаст файл logs/masks.log
    logger.info("Это тестовая запись для проверки логов!")

    data = {"test": "data"}
    result = apply_mask(data)

    assert result == data
