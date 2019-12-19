# Self-Improving Reactive Agent Based on Reinforcement Learning, Planning and Teaching 

Voici le code de notre projet d'IAR. Il se décompose en plusieurs fichiers.


# DEPENDANCES 
- tkinter 
- tensorflow2.0

# DESCRIPTION FICHIERS 

## dynamic_environment.py 

C'est fichier principal qui permet de créer l'environnement de simulation, là où l'agent va pouvoir bouger ainsi que les ennemies. 
La grille d'affichage est réaliser en utilisant la librairie "tkinter" pour afficher l'environnement, les ennemies(E), les obstacles(O), l'agent(I) et la barre de vie en bas à gauche. 

C'est aussi dans cette partie que l'agent va apprendre en s'aidant de ses senseurs et du réseaux de neurones, créé dans un autre fichier. 

## agent.py 

C'est le fichier permettant de faire bouger l'agent selon la politique suivie, il peut aussi utiliser ses senseurs pour observer son environnement comprenant: 

- Les obstacles, la nourriture et les ennemies. 

## ennemy.py 
Ce fichier permet de faire bouger les ennemies selon la politique décrite dans l'article.

## neural_network.py 
C'est dans ce fichier là qui est créée le réseaux de neurones pour calculer l'utilité d'une action étant donné l'état dans lequel l'agent se trouve.

Vous pouvez modifier la fonction d'erreur et utiliser soit la mean absolute error(mae) qui calcule la valeur absolue de l'erreur entre la target et la prédiction. 
Vous pouvez aussi utiliser la mean squared error(mse) qui calcule la valeur l'erreur quadratique entre la target et la prédiction.

Les librairies utilisées sont tensorflow 2.0 pour créer le réseau de neurone et faire l'apprentissage par backpropagation.

## test.py 
Fichier test, pour vérifier principalement si les senseurs y compris les patchs ont bien été codé.  
