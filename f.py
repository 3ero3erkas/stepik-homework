import time
import math
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройки авторизации (замените на свои данные)
STEPIK_LOGIN = "."
STEPIK_PASSWORD = "."

# Список для сбора нестандартных сообщений от платформы
secret_message_parts = []

@pytest.fixture(scope="function")
def browser():
    print("\nstart browser for test..")
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    print("\nquit browser..")
    driver.quit()

@pytest.mark.parametrize("lesson_id", [
    "236895", "236896", "236897", "236898",
    "236899", "236903", "236904", "236905"
])
def test_collect_alien_message(browser, lesson_id):
    link = f"https://stepik.org/lesson/{lesson_id}/step/1"
    browser.get(link)
    wait = WebDriverWait(browser, 15)

    # 1. Авторизация (если сессия не сохранена)
    try:
        login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/login']")))
        login_btn.click()
        wait.until(EC.visibility_of_element_located((By.ID, "id_login_email"))).send_keys(STEPIK_LOGIN)
        browser.find_element(By.ID, "id_login_password").send_keys(STEPIK_PASSWORD)
        browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "modal-dialog")))
    except Exception:
        # Если уже авторизованы, попап входа не появится
        pass

    # 2. Ввод правильного ответа
    answer_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea")))
    answer_field.clear()
    answer_field.send_keys(str(math.log(int(time.time()))))

    # 3. Отправка ответа
    submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit-submission")))
    submit_btn.click()

    # 4. Получение текста из черного поля обратной связи
    feedback = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".smart-hints__hint"))).text

    # 5. Если текст не "Correct!", сохраняем фрагмент и намеренно роняем assert
    if feedback != "Correct!":
        secret_message_parts.append(feedback)
        assert feedback == "Correct!", f"Получен фрагмент сообщения: '{feedback}'"

def test_print_final_message():
    # Выводим собранное предложение в консоль после завершения всех тестов
    print("\n\n=== ИТОГОВОЕ СООБЩЕНИЕ ===")
    print("".join(secret_message_parts))
