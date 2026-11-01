import datetime


def log(filename=None):
    """Декоратор для логирования выполнения функции.

    Аргумент filename — путь к файлу, в который записываются логи.
    Если filename не передан, логи выводятся на консоль.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            log_message = f"[{start_time}] Начало выполнения функции: {func.__name__}\n"
            try:
                result = func(*args, **kwargs)
                end_time = datetime.datetime.now()
                log_message += (
                    f"[{end_time}] Функция: {func.__name__}, Результат: {result}\n"
                )
                return result
            except Exception as e:
                end_time = datetime.datetime.now()
                log_message += (
                    f"[{end_time}] Функция: {func.__name__}, "
                    f"Ошибка: {type(e).__name__}, "
                    f"Параметры: {args}, {kwargs}\n"
                )
                raise
            finally:
                log_message += (
                    f"[{end_time}] Конец выполнения функции: {func.__name__}\n"
                )
                # Запись логов в файл или вывод на консоль
                if filename:
                    with open(filename, "a") as log_file:
                        log_file.write(log_message)
                else:
                    print(log_message)

        return wrapper

    return decorator
