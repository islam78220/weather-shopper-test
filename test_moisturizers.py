"""
Test de la page des hydratants - Choisir les hydratants les moins chers contenant de l'aloe et de l'amande
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
from navigation import navigate_to_moisturizer_shop

def setup_driver():
    """Configure et retourne le driver Selenium"""
    chrome_options = Options()
    if config.selenium_config['headless']:
        chrome_options.add_argument('--headless')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def add_to_cart(product, ingredient_type):
    """
    Ajoute un produit au panier s'il existe
    
    Args:
        product: Élément web du produit
        ingredient_type: Type d'ingrédient (aloe ou amande)
    """
    if product:
        product.find_element(By.XPATH, selector.product_card['add_button']).click()
        print(f"Ajout de l'hydratant à base de {ingredient_type} le moins cher au panier.")
    else:
        print(f"Aucun hydratant à base de {ingredient_type} trouvé.")

def moisturizer_page_test():
    """
    Test principal pour la page des hydratants:
    - Ajouter au panier l'hydratant à base d'aloe le moins cher
    - Ajouter au panier l'hydratant à base d'amande le moins cher
    - Aller au panier
    """
    driver = setup_driver()
    
    try:
        # Accéder à la page principale
        driver.get(config.selenium_config['url'])
        
        # Naviguer vers la boutique d'hydratants
        navigate_to_moisturizer_shop(driver)
        
        # Attendre que les produits soient chargés
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, selector.product_card['all_products']))
        )
        
        # Trouver tous les éléments des produits hydratants
        products = driver.find_elements(By.XPATH, selector.product_card['all_products'])
        
        # Listes pour contenir les produits à base d'aloe et d'amande avec leurs prix
        aloe_products = []
        almond_products = []
        
        # Parcourir tous les produits
        for product in products:
            # Obtenir le nom et le prix du produit
            product_name = product.find_element(By.XPATH, selector.product_card['name']).text
            product_price_text = product.find_element(By.XPATH, selector.product_card['price']).text
            
            # Analyser le prix à partir de la chaîne (format: "Price: Rs. XX")
            # Extraire uniquement la partie numérique du prix
            price_str = product_price_text.replace('Price: ', '').replace('Rs.', '').strip()
            price = float(price_str)
            
            # Ajouter les hydratants à base d'aloe et d'amande à leurs listes respectives
            if 'aloe' in product_name.lower():
                aloe_products.append({'price': price, 'product': product})
            if 'almond' in product_name.lower():
                almond_products.append({'price': price, 'product': product})
        
        # Trouver les hydratants à base d'aloe et d'amande les moins chers
        cheapest_aloe = None
        cheapest_almond = None
        
        if aloe_products:
            cheapest_aloe = min(aloe_products, key=lambda x: x['price'])['product']
        
        if almond_products:
            cheapest_almond = min(almond_products, key=lambda x: x['price'])['product']
        
        # Ajouter les hydratants les moins chers au panier
        add_to_cart(cheapest_aloe, 'aloe')
        add_to_cart(cheapest_almond, 'amande')
        
        # Cliquer sur le bouton du panier
        cart_button = driver.find_element(By.XPATH, selector.product_card['cart_button'])
        cart_button.click()
        print("Navigation vers le panier.")
        
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        # Fermer le navigateur
        driver.quit()

if __name__ == "__main__":
    moisturizer_page_test()