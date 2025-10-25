# AI használat dokumentáció

Ez a fájl nyomon követi és dokumentálja az MI-eszközökkel (pl. ChatGPT) végzett munkafolyamatot: a felhasznált promptok, a kapott válaszok rövid összefoglalója és azok hatása a projekt következő lépéseire.

## Rövid projektismertető
A projekt célja egy webes alkalmazás készítése, amely egy megadott munkakör/pozíció alapján lekéri az álláshirdetéseket, szöveges elemzést végez, és megjeleníti a leggyakoribb készségeket. A backend Flask alapú, a frontend egyszerű HTML/CSS/JS.

## Az MI használatának céljai
- Ötlet- és architektúra tervezés
- Kód-generálás (sablonok, endpointok, segédfüggvények)
- Természetes nyelvi feldolgozás (segítség NLTK/pandas használatában, skill-extrahálás)
- Dokumentáció és README írása
- Hibakeresési / tesztelési javaslatok

## Prompt-log sablon (használható naplózásra)
Tároljuk minden promptot az alábbi mezőkkel, hogy visszakereshető legyen, mit kérdeztünk, milyen modell-választ kaptunk, és mit tettünk a válasz alapján.

- Dátum: YYYY-MM-DD
- Prompt (teljes szöveg):
- Modell / beállítások: (pl. ChatGPT-4, temperature=0.2)
- Válasz rövid összefoglalója:
- Hatás / Mit tettünk a válasz alapján:
- Ellenőrzés: hogyan validáltuk (unit teszt, manuális futtatás, lint)

## Kezdeti naplóbejegyzések
1) Dátum: 2025-10-25
   - Prompt: "Create a project folder structure for a Python Flask backend and a simple HTML/CSS/JS frontend. The project name is 'linkedin-skill-analyzer'..." (rövidítve)
   - Modell / beállítások: ChatGPT (workspace assistant)
   - Válasz összefoglaló: Projektstruktúra létrehozva (mappák: backend, frontend, docs) és `requirements.txt` generálása.
   - Hatás: A projekt könyvtárak és az első `requirements.txt` fájl létrejöttek a repo gyökerében.
   - Ellenőrzés: Fájlok jelenléte megtekintve a workspace-ben.

2) Dátum: 2025-10-25
   - Prompt: "Generate a requirements.txt for a Flask backend that handles basic API routes and JSON responses. Include Flask, requests, and any common utilities like nltk or pandas for simple text analysis."
   - Válasz összefoglaló: `requirements.txt` elkészítve tartalmazva Flask, Flask-Cors, requests, pandas, nltk, python-dotenv, numpy, scikit-learn; megjegyzés gunicornról.
   - Hatás: Fájl létrehozása és a todo lista frissítése.
   - Ellenőrzés: `requirements.txt` megnyitva a workspace-ben.

## Példák hasznos promptokra (stage-alapú)

1) Projektterv / architektúra
- Prompt: "Segíts egy minimal viable product tervben: Flask backend, mely fogad egy `position` paramétert és visszaadja a top N készséget JSON-ben. Írd le a szükséges endpointokat, adatfolyamot és adatstruktúrákat."
- Várt hatás: részletes végrehajtási terv, endpoint lista, bemenet/kimenet contract.

2) Backend endpoint implementáció
- Prompt: "Adj egy teljes `app.py` fájlt Flask használatával, amely tartalmaz egy `/analyze` POST endpointot, ami JSON `{'position': 'data analyst'}` bemenetet vár és visszaad egy példa JSON választ."
- Várt hatás: futtatható Flask sablon, amelyet később kiegészítünk adatgyűjtéssel és elemzéssel.

3) Szövegelemzés / skill extraction
- Prompt: "Mutass példát, hogyan lehet NLTK-vel tokenizálni, stopword-öket eltávolítani és egyszerű freq-based skill extraction-t végezni job listing szövegekből."
- Várt hatás: kódrészlet, ami a `pandas` DataFrame-et felveszi, tisztítja és gyakoriságot számol.

4) Frontend + fetch
- Prompt: "Adj egy minimális `index.html` + `app.js` példát, amely POST-olja a `position` értéket a backend `/analyze` endpointjára és megjeleníti a kapott készségeket listában."
- Várt hatás: működő kliens-oldali kód, könnyű integrálni.

5) Dokumentáció és beadási csomag
- Prompt: "Írj egy `README.md`-t, ami tartalmazza az install és run lépéseket, a projekt célját, és mit kell benyújtani a vizsgához (kód, dokumentáció, esetleg demo)."
- Várt hatás: kész, letölthető útmutató, az egyes pontok ellenőrizhetők.

## Validálás — javasolt ellenőrzési lépések minden MI-alapú outputnál
- Futassa le a generált kódot izolált környezetben (virtuális env, requirements telepítése).
- Készítsen egy egyszerű unit tesztet (pl. pytest) a kritikus függvényekre (skill extraction, endpoint válaszformátum).
- Manual smoke test: POST egy példa kérésre és ellenőrizze a JSON struktúrát.
- Lint/format: használjon `black`/`flake8` ha szükséges.

## Sablon: prompt→válasz→hatás naplózás (markdown)
Használjon mindig egy bejegyzést minden MI-interakciónál; a fájl fogja tartalmazni a promptok teljes szövegét és a rövidített válaszokat, valamint a végrehajtott akciókat.

---

Végezetül: ha szeretnéd, elkezdem automatikusan betölteni az eddigi promptokat/válaszokat ide (beleértve a pontos prompt-szövegeket), és részletesebben dokumentálom, melyik kód- vagy fájlváltoztatás történt minden lépésnél. Kérlek jelezd, elfogadod-e, hogy a PDF-ben szereplő beadási kritériumokat feltételezésekkel kiegészítsem a roadmapben (lásd következő fájl).