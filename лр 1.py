import re
import hashlib
import logging
import sys
from pathlib import Path

# Логирование: консоль + файл
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | [%(levelname)-7s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/app.log", encoding="utf-8")
    ]
)

# Чёрный список логинов
BLACKLIST = {"admin", "root", "system", "user", "test", "guest", "superuser", "moderator", "manager", "support"}


def mask_password(password):
    """Хеш пароля для логов."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()[:16]


def validate_login(login):
    """Возвращает (True, "") или (False, причина)."""
    if login.lower() in BLACKLIST:
        return False, "Логин в чёрном списке"

    if re.match(r'^\+\d-\d{3}-\d{3}-\d{4}$', login):
        return True, ""
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', login):
        return True, ""

    if len(login) < 5:
        return False, "Логин короче 5 символов"
    if not re.match(r'^[a-zA-Z0-9_]+$', login):
        return False, "Логин может содержать только латиницу, цифры и _"

    return True, ""


def validate_password(password, confirm):
    """Возвращает (True, "") или (False, причина)."""
    if password != confirm:
        return False, "Пароль и подтверждение не совпадают"
    if len(password) < 7:
        return False, "Пароль короче 7 символов"
    if not re.match(r'^[А-Яа-яЁё0-9!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|`~]+$', password):
        return False, "Пароль может содержать только кириллицу, цифры и спецсимволы"
    if not any(ch.isupper() and ch.isalpha() for ch in password):
        return False, "Нужна хотя бы одна заглавная буква"
    if not any(ch.islower() and ch.isalpha() for ch in password):
        return False, "Нужна хотя бы одна строчная буква"
    if not any(ch.isdigit() for ch in password):
        return False, "Нужна хотя бы одна цифра"
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|`~]', password):
        return False, "Нужен хотя бы один спецсимвол"

    return True, ""


def validate_registration(login, password, confirm):
    """Основная функция. Возвращает (True, "") или (False, причина)."""
    logging.info(f"Регистрация: login='{login}', password_hash='{mask_password(password)}'")

    ok, msg = validate_login(login)
    if not ok:
        logging.warning(f"Ошибка логина: {msg}")
        return False, msg

    ok, msg = validate_password(password, confirm)
    if not ok:
        logging.warning(f"Ошибка пароля: {msg}")
        return False, msg

    logging.info(f"Регистрация успешна: '{login}'")
    return True, ""


def main():
    """Точка входа: ввод логина, пароля и подтверждения с клавиатуры."""
    print("=== Регистрация пользователя ===")
    login = input("Логин: ")
    password = input("Пароль: ")
    confirm = input("Подтверждение пароля: ")

    ok, msg = validate_registration(login, password, confirm)

    if ok:
        print("\nРегистрация успешна!")
    else:
        print(f"\nОшибка: {msg}")


if __name__ == "__main__":
    main()