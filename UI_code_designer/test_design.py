import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DesignPageTest(unittest.TestCase):
    def setUp(self):
        # Set up ChromeDriver in headless mode with logging suppression.
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")  # Reduce Chrome's log verbosity.
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=chrome_options)
        # Update the URL as needed; here we assume design.html is served on port 8080.
        self.driver.get("http://127.0.0.1:8080/design.html")
    
    def tearDown(self):
        # Save a screenshot for every test in the current directory.
        timestamp = int(time.time())
        filename = f"screenshot_{self._testMethodName}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Saved screenshot: {filename}")
        self.driver.quit()
    
    def test_header_text(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        # Wait for the header element and verify its text.
        header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".header h1")))
        self.assertEqual(header.text.strip(), "Live Code & UI Analyzer",
                         "Header should be 'Live Code & UI Analyzer'")
    
    def test_analyze_button_populates_analysis_fields(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        # Wait for the Analyze Now button and force a click using JavaScript.
        analyze_btn = wait.until(EC.element_to_be_clickable((By.ID, "analyze-btn")))
        driver.execute_script("arguments[0].click();", analyze_btn)
        
        # Wait a moment for the analysis fields to populate.
        time.sleep(1)
        design_analysis = driver.find_element(By.ID, "design-analysis").get_attribute("value")
        code_analysis = driver.find_element(By.ID, "code-analysis").get_attribute("value")
        self.assertIn("Design Analysis Suggestions:", design_analysis,
                      "Design analysis suggestions should be populated.")
        self.assertIn("Code Analysis Suggestions:", code_analysis,
                      "Code analysis suggestions should be populated.")
    
    def test_run_button_outputs_code(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        # Set a sample snippet in the code editor.
        sample_code = "<h2>Test Code Output</h2><p>This is a test.</p>"
        code_editor = wait.until(EC.presence_of_element_located((By.ID, "code-editor")))
        code_editor.clear()
        code_editor.send_keys(sample_code)
        # Click the Run Code button.
        run_btn = wait.until(EC.element_to_be_clickable((By.ID, "run-btn")))
        run_btn.click()
        # Wait a short time for the iframe to load its content.
        time.sleep(2)
        # Switch to the iframe and verify that its body displays the sample code.
        iframe = driver.find_element(By.ID, "output-window")
        driver.switch_to.frame(iframe)
        body_html = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")
        self.assertIn("Test Code Output", body_html,
                      "The output iframe should display the sample test code.")
        driver.switch_to.default_content()

if __name__ == "__main__":
    unittest.main()
