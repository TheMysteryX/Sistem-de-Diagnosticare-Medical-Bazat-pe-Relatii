# MODELE DE BAZA
SEVERIT_PENAL = {
    "grav": 0,
    "mediu": 1,
    "usor": 2
}

class Conditie:
    def __init__(self, nume, simptomuri, reguli=None):
        self.nume = nume
        self.simptomuri = simptomuri
        self.reguli = reguli if reguli else []

    def __str__(self):
        return self.nume


class DiagnosticSistem:
    def __init__(self, specializare):
        self.specializare = specializare
        self.conditii = []

    def add_conditie(self, conditie):
        self.conditii.append(conditie)

    # SCOR CU SEVERITATE
    def calc_scor(self, conditie, simptomuri):
        scor = 0
        explicatii = []

        for simptom, severitate in simptomuri.items():
            if simptom in conditie.simptomuri:
                greutate = conditie.simptomuri[simptom]
                penalizare = SEVERIT_PENAL[severitate]

                contrib = max(greutate - penalizare, 0)
                scor += contrib

                explicatii.append(
                    f"Simptomul '{simptom}' este {severitate} "
                    f"(greutate {greutate}, penalizare {penalizare}) => contributie {contrib}"
                )

        return scor, explicatii
    
    def calc_scor_max(self, simptomuri):
        max_scor = 0
        for simptom in simptomuri:
            max_greutate = 0
            for conditie in self.conditii:
                if simptom in conditie.simptomuri:
                    max_greutate = max(max_greutate, conditie.simptomuri[simptom])
            max_scor += max_greutate
        return max_scor

    
    # MOTOR DE INFERENTA
    def diagnostica(self, simptomuri):
        temp_rez = []

        for conditie in self.conditii:
            scor, explicatii = self.calc_scor(conditie, simptomuri)
            if scor == 0:
                continue

            sfaturi = []
            for regula in conditie.reguli:
                msg = regula(simptomuri)
                if msg:
                    sfaturi.append(msg)

            temp_rez.append({
                "conditii": conditie,
                "scor": scor,
                "explicatii": explicatii,
                "sfaturi": sfaturi
            })

        if not temp_rez:
            return []

        total_scor = sum(r["scor"] for r in temp_rez)

        rez = []
        for r in temp_rez:
            proc = round((r["scor"] / total_scor) * 100)
            rez.append((
                r["conditii"],
                proc,
                r["scor"],
                r["explicatii"],
                r["sfaturi"]
            ))

        rez.sort(key=lambda x: x[2], reverse=True)
        return rez


# REGULI IF–THEN
#orl
def otita_regula(simptom):
    if (
        simptom.get("durere de ureche") == "grav"
        and simptom.get("febra") in ["mediu", "grav"]
    ):
        return "O durere de ureche grava cu febra rezulta suspiciune mare de otita."
    return None


def sinuzita_regula(simptom):
    if (
        simptom.get("durere faciala") in ["mediu", "grav"]
        and simptom.get("nas infundat")
    ):
        return "Durere faciala impreuna cu nas infundat poate sa fie sinuzita."
    return None

def laringita_regula(simptom):
    if (
        simptom.get("raguseala") == "grav"
        and simptom.get("voce slabita") in ["mediu", "grav"]
    ):
        return "Raguseala grava cu voce slabita cel mai probabil prezinta laringita."
    return None

def faringita_regula(simptom):
    if (
        simptom.get("durere in gat") == "grav"
        and simptom.get("dificultate la inghitire") in ["mediu", "grav"]
    ):
        return "Durere in gat grava si dificultate la inghitire poate fi de la faringita."
    return None


#oftalmologie
def conjunctivita_regula(simptom):
    if simptom.get("ochi rosii") == "grav" and simptom.get("secretii oculare"):
        return "Ochi rosii cu secretii cel mai probabil de la conjunctivita."
    return None

def glaucom_regula(simptom):
    if simptom.get("durere oculara") == "grav" and simptom.get("vedere incetosata"):
        return "O durere oculara grava impreuna cu vederea incetosata pot prezenta glaucom."
    return None

