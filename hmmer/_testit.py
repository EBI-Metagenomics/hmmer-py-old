def test(verbose: bool = True):
    """
    Run tests to verify this package's integrity.

    Parameters
    ----------
    verbose
        ``True`` to show diagnostic. Defaults to ``True``.

    Returns
    -------
    int
        Exit code: ``0`` for success.
    """

    args = ["--doctest-modules"]
    if not verbose:
        args += ["--quiet"]

    args += ["--pyargs", __name__.split(".")[0]]
    return __import__("pytest").main(args)
