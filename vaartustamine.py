from fuzzywuzzy import fuzz
from tuvastustest import tuvasta_hääl
from parandamine import parandame
from hindamine import ühtlusta, anna_hinne
import re

def väärtusta(alg, mikrofoni_salvestus):
    #alg = "Tekst, mida ma sooviksin väga-väga pähe õppida.".lower()
    #alg = "Sõnad nagu plekk-katus.".lower()

    voice_valikud = tuvasta_hääl(mikrofoni_salvestus)
    process_valikud = []
    #print()
    print("Potentsiaalsed kasutaja öeldud laused:")
    for transc in voice_valikud['alternative']:
        print(transc['transcript'])
        process_valikud.append(transc['transcript'])

    print()
    # Eelnevalt oli see, nüüd oma meetod selle jaoks
    #parim_valik = process.extractOne(alg, process_valikud)
    # läbi vaadata ja uurida täpselt mille järgi ta valib milline parim on
    
    parim_valik = parandame(alg, process_valikud)
    #print(parim_valik)

    #alg = re.sub("[,.!?]", "", alg)
    alg_üht = ühtlusta(alg)
    parim_valik_üht = ühtlusta(parim_valik)
    print (f"alg: {alg}")
    print(f"parim_valik: {parim_valik}")
    protsent = fuzz.ratio(parim_valik_üht, alg_üht)
    print(f"Protsent: {protsent}")
    vastus = (parim_valik, anna_hinne(protsent))
    #print(f"Klappivus: {fuzz.ratio(parim_valik, alg)}")

    return vastus
    # Saab kasutada ka sellist võimalust, et näpukad ära parandada, nt
    # siis kui tuvastas "kurgi" asemel "purgi" saab programm ise parandada

    # import difflib as dl
    # dl.get_close_matches('thme', ['them', 'that', 'this'])
    # ['them]

# väärtusta("kui arno isaga koolimajja jõudis olid tunnid juba alanud".lower())