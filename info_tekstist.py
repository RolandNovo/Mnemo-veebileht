class teksti_info:
    # int praegu_rida, näitab hetkel vaadatavat rida
        # funktsioon, et saada seda, et muuta seda ühe võrra suuremaks, väiksemaks
        
    # int max_read, näitab mitu rida kokku, vajalik ülemise jaoks
    
    # kasutajale nähtav tekst, sellisel kujul:
        # terve_tekst[paragrahv[rida, rida,..], paragrahv[rida, rida],..]
        # suur list, mis on terve tekst, jaotatud eraldi paragrahvideks, oma korda tehtud ridadeks
        
    # kasutaja korratav tekst
        # list, tuple-dest, (muudetud kujul tekst, hinnatav tekst)
    
    def __init__(self, praegu_rida, max_read, terve_tekst, hinnatav_tekst):
        self.praegu_rida = praegu_rida
        self.max_read = max_read
        self.terve_tekst = terve_tekst
        self.hinnatav_tekst = hinnatav_tekst
    
    def suurenda(self):
        self.praegu_rida += 1
        if (self.praegu_rida >= self.max_read):
            self.praegu_rida -= 1
            return False
        return True
    
    def vähenda(self):
        self.praegu_rida -= 1
        if (self.praegu_rida < 0):
            self.praegu_rida += 1
            return False
        return True

    def algusest(self):
        self.praegu_rida = 0
        return
    
    def õpitav_rida(self, rida):
        return self.hinnatav_tekst[rida][0]

#tekstike = teksti_info(0, 1, "mingi\ntekst\njep", "tekst\n")
#print(tekstike.vähenda())
#print(tekstike.praegu_rida)
#print(tekstike.suurenda())
#print(tekstike.praegu_rida)
#print(tekstike.suurenda())
#print(tekstike.praegu_rida)
#print(tekstike.vähenda())
#print(tekstike.praegu_rida)

#update_info("suva tekst", "010203")
#print(get_info("010203"))