def miopie_regula(simptom):
    if simptom.get("vedere neclara la distanta") in ["mediu", "grav"]:
        return "Vederea neclara la distanta poate fi cel mai probabil de la miopie."
    return None


#cardiologie
def hipertensiune_regula(simptom):
    if simptom.get("tensiune crescuta") == "grav" and simptom.get("cefalee"):
        return "Tensiunea crescuta grava cu cefalee pot fi de la hipertensiune."
    return None

def angina_regula(simptom):
    if simptom.get("durere toracica") == "grav" and simptom.get("efort fizic"):
        return "Durere toracica la efort poate fi angina."
    return None

def aritmie_regula(simptom):
    if simptom.get("palpitatii") == "grav" and simptom.get("lesin"):
        return "Palpitatii grave cu lesin cel mai probabil de la aritmie."
    return None

#neurologie
def migrena_regula(simptom):
    if simptom.get("durere de cap") == "grav" and simptom.get("greata"):
        return "Durere de cap grava cu greata cel mai probabil poate fi o migrena."
    return None
def epilepsie_regula(simptom):
    if simptom.get("convulsii") == "grav" and simptom.get("pierdere de constienta"):
        return "Convulsii grave cu pierdere de constienta prezinta epilepsie."
    return None
def avc_regula(simptom):
    if simptom.get("amorteala brusca") == "grav" and simptom.get("dificultate la vorbire"):
        return "Amorteala brusca grava cu dificultate la vorbire pot fi suspiciune de AVC."
    return None

#ortopedie
def fractura_regula(simptom):
    if simptom.get("durere severa") == "grav" and simptom.get("deformare vizibila"):
        return "Durere severa si deformare vizibila prezinta o fractura osoasa"
    return None
def entorsa_regula(simptom):
    if simptom.get("durere moderata") in ["mediu", "grav"] and simptom.get("dificultate la miscare"):
        return "Durere moderata si dificultate la miscare prezinta o posibila entorsa."
    return None
def artrita_regula(simptom):
    if simptom.get("durere articulatii") in ["mediu", "grav"] and simptom.get("rigiditate"):
        return "Durere la articulatii si rigiditate rezulta o posibila artrita."
    return None

#urologie
def infectie_regula(simptom):
    if simptom.get("durere la urinare") == "grav" and simptom.get("urinare frecventa"):
        return "Durere la urinare grava si urinare frecventa poate fi infectie urinara."
    return None
def calculi_regula(simptom):
    if simptom.get("durere lombara") == "grav" and simptom.get("sange in urina"):
        return "Durere lombara grava si sange in urina pot fi suspiciune de calculi renali."
    return None
def prostatita_regula(simptom):
    if simptom.get("dificultate la urinare") == "grav" and simptom.get("durere pelvina"):
        return "Durere la urinare grava si durere pelvina pot fi suspiciune de prostatita."
    return None

#dermatologie
def eczema_regula(simptom):
    if simptom.get("mancarime") == "grav" and simptom.get("uscaciune"):
        return "MAncărime grava si uscaciune prezinta suspiciune de eczema."
    return None
def psoriazis_regula(simptom):
    if simptom.get("placi solzoase") == "grav" and simptom.get("roseata"):
        return "Placi solzoase grave si roseata prezinta suspiciune de psoriazis."
    return None
def acnee_regula(simptom):
    if simptom.get("cosuri") == "grav" and simptom.get("inflamatie"):
        return "Cosuri grave cu inflamatie prezinta suspiciune de acnee."
    return None

#psihiatrie
def depresie_regula(simptom):
    if simptom.get("tristete persistenta") == "grav" and simptom.get("pierderea interesului"):
        return "Tristete persistenta grava cu pierderea interesului pot fi depresie."
    return None
def anxietate_regula(simptom):
    if simptom.get("neliniste") == "grav" and simptom.get("tensiune musculara"):
        return "Neliniste grava + tensiune musculara → suspiciune de anxietate."
    return None
