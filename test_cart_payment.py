"""
Test de la page du panier et du processus de paiement
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
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

def find_product(driver, containing):
    """
    Trouve et ajoute un produit contenant une chaîne spécifique
    
    Args:
        driver: Instance du WebDriver Selenium
        containing: Chaîne à rechercher dans le nom du produit
    """
    products = driver.find_elements(By.XPATH, selector.product_card['all_products'])
    
    for product in products:
        product_name = product.find_element(By.XPATH, selector.product_card['name']).text
        
        # Si le produit contient la chaîne donnée, cliquer sur ajouter et retourner
        if containing in product_name.lower():
            product.find_element(By.XPATH, selector.product_card['add_button']).click()
            print(f"Produit contenant '{containing}' ajouté au panier")
            return
    
    print(f"Aucun produit contenant '{containing}' trouvé")

def send_keys_with_delay(element, keys):
    """
    Envoie les touches individuellement avec un délai
    
    Args:
        element: Élément web auquel envoyer les touches
        keys: Chaîne de caractères à envoyer
    """
    for key in keys:
        element.send_keys(key)
        time.sleep(0.1)  # Ajouter un court délai entre chaque touche

def cart_page_test():
    """
    Test principal pour la page du panier et le processus de paiement:
    - Ajouter des écrans solaires SPF-30 et SPF-50 au panier
    - Naviguer vers le panier
    - Vérifier les articles du panier
    - Procéder au paiement via Stripe
    - Vérifier la confirmation du paiement
    """
    driver = setup_driver()
    
    try:
        # Accéder à la page principale
        driver.get(config.selenium_config['url'])
        
        # Naviguer vers la boutique d'écrans solaires
        navigate_to_sunscreen_shop(driver)
        
        # Ajouter des écrans solaires spf-30 et spf-50 au panier
        find_product(driver, 'spf-30')
        find_product(driver, 'spf-50')
        
        # Naviguer vers le panier
        cart_button = driver.find_element(By.XPATH, selector.product_card['cart_button'])
        cart_button.click()
        print("Navigation vers le panier.")
        
        # Vérifier les articles du panier
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, selector.cart['base']))
        )
        cart_items = driver.find_elements(By.XPATH, selector.cart['base'])
        
        for item in cart_items:
            item_name = item.text
            print(f"Le panier contient: {item_name}")
            if not ('spf-30' in item_name.lower() or 'spf-50' in item_name.lower()):
                print("Le panier ne contient pas les bons articles!")
                break
        
        # Cliquer sur le bouton de paiement
        pay_button = driver.find_element(By.CLASS_NAME, selector.cart['pay_button'])
        pay_button.click()
        print("Bouton de paiement cliqué.")
        
        # Attendre que l'iframe Stripe se charge et basculer vers celui-ci
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, selector.cart['stripe_iframe']))
        )
        stripe_frame = driver.find_element(By.XPATH, selector.cart['stripe_iframe'])
        driver.switch_to.frame(stripe_frame)
        print("Basculé vers l'iframe Stripe.")
        
        # Remplir l'adresse e-mail et les détails de la carte
        email_address = driver.find_element(By.XPATH, selector.payment['email'])
        email_address.send_keys('projet_test@mundiapolis.ma')
        
        card_number = driver.find_element(By.XPATH, selector.payment['card_number'])
        send_keys_with_delay(card_number, '4242424242424242')
        
        expiry_date = driver.find_element(By.XPATH, selector.payment['expiry_date'])
        send_keys_with_delay(expiry_date, '12/34')
        
        cvc_code = driver.find_element(By.XPATH, selector.payment['cvc_code'])
        cvc_code.send_keys('123')
        
        zip_code = driver.find_element(By.XPATH, selector.payment['zip_code'])
        zip_code.send_keys('12345')
        print("Détails de paiement saisis.")
        
        # Soumettre le formulaire
        submit_button = driver.find_element(By.ID, selector.payment['submit_button'])
        submit_button.click()
        print("Formulaire de paiement soumis.")
        
        # Revenir au contenu principal
        driver.switch_to.default_content()
        
        # Vérifier si le paiement a réussi
        WebDriverWait(driver, 10).until(
            EC.url_contains('confirmation')
        )
        
        header = driver.find_element(By.TAG_NAME, selector.confirmation['header'])
        header_text = header.text
        
        if header_text == "PAYMENT SUCCESS":
            print("Le paiement a réussi.")
        else:
            print("Le paiement a échoué.")
        
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        # Fermer le navigateur
        driver.quit()

if __name__ == "__main__":
    cart_page_test()