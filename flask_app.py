from flask import Flask, flash, jsonify, render_template, request, make_response
from fuzzywuzzy import fuzz
import re
from datetime import datetime
import pickle
from kaotamine import *
from vaartustamine import väärtusta
from hindamine import ühtlusta, anna_hinne
from hash_menüü_seostuv import rippmenüü
from failid import *
from info_tekstist import *

app = Flask(__name__)

@app.route('/')
def index():
    hash_tunnus, dropdown_valikud = rippmenüü()
    teksti_id = request.cookies.get('teksti_id')
    text = None
    if hash_tunnus != None:
        if teksti_id != None:
            if teksti_id == "valik1":
                text = loeme("valik1")
            elif teksti_id == "valik2":
                text = loeme("valik2")
            else:
                text = loeme(teksti_id, hash_tunnus)
            return render_template('index.html', new_text = None, hash_tunnus = hash_tunnus, dropdown = dropdown_valikud)
    print(text)
    if text != None:
        return render_template('index.html', old_text = text)
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def change_text():

    text = request.form.get('text')
    print(text)
    hash_tunnus, dropdown_valikud = rippmenüü()
    teksti_id = request.cookies.get('teksti_id')
    if text == None:
        if hash_tunnus != None:
            if teksti_id != None:
                if teksti_id == "valik1":
                    text = loeme("valik1")
                elif teksti_id == "valik2":
                    text = loeme("valik2")
                else:
                    text = loeme(teksti_id, hash_tunnus)
    action = request.form.get('action')
    hash_nupp = request.form.get('hash-nupp')

    # kasutaja vajutab "Logi sisse" nupule
    if hash_nupp == "hash-nupp":
        hash_tunnus, dropdown_valikud = rippmenüü()
        if hash_tunnus != None:
            if not hash_tunnus.isdigit():
                hash_tunnus = None
        res = make_response(render_template('index.html', hash_tunnus = hash_tunnus, dropdown = dropdown_valikud))
        if hash_tunnus != None:
            res.set_cookie("kasutaja_hash_id", str(hash_tunnus))
        return res

    if re.search("[a-zA-Z0-9]", text):
        if request.form.get("dialoog") != None:
            karakteri_nimi = request.form.get("karakter")
            if not re.search("[a-zA-Z]", karakteri_nimi):
                karakteri_nimi = None
        else:
            karakteri_nimi = None
        print(f"nimi:{karakteri_nimi}")
        if action == 'tähed':
            changed_text = kaota(esimene_täht, text, karakteri_nimi)
        elif action == 'sõnad':
            changed_text = kaota(esimene_sõna, text, karakteri_nimi)
        elif action == 'read':
            changed_text = kaota(esimene_rida, text, karakteri_nimi)
        elif action == 'tühjus':
            changed_text = kaota(mitte_midagi, text, karakteri_nimi)
        # Replace new line characters with <br> tag
        hash_tunnus, dropdown_valikud = rippmenüü()

        if hash_tunnus != None:
            if not hash_tunnus.isdigit():
                hash_tunnus = None
        if hash_tunnus == None:
            # loop, kontrollib kas selline kasutaja juba olemas, kui on, +1 value'le
            now = datetime.now()
            hash_tunnus = hash(now)%100000
            while kasutaja_eksisteerib(str(hash_tunnus)):
                hash_tunnus += 1
                if (hash_tunnus > 99999):
                    hash_tunnus = 00000
            # lahkub loopist kui on olemas unikaalne tunnus
        new_text = ""

        # SIIN LISAB UUE TEKSTI HASHI ALLA
        # Teeme tekstile tunnuse
        teksti_id = text[:20]
        teksti_id = puhasta_nimi(teksti_id)
        if teksti_id == "Kits käis metsas mar":
            teksti_id = "valik1"
        if teksti_id == "Autor Tere Loodeta":
            teksti_id = "valik2"
        if not teksti_id == "valik1" and not teksti_id == "valik2":
            lisame_kasutajale_teksti(str(hash_tunnus), teksti_id, text)
        valitud_teksti_info = None
        if karakteri_nimi != None:
            print(changed_text)
            update_info(changed_text, str(hash_tunnus))
            changed_text = changed_text.terve_tekst
            valitud_teksti_info = get_info(str(hash_tunnus))
        # print(valitud_teksti_info.max_read)
        # print(valitud_teksti_info.praegu_rida)
        # print(valitud_teksti_info.terve_tekst)
        # print(valitud_teksti_info.hinnatav_tekst)

        if valitud_teksti_info != None:
            hetkel_rida = valitud_teksti_info.praegu_rida
            new_text = valitud_teksti_info.hinnatav_tekst[hetkel_rida][0]

            print(f"new text kohe enne saidile minekut: {new_text}")
        else:
            for parag in changed_text:
                for rida in parag:
                    new_text += rida + "<br>"
                new_text += "<br>"
        name = request.cookies.get("tegev-nimi")
        print(f"cookies name: {name}")

        res = make_response(render_template('index.html', new_text=new_text, old_text = text, karakteri_nimi = karakteri_nimi, hash_tunnus = hash_tunnus, dropdown = dropdown_valikud))
        res.set_cookie("kasutaja_hash_id", str(hash_tunnus))
        res.set_cookie("teksti_id", teksti_id)
        if karakteri_nimi != None:
            res.set_cookie("tegev-nimi", karakteri_nimi)
        else:
            res.set_cookie("tegev-nimi", max_age=0)
        return res
    else:
        # enter text on null & minu karakter on null & hash ei ole null ->
        #     tagasta leht ise meetodi nupu vajutusel
        #     tagasta dropdown menu tekstiga leht hash nupu vajutamisel
        hash_tunnus, dropdown_valikud = rippmenüü()
        if hash_tunnus != None:
            if not hash_tunnus.isdigit():
                hash_tunnus = None
        # kasutaja_id = request.form.get("hashid")
        res = make_response(render_template('index.html', hash_tunnus = hash_tunnus, dropdown = dropdown_valikud))
        if hash_tunnus != None:
            res.set_cookie("kasutaja_hash_id", str(hash_tunnus))
        return res

        # enter text on null & minu karakter ei ole tühi -> //rida 57 kui pole teksti
        #     jätka tööd nagu minu karakter oleks tühi

        # kõige viimane else
        # Ei oole sisestatud algteksti
        # enter text on null & minu karakter on null & hash on null ->
        #     tagasta leht ise nupu vajutusel (nii meetod nupud kui hash nupp)

