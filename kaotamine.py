#import estnltk
#from estnltk import Text
#from estnltk.taggers import WordTagger
import re
import codecs
import info_tekstist

def sonadeks(tekst):
    #sisu = Text(tekst).tag_layer()
    
    #print(sisu['words'].text)
    sisu2 = tekst.split()
    #print(sisu2)
    #sonad = sisu.words.text
    #WordTagger().tag(sisu)

    # lausete kaupa
    # for lause in sisu.sentences:
    #     print(f"Lause:{lause.enclosing_text}")
    #return sisu['words'].text
    return sisu2

def esimene_sõna(tekst):
    sonad = sonadeks(tekst)
    ainult_esimene = sonad[0] + " "
    
    for sona in sonad[1:]:
        for taht in sona:
            if (bool(re.search('[,.!-:;\\?]', taht))):
                ainult_esimene += taht
            else:
                ainult_esimene += "_"
        ainult_esimene += "  "
    return ainult_esimene

def esimene_täht(tekst):
    sonad = sonadeks(tekst)
    ainult_esimene = ""

    for sona in sonad:
        mitu_tähte = 1
        if len(sona) > mitu_tähte:
            mitu_tähte = 2
        ainult_esimene += sona[:mitu_tähte]
        for taht in sona[mitu_tähte:]:
            if (bool(re.search('[,.!-:;\\?]', taht))):
                ainult_esimene += taht
            else:
                ainult_esimene += "_"
        ainult_esimene += "  "
    return ainult_esimene

def esimene_rida(tekst):
    read = tekst.splitlines()
    ainult_esimene = [read[0]]
    for rida in read[1:]:
        uus_rida = ""
        #print(f"Rida: {rida}")
        for taht in rida:
            #print(f"Taht: {taht}")
            if (bool(re.search('[,.!-:;\\? ]', taht))):
                uus_rida += " " + taht
            else:
                uus_rida += "_"
        uus_rida += "  "
        ainult_esimene.append(uus_rida)
    return ainult_esimene
    #for rida_2 in ainult_esimene:
    #    print(rida_2)

def mitte_midagi(tekst):
    sonad = sonadeks(tekst)
    ainult_esimene = ""

    for sona in sonad:
        for taht in sona:
            if (bool(re.search('[,.!-:;\\?]', taht))):
                ainult_esimene += taht
            else:
                ainult_esimene += "_"
        ainult_esimene += "  "
    return ainult_esimene

#valik_1 = "Ei mäletagi seda päeva\nmil suvi tuli täie väega\nÜkski vaim ei murra maha\naastaaega, mis tulla tahab\nVõim on Emakese Looduse käes\niga päevaga teda tulemas näed"

#valik_2 = "Sõnad nagu plekk-katus."

#valik_4 = "See on v-vä-väga huvitav, aga kas ka ka-su-lik?!"

# def kirjutame(mingitekst):
#     with codecs.open('testime.txt', 'w', 'utf-8-sig') as file:
#         file.write(mingitekst)
#     return

# def loeme(nimi):
#     file = open(nimi, 'r')
#     tekst = file.read()
#     return(tekst)

