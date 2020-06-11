# Lecteur de BD

## Lancer l'application
Pour lancer l'application, exécutez le fichier `app.py`

## Structure de fichiers
Pour le bon fonctionnement de l'application la structure des fichiers doit demeurer comme indiqué ci-dessous.

```
project
│   README.md
│   app.py
|   comics.py   
│
└───library
│   │   vosfichiers.cbz/.cbr
│   │   library.json
│   
└───icons
    │   add.png
    │   next.png
    |   previous.png
```

## Fonctionnement
Une fois l'application lancée, la bibliothèque est affichée, si rien n'est dans la bibliothèque, cliquez sur le bouton "+" pour ouvrir le dossier library dans lequel vous devrez ajouter vos fichiers .cbz ou .cbr. 

Une fois les BD ajoutées vous avez la possibilité de lire la BD ou de modifier les informations correspondantes à la BD qui seront stockées dans le fichier `library/library.json`.

Pour lire une BD cliquez simplement sur le bouton "lire la BD" puis déplacez vous dans la BD à l'aide des flèches directionnelles dans la barre d'outils.
