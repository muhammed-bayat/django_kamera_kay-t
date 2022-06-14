def chunks(L, n: int) -> list:
    """
    Splits list into n chunks
    :param L: list
    :param n: chunk to be generated
    :return: list
    """
    k, m = divmod(len(L), n)
    return (L[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
