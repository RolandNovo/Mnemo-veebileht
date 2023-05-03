from flask import request
from failid import kasutaja_eksisteerib, loeme_listi

def rippmenüü():
    kasutaja_id = request.form.get("hashid")
    if kasutaja_id == None:
        kasutaja_id = request.cookies.get("kasutaja_hash_id")
    print(kasutaja_id)
    if kasutaja_id != "" and kasutaja_id != None:
        #TODO siia tuleb kirjutada hashi otsija ja failide otsija
        # done? testing

        #leiab kas kasutaja hash eksisteerib
        if (kasutaja_eksisteerib(kasutaja_id)):
            #kui eksisteerib, annab talle kuuluvat failid dropdowni
            salvestatud = loeme_listi("kasutaja_tekstid.txt", kasutaja_id)
            return kasutaja_id, salvestatud
        else:
            #ei eksisteeri, ei tule dropdowni midagi
            return kasutaja_id, []
           # kasutaja ei eksisteeri
        # if kasutaja_id in id_ja_tekstid:
        #     dropdown_valikud = id_ja_tekstid.get(kasutaja_id)
        # else:
        #     dropdown_valikud = []
        # return kasutaja_id, dropdown_valikud
    else:
        return None, ""