# @app.route('/voicerecord', methods=['POST', 'GET'])
# def voicerecord():
#     output_text = väärtusta("Mingi tekst mida ma pähe õpin")
#     print(output_text)
#     return render_template('index.html', voice_text = output_text)

@app.route('/process-text', methods=['POST'])
def process_text():
    text_data = request.json['textData']
    text_data = ühtlusta(text_data)
    print(f"textData saadud process_text() funktsioonis: {text_data}")
    # valitud_teksti_info = get_info(hash_tunnus)
    # if (valitud_teksti_info.suurenda()):
    #     # uuenda teksti
    #     update_info(valitud_teksti_info, str(hash_tunnus))

    # mitmes_rida = valitud_teksti_info.praegu_rida
    # print(valitud_teksti_info.hinnatav_tekst[mitmes_rida])
    # nähtav_tekst = valitud_teksti_info.hinnatav_tekst[mitmes_rida][1]

    hash_tunnus = request.cookies.get("kasutaja_hash_id")
    algne =""

    # return jsonify(nähtav_tekst)
    if request.cookies.get("tegev-nimi") != None and request.cookies.get("tegev-nimi") != "":
        valitud_teksti_info = get_info(hash_tunnus)
        mitmes_rida = valitud_teksti_info.praegu_rida
        print(valitud_teksti_info.hinnatav_tekst[mitmes_rida])
        uus_algne = valitud_teksti_info.hinnatav_tekst[mitmes_rida][1]
        algne = ühtlusta(uus_algne)
        print(f"uus_algne: {algne}")
    else:
        teksti_nimi = request.cookies.get("teksti_id")
        print(teksti_nimi)
        if teksti_nimi == "valik1":
            alg = loeme("valik1")
        elif teksti_nimi == "valik2":
            alg = loeme("valik2")
        else:
            alg = loeme(teksti_nimi, hash_tunnus)
        print("Lähen siia")
        algne = ühtlusta(alg)

    #processed_data = "Klappivus: ", fuzz.ratio(ühtlusta(text_data), ühtlusta(algne))
    protsent = fuzz.ratio(text_data, algne)
    print(protsent)
    processed_data = anna_hinne(protsent)
    print(processed_data)
    return jsonify(processed_data)

