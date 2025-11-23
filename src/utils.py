"""
Função utilitária para configuração de logging.
"""

import logging
import sys


def get_logger(name: str = "app"):
    """
    Função para configurar e retornar um logger.
    name: Nome do logger.
    Retorna um objeto logger configurado.

    example:
        logger = get_logger("meu_logger")
        logger.info("Mensagem de informação")
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
