import secrets
import string

letters = string.ascii_letters
digits = string.digits
special_chars = string.punctuation
password_alphabet = letters + digits

password_length = 32


def gen():
    password = ''
    for i in range(password_length):
        password += ''.join(secrets.choice(password_alphabet))
    return password


def key():
    secret_key = secrets.token_hex(16)
    print(secret_key)


em_password = '***********'

pass_key = gen()
print(pass_key)
