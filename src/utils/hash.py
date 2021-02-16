from passlib.hash import pbkdf2_sha256 as sha256
import string, secrets


def generate_hash(password):
    return sha256.hash(password)


def verify_hash(password, phrase):
    return sha256.verify(password, phrase)


def generate_password(length):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + '!#$%&@'
    return ''.join(secrets.choice(characters) for i in range(length))
