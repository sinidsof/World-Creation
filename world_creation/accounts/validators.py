import re
from django.core.exceptions import ValidationError

# Валидация за потребителското име
def validate_username(username):
    if len(username) < 5:
        raise ValidationError("Потребителското име трябва да бъде поне 5 символа дълго.")

# Валидация за паролата
def validate_password(password):
    # Проверка за минимална дължина
    if len(password) < 8:
        raise ValidationError("Паролата трябва да бъде поне 8 символа дълга.")

    # Проверка дали паролата съдържа поне една цифра
    if not re.search(r'\d', password):
        raise ValidationError("Паролата трябва да съдържа поне една цифра.")

    # Проверка дали паролата съдържа поне една малка и една голяма буква
    if not re.search(r'[a-z]', password):
        raise ValidationError("Паролата трябва да съдържа поне една малка буква.")

    if not re.search(r'[A-Z]', password):
        raise ValidationError("Паролата трябва да съдържа поне една голяма буква.")
