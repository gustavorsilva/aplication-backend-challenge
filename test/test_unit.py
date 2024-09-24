import pytest
from backendchallenge.main import is_prime

def test_is_prime():
    # Números primos
    assert is_prime(2) == "verdadeiro"
    assert is_prime(3) == "verdadeiro"
    assert is_prime(5) == "verdadeiro"
    assert is_prime(7) == "verdadeiro"
    assert is_prime(13) == "verdadeiro"

    # Números não primos
    assert is_prime(1) == "falso"
    assert is_prime(4) == "falso"
    assert is_prime(6) == "falso"
    assert is_prime(9) == "falso"
    assert is_prime(15) == "falso"

    # Números negativos
    assert is_prime(-3) == "falso"
    assert is_prime(-7) == "falso"

    # Zero
    assert is_prime(0) == "falso"