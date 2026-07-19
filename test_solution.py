import pandas as pd
from solution import add_virtual_column


def test_sum_of_two_columns():
    df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
    df_expected = pd.DataFrame([[1, 1, 2]] * 2, columns=["label_one", "label_two", "label_three"])
    df_result = add_virtual_column(df, "label_one+label_two", "label_three")
    assert df_result.equals(df_expected)


def test_multiplication_of_two_columns():
    df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
    df_expected = pd.DataFrame([[1, 1, 1]] * 2, columns=["label_one", "label_two", "label_three"])
    df_result = add_virtual_column(df, "label_one * label_two", "label_three")
    assert df_result.equals(df_expected)


def test_subtraction_of_two_columns():
    df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
    df_expected = pd.DataFrame([[1, 1, 0]] * 2, columns=["label_one", "label_two", "label_three"])
    df_result = add_virtual_column(df, "label_one - label_two", "label_three")
    assert df_result.equals(df_expected)


def test_empty_result_when_invalid_labels():
    df = pd.DataFrame([[1, 2]] * 3, columns=["label_one", "label_two"])
    df_result = add_virtual_column(df, "label_one + label_two", "label3")
    assert df_result.empty

    df = pd.DataFrame([[1, 2]] * 3, columns=["label-one", "label_two"])
    df_result = add_virtual_column(df, "label-one + label_two", "label")
    assert df_result.empty

    df = pd.DataFrame([[1, 2]] * 3, columns=["label-one", "label_two"])
    df_result = add_virtual_column(df, "label_one + label_two", "label")
    assert df_result.empty


def test_empty_result_when_invalid_rules():
    df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
    df_result = add_virtual_column(df, "label_one \\ label_two", "label_three")
    assert df_result.empty

    df_result = add_virtual_column(df, "label&one + label_two", "label_three")
    assert df_result.empty

    df_result = add_virtual_column(df, "label_five + label_two", "label_three")
    assert df_result.empty


def test_when_extra_spaces_in_rules():
    df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
    df_expected = pd.DataFrame([[1, 1, 2]] * 2, columns=["label_one", "label_two", "label_three"])

    df_result = add_virtual_column(df, "label_one+label_two", "label_three")
    assert df_result.equals(df_expected)

    df_result = add_virtual_column(df, "label_one + label_two ", "label_three")
    assert df_result.equals(df_expected)

    df_result = add_virtual_column(df, " label_one + label_two ", "label_three")
    assert df_result.equals(df_expected)