def bipolar_regula(simptom):
    if simptom.get("episoade maniacale") == "grav" and simptom.get("schimbari de dispozitie"):
        return "Episoade maniacale grave cu schimbari de dispozitie prezinta suspiciune de tulburare bipolara."
    return None

#pneumologie
def astm_regula(simptom):
    if simptom.get("dificultate de respiratie") == "grav" and simptom.get("tuse"):
        return "Dificultate grava de respiratie si tuse prezinta astm."
    return None
def bronsita_regula(simptom):
    if simptom.get("tuse productiva") == "grav" and simptom.get("febra"):
        return "Tuse productiva grava si febra reprezinta bronsita."
    return None
def pneumonie_regula(simptom):
    if simptom.get("febra mare") == "grav" and simptom.get("tuse severa"):
        return "Febra mare grava si tuse severa prezinta suspiciune de pneumonie"
    return None

#gastroenterologie
def gastrita_regula(simptom):
    if simptom.get("durere abdominala") == "grav" and simptom.get("greata"):
        return "Durere abdominala grava si greata prezinta pot fi gastrita"
    return None
def reflux_regula(simptom):
    if simptom.get("arsura la stomac") == "grav" and simptom.get("regurgitare acida"):
        return "Arsura gravă la stomac si regurgitare acida prezinta reflux gastroesofagian."
    return None
def colon_regula(simptom):
    if simptom.get("durere abdominala") == "grav" and simptom.get("balonare"):
        return "Durere abdominala grava si balonare pot fi sindrom de colon iritabil."
    return None

#endocrinologie
def diabet_regula(simptom):
    if simptom.get("sete excesiva") == "grav" and simptom.get("urinare frecventa"):
        return "Sete excesiva grava cu urinare frecventa prezinta suspiciune de diabet zaharat"
    return None
def hipotiroidism_regula(simptom):
    if simptom.get("oboseala") == "grav" and simptom.get("crestere in greutate"):
        return "Oboseala grava si crestere in greutate pot fi hipotiroidism."
    return None
def hipertiroidism_regula(simptom):
    if simptom.get("pierdere in greutate") == "grav" and simptom.get("iritabilitate"):
        return "Pierdere grava in greutate cu iritabilitate prezinta suspiciune de hipertiroidism."
    return None

#stomatologie
def carie_regula(simptom):
    if simptom.get("durere dentara") == "grav" and simptom.get("sensibilitate la cald/rece"):
        return "Durere dentara grava si sensibilitate la cald/rece prezinta suspiciune de carie dentara."
    return None
def gingivita_regula(simptom):
    if simptom.get("sangerare gingivala") == "grav" and simptom.get("umflare gingivala"):
        return "Sangerare gingivala grava si umflare gingivala pot fi gingivita"
    return None
def abces_regula(simptom):
    if simptom.get("durere severa") == "grav" and simptom.get("umflare faciala"):
        return "Durere dentara severa si umflare faciala pot fi abces dentar."
    return None

#pediatrie
def varicela_regula(simptom):
    if simptom.get("eruptie cutanata") == "grav" and simptom.get("mancarime"):
        return "Eruptie cutanata grava cu mancarime poate fi varicela."
    return None
def rujeola_regula(simptom):
    if simptom.get("eruptie cutanata") == "grav" and simptom.get("tuse"):
        return "Eruptie cutanata grava cu tuse pot fi rujeola."
    return None
def otita_copii_regula(simptom):
    if simptom.get("durere de ureche") == "grav" and simptom.get("febra"):
        return "Durere de ureche grava si febra pot fi otita la copii."
    return None

