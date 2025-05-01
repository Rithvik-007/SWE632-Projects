import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IndexPageTest(unittest.TestCase):
    def setUp(self):
        # Set up ChromeDriver in headless mode.
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        # Update the URL if needed. This assumes Live Server is running on port 5500.
        self.driver.get("http://127.0.0.1:8080/index.html")
    
    def tearDown(self):
        self.driver.quit()
    
    def test_header_and_tagline(self):
        driver = self.driver
        # Wait for the header element inside .header-box inside .text-center.
        header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".index-page .text-center .header-box h1"))
        )
        # Verify the header text.
        self.assertEqual(header.text.strip(), "UI Code Assistant", "Header text should be 'UI Code Assistant'")
        
        # Verify the tagline paragraph text.
        tagline = driver.find_element(By.CSS_SELECTOR, ".index-page .text-center .header-box p")
        self.assertEqual(tagline.text.strip(),
                         "Speed up your web development by generating ready-to-use HTML/CSS code and analyzing UI designs in seconds.",
                         "Tagline text does not match expected.")
    
    def test_generate_link_navigation(self):
        driver = self.driver
        # Wait for the "Generate HTML/CSS Code" button/link.
        generate_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Generate HTML/CSS Code"))
        )
        generate_link.click()
        # Wait until the URL changes and contains "generate.html".
        WebDriverWait(driver, 10).until(EC.url_contains("generate.html"))
        current_url = driver.current_url
        self.assertIn("generate.html", current_url,
                      "After clicking 'Generate HTML/CSS Code', the URL should contain 'generate.html'.")
    
    def test_design_link_navigation(self):
        driver = self.driver
        # Reload the index page in case we're not on it.
        driver.get("http://127.0.0.1:8080/index.html")
        # Wait for the "Analyse UI Design/code" button/link.
        design_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Analyse UI Design/code"))
        )
        design_link.click()
        # Wait until the URL changes and contains "design.html".
        WebDriverWait(driver, 10).until(EC.url_contains("design.html"))
        current_url = driver.current_url
        self.assertIn("design.html", current_url,
                      "After clicking 'Analyse UI Design/code', the URL should contain 'design.html'.")

    def test_button_css_property(self):
        driver = self.driver
        # Check that one of the buttons has the expected background color.
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".index-page .btn"))
        )
        # Get computed background color using JavaScript.
        bg_color = driver.execute_script(
            "return window.getComputedStyle(arguments[0]).backgroundColor;", button)
        # According to your CSS, the expected background color is rgb(78, 4, 4).
        self.assertEqual(bg_color, "rgb(78, 4, 4)",
                         f"Button background color is {bg_color}, expected 'rgb(78, 4, 4)'.")
        
if __name__ == "__main__":
    unittest.main()
