# Roadmap a teljes pontszám eléréséhez

Megjegyzés: az alábbi roadmap a csatolt `Házi feladat követelmények.pdf` dokumentum általános követelményeire alapoz, és néhány ésszerű feltételezést tartalmaz arról, mit vár el a kidolgozó (functionalitás, dokumentáció, AI használat dokumentálása, bemutatás). Ha a PDF pontos pontozási rubrikája eltér, kérlek jelezd a konkrét pontokat — frissítem a roadmapet ennek megfelelően.

## Feltételezések (kérlek erősítsd meg)
1. Funkcionalitás: Az alkalmazásnak működő backenddel és frontenddel kell rendelkeznie. A backend elfogad egy pozíciót és JSON-ben ad vissza rangsorolt készségeket.
2. Adatforrás: az álláshirdetések lekérése lehet scraping vagy mock/adatminták; működő megoldás esetén a scraping-hez hasznos a `requests` + HTML parsing / API-k használata.
3. Elemzés: legalább egyszerű freq-based skill extraction (pandas + nltk) kell legyen.
4. Dokumentáció: részletes README + AI-használat naplója + rövid architektúra leírás szükséges.
5. Bemutatás: egy rövid demo (screenshot vagy képernyőfelvétel) szükséges lehet.


## Összefoglaló lépések (magas szinten)
1. Repo inicializálása és projekt struktúra (done)
2. Backend: alap Flask app és `/analyze` endpoint (sablon)
3. Elemzés: sample pipeline (text cleaning → skill extraction → aggregálás)
4. Frontend: egyszerű UI a pozíció bevitellel és eredmények megjelenítésével
5. Tesztek + validáció (smoke tests)
6. Dokumentáció: README, docs/ai-usage.md, docs/architecture.md, beadási lista
7. Végső ellenőrzés és beadás

## Részletes feladatlista, sikerfeltételek és ellenőrzés

### 1) Repo és környezet
- Feladatok:
  - `requirements.txt` létrehozása (készült)
  - `.gitignore` hozzáadása
- Sikerfeltétel: egy fejlesztő reprodukálni tudja a környezetet `pip install -r requirements.txt` parancssal.
- Ellenőrzés: `pip install` sikeres (CI vagy lokálisan).

### 2) Backend implementáció (alapok)
- Feladatok:
  - `backend/app.py` létrehozása: Flask app, `/analyze` POST endpoint, CORS engedélyezés
  - Endpoint contract: bemenet JSON {"position": "..."}, kimenet JSON {"skills": [{"skill": "Python", "count": 123}, ...]}
- Sikerfeltétel: endpoint válaszol példa JSON-nel és HTTP 200 státusszal.
- Ellenőrzés: `curl` vagy a frontend `fetch` használatával smoke-test.

### 3) Adatgyűjtés / mock adatok
- Feladatok:
  - Kezdetben készíts egyszerű mock datasetet (CSV vagy JSON) 10-50 hirdetéssel pozíciónként.
  - (Opció) Később implementálj egy lekérő modult (pl. `backend/scraper.py`) `requests` + HTML parsing (BeautifulSoup) segítségével.
- Sikerfeltétel: az elemzés képes bemeneti szövegek listáját feldolgozni.
- Ellenőrzés: elemez egy mintasettet és ad vissza értelmes skill listát.

### 4) Elemző pipeline
- Feladatok:
  - `backend/analysis.py`: text cleaning, tokenizáció (nltk), stopword eltávolítás, skill kinyerés (freq-table) és normalizálás (kis/nagybetű, egybevonások)
  - Opció: használj egyszerű természetes nyelvi szabályokat vagy egy skill-lexikont
- Sikerfeltétel: visszakapott skillek logikus sorrendben (leggyakoribbak elöl).
- Ellenőrzés: unit teszt a `top_skills(texts)` függvényre.

### 5) Frontend
- Feladatok:
  - `frontend/index.html`, `frontend/styles.css`, `frontend/app.js`
  - Input mező pozícióhoz, elküldés `/analyze`-ra, és megjelenítés listában vagy egyszerű diagramon (pl. Chart.js opcionális)
- Sikerfeltétel: interaktív keresés → backend válasz → UI frissítés.
- Ellenőrzés: manuális smoke test a böngészőben.

### 6) Tesztek, linting, futtathatóság
- Feladatok:
  - Kis unit tesztek a `backend/analysis.py`-hoz (pytest)
  - Lint (opcionális: flake8)
- Sikerfeltétel: a kritikus logika lefedve, egyszerű hibákat a tesztek elkapnak.
- Ellenőrzés: `pytest` fut és a kritikus tesztek zöldek.

### 7) Dokumentáció és beadás
- Feladatok:
  - `README.md`: telepítés, futtatás, használat, beadási lista
  - `docs/ai-usage.md`: MI-vel végzett interakciók naplója (elkezdtük)
  - `docs/architecture.md`: komponensek és adatfolyam leírása
  - Képernyőképek vagy rövid demo video készítése
- Sikerfeltétel: minden beadáshoz kért fájl megtalálható a repo gyökerében.
- Ellenőrzés: kövesd a PDF-ben található beadási checklist-et; ha pontos lista van, cross-check.

## Pontozási stratégia (hogyan biztosítsd a maximális pontszámot)
1. Teljes funkcionalitás demonstrálása: futtatható app + működő end-to-end példa.
2. Kódminőség: áttekinthető, moduláris kód; rövid unit tesztek.
3. Dokumentáció: részletes README és AI-használat dokumentáció (minden kulcs-prompt naplózva).
4. Extra: egyszerű vizualizáció (diagram), scraping helyett tisztán működő adatgyűjtő pipeline, vagy automatizált adatfrissítés.

## Javasolt időbeosztás (példa 2 hetes fejlesztésre)
- Nap 1: Repo beállítás, váz szerkezet, requirements, alap Flask app
- Nap 2-3: Mock adatok, analysis pipeline prototípus
- Nap 4-5: Endpoint összekötése az analizissel, smoke tests
- Nap 6: Frontend alapok és integráció
- Nap 7: Tesztek, dokumentáció kezdete
- Nap 8-10: Finomítások, vizualizáció, AI-dokumentáció kitöltése
- Nap 11-14: Ellenőrzés, beadásra előkészítés, demo képernyőkép/video

## Mit kérjek tőled most?
1. Erősítsd meg a PDF pontos pontozását, ha vannak konkrét tételek (ha igen, átszabom a roadmapet pontos rubrikára).
2. Engedélyezd-e, hogy a további AI-interakciókat részletesen naplózzam ide (így a beadási dokumentumban szerepelni fog minden prompt és kapott válasz)?

---

Ha jóváhagyod a fenti feltételezéseket, folytatom:
- létrehozom a `backend/app.py` és `backend/analysis.py` kezdő fájlokat,
- elkészítem a `frontend` starter fájlokat,
- és írok 2-3 gyors unit tesztet az `analysis.py`-hoz.

Jelöld vissza, elfogadod-e a feltételezéseket, vagy küldd a PDF pontos pontozási rubrikáját (ha eltér).