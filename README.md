# Mnemo-veebileht
Tartu Ülikooli bakalaureuse lõputöö raames valminud abistav veebileht tekstide päheõppimiseks

Veebilehte hoiustatakse PythonAnywhere leheküljel, ja siia lisatud failid on kujul, nagu nad on PythonAnywhere leheküljel. Lehekülje ülesseadmiseks omaenda arvutis tutvuge "Lehekülje ülesseadmisel nõuanded" osaga allpool
Järgnevalt on toodud välja erinevate failide lühikirjeldused.

##failid.py
See file tegeleb failidesse kirjutamisega, sellega salvestatakse uued tekstid ja hoitakse järge, kus kasutaja oma arenguga on Dialoogi režiimi kasutamisel.
Kasutus oleneb operatsioonisüsteemist, üle vaadata muutuja "full_path" ja valida, kus see peaks asuma, nt print(os.getcwd()) sobib asukohaks, aga lihtsalt see command võib tekitada probleeme, all täpsemalt.

##vajalikud teegid.txt
vajalikud teegid on olemas selles failis

##tuvastustest.py
tegeleb Google'i kõnetuvastuse korral mikrofoni kuulamisega.

##vaartustamine.py
võtab õpitava teksti ja kasutaja sisendi (voice_input()) ja otsib sealt kõige rohkem klappiva variandi, ning annab tagasisidet kasutajale kui täpselt ta teksti ette luges.

##kaotamine.py
võtab tekstsisendi ja muudab seda enne kasutajale näitamist. Hetkel on olemas esimene_rida(), esimene_sõna(), esimene_täht() ja tühjus() meetodid.

##kasutamine.py
paneb kõik kenamini kokku veebilehe kasutamise laadseks simulatsiooniks.

##parandamine.py
võtab erinevad kuuldud laused ja paneb neist kokku kõige lähedasema versiooni algtekstile, lootuses parandada kasutaja kogemust

## Lehekülje ülesseadmisel nõuanded
Enne käima panekut vaadata üle "full_path" muutuja failid.py failis.
PythonAnywhere'is on näiteks full_path = /home/rolandnovoseltsev
Windowsis lehte kasutades kirjutada asukoht teisiti, näiteks full_path = "C:\\Users\\minu_kasutaja\\Documents\\GitHub\\Mnemo"

Kui repo sisu on paigutatud "\GitHub\\Mnemo" kausta, siis Mnemo kaustas jooksuta VSC terminalis koodi "Python ./flask_app.py" veebilehe käivitamise jaoks
