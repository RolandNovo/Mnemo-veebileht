# Klass, et muuta sarnasemaks kasutaja ja StT saadud tulemusi.
import re

def ühtlusta(tekst):
    if tekst[0] == "0":
        return(re.sub(r'\W*','',tekst)[1:])
    return(re.sub(r'\W*','',tekst).lower())

# essa = "0:  kits käis metsas marju söömas , karikakrais kepsu löömas ."
# tessa = "Kits käis metsas marju söömas, \nkarikakrais kepsu löömas"

# essa = re.sub(r'\W*','',essa)[1:]

# tessa = re.sub(r'\W*','',tessa).lower()
# print(essa)
# print(tessa)

def anna_hinne(protsent):
    if (protsent < 50):
        return ("Ehk on taustal palju müra? Proovi selgemini rääkida!")
    elif (protsent >= 50 and protsent < 75):
        return ("See oli täitsa okei. Saab ka paremini.")
    elif (protsent >= 75 and protsent < 90):
        return ("See oli väga hea. Niimoodi juba läheb!")
    else:
        return ("Suurepärane! Oled asja selgeks saanud.")