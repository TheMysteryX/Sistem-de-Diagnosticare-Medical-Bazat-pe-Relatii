# Sistem-de-Diagnosticare-Medical-Bazat-pe-Relatii
Sistem expert bazat pe reguli, scris în Python, care sugerează afecțiuni probabile pornind de la simptomele introduse de utilizator și de la severitatea lor. Rularea se face în linia de comandă, iar rezultatul include un scor procentual, explicația calculului și observații generate de reguli IF–THEN.

# Caracteristici
- 13 specialități medicale, fiecare cu 3 afecțiuni modelate
- Simptome cu greutăți diferite pentru fiecare afecțiune
- Severitate per simptom (usor, mediu, grav) care influențează scorul
- Scor brut + scor procentual normalizat între afecțiunile potrivite
- Explicabilitate: pentru fiecare afecțiune se afișează cum a contribuit fiecare simptom
- Reguli IF–THEN care generează recomandări/observații suplimentare
- Fără dependențe externe (doar biblioteca standard Python)
- Specialități și afecțiuni acoperite
- 
**Specialitate                     Afecțiuni**
  ORL                              Otită, Sinuzită, Laringită
  Oftalmologie	              Conjunctivită, Glaucom, Miopie
  Cardiologie	                Hipertensiune, Angină pectorală, Aritmie
  Neurologie	                  Migrenă, Epilepsie, AVC
  Ortopedie	                    Fractură osoasă, Entorsă, Artrită
  Urologie	                      Infecție urinară, Calculi renali, Prostatită
  Dermatologie	              Eczemă, Psoriazis, Acnee
  Psihiatrie	                    Depresie, Anxietate, Tulburare bipolară
  Pneumologie	              Astm, Bronșită, Pneumonie
  Gastroenterologie	    Gastrită, Reflux gastroesofagian, Sindrom de colon iritabil
  Endocrinologie	        Diabet zaharat, Hipotiroidism, Hipertiroidism
  Stomatologie	            Carie dentară, Gingivită, Abces dentar
  Pediatrie	                    Varicelă, Rujeolă, Otită la copii

# Mod de utilizare
Alege specialitatea introducând numărul corespunzător (1–13).
Introdu simptomele în formatul simptom:severitate, câte unul pe linie.
Apasă ENTER pe o linie goală pentru a opri introducerea și a vedea rezultatele.

Severități acceptate: usor, mediu, grav.

Exemplu de sesiune
```
=== SISTEM EXPERT MEDICAL ===
Alege specialitatea:
1. ORL
...
Optiune: 1
Introduceti simptomele si severitatea lor (ex: durere de ureche:grav)
Simptom (ENTER pentru a opri): durere de ureche:grav
Simptom (ENTER pentru a opri): febra:mediu
Simptom (ENTER pentru a opri):

--- Rezultate diagnostic ---

🔹 Otita → scor: 100% (scor brut: 6)
   Simptome relevante:
   - Simptomul 'durere de ureche' este grav (greutate 5, penalizare 0) => contributie 5
   - Simptomul 'febra' este mediu (greutate 2, penalizare 1) => contributie 1
   Recomandari / observatii:
    O durere de ureche grava cu febra rezulta suspiciune mare de otita.
```
(Exemplu ilustrativ; procentul depinde de simptomele care se potrivesc cu celelalte afecțiuni din specialitate.)

Cum funcționează
1. Calculul scorului (cu penalizare de severitate)

Fiecare afecțiune are un dicționar simptom → greutate. Pentru fiecare simptom introdus care aparține afecțiunii:
```
contribuție = max(greutate − penalizare(severitate), 0)
scor = Σ contribuții
```
Penalizările sunt definite în SEVERIT_PENAL:
**Severitate	  Penalizare**
grav	          0
mediu	        1
usor	          2

Cu cât simptomul este mai sever, cu atât contribuie mai mult la scor.

2. Motorul de inferență (diagnostica)
Se calculează scorul pentru fiecare afecțiune a specialității alese.
Afecțiunile cu scor 0 sunt ignorate.
Se evaluează regulile IF–THEN asociate fiecărei afecțiuni rămase.
Scorurile se normalizează la procente: procent = scor / suma scorurilor × 100.
Rezultatele sunt sortate descrescător după scorul brut.

3. Reguli IF–THEN
Fiecare afecțiune poate avea una sau mai multe funcții-regulă care primesc dicționarul de simptome și returnează un mesaj (sau None). Exemplu:

```py
def otita_regula(simptom):
    if (
        simptom.get("durere de ureche") == "grav"
        and simptom.get("febra") in ["mediu", "grav"]
    ):
        return "O durere de ureche grava cu febra rezulta suspiciune mare de otita."
    return None
```
# Arhitectura codului
**Componentă	                Rol**
SEVERIT_PENAL	              Maparea severitate → penalizare
Conditie	                            Modelează o afecțiune: nume, simptome cu greutăți, reguli
DiagnosticSistem	            Sistemul unei specialități: colecție de afecțiuni, calcul scor, motor de inferență
*_regula(...)	                      Funcții IF–THEN pentru fiecare afecțiune
create_*_sistem()	            Funcții de configurare pentru fiecare specialitate
sisteme	                            Dicționar număr meniu → sistem
Secțiunea Input utilizator	Meniu, citirea simptomelor, afișarea rezultatelor

# Extinderea sistemului
Adăugarea unei afecțiuni într-o specialitate existentă:
```py
def guturai_regula(simptom):
    if simptom.get("nas infundat") and simptom.get("stranut") == "grav":
        return "Nas infundat si stranut frecvent pot indica un guturai."
    return None

orl.add_conditie(Conditie(
    "Guturai",
    {"nas infundat": 5, "stranut": 4, "secretii nazale": 3},
    reguli=[guturai_regula]
))
```
Adăugarea unei specialități noi:
- Creează o funcție create_<specialitate>_sistem() care returnează un DiagnosticSistem.
- Adaug-o în dicționarul sisteme cu o cheie nouă.
- Adaugă opțiunea în meniul afișat.
