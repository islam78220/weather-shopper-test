"""
Test de la page des écrans solaires - Choisir les écrans solaires SPF-30 et SPF-50 les moins chers
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
from navigation import navigate_to_sunscreen_shop

def setup_driver():
    """Configure et retourne le driver Selenium"""
    chrome_options = Options()
    if config.selenium_config['headless']:
        chrome_options.add_argument('--headless')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def add_to_cart(product, spf_type):
    """
    Ajoute un produit au panier s'il existe
    
    Args:
        product: Élément web du produit
        spf_type: Type de SPF (SPF-30 ou SPF-50)
    """
    if product:
        product.find_element(By.XPATH, selector.product_card['add_button']).click()
        print(f"Ajout de l'écran solaire {spf_type} le moins cher au panier.")
    else:
        print(f"Aucun écran solaire {spf_type} trouvé.")

def sunscreen_page_test():
    """
    Test principal pour la page des écrans solaires:
    - Ajouter au panier l'écran solaire SPF-50 le moins cher
    - Ajouter au panier l'écran solaire SPF-30 le moins cher
    - Aller au panier
    """
    driver = setup_driver()
    
    try:
        # Accéder à la page principale
        driver.get(config.selenium_config['url'])
        
        # Naviguer vers la boutique d'écrans solaires
        navigate_to_sunscreen_shop(driver)
        
        # Attendre que les produits soient chargés
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, selector.product_card['all_products']))
        )
        
        # Trouver tous les éléments des produits d'écrans solaires
        products = driver.find_elements(By.XPATH, selector.product_card['all_products'])
        
        # Initialiser les trackers de produits les moins chers
        cheapest_spf50_product = None
        cheapest_spf50_price = float('inf')
        cheapest_spf30_product = None
        cheapest_spf30_price = float('inf')
        
        # Parcourir tous les produits pour trouver les écrans solaires SPF-50 et SPF-30 les moins chers
        for product in products:
            # Obtenir le nom et le prix du produit
            product_name = product.find_element(By.XPATH, selector.product_card['name']).text
            product_price_text = product.find_element(By.XPATH, selector.product_card['price']).text
            
            # Analyser le prix à partir de la chaîne (format: "Price: Rs. XX")
            # Extraire uniquement la partie numérique du prix
            price_str = product_price_text.replace('Price: ', '').replace('Rs.', '').strip()
            price = float(price_str)
            
            # Vérifier si le produit est SPF-50 ou SPF-30 et moins cher que le moins cher actuel
            if 'spf-50' in product_name.lower() and price < cheapest_spf50_price:
                cheapest_spf50_product = product
                cheapest_spf50_price = price
            elif 'spf-30' in product_name.lower() and price < cheapest_spf30_price:
                cheapest_spf30_product = product
                cheapest_spf30_price = price
        
        # Ajouter les écrans solaires les moins chers au panier
        add_to_cart(cheapest_spf50_product, 'SPF-50')
        add_to_cart(cheapest_spf30_product, 'SPF-30')
        
        # Attendre que le bouton du panier soit visible
        cart_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, selector.product_card['cart_button']))
        )
        cart_button.click()
        print("Navigation vers le panier.")
        
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        # Fermer le navigateur
        driver.quit()

if __name__ == "__main__":
    sunscreen_page_test()