# CONFIGURARE SISTEM DIAGNOSTIC
def create_orl_sistem():
    orl = DiagnosticSistem("ORL")

    orl.add_conditie(Conditie(
        "Otita",
        simptomuri={
            "durere de ureche": 5,
            "scadere auz": 3,
            "senzatie de presiune": 4,
            "febra": 2
        },
        reguli=[otita_regula]
    ))

    orl.add_conditie(Conditie(
        "Sinuzita",
        simptomuri={
            "durere faciala": 5,
            "nas infundat": 4,
            "durere de cap": 3,
            "secretii nazale": 2,
            "febra": 2
        },
        reguli=[sinuzita_regula]
    ))

    orl.add_conditie(Conditie(
        "Laringita",
        simptomuri={
            "raguseala": 5,
            "voce slabita": 4,
            "tuse uscata": 3,
            "durere in gat": 2
        },
        reguli=[laringita_regula]
    ))

    return orl


def create_oftalmo_sistem():
    oft = DiagnosticSistem("Oftalmologie")

    oft.add_conditie(Conditie(
        "Conjunctivita",
        {
            "ochi rosii": 5,
            "mancarime ochi": 3,
            "secretii oculare": 4
        },
        reguli=[conjunctivita_regula]
    ))

    oft.add_conditie(Conditie(
        "Glaucom",
        {
            "durere oculara": 5,
            "vedere incetosata": 4,
            "halouri luminoase": 3
        },
        reguli=[glaucom_regula]
    ))

    oft.add_conditie(Conditie(
        "Miopie",
        {
            "vedere neclara la distanta": 5,
            "oboseala oculara": 3
        },
        reguli=[miopie_regula]
    ))

    return oft


def create_cardio_sistem():
    card = DiagnosticSistem("Cardiologie")

    card.add_conditie(Conditie(
        "Hipertensiune",
        {
            "tensiune crescuta": 5,
            "ameteli": 3,
            "cefalee": 2
        },
        reguli=[hipertensiune_regula]
    ))

    card.add_conditie(Conditie(
        "Angina pectorala",
        {
            "durere toracica": 5,
            "dispnee": 4,
            "transpiratii reci": 3
        },
        reguli=[angina_regula]
    ))

    card.add_conditie(Conditie(
        "Aritmie",
        {
            "palpitatii": 5,
            "ameteli": 3,
            "lesin": 4
        },
        reguli=[aritmie_regula]
    ))

    return card 

def create_neuro_sistem():
    neu = DiagnosticSistem("Neurologie")

    neu.add_conditie(Conditie(
        "Migrenă",
        {
            "durere de cap": 5,
            "greata": 3,
            "sensibilitate la lumina": 4
        },
        reguli=[migrena_regula]
    ))

    neu.add_conditie(Conditie(
        "Epilepsie",
        {
            "convulsii": 5,
            "pierdere de constienta": 4,
            "confuzie": 3
        },
        reguli=[epilepsie_regula]
    ))

    neu.add_conditie(Conditie(
        "Accident vascular cerebral",
        {
            "amorteala brusca": 5,
            "dificultate la vorbire": 4,
            "pierdere de echilibru": 3
        },
        reguli=[avc_regula]
    ))

    return neu

def create_orto_sistem():
    ort = DiagnosticSistem("Ortopedie")

    ort.add_conditie(Conditie(
        "Fractura osoasa",
        {
            "durere severa": 5,
            "umflare": 4,
            "deformare vizibila": 3
        },
        reguli=[fractura_regula]
    ))

    ort.add_conditie(Conditie(
        "Entorsa",
        {
            "durere moderata": 4,
            "umflare": 3,
            "dificultate la miscare": 2
        },
        reguli=[entorsa_regula]
    ))

    ort.add_conditie(Conditie(
        "Artrita",
        {
            "durere articulatii": 4,
            "rigiditate": 3,
            "umflare": 2
        },
        reguli=[artrita_regula]
    ))

    return ort

def create_urol_sistem():
    uro = DiagnosticSistem("Urologie")

    uro.add_conditie(Conditie(
        "Infectie urinara",
        {
            "durere la urinare": 5,
            "urinare frecventa": 4,
            "senzatie de arsura": 3
        },
        reguli=[infectie_regula]
    ))
    uro.add_conditie(Conditie(
        "Calculi renali",
        {
            "durere lombara": 5,
            "sange în urina": 4,
            "greata": 3
        },
        reguli=[calculi_regula]
    ))
    uro.add_conditie(Conditie(
        "Prostatita",
        {
            "dificultate la urinare": 5,
            "durere pelvina": 4,
            "febra": 3
        },
        reguli=[prostatita_regula]
    ))
    return uro

