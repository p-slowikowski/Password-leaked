import requests
import requests_mock
import pytest
from main import *


def test_if_has_number_validator_positive():
    validator = HasNumberValidator('abc123')
    result = validator.is_valid()
    assert result is True


def test_if_has_number_validator_negative():
    validator = HasNumberValidator('abc')
    with pytest.raises(ValidationError) as error:
        validator.is_valid()
        assert "Text must contain number!" in str(error.value)


def test_if_has_special_character_validator_positive():
    validator = HasSpecialCharactersValidator('abc123@')
    result = validator.is_valid()
    assert result is True


def test_if_has_special_character_validator_negative():
    validator = HasSpecialCharactersValidator('abc')
    with pytest.raises(ValidationError) as error:
        validator.is_valid()
        assert "Text must special character!" in str(error.value)


def test_if_has_upper_character_validator_positive():
    validator = HasUpperCharacterValidator('abc123@F')
    result = validator.is_valid()
    assert result is True


def test_if_has_upper_character_validator_negative():
    validator = HasUpperCharacterValidator('abc')
    with pytest.raises(ValidationError) as error:
        validator.is_valid()
        assert "Text must one or more upper letters!" in str(error.value)


def test_if_has_lower_character_validator_positive():
    validator = HasLowerCharacterValidator('abc123@F')
    result = validator.is_valid()
    assert result is True


def test_if_has_lower_character_validator_negative():
    validator = HasLowerCharacterValidator('ABC111')
    with pytest.raises(ValidationError) as error:
        validator.is_valid()
        assert "Text must one or more lower letters!" in str(error.value)


def test_if_lenght_of_password_validator_positive():
    validator = LenghtValidator('abc123@F')
    result = validator.is_valid()
    assert result is True


def test_if_lenght_of_password_validator_negative():
    validator = LenghtValidator('Abc')
    with pytest.raises(ValidationError) as error:
        validator.is_valid()
        assert "Text is too short!" in str(error.value)


def test_have_i_been_pwnd_validator_positive(requests_mock):
    data = "091234F6457BEB8E9EB990A59DA6672CC9C:20\r\n"
    requests_mock.get("https://api.pwnedpasswords.com/range/ED5E3", text=data)
    validator = HaveIbeenPwndValidator("kacper123")
    assert validator.is_valid() is True


def test_have_i_been_pwnd_validator_negative(requests_mock):
    data = "091234F6457BEB8E9EB990A59DA6672CC9C:20\r\n"
    requests_mock.get("https://api.pwnedpasswords.com/range/ED5E3", text=data)
    validator = HaveIbeenPwndValidator("kacper123")
    with pytest.raises(ValidationError) as error:
        validator.is_valid()
        assert "This password is a leaked passwaord! Choose another one!" in str(error.value)
