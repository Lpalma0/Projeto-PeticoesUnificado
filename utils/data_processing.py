import logging
import pandas as pd
import numpy as np
from typing import List
import os

from dotenv import load_dotenv

load_dotenv()


MAX_REQUISICOES_SIMULTANEAS = int(os.getenv("MAX_REQUISICOES_SIMULTANEAS", 10))


def split_dataframe_into_chunks(
    df: pd.DataFrame, num_chunks: int = None
) -> List[pd.DataFrame]:
    """
    Divide um DataFrame em um número especificado de DataFrames menores (chunks).

    Args:
        df: O DataFrame a ser dividido.
        num_chunks: O número de partes em que o DataFrame deve ser dividido.

    Returns:
        Uma lista de DataFrames, cada um sendo um chunk do DataFrame original.
    """

    qtd_linhas = len(df)

    if df.empty:
        logging.info("DataFrame vazio. Nada a fazer.")
        return []

    if not num_chunks:
        num_chunks = min(MAX_REQUISICOES_SIMULTANEAS, qtd_linhas)
    logging.info(f"Total de linhas carregadas: {qtd_linhas}")
    logging.info(f"Total de requisições simultâneas: {num_chunks}")

    return np.array_split(df, num_chunks)
