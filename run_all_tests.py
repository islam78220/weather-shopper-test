"""
Script pour exécuter tous les tests séquentiellement avec un délai entre chaque test
"""
import time
import subprocess
import sys
import importlib.util

def run_test(test_file):
    """
    Exécute un fichier de test et attend sa complétion
    
    Args:
        test_file: Nom du fichier de test à exécuter
    """
    print(f"\n{'='*50}")
    print(f"Exécution de {test_file}")
    print(f"{'='*50}\n")
    
    # Exécuter le test
    process = subprocess.Popen(['python', test_file], 
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)
    
    # Afficher la sortie en temps réel
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    # Attendre que le processus se termine
    process.wait()
    
    # Afficher les erreurs s'il y en a
    stderr = process.stderr.read()
    if stderr:
        print(f"Erreurs: {stderr}")

def import_module_from_file(file_path):
    """Importe un module Python à partir d'un chemin de fichier"""
    module_name = file_path.replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def main():
    """Fonction principale pour exécuter les tests en fonction de la température"""
    print("\n" + "="*50)
    print("Démarrage du test de la page d'accueil")
    print("="*50 + "\n")
    
    # Importer le module test_landing_page
    landing_page_module = import_module_from_file('test_landing_page.py')
    
    # Exécuter le test de la page d'accueil et récupérer le type de boutique
    shop_type = landing_page_module.landing_page_test()
    
    print(f"\nRésultat du test de la page d'accueil: {shop_type}")
    print("Pause de 3 secondes...\n")
    time.sleep(3)
    
    # Exécuter le test approprié en fonction du type de boutique
    if shop_type == 'moisturizer':
        print("\n" + "="*50)
        print("Exécution du test des hydratants")
        print("="*50 + "\n")
        run_test('test_moisturizers.py')
    elif shop_type == 'sunscreen':
        print("\n" + "="*50)
        print("Exécution du test des crèmes solaires")
        print("="*50 + "\n")
        run_test('test_sunscreens.py')
    else:
        print("\nAucun test spécifique à exécuter car la température est dans une plage confortable ou une erreur s'est produite.")
        # Dans ce cas, on ne continue pas avec le test du panier
        print("\nTous les tests ont été exécutés.")
        return
    
    # Pause avant d'exécuter le test du panier et du paiement
    print("\nPause de 3 secondes avant le test du panier et du paiement...")
    time.sleep(3)
    
    # Exécuter le test du panier et du paiement
    print("\n" + "="*50)
    print("Exécution du test du panier et du paiement")
    print("="*50 + "\n")
    run_test('test_cart_payment.py')
    
    print("\nTous les tests ont été exécutés.")



if __name__ == "__main__":
    main()
