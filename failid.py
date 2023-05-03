import os
import codecs
import re
import pickle

full_path = '/home/rolandnovoseltsev'

def failis_eksisteerib(otsitav_string, faili_path):
    # string to search in file - code from: https://www.geeksforgeeks.org/python-how-to-search-for-a-string-in-text-files/
    # Kutsuda välja ainult siis, kui fail eksisteerib
    with codecs.open(faili_path, 'r', 'utf-8-sig') as fp:
        # read all lines using readline()
        for rida in fp:
            # check if string present on a current line
            if rida.find(otsitav_string) != -1:
                return True
        return False

#funktsioon, et leida kas sellise id-ga kasutaja eksisteerib süsteemis
def kasutaja_eksisteerib(kasutaja_id):
    #full_path = os.getcwd()
    kasutajad_file = os.path.join(full_path, "kasutajad.txt")
    #kontrolli, kas kasutajate fail olemas
    if os.path.exists(kasutajad_file):
        # Kontrolli, kas selline kasutaja olemas:
        return failis_eksisteerib(kasutaja_id, kasutajad_file)
    else:
        return False

def kirjutame(mingifail, mingitekst, mode, kaust = ""):
    #full_path = os.getcwd()
    faili_path = os.path.join(full_path, kaust, mingifail)
    with codecs.open(faili_path, mode, 'utf-8-sig') as file:
        file.write(mingitekst + "\n")
    return

#kirjutame("testime.txt", "Test tekst vol 2 näiteks õüäö", 'a')

def update_info(mingitekst, hash_id):
    #full_path = os.getcwd()
    faili_path = os.path.join(full_path, hash_id, "state.bin")
    kausta_path = os.path.join(full_path, hash_id)
    loo_kaust(kausta_path)
    with codecs.open(faili_path, 'wb') as file:
        pickle.dump(mingitekst, file)
    return

def lisame_kasutajale_teksti(kasutaja_id, uus_tekst_id, uus_tekst):
    #full_path = os.getcwd()
    # Kasutaja kausta path
    kausta_path = os.path.join(full_path, kasutaja_id)
    # Kontrolli, kas selline kasutaja olemas
    if (not kasutaja_eksisteerib(kasutaja_id)):
        # kirjutame uue kasutaja juurde
        kirjutame("kasutajad.txt", kasutaja_id, "a", full_path)
    # vajadusel loome kasutajale kausta
    kausta_path = loo_kaust(kasutaja_id)
    tekstide_id_file = os.path.join(kausta_path, "kasutaja_tekstid.txt")
    if (os.path.exists(tekstide_id_file)):
        if (failis_eksisteerib(uus_tekst_id, tekstide_id_file)):
            return False
    # kirjutame uue teksti_id faili
    kirjutame(tekstide_id_file, uus_tekst_id, "a")
    # kirjutame uue teksti uude faili
    faili_path = os.path.join(kausta_path, uus_tekst_id)
    kirjutame(faili_path, uus_tekst, "w")
    return True

def loeme(faili_nimi, kaust = ""):
    #full_path = os.getcwd()
    faili_path = os.path.join(full_path, kaust, faili_nimi)
    with codecs.open(faili_path, 'r', 'utf-8-sig') as fail:
        failis_tekst = fail.read()
    return failis_tekst

def get_info(hash_id):
    #full_path = os.getcwd()
    bin_path = os.path.join(full_path, hash_id, "state.bin")
    with open(bin_path, "rb") as file:
        info_tekst = pickle.load(file)
    return info_tekst

#print(loeme("testime.txt"))

def loeme_listi(faili_nimi, kaust = ""):
    #full_path = os.getcwd()
    faili_path = os.path.join(full_path, kaust, faili_nimi)
    rea_kaupa = []
    with codecs.open(faili_path, 'r', 'utf-8-sig') as fail:
        for rida in fail:
            rea_kaupa.append(rida)
    return rea_kaupa

def loo_kaust(kausta_nimi):
    dir = os.path.join(os.getcwd(), kausta_nimi)
    if not os.path.exists(dir):
        os.mkdir(dir)
    return dir


def puhasta_nimi(nimi):
    # võetud 16.04.2023 artiklist Python Tricks: Replace All Non-alphanumeric Characters in a String, Autor: Nicholas Nadeau
    # addressilt: https://nadeauinnovations.com/post/2020/11/python-tricks-replace-all-non-alphanumeric-characters-in-a-string/

    # define our regex expression
    pattern = "[^0-9a-zA-ZõüäöÕÜÄÖ\s]+"

    rea_vahetusteta = re.sub("[\n|\t|\r]", "", nimi) # Rolandi lisatud
    # perform a regex substitution to clean the string
    clean_string = re.sub(pattern, "", rea_vahetusteta)
    print(clean_string)

    return clean_string

#update_info("suva tekst", "37195")
#print(get_info("37195"))
# print("vol_1")

# loo_kaust("testkaust")

# kirjutame("testime.txt", "tekst kaustas olevas failis", "w", "testkaust")
# print(loeme("testime.txt", "testkaust"))

# print("vol_2")

# test_path = os.path.join(os.getcwd(),"testime2.txt")
# kirjutame(test_path, "valisid valik 1", 'a')
# print(failis_eksisteerib("valisid valik 2", test_path))
# kirjutame(test_path, "valisid valik 2", 'a')
# kirjutame(test_path, "valisid valik 3", 'a')
# print(failis_eksisteerib("valisid valik 2", test_path))
# print(loeme(test_path))

# print("vol_3")

# kasutaja_id = "123"
# vaike_tekst = "Mingi suvaline tekst"
# pikem = "Mingi suvaline tekst\nmida ma tihti kasutan"
# vaike_tekst2 = "Mingi teine tekst"
# pikem2 = "Mingi suvaline tekst\nmida ma veel tihedamini kasutan"
# print(kasutaja_eksisteerib(kasutaja_id))
# print(lisame_kasutajale_teksti(kasutaja_id, vaike_tekst, pikem))
# print(kasutaja_eksisteerib(kasutaja_id))
# print(lisame_kasutajale_teksti(kasutaja_id, vaike_tekst2, pikem2))
# print(loeme(vaike_tekst, kasutaja_id))
# print()
# print(loeme(vaike_tekst2, kasutaja_id))