@app.route('/dropdown-text', methods=['POST'])
# Siin sees valitakse tekst dropdown menüüst ja antakse sellele value
def dropdown_text():
    value = request.json['value']
    value = puhasta_nimi(value)
    print(f"value: {value}")
    hash_tunnus = request.cookies.get("kasutaja_hash_id")
    # tee value'ga asju
    if value == "valik1":
        suur_tekst = loeme("valik1")

    elif value == "valik2":
        suur_tekst = loeme("valik2")
    else:
        suur_tekst = loeme(value, hash_tunnus)
    print(f"suur_tekst: {suur_tekst}")

    #if value == "valik1":
        #suur_tekst = "valisid valik 1"
    #elif value == "valik2":
        #suur_tekst = "valisid valik 2"
    #elif value == "valik3":
        #suur_tekst = "valisid valik 3"
    #else:
        #suur_tekst = "Ei ole olemas"
    #suur_tekst = "mingi suvakas"
    #print(suur_tekst)
    res = make_response(jsonify(suur_tekst))
    res.set_cookie("teksti_id", value)
    return res

@app.route('/eelmine-text', methods=['POST'])
# Siin sees valitakse tekst dropdown menüüst ja antakse sellele value
def eelmine_text():
    hash_tunnus = request.cookies.get("kasutaja_hash_id")
    valitud_teksti_info = get_info(hash_tunnus)
    if (valitud_teksti_info.vähenda()):
        # uuenda teksti
        update_info(valitud_teksti_info, str(hash_tunnus))

    mitmes_rida = valitud_teksti_info.praegu_rida
    print(valitud_teksti_info.hinnatav_tekst[mitmes_rida])
    nähtav_tekst = valitud_teksti_info.hinnatav_tekst[mitmes_rida][0]

    return jsonify(nähtav_tekst)

@app.route('/järgmine-text', methods=['POST'])
# Siin sees valitakse tekst dropdown menüüst ja antakse sellele value
def järgmine_text():
    print("jõuab siia")
    hash_tunnus = request.cookies.get("kasutaja_hash_id")
    valitud_teksti_info = get_info(hash_tunnus)
    if (valitud_teksti_info.suurenda()):
        # uuenda teksti
        update_info(valitud_teksti_info, str(hash_tunnus))

    mitmes_rida = valitud_teksti_info.praegu_rida
    print(valitud_teksti_info.hinnatav_tekst[mitmes_rida])
    nähtav_tekst = valitud_teksti_info.hinnatav_tekst[mitmes_rida][0]

    return jsonify(nähtav_tekst)

@app.route('/transcibAndFuncs', methods=['POST'])
def trAndFuncs():
    alg = request.json['algtekst']
    print(alg)
    peale_funktsioone = väärtusta(alg)
    print(f"peale Funkstioone: {peale_funktsioone} ")
    return jsonify(peale_funktsioone)

@app.route("/googleTranscrib", methods=['POST', 'GET'])
def googleTranscrib():
    sound_fail = request.files['audio_data']
    hash_tunnus = request.cookies.get("kasutaja_hash_id")
    alg = ""
    if request.cookies.get("tegev-nimi") != None:
        valitud_teksti_info = get_info(hash_tunnus)
        mitmes_rida = valitud_teksti_info.praegu_rida
        print(valitud_teksti_info.hinnatav_tekst[mitmes_rida])
        alg = valitud_teksti_info.hinnatav_tekst[mitmes_rida][1]
    else:
        teksti_nimi = request.cookies.get("teksti_id")
        if teksti_nimi == "valik1":
            alg = loeme("valik1")
        elif teksti_nimi == "valik2":
            alg = loeme("valik2")
        else:
            alg = loeme(teksti_nimi, hash_tunnus)
    print(sound_fail)
    print(alg)
    peale_funktsioone = väärtusta(alg, sound_fail)
    print(f"peale Funkstioone: {peale_funktsioone} ")

    hinne = peale_funktsioone[1]
    print(hinne)
    parim_tekst = peale_funktsioone[0]
    vastus = [parim_tekst, hinne]
    return jsonify(vastus)

if __name__ == '__main__':
    app.run(debug=True)