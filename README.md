
# Scopo del progetto

Questo e' un progetto universitario.
Ho fatto una piattaforma e-commerce dove vengono venduti e recensiti manga e anime (MangaStore).


# Dipendenze

Per questo progetto e' stato usato poetry come venv (v 1.1.14) ma non era obbligatorio, infatti ho cominciato con pipenv.
Nel file pyproject.tml vengono elencate tutte le dipendenze usate con anche le versioni.
Se non si sa usare poetry consiglio di seguire la [documentazione officiale](https://python-poetry.org/docs/).
Dopo aver installato poetry si puo' inizializzare il nuovo ambiente e installare le dipendenze con:
+ `poetry install`


# Run del progetto

Dopo aver installato le dipendenze si puo' fare il run del progetto con:
+ `cd core`, ci porta nella cartella con il file *manage.py*
+ `poetry run py -m manage runserver`, comando che serve per fare il run del server

Si puo' entrare nell'ambiente virtuale con py -m poetry shell e, finche' non ne usciamo, saremo all'interno del venv. 

NB: py -m manage puo' essere usato al posto di py manage.py, per vederne le differenze si puo' guardare nella [documentazione python](https://docs.python.org/3/using/cmdline.html).
NB: Ho ripreso in mano questo progetto e mi sono accorta che py non mi funziona piu come comando e sono ora 'costretta' ad usare `python`. In linea di massima basta usare un qualunque comando python/py/python3/etc...

A questo punto si puo' riuscire a vedere il website alla [pagina](http://127.0.0.1:8000/).
Se il database non e' stato cancellato si possono trovare vari utenti gia prefatti come esempio. 
Le loro credenziali sono nel file account.txt.



# Directory e  File

- **/account**, Cartella con tutte le funzioni e modelli per gli account degli utenti
    
- **/cart**, Cartella con le funzioni del carrelloper l'utente in quella sessione 
    
- **/core**, Cartella col core del progetto

- **/media/images**, Dove vengono salvate tutte le foto

- **/orders**, Cartella con le funzioni e i modelli per gli ordini degli utenti

- **/payment**, Cartella che gestisce i vari pagamenti prima di creare l'ordine

- **/store**, Cartella con funzioni e modelli per i prodotti e le loro categorie

- **/templates**, Tamplate usati 

- **manage.py**, File usato per lo start del programma.


# Altro 
Se ci sono problemi di qualunque natura potete scrivere nelle issue di questo progetto.
Nel caso fossero problemi dovuti alle dipendenze, prima di aprire un issue, chiedo di controllare su altri forum dove possono gia essere stati riscontrati quei problemi (es: stackoverflow,...)

**Ringrazio in anticipo tutti coloro che scaricheranno o riporteranno dei bug o semplicemente lo usano ^-^**
**Ringrazio inoltre [veryacademy](https://www.youtube.com/@veryacademy) in quanto ho preso fortemente spunto dal suo progetto, consiglio di andare a guardare anche il suo tutorial su [Django Ecommerce](https://www.youtube.com/watch?v=UqSJCVePEWU) da cui ho preso spunto!

