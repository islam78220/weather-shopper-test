<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
<body>

<h1>Projet d’automatisation des tests Selenium - Weather Shopper</h1>

<h2>Présentation du projet</h2>
<p>
  Dans le cadre de notre projet d’automatisation des tests, nous avons choisi le site
  <a href="https://weathershopper.pythonanywhere.com" target="_blank" rel="noopener noreferrer">Weather Shopper</a>,
  un site e-commerce simple qui recommande des produits en fonction de la température extérieure.
</p>
<p>
  L’objectif principal est d’automatiser les scénarios de test fonctionnels à l’aide de Selenium WebDriver afin de vérifier que les fonctionnalités clés du site fonctionnent correctement, notamment la sélection des produits en fonction de la météo et l’ajout au panier.
</p>
<p>
  Ce projet a été réalisé en binôme: Salma Noujjaji et Islam Mezouar.
</p>

<hr />

<h2>Fonctionnalités testées</h2>
<ul>
  <li>Lecture de la température affichée sur la page d’accueil.</li>
  <li>Sélection automatique du produit adapté en fonction de la température :
    <ul>
      <li>Crème solaire si la température est supérieure à 34°C.</li>
      <li>Manteau si la température est inférieure à 19°C.</li>
    </ul>
  </li>
  <li>Ajout du produit recommandé au panier.</li>
  <li>Vérification que le produit ajouté correspond bien à la recommandation.</li>
  <li>Validation du panier pour s’assurer que les articles sont bien présents.</li>
  <li>Exécution des tests sur différents cas pour garantir la robustesse.</li>
</ul>

<hr />

<h2>Technologies et outils utilisés</h2>
<ul>
  <li><strong>Python 3.x</strong> : Langage principal du projet.</li>
  <li><strong>Selenium WebDriver</strong> : Pour automatiser les interactions avec le navigateur.</li>
  <li><strong>WebDriver Manager</strong> : Pour gérer automatiquement les pilotes des navigateurs (ChromeDriver).</li>
  <li><strong>pytest</strong> : Framework de tests pour organiser et exécuter les scénarios.</li>
  <li><strong>Navigateur Chrome</strong> (version compatible avec ChromeDriver).</li>
</ul>

<hr />

<h2>Installation et configuration</h2>
<ol>
  <li><strong>Cloner le dépôt</strong> sur votre machine locale :</li>
</ol>
<pre><code>git clone https://github.com/votre-utilisateur/weather-shopper-test.git
cd weather-shopper-test
</code></pre>
<ol start="2">
  <li><strong>Installer les dépendances</strong> :</li>
</ol>
<pre><code>pip install -r requirements.txt
</code></pre>
<p><strong>Pré-requis :</strong></p>
<ul>
  <li>Avoir installé Google Chrome </li>
  <li>Le WebDriver correspondant sera automatiquement téléchargé grâce à WebDriver Manager.</li>
</ul>

<hr />

<h2>Comment exécuter les tests</h2>
<p>
  Pour lancer tous les tests automatisés, il suffit de lancer la commande suivante:
</p>
<pre><code> python run_complete_test
</code></pre>


</body>
</html>
