import unittest
from lb2.lr1 import validate_login, validate_password, validate_registration


class TestLr1(unittest.TestCase):

    def test_login_phone(self):
        result = validate_login("+1-234-567-8901")
        self.assertEqual(result, (True, ""))

    def test_login_email(self):
        result = validate_login("student@example.com")
        self.assertEqual(result, (True, ""))

    def test_login_blacklist(self):
        result = validate_login("Admin")
        self.assertEqual(result, (False, "Логин в чёрном списке"))

    def test_login_short(self):
        result = validate_login("abc")
        self.assertEqual(result, (False, "Логин короче 5 символов"))

    def test_login_bad_chars(self):
        result = validate_login("user!")
        self.assertEqual(result, (False, "Логин может содержать только латиницу, цифры и _"))

    def test_password_mismatch(self):
        result = validate_password("Пароль1!", "Пароль2!")
        self.assertEqual(result, (False, "Пароль и подтверждение не совпадают"))

    def test_password_short(self):
        result = validate_password("A1!a", "A1!a")
        self.assertEqual(result, (False, "Пароль короче 7 символов"))

    def test_password_no_upper(self):
        result = validate_password("пароль1!", "пароль1!")
        self.assertEqual(result, (False, "Нужна хотя бы одна заглавная буква"))

    def test_password_no_digit(self):
        result = validate_password("Пароль!!", "Пароль!!")
        self.assertEqual(result, (False, "Нужна хотя бы одна цифра"))

    def test_registration_ok(self):
        result = validate_registration("ivan_01", "Пароль1!", "Пароль1!")
        self.assertEqual(result, (True, ""))


if __name__ == "__main__":
    unittest.main()