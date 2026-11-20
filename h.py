import time
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

lesson_ids = ["236895", "236896", "236897", "236898", "236899", "236903", "236904", "236905"]
secret_message = ""

browser = webdriver.Chrome()
try:
    # Открываем первую страницу
    browser.get(f"https://stepik.org/lesson/{lesson_ids[0]}/step/1")
    
    print("=====================================================")
    print("ВНИМАНИЕ! Открыт браузер. Убедитесь, что вы авторизованы.")
    print("Если вы не авторизованы - войдите ВРУЧНУЮ и решите капчу.")
    print("=====================================================")
    
    input("Когда вы успешно авторизуетесь, нажмите ENTER здесь в консоли...")

    # Теперь проходим по всем шагам
    for lesson_id in lesson_ids:
        browser.get(f"https://stepik.org/lesson/{lesson_id}/step/1")
        # Даем странице время на загрузку (Stepik грузится не сразу)
        time.sleep(3) 
        
        wait = WebDriverWait(browser, 10)
        
        try:
            # ПРОВЕРКА: Если задача уже решена, появится кнопка "Решить снова"
            try:
                # Ищем кнопку "Решить снова" (может быть скрыта, если задача не решена)
                solve_again_btn = browser.find_element(By.XPATH, "//button[contains(text(), 'Решить снова') or contains(text(), 'Solve again')]")
                solve_again_btn.click()
                time.sleep(2) # Ждем, пока откроется поле ввода
            except:
                pass # Если кнопки нет, значит задача не решена, поле ввода уже открыто

            # Теперь ищем поле ввода и вводим ответ
            answer_field = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "textarea")))
            answer_field.clear()
            answer_field.send_keys(str(math.log(int(time.time()))))
            
            # Нажимаем "Отправить"
            submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit-submission")))
            submit_btn.click()
            
            # Ждем появления фидбека (черное поле)
            feedback_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".smart-hints__hint")))
            # Даем полсекунды, чтобы текст точно прогрузился
            time.sleep(0.5) 
            feedback = feedback_element.text
            
            print(f"Шаг {lesson_id}: получено -> '{feedback}'")
            
            # Если это не "Correct!", сохраняем кусочек
            if feedback != "Correct!":
                secret_message += feedback + " "
                
        except Exception as e:
            print(f"Ошибка на шаге {lesson_id}. Пропускаем...")

    print("\n=====================================================")
    print(f"ИТОГОВОЕ СООБЩЕНИЕ (отправьте его на Stepik): \n{secret_message.strip()}")
    print("=====================================================")

finally:
    input("Нажмите ENTER, чтобы закрыть браузер...")
    browser.quit()