def kaota(meetod, tekst, nimi):
    terve_text = []
    # kirjutame(tekst)
    tekst = tekst.split('\r\n\r\n')
    if nimi == None:
        for paragrahv in tekst:
            if meetod == esimene_rida:
                terve_text.append(esimene_rida(paragrahv))
            else:
                #print(f"Paragrahv: {paragrahv}")
                rea_kaupa = paragrahv.splitlines()
                #print(f"Rea kaupa: {rea_kaupa}")
                terve_paragrahv = []
                for rida in rea_kaupa:
                    terve_paragrahv.append(meetod(rida))
                terve_text.append(terve_paragrahv)
        #print(f'Lugesime seda: {loeme("testime.txt")}')
        return terve_text
    else:
        # paneme info kokku nii, et saaks rea kaupa õppida karakterit
        # info = info_tekstist.teksti_info(int praegu_rida, int max_read, terve_tekst, hinnatav_tekst)
        ridu_kokku = 0
        hinnatav_tekst = []
            # abimuutuja esimene_rida meetodiga tegelemiseks
        for paragrahv in tekst:
            rida_flag = False
            if meetod == esimene_rida:
                rida_flag = True
            terve_paragrahv = []
            mitmendast_reast = 0
            rea_kaupa = paragrahv.splitlines()

            # if meetod == esimene_rida:
            #     ridu_kokku += 1
            #     terve_paragrahv.append(rea_kaupa[0])
            #     hinnatav_tekst.append((rea_kaupa[0], rea_kaupa[0]))
            #     mitmendast_reast = 1
            
            for rida in rea_kaupa[mitmendast_reast:]:
                # üks rida juures
                ridu_kokku += 1
                # otsime igast reast, kas leiame karakteri nime
                if bool(re.search(r"^"+nimi.lower(), rida.lower())):
                    # kui on rea alguses nimi, siis vaatame kas ta leidub õiges formaadis
                    leitud = re.search('^[A-Za-zõüäöÕÜÄÖ]* \([\w|õüäöÕÜÄÖ| ]*\):|^[A-Za-zõüäöÕÜÄÖ]*:', rida)
                    # ei leidnud, siis töötlemata rida läheb paragrahvi
                    if leitud == None:
                        terve_paragrahv.append(rida)
                        hinnatav_tekst.append((rida, rida))
                    else:
                        # karakteri rida
                        if (rida_flag):
                            terve_paragrahv.append(rida)
                            hinnatav_tekst.append((rida, rida))
                            rida_flag = False
                        else:
                            asukoht = leitud.span()
                            nimi_remark = rida[asukoht[0] : asukoht[1]]
                            karakteri_tekst = rida[asukoht[1]:]
                            if meetod == esimene_rida:
                                muudetud_tekst = mitte_midagi(karakteri_tekst)
                            else:
                                muudetud_tekst = meetod(karakteri_tekst)
                            hinnatav_tekst.append((nimi_remark + muudetud_tekst, karakteri_tekst))
                            terve_paragrahv.append(nimi_remark + muudetud_tekst)
                else:
                    # ei leidu karakteri nime
                    terve_paragrahv.append(rida)
                    hinnatav_tekst.append((rida, rida))
            terve_text.append(terve_paragrahv)
        #print(f'Lugesime seda: {loeme("testime.txt")}')
        info = info_tekstist.teksti_info(0, ridu_kokku, terve_text, hinnatav_tekst)
        # enne returnis terve_text
        return info

# otsin = "PrInN"
# tekst = "MAARA (põlglikult huuli krimpsutades): Sina ... Prinn! Tahad ma ütlen sulle, kes sa oled? Sa oled üks rikkiläinud looduseime.\nPRINN: Ohoo! Küll on terava keelega! Võta siis teatavaks, et paps käskis mul siin dežuuris olla."
# tekst = tekst.splitlines()
# for rida in tekst:
#     if (bool(re.search(r"^"+otsin.lower(), rida.lower()))):
#         print(f"Selles reas leidsin: {rida}")
#         print()
#         z = re.search('^[A-Za-zõüäöÕÜÄÖ]* \([\w|õüäöÕÜÄÖ| ]*\):|^[A-Za-zõüäöÕÜÄÖ]*:', rida).span()
        # print(z)
        # print(rida[z[0]:z[1]])
        # print("ülejäänud stuff")
        # print(rida[z[1]:])
#     else:
#         print(f"Ei leidnud, nii et terve rida: {rida}")

#valik_3 = 'Kits käis metsas marju söömas,\nkarikakrais kepsu löömas,\nkukeseeni kugistamas,\nmustikmarju mugistamas,\nmaasikmarju matsutamas,\npuravikke patsutamas.\n\nKõik need ampsud tegi viimaks\nrammusaks ja rõõsaks piimaks,\njooksis koju kipsa-kõpsa:\n"Perenaine, palun lüpsa"\nSaagu piima iga laps\njumekaks ja tugevaks!"\n'

# print("\nSuuremast lõigust esimene rida ainult:\n")
# print(esimene_rida(valik_3))
# print("\nEsimene sõna ainult:\n")
# #print(kaota(esimene_sõna, valik_3))
# print("\nEsimene täht ainult:\n")
# print(kaota(esimene_täht, valik_3))

