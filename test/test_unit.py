import pytest
from app.main import is_prime

def test_is_prime():
    # Números primos
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(5) == True
    assert is_prime(7) == True
    assert is_prime(13) == True

    # Números não primos
    assert is_prime(1) == False
    assert is_prime(4) == False
    assert is_prime(6) == False
    assert is_prime(9) == False
    assert is_prime(15) == False

    # Números negativos
    assert is_prime(-3) == False
    assert is_prime(-7) == False

    # Zero
    assert is_prime(0) == False