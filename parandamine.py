from fuzzywuzzy import fuzz

# laused = ["märgista päeva mil suvi tuli täiega",
# "märgista päeva suvi tuli täiega",
# "märgista päeva me suvi tuli täiega",
# "märgista päeva või suvi tuli täiega",
# "märgista päeva mitte suvi tuli täiega"]

# alg_lause = """Ei mäletagi seda päeva
# mil suvi tuli täie väega"""

def parandame(alg_lause, laused):
    parim_protsent = 0
    parim_valik = laused[0]
    for lause in laused:
        protsent = fuzz.ratio(lause, alg_lause)
        if protsent > parim_protsent:
            parim_valik = lause
    return(parim_valik)

# print("Alg lause:", alg_lause)
# sarnaseim = parandame(alg_lause, laused)
# print("Kõige sarnasem lause:", sarnaseim)
# print(process.extractOne(alg_lause, laused))
# print(process.extractOne(alg_lause, [sarnaseim]))