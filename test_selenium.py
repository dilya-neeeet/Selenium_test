import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def base_url():
    return 'https://the-internet.herokuapp.com/login'


@pytest.fixture
def sample_data():
    return {'login': 'tomsmith', 'password': 'SuperSecretPassword!'}


@pytest.fixture
def logging_in(driver, base_url):
    def _logging_in(login, password):
        driver.get(base_url)
        login_input = driver.find_element(By.ID, 'username')
        login_input.clear()
        login_input.send_keys(login)
        password_input = driver.find_element(By.ID, 'password')
        password_input.clear()
        password_input.send_keys(password)
        submit_button = driver.find_element(By.TAG_NAME, 'button')
        submit_button.click()
    return _logging_in


def test_successful_login(driver, logging_in, sample_data):
    logging_in(sample_data['login'], sample_data['password'])
    assert driver.current_url == 'https://the-internet.herokuapp.com/secure'
    success_message = driver.find_element(By.CSS_SELECTOR, '.subheader')
    assert 'Welcome to the Secure Area. When you are done click logout below.' in success_message.text


def test_unsuccessful_login(driver, logging_in, sample_data):
    logging_in(sample_data['login'], '12345')
    assert driver.current_url == 'https://the-internet.herokuapp.com/login'
    error_message = driver.find_element(By.ID, 'flash')
    assert 'Your password is invalid' in error_message.text
