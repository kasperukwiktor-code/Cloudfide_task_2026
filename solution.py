import re
import operator
import pandas as pd

_LABEL_RE = re.compile(r'^[A-Za-z_]+$')
_TOKEN_RE = re.compile(r'\s*([A-Za-z_]+|[+\-*])\s*')
_OPS = {'+': operator.add, '-': operator.sub, '*': operator.mul}


def _tokenize(role: str):
    """Split role into a flat list of operand/operator tokens.
    Returns None if any character in role can't be consumed by the grammar
    (operand = letters/underscores, operator = one of + - *)."""
    tokens = []
    pos, n = 0, len(role)
    while pos < n:
        m = _TOKEN_RE.match(role, pos)
        if not m or m.end() == pos:
            return None
        tokens.append(m.group(1))
        pos = m.end()
    return tokens


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    # 1. validate the new column's name
    if not isinstance(new_column, str) or not _LABEL_RE.match(new_column):
        return pd.DataFrame([])

    if not isinstance(role, str):
        return pd.DataFrame([])

    role = role.strip()
    if not role:
        return pd.DataFrame([])

    # 2. tokenize -> reject any disallowed character (\, &, /, ^, digits, etc.)
    tokens = _tokenize(role)
    if not tokens or len(tokens) % 2 == 0:
        return pd.DataFrame([])

    operands = tokens[0::2]   # expected: column names
    operators = tokens[1::2]  # expected: + - *

    # 3. every operator must be one of the supported ones
    if any(op not in _OPS for op in operators):
        return pd.DataFrame([])

    # 4. every operand must be a real, validly-named column of df
    for col in operands:
        if not _LABEL_RE.match(col) or col not in df.columns:
            return pd.DataFrame([])

    # 5. evaluate with standard precedence: * before + / -
    values = [df[c] for c in operands]
    ops = list(operators)

    i = 0
    while i < len(ops):
        if ops[i] == '*':
            values[i] = values[i] * values[i + 1]
            del values[i + 1]
            del ops[i]
        else:
            i += 1

    result = values[0]
    for op_symbol, val in zip(ops, values[1:]):
        result = _OPS[op_symbol](result, val)

    df_result = df.copy()
    df_result[new_column] = result
    return df_result
