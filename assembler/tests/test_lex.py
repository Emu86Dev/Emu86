import pytest

import assembler.lex as lex


def test_word_is_float():
    assert lex.word_is_float("0.999") is True


def test_word_is_float_int_str():
    assert lex.word_is_float("1") is False


def test_word_is_float_int():
    with pytest.raises(TypeError):
        lex.word_is_float(1)
