import copy
import random

def provjeri_ispravnost_bojanja(obojani_vrhovi, matrica_povezanosti):
    for vrh in matrica_povezanosti:
        for susjedan_vrh in matrica_povezanosti[vrh]:
            if obojani_vrhovi[vrh] == obojani_vrhovi[susjedan_vrh]:
                return False
    
    return True


def iscrpno_pretrazivanje(vrhovi, matrica_povezanosti, k, indeks_vrha):
    # kraj rekurzije
    if indeks_vrha == len(vrhovi):
        if provjeri_ispravnost_bojanja(vrhovi, matrica_povezanosti):
            return vrhovi
        else:
            return None

    for boja in range(k):
        vrhovi[indeks_vrha] = boja
        bojanje_vrhova = iscrpno_pretrazivanje(vrhovi, matrica_povezanosti, k, indeks_vrha + 1)
        if bojanje_vrhova is not None:
            return bojanje_vrhova
    
    return None


def vrhovi_po_prioritetu(matrica_povezanosti):
    # sortiraj po broju incidentnih vrhova
    sortirani_vrhovi_po_prioritetu = sorted(list(matrica_povezanosti.items()), key=lambda x: len(x[1]), reverse=True)
    sortirani_vrhovi_po_prioritetu = [x[0] for x in sortirani_vrhovi_po_prioritetu]
    return sortirani_vrhovi_po_prioritetu


def usmjereno_iscrpno_pretrazivanje(vrhovi, matrica_povezanosti, vrhovi_po_prioritetu, k, indeks):
    if indeks == len(vrhovi):
        return vrhovi
    
    dostupne_boje = [i for i in range(k)]
    susjedni_vrhovi = matrica_povezanosti[vrhovi_po_prioritetu[indeks]]
    for i in range(indeks):
        if vrhovi_po_prioritetu[i] in susjedni_vrhovi:
            boja_susjeda = vrhovi[vrhovi_po_prioritetu[i]]
            if boja_susjeda in dostupne_boje:
                dostupne_boje.remove(boja_susjeda)
    
    for boja in dostupne_boje:
        vrhovi[vrhovi_po_prioritetu[indeks]] = boja
        bojanje = usmjereno_iscrpno_pretrazivanje(vrhovi, matrica_povezanosti, vrhovi_po_prioritetu, k, indeks + 1)
        if bojanje is not None:
            return bojanje
        if indeks == 0:
            return None
    
    return None


def pohlepno_pretrazivanje(vrhovi, matrica_povezanosti, vrhovi_po_prioritetu, k, indeks):
    if indeks == len(vrhovi):
        return vrhovi
    
    dostupne_boje = [i for i in range(k)]
    susjedni_vrhovi = matrica_povezanosti[vrhovi_po_prioritetu[indeks]]
    for i in range(indeks):
        if vrhovi_po_prioritetu[i] in susjedni_vrhovi:
            boja_susjeda = vrhovi[vrhovi_po_prioritetu[i]]
            if boja_susjeda in dostupne_boje:
                dostupne_boje.remove(boja_susjeda)
    
    if len(dostupne_boje) == 0:
        return None
    
    vrhovi[vrhovi_po_prioritetu[indeks]] = dostupne_boje[0]
    return pohlepno_pretrazivanje(vrhovi, matrica_povezanosti, vrhovi_po_prioritetu, k, indeks + 1)


def odredi_kromatski_broj(vrhovi, matrica_povezanosti):
    ispravno_bojanje = None
    for k in range(len(vrhovi), 0, -1):
        bojanje_vrhova = iscrpno_pretrazivanje(vrhovi, matrica_povezanosti, k, 0)
        if bojanje_vrhova is None:
            return ispravno_bojanje, k + 1
        ispravno_bojanje = copy.copy(bojanje_vrhova)
    return ispravno_bojanje, 1



def funkcija_cijene(vrhovi, matrica_povezanosti):
    cijena = 0
    for vrh in matrica_povezanosti:
        for susjedan_vrh in matrica_povezanosti[vrh]:
            if vrhovi[vrh] == vrhovi[susjedan_vrh]:
                cijena = cijena + 1
    return cijena / 2


def generiraj_slucajnu_jedinku():
    ...

def rang_selekcija(populacija):
    ...

def generiraj_djecu(roditelj1, roditelj2):
    ...

def maksimalna_dobrota(populacija):
    ...

def slucajan_dogadaj():
    ...

def slucajan_gen():
    ...


def generiraj_pocetnu_populaciju(velicina_populacije):
    pocetna_populacija = []
    for _ in range(velicina_populacije):
        pocetna_populacija.append(generiraj_slucajnu_jedinku())
    return pocetna_populacija


