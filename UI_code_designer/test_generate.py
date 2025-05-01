import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GeneratePageTest(unittest.TestCase):
    def setUp(self):
        # Set up ChromeDriver in headless mode with additional logging suppression.
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")  # Reduce Chrome's log verbosity.
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=chrome_options)
        # Update the URL to match your Live Server address for generate.html.
        self.driver.get("http://127.0.0.1:8080/generate.html")
    
    def tearDown(self):
        # Always save a screenshot in the current directory with test method and timestamp.
        timestamp = int(time.time())
        filename = f"screenshot_{self._testMethodName}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Saved screenshot: {filename}")
        self.driver.quit()
    
    def test_generate_login_component(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        # Wait for the component input field to be present and enter "login"
        input_field = wait.until(EC.presence_of_element_located((By.ID, "component-input")))
        input_field.clear()
        input_field.send_keys("login")
        
        # Click the Generate button.
        generate_btn = wait.until(EC.element_to_be_clickable((By.ID, "generate-btn")))
        generate_btn.click()
        
        # Wait until the code editor's value contains the substring "Email address:"
        wait.until(lambda d: "Email address:" in d.find_element(By.ID, "code-editor").get_attribute("value"))
        code_text = driver.find_element(By.ID, "code-editor").get_attribute("value")
        self.assertIn("Email address:", code_text,
                      "The code editor should contain a login snippet with 'Email address:'")
    
    def test_run_button_outputs_code(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        # Generate the login component.
        input_field = wait.until(EC.presence_of_element_located((By.ID, "component-input")))
        input_field.clear()
        input_field.send_keys("login")
        generate_btn = wait.until(EC.element_to_be_clickable((By.ID, "generate-btn")))
        generate_btn.click()
        wait.until(lambda d: "Email address:" in d.find_element(By.ID, "code-editor").get_attribute("value"))
        
        # Click the Run button to output the generated code in the iframe.
        run_btn = wait.until(EC.element_to_be_clickable((By.ID, "run-btn")))
        run_btn.click()
        # Wait a short time to allow the iframe to load content.
        time.sleep(2)
        
        # Switch to the iframe and verify its body contains "Email address:"
        iframe = driver.find_element(By.ID, "output")
        driver.switch_to.frame(iframe)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Email address:", body_text,
                      "The output iframe should display the login snippet including 'Email address:'")
        driver.switch_to.default_content()
    
    def test_invalid_component_alert(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        # Enter an invalid component value.
        input_field = wait.until(EC.presence_of_element_located((By.ID, "component-input")))
        input_field.clear()
        input_field.send_keys("invalid_component")
        
        # Click the Generate button.
        generate_btn = wait.until(EC.element_to_be_clickable((By.ID, "generate-btn")))
        generate_btn.click()
        
        # Wait until a JavaScript alert appears.
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        expected_alert = "No specific code is available for the given component"
        self.assertEqual(alert_text, expected_alert,
                         "Alert text should indicate invalid component input.")
        alert.accept()

if __name__ == "__main__":
    unittest.main()
