"""
Script pour exécuter tous les tests en une seule session continue
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
from navigation import navigate_to_moisturizer_shop, navigate_to_sunscreen_shop

def setup_driver():
    """Configure et retourne le driver Selenium"""
    chrome_options = Options()
    if config.selenium_config['headless']:
        chrome_options.add_argument('--headless')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def find_cheapest_products(driver, shop_type):
    """
    Trouve et ajoute au panier les produits les moins chers selon le type de boutique
    
    Args:
        driver: Instance du WebDriver Selenium
        shop_type: 'moisturizer' ou 'sunscreen'
    """
    # Attendre que les produits soient chargés
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, selector.product_card['all_products']))
    )
    print("\nAnalyse des produits disponibles...")
    time.sleep(1)  # Pause pour voir la page des produits
    
    # Trouver tous les éléments des produits
    products = driver.find_elements(By.XPATH, selector.product_card['all_products'])
    print(f"Nombre total de produits trouvés: {len(products)}")
    
    if shop_type == 'moisturizer':
        # Listes pour contenir les produits à base d'aloe et d'amande avec leurs prix
        aloe_products = []
        almond_products = []
        
        # Parcourir tous les produits
        print("\nRecherche des produits contenant de l'aloe et de l'amande...")
        for product in products:
            # Obtenir le nom et le prix du produit
            product_name = product.find_element(By.XPATH, selector.product_card['name']).text
            product_price_text = product.find_element(By.XPATH, selector.product_card['price']).text
            
            # Analyser le prix à partir de la chaîne (format: "Price: Rs. XX")
            price_str = product_price_text.replace('Price: ', '').replace('Rs.', '').strip()
            price = float(price_str)
            
            # Ajouter les hydratants à base d'aloe et d'amande à leurs listes respectives
            if 'aloe' in product_name.lower():
                print(f"Produit aloe trouvé: {product_name} - Prix: {price}")
                aloe_products.append({'price': price, 'product': product, 'name': product_name})
            if 'almond' in product_name.lower():
                print(f"Produit amande trouvé: {product_name} - Prix: {price}")
                almond_products.append({'price': price, 'product': product, 'name': product_name})
        
        time.sleep(1)  # Pause pour voir les produits identifiés
        
        # Trouver les hydratants à base d'aloe et d'amande les moins chers
        if aloe_products:
            cheapest_aloe = min(aloe_products, key=lambda x: x['price'])
            print(f"\nSélection du produit aloe le moins cher: {cheapest_aloe['name']} - Prix: {cheapest_aloe['price']}")
            time.sleep(1)  # Pause avant de cliquer
            
            # Faire défiler jusqu'au produit pour le rendre visible
            driver.execute_script("arguments[0].scrollIntoView(true);", cheapest_aloe['product'])
            time.sleep(1)  # Pause après le défilement
            
            cheapest_aloe['product'].find_element(By.XPATH, selector.product_card['add_button']).click()
            print(f"Ajout de l'hydratant à base d'aloe le moins cher au panier.")
            time.sleep(1)  # Pause après avoir cliqué
        else:
            print("Aucun hydratant à base d'aloe trouvé.")
        
        if almond_products:
            cheapest_almond = min(almond_products, key=lambda x: x['price'])
            print(f"\nSélection du produit amande le moins cher: {cheapest_almond['name']} - Prix: {cheapest_almond['price']}")
            time.sleep(1)  # Pause avant de cliquer
            
            # Faire défiler jusqu'au produit pour le rendre visible
            driver.execute_script("arguments[0].scrollIntoView(true);", cheapest_almond['product'])
            time.sleep(1)  # Pause après le défilement
            
            cheapest_almond['product'].find_element(By.XPATH, selector.product_card['add_button']).click()
            print(f"Ajout de l'hydratant à base d'amande le moins cher au panier.")
            time.sleep(1)  # Pause après avoir cliqué
        else:
            print("Aucun hydratant à base d'amande trouvé.")
    
    elif shop_type == 'sunscreen':
        # Initialiser les trackers de produits les moins chers
        cheapest_spf50_product = None
        cheapest_spf50_price = float('inf')
        cheapest_spf30_product = None
        cheapest_spf30_price = float('inf')
        spf50_products = []
        spf30_products = []
        
        # Parcourir tous les produits pour trouver les écrans solaires SPF-50 et SPF-30 les moins chers
        print("\nRecherche des produits SPF-30 et SPF-50...")
        for product in products:
            # Obtenir le nom et le prix du produit
            product_name = product.find_element(By.XPATH, selector.product_card['name']).text
            product_price_text = product.find_element(By.XPATH, selector.product_card['price']).text
            
            # Analyser le prix à partir de la chaîne (format: "Price: Rs. XX")
            price_str = product_price_text.replace('Price: ', '').replace('Rs.', '').strip()
            price = float(price_str)
            
            # Vérifier si le produit est SPF-50 ou SPF-30
            if 'spf-50' in product_name.lower():
                print(f"Produit SPF-50 trouvé: {product_name} - Prix: {price}")
                spf50_products.append({'name': product_name, 'price': price, 'product': product})
                if price < cheapest_spf50_price:
                    cheapest_spf50_product = product
                    cheapest_spf50_price = price
            elif 'spf-30' in product_name.lower():
                print(f"Produit SPF-30 trouvé: {product_name} - Prix: {price}")
                spf30_products.append({'name': product_name, 'price': price, 'product': product})
                if price < cheapest_spf30_price:
                    cheapest_spf30_product = product
                    cheapest_spf30_price = price
        
        time.sleep(1)  # Pause pour voir les produits identifiés
        
        # Ajouter les écrans solaires les moins chers au panier
        if cheapest_spf50_product:
            # Trouver le nom du produit le moins cher
            cheapest_spf50_name = next(item['name'] for item in spf50_products if item['price'] == cheapest_spf50_price)
            print(f"\nSélection du produit SPF-50 le moins cher: {cheapest_spf50_name} - Prix: {cheapest_spf50_price}")
            time.sleep(1)  # Pause avant de cliquer
            
            # Faire défiler jusqu'au produit pour le rendre visible
            driver.execute_script("arguments[0].scrollIntoView(true);", cheapest_spf50_product)
            time.sleep(1)  # Pause après le défilement
            
            cheapest_spf50_product.find_element(By.XPATH, selector.product_card['add_button']).click()
            print(f"Ajout de l'écran solaire SPF-50 le moins cher au panier.")
            time.sleep(1)  # Pause après avoir cliqué
        else:
            print("Aucun écran solaire SPF-50 trouvé.")
            
        if cheapest_spf30_product:
            # Trouver le nom du produit le moins cher
            cheapest_spf30_name = next(item['name'] for item in spf30_products if item['price'] == cheapest_spf30_price)
            print(f"\nSélection du produit SPF-30 le moins cher: {cheapest_spf30_name} - Prix: {cheapest_spf30_price}")
            time.sleep(1)  # Pause avant de cliquer
            
            # Faire défiler jusqu'au produit pour le rendre visible
            driver.execute_script("arguments[0].scrollIntoView(true);", cheapest_spf30_product)
            time.sleep(1)  # Pause après le défilement
            
            cheapest_spf30_product.find_element(By.XPATH, selector.product_card['add_button']).click()
            print(f"Ajout de l'écran solaire SPF-30 le moins cher au panier.")
            time.sleep(1)  # Pause après avoir cliqué
        else:
            print("Aucun écran solaire SPF-30 trouvé.")

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

def process_payment(driver):
    """
    Traite le paiement dans l'iframe Stripe
    
    Args:
        driver: Instance du WebDriver Selenium
    """
    # Cliquer sur le bouton de paiement
    print("\nRecherche du bouton de paiement...")
    pay_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, selector.cart['pay_button']))
    )
    print("Bouton de paiement trouvé, prêt à cliquer...")
    time.sleep(1)  # Pause avant de cliquer
    pay_button.click()
    print("Bouton de paiement cliqué.")
    time.sleep(1)  # Pause après avoir cliqué
    
    # Attendre que l'iframe Stripe se charge et basculer vers celui-ci
    print("\nAttente du chargement de l'iframe Stripe...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, selector.cart['stripe_iframe']))
    )
    stripe_frame = driver.find_element(By.XPATH, selector.cart['stripe_iframe'])
    time.sleep(1)  # Pause avant de basculer vers l'iframe
    driver.switch_to.frame(stripe_frame)
    print("Basculé vers l'iframe Stripe.")
    time.sleep(1)  # Pause après avoir basculé
    
    # Remplir l'adresse e-mail et les détails de la carte
    print("\nRemplissage du formulaire de paiement...")
    email_address = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, selector.payment['email']))
    )
    print("Saisie de l'adresse e-mail: projet_test@mundiapolis.ma")
    email_address.send_keys('projet_test@mundiapolis.ma')
    time.sleep(1)  # Pause après avoir saisi l'e-mail
    
    print("Saisie du numéro de carte: 4242 4242 4242 4242")
    card_number = driver.find_element(By.XPATH, selector.payment['card_number'])
    send_keys_with_delay(card_number, '4242424242424242')
    time.sleep(1)  # Pause après avoir saisi le numéro de carte
    
    print("Saisie de la date d'expiration: 12/34")
    expiry_date = driver.find_element(By.XPATH, selector.payment['expiry_date'])
    send_keys_with_delay(expiry_date, '1234')
    time.sleep(1)  # Pause après avoir saisi la date d'expiration
    
    print("Saisie du code CVC: 123")
    cvc_code = driver.find_element(By.XPATH, selector.payment['cvc_code'])
    cvc_code.send_keys('123')
    time.sleep(1)  # Pause après avoir saisi le CVC
    
    print("Saisie du code postal: 12345")
    zip_code = driver.find_element(By.XPATH, selector.payment['zip_code'])
    zip_code.send_keys('12345')
    time.sleep(1)  # Pause après avoir saisi le code postal
    print("Détails de paiement saisis.")
    
    # Soumettre le formulaire
    print("\nSoumission du formulaire de paiement...")
    submit_button = driver.find_element(By.ID, selector.payment['submit_button'])
    time.sleep(1)  # Pause avant de cliquer
    submit_button.click()
    print("Formulaire de paiement soumis.")
    time.sleep(1)  # Pause après avoir cliqué
    
    # Revenir au contenu principal
    driver.switch_to.default_content()
    
    try:
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
        print(f"Erreur lors de la vérification du paiement: {e}")

def run_complete_test():
    """
    Exécute le flux de test complet en une seule session
    """
    driver = setup_driver()
    
    try:
        print("\n" + "="*50)
        print("DÉBUT DU TEST COMPLET")
        print("="*50)
        
        # 1. Accéder à la page principale
        driver.get(config.selenium_config['url'])
        print("\nAccès à la page principale")
        
        # 2. Obtenir la température
        temperature_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, selector.landing_page['temperature']))
        )
        temperature_text = temperature_element.text
        temperature = float(temperature_text.split()[0])
        print(f"Température détectée: {temperature}°C")
        
        # 3. Décider quelle boutique visiter selon la température
        shop_type = None
        if temperature < 19:
            print("\n" + "-"*50)
            print("ÉTAPE 1: Navigation vers la boutique d'hydratants")
            print("-"*50)
            navigate_to_moisturizer_shop(driver)
            shop_type = 'moisturizer'
        elif temperature > 34:
            print("\n" + "-"*50)
            print("ÉTAPE 1: Navigation vers la boutique de crèmes solaires")
            print("-"*50)
            navigate_to_sunscreen_shop(driver)
            shop_type = 'sunscreen'
        else:
            print("\nLa température est dans une plage confortable. Aucun produit de soins spécifique n'est nécessaire.")
            return
        
        # 4. Trouver et ajouter les produits les moins chers au panier
        print("\n" + "-"*50)
        print(f"ÉTAPE 2: Sélection des produits {shop_type}")
        print("-"*50)
        find_cheapest_products(driver, shop_type)
        
        # 5. Naviguer vers le panier
        print("\n" + "-"*50)
        print("ÉTAPE 3: Navigation vers le panier")
        print("-"*50)
        print("\nRecherche du bouton du panier...")
        cart_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, selector.product_card['cart_button']))
        )
        print("Bouton du panier trouvé, prêt à cliquer...")
        time.sleep(2)  # Pause avant de cliquer
        cart_button.click()
        print("Navigation vers le panier.")
        time.sleep(1)  # Pause plus longue pour voir la transition vers le panier
        
        # 6. Vérifier les articles du panier
        print("\nAttente du chargement du panier...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, selector.cart['base']))
        )
        print("Panier chargé, vérification des articles...")
        time.sleep(1)  # Pause pour voir le panier chargé
        
        cart_items = driver.find_elements(By.XPATH, "//tbody/tr")
        print("\nArticles dans le panier:")
        for item in cart_items:
            print(f"- {item.text}")
            time.sleep(1)  # Pause entre chaque article pour mieux voir
        
        print("\nVérification du panier terminée.")
        time.sleep(1)  # Pause avant de passer à l'étape suivante
        
        # 7. Procéder au paiement
        print("\n" + "-"*50)
        print("ÉTAPE 4: Processus de paiement")
        print("-"*50)
        process_payment(driver)
        
        print("\n" + "="*50)
        print("FIN DU TEST COMPLET")
        print("="*50)
        
    except Exception as e:
        print(f"\nErreur pendant le test: {e}")
    finally:
        # Fermer le navigateur
        driver.quit()

if __name__ == "__main__":
    run_complete_test()
