from abc import ABC, abstractmethod
from hashlib import sha1
from requests import get


class ValidationError(Exception):
    pass


class Validator(ABC):
    @abstractmethod
    def __init__(self, text):
        pass

    @abstractmethod
    def is_valid(self):
        pass


class HasNumberValidator(Validator):
    def __init__(self, text):
        self.text = text

    def is_valid(self):
        for number in range(0, 10):
            if str(number) in self.text:
                return True
        raise ValidationError('Text must contain number!')


class HasSpecialCharactersValidator(Validator):
    def __init__(self, text):
        self.text = text

    def is_valid(self):
        if any([not character.isalnum() for character in self.text]):
            return True
        raise ValidationError("Text must special character!")


class HasUpperCharacterValidator(Validator):
    def __init__(self, text):
        self.text = text

    def is_valid(self):
        if any([character.isupper() for character in self.text]):
            return True
        raise ValidationError("Text must one or more upper letters!")


class HasLowerCharacterValidator(Validator):
    def __init__(self, text):
        self.text = text

    def is_valid(self):
        if any([character.islower() for character in self.text]):
            return True
        raise ValidationError("Text must one or more lower letters!")


class HaveIbeenPwndValidator(Validator):
    def __init__(self, password):
        self.passwaord = password

    def is_valid(self):
        hash_of_password = sha1(self.passwaord.encode('utf-8')).hexdigest().upper()
        response = get("https://api.pwnedpasswords.com/range/" + hash_of_password[:5])

        for line in response.text.splitlines():
            found_hash, _ = line.split(':')
            if found_hash == hash_of_password[5:]:
                raise ValidationError("This password is a leaked passwaord! Choose another one!")
        return True


class LenghtValidator(Validator):
    def __init__(self, text, min_leght=8):
        self.text = text
        self.min_lenght = min_leght

    def is_valid(self):
        if len(self.text) >= self.min_lenght:
            return True
        raise ValidationError("Text is too short!")


class PasswordValidator(Validator):
    def __init__(self, password):
        self.password = password
        self.validators = [
            LenghtValidator,
            HasNumberValidator,
            HasSpecialCharactersValidator,
            HasUpperCharacterValidator,
            HasLowerCharacterValidator,
            HaveIbeenPwndValidator,
        ]

    def is_valid(self):
        for class_name in self.validators:
            validator = class_name(self.password)
            if validator.is_valid() is False:
                return False
        return True
