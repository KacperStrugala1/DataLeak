import logging
logging.basicConfig(
    filename="debug.log",
    filemode='a',
    format="{asctime} | {levelname} | {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,
)