def create_dermato_sistem():
    der = DiagnosticSistem("Dermatologie")
    der.add_conditie(Conditie(
        "Eczema",
        {
            "mancarime": 5,
            "uscaciune": 4,
            "roseata": 3
        },
        reguli=[eczema_regula]
    ))
    der.add_conditie(Conditie(
        "Psoriazis",
        {
            "placi solzoase": 5,
            "roseata": 4,
            "mancarime": 3
        },
        reguli=[psoriazis_regula]
    ))
    der.add_conditie(Conditie(
        "Acnee",
        {
            "cosuri": 5,
            "puncte negre": 4,
            "inflamatie": 3
        },
        reguli=[acnee_regula]
    ))

    return der

def create_psih_sistem():
    psi = DiagnosticSistem("Psihiatrie")
    psi.add_conditie(Conditie(
        "Depresie",
        {
            "tristete persistenta": 5,
            "pierderea interesului": 4,
            "oboseala": 3
        },
        reguli=[depresie_regula]
    ))
    psi.add_conditie(Conditie(
        "Anxietate",
        {
            "neliniste": 5,
            "tensiune musculara": 4,
            "iritabilitate": 3
        },
        reguli=[anxietate_regula]
    ))
    psi.add_conditie(Conditie(
        "Tulburare bipolara",
        {
            "episoade maniacale": 5,
            "schimbari de dispozitie": 4,
            "energie crescuta": 3
        },
        reguli=[bipolar_regula]
    ))

    return psi

def create_pneumo_sistem():
    pneu = DiagnosticSistem("Pneumologie")
    pneu.add_conditie(Conditie(
        "Astm",
        {
            "dificultate de respiratie": 5,
            "tuse": 4,
            "respiratie suieratoare": 3
        },
        reguli=[astm_regula]
    ))
    pneu.add_conditie(Conditie(
        "Bronsita",
        {
            "tuse productiva": 5,
            "febra": 4,
            "durere toracica": 3
        },
        reguli=[bronsita_regula]
    ))
    pneu.add_conditie(Conditie(
        "Pneumonie",
        {
            "febra mare": 5,
            "tuse severa": 4,
            "dificultate de respiratie": 3
        },
        reguli=[pneumonie_regula]
    ))
    return pneu

def create_gastro_sistem():
    gast = DiagnosticSistem("Gastroenterologie")
    gast.add_conditie(Conditie(
        "Gastrita",
        {
            "durere abdominala": 5,
            "greata": 4,
            "voma": 3
        },
        reguli=[gastrita_regula]
    ))
    gast.add_conditie(Conditie(
        "Reflux gastroesofagian",
        {
            "arsura la stomac": 5,
            "regurgitare acida": 4,
            "dificultate la inghitire": 3
        },
        reguli=[reflux_regula]
    ))
    gast.add_conditie(Conditie(
        "Sindrom de colon iritabil",
        {
            "durere abdominala": 5,
            "balonare": 4,
            "diaree": 3,
            "constipatie": 3
        },
        reguli=[colon_regula]
    ))

    return gast

def create_endo_sistem():
    endo = DiagnosticSistem("Endocrinologie")
    endo.add_conditie(Conditie(
        "Diabet zaharat",
        {
            "sete excesiva": 5,
            "urinare frecventă": 4,
            "oboseala": 3
        },
        reguli=[diabet_regula]
    ))
    endo.add_conditie(Conditie(
        "Hipotiroidism",
        {
            "oboseala": 5,
            "crestere in greutate": 4,
            "sensibilitate la frig": 3
        },
        reguli=[hipotiroidism_regula]
    ))
    endo.add_conditie(Conditie(
        "Hipertiroidism",
        {
            "pierdere in greutate": 5,
            "iritabilitate": 4,
            "palpitatii": 3
        },
        reguli=[hipertiroidism_regula]
    ))

    return endo