def izaberi_roditelje(populacija):
    roditelji = []
    for _ in range(len(populacija)):
        roditelji.append(rang_selekcija())
    return roditelji


def krizanje(roditelji):
    djeca = []
    for i in range(0, len(roditelji), 2):
        dijete_1, dijete_2 = generiraj_djecu(roditelji[i], roditelji[i+1])
        djeca.append(dijete_1)
        djeca.append(dijete_2)
    return djeca


def mutiraj(djeca):
    for dijete in djeca:
        for gen in dijete.kromosom:
            if slucajan_dogadaj():
                gen = slucajan_gen()
    return djeca


def genetski_algoritam(broj_iteracija, limit_dobrote, velicina_populacije):
    populacija = generiraj_pocetnu_populaciju(velicina_populacije)
    for _ in range(broj_iteracija):
        najbolja_dobrota, najbolja_jedinka = maksimalna_dobrota(populacija)
        if najbolja_dobrota >= limit_dobrote:
            return True, najbolja_jedinka
        
        roditelji = izaberi_roditelje(populacija)
        djeca = krizanje(roditelji)
        populacija = mutiraj(djeca)

    return False, najbolja_jedinka


def slucajna_mutacija_na_krivim_vrhovima(djeca, matrica_susjedstva, k):
    for dijete in djeca:
        for vrh, boja_vrha in enumerate(dijete):
            potrebno_novo_bojanje = False
            for susjedan_vrh in matrica_susjedstva[vrh]:
                if boja_vrha == dijete[susjedan_vrh]:
                    potrebno_novo_bojanje = True
                    break
            if not potrebno_novo_bojanje:
                continue
            nova_boja = random.randint(k)
            dijete[vrh] = nova_boja
    return djeca


def ciljana_mutacija_na_krivim_vrhovima(djeca, matrica_susjedstva, k):
    for dijete in djeca:
        for vrh, boja_vrha in enumerate(dijete):
            potrebno_novo_bojanje = False
            boje_susjeda = set()
            for susjedan_vrh in matrica_susjedstva[vrh]:
                boje_susjeda.add(dijete[susjedan_vrh])
                if boja_vrha == dijete[susjedan_vrh]:
                    potrebno_novo_bojanje = True
            
            if not potrebno_novo_bojanje:
                continue

            if len(boje_susjeda) == k:
                nova_boja = random.randint(k)
            else:
                dostupne_boje = []
                for boja in range(k):
                    if boja not in boje_susjeda:
                        dostupne_boje.append(boja)
                nova_boja = random.choice(dostupne_boje)
            dijete[vrh] = nova_boja
    return djeca


def kombinacija_slucajne_i_ciljane_mutacije(djeca, matrica_susjedstva, k, najbolja_dobrota, granica):
    if najbolja_dobrota >= granica:
        return slucajna_mutacija_na_krivim_vrhovima(djeca, matrica_susjedstva, k)
    else:
        return ciljana_mutacija_na_krivim_vrhovima(djeca, matrica_susjedstva, k)
    

class genetski_algoritam():

    ...


def odredi_kromatski_broj(graf, parametri_genetskog_algoritma):
    delta = graf.maksimalan_stupanj_grafa
    kromatski_broj = graf.kromatski_broj
    k = delta + 1
    prethodno_rjesenje = None
    while(k >= kromatski_broj):
        algoritam = genetski_algoritam(parametri_genetskog_algoritma, graf, k)
        rjesenje = algoritam.run()
        if rjesenje is None:
            return k + 1, prethodno_rjesenje
        prethodno_rjesenje = rjesenje
        k = k - 1
    return k + 1, prethodno_rjesenje


def main():
    vrhovi = [0, 0, 0, 0, 0]
    k = len(vrhovi) - 2
    matrica_povezanosti = {0: [1, 2, 3, 4], 1: [0, 3, 4], 2: [0], 3: [0, 1, 4], 4: [0, 1, 3]}
    # print(iscrpno_pretrazivanje(vrhovi, matrica_povezanosti, k, 0))
    # print(odredi_kromatski_broj(vrhovi, matrica_povezanosti))
    # print(funkcija_cijene(vrhovi, matrica_povezanosti))
    po_prioritetu = vrhovi_po_prioritetu(matrica_povezanosti)
    print(usmjereno_iscrpno_pretrazivanje(vrhovi, matrica_povezanosti, po_prioritetu, k, 0))
    print(pohlepno_pretrazivanje(vrhovi, matrica_povezanosti, po_prioritetu, k, 0))


if __name__ == "__main__":
    main()