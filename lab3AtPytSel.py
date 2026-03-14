import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class TestSauceDemo:
    """
    Клас для автоматизації функціонального тестування вебзастосунку SauceDemo.
    Включає в себе перевірки входу в систему, навігації та роботи кошика.
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        # Ініціалізація драйвера Chrome з автоматичним завантаженням
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # Налаштування синхронізації між кодом програми та швидкістю завантаження елементів браузером
        self.driver.implicitly_wait(10)
        # Перехід на головну сторінку перед кожним тестом
        self.driver.get("https://www.saucedemo.com/")
        yield
        # Закриття сесії браузера після кожного тесту
        self.driver.quit()

    def test_01_login_success(self):
        # Тест успішного входу з коректними даними
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Перевірка наявності заголовка 'Products'
        title = self.driver.find_element(By.CLASS_NAME, "title").text
        assert title == "Products", "Помилка: користувач не зміг увійти!"

    def test_02_login_invalid_password(self):
        # Тест обробки помилки при введенні неправильного пароля
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("wrong_password")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Перевірка тексту повідомлення про помилку
        error_element = self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        expected_error = "Username and password do not match"  
        fail_report = "Помилка: сайт не показав попередження про невірний пароль!"
        assert expected_error in error_element.text, fail_report

    def test_03_navigation_to_cart(self):
        # Тест перевірки переходу на сторінку кошика після логіну
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Клік по іконці кошика
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        
        # Перевірка URL сторінки кошика
        fail_report = "Помилка: URL сторінки кошика некоректний!"
        assert "cart.html" in self.driver.current_url, fail_report

    def test_04_add_item_functionality(self):
        # Тест додавання товару та оновлення лічильника кошика"""
        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        self.driver.find_element(By.ID, "login-button").click()
        
        # Додавання рюкзака в кошик
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        
        # Перевірка, що кнопка змінила стан на 'Remove'
        button_text = self.driver.find_element(By.ID, "remove-sauce-labs-backpack").text
        assert button_text == "Remove", "Помилка: Кнопка не змінила текст на Remove!"
        
        # Перевірка лічильника товарів на іконці кошика
        cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        fail_report = "Помилка: лічильник кошика не оновився!"
        assert cart_badge == "1", fail_report