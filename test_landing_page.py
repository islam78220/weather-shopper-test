"""
Script de test principal pour la page d'accueil de Weather Shopper
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import config
import selector

def setup_driver():
    """Configure et retourne le driver Selenium"""
    chrome_options = Options()
    if config.selenium_config['headless']:
        chrome_options.add_argument('--headless')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def navigate_to_shop(driver, shop_type):
    """
    Navigue vers la boutique spécifiée
    
    Args:
        driver: Instance du WebDriver Selenium
        shop_type: 'moisturizer' ou 'sunscreen'
    """
    button_selector = selector.landing_page['moisturizer_button'] if shop_type == 'moisturizer' else selector.landing_page['sunscreen_button']
    button = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, button_selector))
    )
    button.click()
    print(f"Navigation vers la boutique {shop_type}")

def landing_page_test():
    """
    Test principal pour la page d'accueil:
    - Acheter des hydratants si la température est inférieure à 19°C
    - Acheter des crèmes solaires si la température est supérieure à 34°C
    
    Returns:
        str: Type de boutique vers laquelle le test a navigué ('moisturizer', 'sunscreen', ou None)
    """
    driver = setup_driver()
    shop_type = None
    
    try:
        # Accéder à la page principale
        driver.get(config.selenium_config['url'])
        
        # Obtenir la température
        temperature_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, selector.landing_page['temperature']))
        )
        temperature_text = temperature_element.text
        temperature = float(temperature_text.split()[0])
        
        # Décider quelle boutique visiter selon la température
        if temperature < 19:
            navigate_to_shop(driver, 'moisturizer')
            shop_type = 'moisturizer'
            print(f"Température: {temperature}°C - Navigation vers la boutique d'hydratants")
        elif temperature > 34:
            navigate_to_shop(driver, 'sunscreen')
            shop_type = 'sunscreen'
            print(f"Température: {temperature}°C - Navigation vers la boutique de crèmes solaires")
        else:
            print(f"Température: {temperature}°C - Dans une plage confortable. Aucun produit spécifique n'est nécessaire.")
        
        # Vérifier que nous sommes bien sur la page attendue
        if shop_type:
            # Attendre que la page soit chargée
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2"))
            )
            
            # Vérifier le titre de la page
            page_title = driver.find_element(By.XPATH, "//h2").text
            expected_title = "Moisturizers" if shop_type == 'moisturizer' else "Sunscreens"
            
            if expected_title in page_title:
                print(f"Vérification réussie: Page {expected_title} correctement chargée")
            else:
                print(f"Erreur: Page {expected_title} non chargée. Titre actuel: {page_title}")
                shop_type = None
            
    except Exception as e:
        print(f"Erreur: {e}")
        shop_type = None
    finally:
        # Fermer le navigateur
        driver.quit()
    
    return shop_type

if __name__ == "__main__":
    landing_page_test()