def create_stomato_sistem():
    stom = DiagnosticSistem("Stomatologie")
    stom.add_conditie(Conditie(
        "Caria dentară",
        {
            "durere dentara": 5,
            "sensibilitate la cald/rece": 4,
            "gaura vizibila": 3
        },
        reguli=[carie_regula]
    ))
    stom.add_conditie(Conditie(
        "Gingivită",
        {
            "sangerare gingivală": 5,
            "umflare gingivala": 4,
            "respirație urât mirositoare": 3
        },
        reguli=[gingivita_regula]
    ))
    stom.add_conditie(Conditie(
        "Abces dentar",
        {
            "durere severa": 5,
            "umflare faciala": 4,
            "febra": 3
        },
        reguli=[abces_regula]
    ))

    return stom

def create_pedia_sistem():
    ped = DiagnosticSistem("Pediatrie")
    ped.add_conditie(Conditie(
        "Varicelă",
        {
            "eruptie cutanata": 5,
            "mancarime": 4,
            "febra": 3
        },
        reguli=[varicela_regula]
    ))
    ped.add_conditie(Conditie(
        "Rujeola",
        {
            "eruptie cutanata": 5,
            "tuse": 4,
            "febra": 3
        },
        reguli=[rujeola_regula]
    ))
    ped.add_conditie(Conditie(
        "Otita la copii",
        {
            "durere de ureche": 5,
            "iritabilitate": 4,
            "febra": 3
        },
        reguli=[otita_copii_regula]
    ))

    return ped

# INPUT UTILIZATOR
sisteme = {
    "1": create_orl_sistem(),
    "2": create_oftalmo_sistem(),
    "3": create_cardio_sistem(),
    "4": create_neuro_sistem(),
    "5": create_orto_sistem(),
    "6": create_urol_sistem(),
    "7": create_dermato_sistem(),
    "8": create_psih_sistem(),
    "9": create_pneumo_sistem(),
    "10": create_gastro_sistem(),
    "11": create_endo_sistem(),
    "12": create_stomato_sistem(),
    "13": create_pedia_sistem()
}

print("=== SISTEM EXPERT MEDICAL ===")
print("Alege specialitatea:")
print("1. ORL")
print("2. Oftalmologie")
print("3. Cardiologie")
print("4. Neurologie")
print("5. Ortopedie")
print("6. Urologie")
print("7. Dermatologie")
print("8. Psihiatrie")
print("9. Pneumologie")
print("10. Gastroenterologie")
print("11. Endocrinologie")
print("12. Stomatologie")
print("13. Pediatrie")

alegere = input("Optiune: ").strip()

if alegere not in sisteme:
    print("Optiune invalida.")
    exit()

sistem = sisteme[alegere]

print("Introduceti simptomele si severitatea lor (ex: durere de ureche:grav)")

simptomuri = {}

while True:
    linie = input("Simptom (ENTER pentru a opri): ").lower().strip()
    if linie == "":
        break

    if ":" not in linie:
        print("Format invalid. Folositi format-ul simptom:severitate")
        continue

    simptom, severitate = linie.split(":")
    simptom = simptom.strip()
    severitate = severitate.strip()

    if severitate not in SEVERIT_PENAL:
        print("Severitate invalida. Introduceti una din severitatile date: usor, mediu, grav.")
        continue

    simptomuri[simptom] = severitate


rezultate = sistem.diagnostica(simptomuri)

# AFISARE REZULTATE
print("\n--- Rezultate diagnostic ---")

if not rezultate:
    print("Nu s-au identificat potriviri.")
else:
    for cond, proc, raw, expl, sfat in rezultate:
        print(f"\n🔹 {cond.nume} → scor: {proc}% (scor brut: {raw})")

        print("   Simptome relevante:")
        for e in expl:
            print("   -", e)

        if sfat:
            print("   Recomandari / observatii:")
            for a in sfat:
                print("   ", a)