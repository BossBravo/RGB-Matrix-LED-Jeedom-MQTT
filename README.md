# Visuel
<img width="4032" height="2268" alt="image" src="https://github.com/user-attachments/assets/2a6b47ce-9772-4806-87ed-57d788727399" />


# Matériel
- [Adafruit Matrix Portal - CircuitPython Powered](https://www.adafruit.com/product/4745)
- [64x32 RGB LED Matrix](https://www.adafruit.com/product/2278)
- [3D printable support](https://www.printables.com/model/1095162-64x64-p5-rgb-led-matrix-frame-and-feet-with-rasper)

# Outils
- [Convert image to pixels](https://giventofly.github.io/pixelit/#tryit)
- [RGB LED Matrices with CircuitPython](https://learn.adafruit.com/rgb-led-matrices-matrix-panels-with-circuitpython/advanced-multiple-panels)

# Configuration
Modifiez le fichier [settings.toml](settings.toml) avec vos paramètres wifi, jeedom et mqtt

# Installation

Source : [Matrix Portal M4 - Starter Guide](https://github.com/davidrazmadzeExtra/Matrix_Portal_M4_Starter/tree/main)

<hr />

## MatrixPortal
### 1. Prep the MatrixPortal

Connect power to the matrix display panel using the power terminals. Also install to the board via the connectors.

https://learn.adafruit.com/adafruit-matrixportal-m4/prep-the-matrixportal

### 2. Install CircuitPython

We will drag a `.uf2` file into the `MATRIXBOOT` Volume to get a `CIRCUITPY` drive where we can edit files.

`cp adafruit-circuitpython-matrixportal_m4-en_US-7.3.3.uf2 /Volumes/MATRIXBOOT`

https://learn.adafruit.com/adafruit-matrixportal-m4/install-circuitpython

### 3. Install the Mu Editor

This is the recommended editor you should be using for CircuitPython development.

https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor

### 4. Put files

Put all files from this repo inside the Adafruit Matrix Portal, it contains lib, code, settings

<hr />

## Jeedom
### 1. Ajout Object MQTT
Ajoutez un objet MQTT du même nom que l'objet dans le fichier settings.toml  
<img width="115" height="141" alt="image" src="https://github.com/user-attachments/assets/d975f1b2-e138-42c6-9a62-fb5fce2a82a1" />  
Mettez le même nom dans le topic racine  
<img width="815" height="131" alt="image" src="https://github.com/user-attachments/assets/409f1af6-6de5-423e-b693-1673c1405708" />

### 2. Ajouter commandes et infos
Voici la liste des commandes et infos à ajouter, disponible sur le code  
<img width="1890" height="1463" alt="image" src="https://github.com/user-attachments/assets/78a4f9aa-8687-43d8-9eb5-88afb5da0df9" />

### 3. Pilotage
Vous devez ensuite créer un scénario pour mettre à jour toutes ces données MQTT.  
Evidemment ici je vous partage mon code avec mes informations que je souhaite afficher, vous pouvez très bien tout modifier de chaque côté, ajouter / supprimer des commandes.

# Informations
- Il subsiste un petit bug, de temps en temps l'écran s'éteint et le module ne reboot pas, je n'ai pas encore trouvé l'origine, j'ai juste à appuyer sur le bouton power pour le redémarrer.  
- Je n'ai pas encore trouvé le moyen de le faire reboot une fois par jour, apaprement ce ne serait pas possible avec ce module  Matrix Portal, si quelqu'un trouve, je suis preneur. La commande QQTT screen/reboot ne fonctione donc pas pour le moment.
- Je n'ai non plus pas réussi à contrôler la luminosité, il semblerai que ce soit pas faisable, idem si quelqu'un trouve, je suis preneur.
