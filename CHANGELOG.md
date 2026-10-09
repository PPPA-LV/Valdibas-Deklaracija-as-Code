# Izmaiņas

## 0.2 — 2026-10-09

- ProcessGit skatītājs: `data/processgit.viewer.json` piesaista redaktoru deklarācijas, rīcības plāna un organizāciju reģistra datnēm; redaktors ProcessGit iframe ielādē datni no repozitorija (PGV_INIT, PGV_FETCH) un saistītās datnes no tās pašas mapes; lejupielādes un projekta funkcijas skatītājā paslēptas.

- Autoritatīvās datnes mapē `data/` (iepriekš `examples/`); datnes nosaukums = objekta identifikators (`lv-dekl-2026-05-28.xml`, `lv-mk-2026-05-28.rp.xml`); pārbaudītājs to pārbauda.

- Viena vārdtelpa visai saimei: `urn:pppa:cac:valdiba:0.2`.
- Globāli unikāli identifikatori visiem elementiem (`docs/IDENTIFIKATORI.md`); valdības ID `lv-mk-…`, deklarācijas ID `lv-dekl-…`.
- Jauns: valdību un organizāciju reģistrs (`GovernmentRegistry`).
- Jauns: apņemšanās analīze XML formā (`CommitmentReading`), agrāk JSON.
- Jauns: rīcības plāns (`ActionPlan`) pēc kārtības ruļļa pielikuma 11 ailēm un MK rīkojuma Nr. 449 prakses.
- Deklarācijā: `Government` (atsauce un statuss), `DataVersion` ar `RetiredId`, `Classification` sadaļām, `Goal` un `Result` jaunām deklarācijām.
- Pārbaudītājs un negatīvie testi.
- Redaktors (`editor/`) pārveidots uz v0.2: identifikatori pēc `docs/IDENTIFIKATORI.md`, datu versija palielinās pēc labojumiem, apņemšanās XML formā, sadaļā „Par” — mērķis, pamatojums, struktūra un tiesiskais pamats. Atver arī v0.1 datnes.
- Piemēros pēdiņas elementu tekstā vairs netiek aizstātas ar `&quot;`.
- Redaktora izskats pēc Claude Docs parauga: malā katra bloka identifikators, kartīte ar metadatiem (identifikators, sadaļa, apņemšanās, rīcības plāna pasākumi, datu versija), saturs ar visiem uzdevumiem, poga „ID”.
- Sadaļā „Par” pievienota „Uzbūve”: visu četru līmeņu (deklarācija, apņemšanās analīze, rīcības plāns, reģistrs) elementi ar XML nosaukumu, identifikatoru, obligātumu, burtiski/vērtējums atzīmēm un rīcības plāna ailēm; „Kā elementi saistās”.
- Nosaukums „Valdības deklarācijas datukopa” (redaktorā, shēmu aprakstos, README); redaktora datne `editor/Valdibas_deklaracijas_datukopa.html`.
- Valoda redaktorā un sadaļā „Par” pielāgota oficiālo dokumentu stilam: profesionāla terminoloģija, norādes nenoteiksmē; „lasījums” aizstāts ar „apņemšanās analīze”, jo „lasījums” valsts pārvaldē apzīmē Saeimas lasījumu.

- Jaunas deklarācijas projekts: `Metadata/DerivedFrom` un `Task/@derivedFrom` — saite uz avota deklarāciju un tās uzdevumu. Uzdevumam divas paralēlas numerācijas: drukātais numurs (`@number`) un pastāvīgs identifikators (`@id`); projektā tie var atšķirties (`docs/IDENTIFIKATORI.md`, 4.a). Pārbaudītājs pārbauda saites uz avota uzdevumiem un ziņo, cik uzdevumu pārņemts, pievienots un izņemts.
- Redaktorā cilnes „Valdības deklarācija” un „Rīcības plāns”: deklarācija tiek atvērta lasīšanai, rediģēšanu ieslēdz slēdzis „Rediģēt”; rīcības plāna skatā pie katra uzdevuma labajā pusē — tā pasākumi (pasākums, rezultāts, atbildīgie, termiņš, prioritāte, finansējums) un kārtības ruļļa 18. un 20. punkta pārbaude.
- Redaktors atveras ar Andra Kulberga vadītā Ministru kabineta deklarāciju (lasīšanas režīmā). „Jaunas deklarācijas projekts” atveras kā tukšs projekts rediģēšanas režīmā; poga „Importēt esošo” pārņem projektā Andra Kulberga deklarāciju. Citu deklarāciju importa saraksts izņemts.
- Redaktorā cilne „Organizācijas”: reģistra nepieciešamība, CaC ID uzbūve, meklējams reģistrs ar pasākumu skaitu katrai institūcijai, plānā minētās institūcijas, kuru reģistrā nav, shēma. Rīcības plāna skatā pie atbildīgajām institūcijām — CaC ID.
- Jauns: organizāciju reģistrs (institūcijas identifikators — CaC ID) (`organizaciju-registrs-0.2.xsd`, `data/organizacijas.xml`), uzturētājs — Valsts kanceleja. Identifikators `SS-IIII` — resors un institūcija resorā, resora vadošā institūcija `SS-0000` (piemēram `20-0000` — Klimata un enerģētikas ministrija); identifikatorus piešķir reģistra uzturētājs, Valsts kases kodi — sasaiste pa gadiem (`BudgetCode`); reģistrācijas numurs — `regNo`; rezervētie resori 00, 90–93; pārceļot institūciju uz citu resoru — jauns identifikators un `successor`; resors, iestādes kods, augstākā iestāde, saīsinājumi, iepriekšējais nosaukums. Izveidots no VDVC reģistra (`tools/organizacijas_no_vdvc.py`); atgūtas 10 institūcijas no sapludinātām avota rindām, pārbaudot pret Valsts kases „Valsts budžeta iestāžu sarakstu” (01.09.2023).
- Rīcības plānā atbildīgās un līdzatbildīgās institūcijas norāda ar organizāciju reģistra identifikatoru (`orgs`), nevis kodu; organizācijas izņemtas no valdību reģistra.
- Rīcības plāna skatā katram pasākumam identifikators (`rp.u001.p3`) un kartīte ar metadatiem: deklarācijas uzdevums, pasākuma vieta uzdevumā, sadaļa, rīkojums, finansējums, prioritāte, atbildīgie, termiņš. Uzdevuma kartītē — tā pasākumu identifikatori.
- Rīcības plāns — otrā datu kopa: shēma pārdēvēta un pārstrādāta (`valdibas-deklaracijas-ricibas-plans-0.2.xsd`, saknes elements `GovernmentActionPlan`). Plāna ailes 1–3 (sadaļa, uzdevuma numurs, uzdevuma teksts) netiek kopētas — pasākums norāda deklarācijas uzdevuma identifikatoru. Pasākumam: teksts, darbības rezultāts, atbildīgās un līdzatbildīgās institūcijas, termiņš (burtiski) un pazīmes — finansējums (rīkojuma 1. vai 2. pielikums) un prioritāte.
- Piemērs `lv-mk-2026-05-28.rp.xml`: viss MK rīkojuma Nr. 449 plāns — 185 pasākumi 52 uzdevumiem, burtiski no likumi.lv; `tools/ricibas_plans_no_likumi.py`.
- Reģistrā: Satiksmes ministrija `SM` (iepriekš `SAM`), Konkurences padome `KP`.
- Vienkāršots: identifikatori tikai deklarācijai, sadaļām, uzdevumiem, pielikumiem un rīcības plāna elementiem; rindkopām, sarakstiem un parakstītājiem identifikatoru nav (shēmā tie vairs nav obligāti). Piemērs `lv-dekl-2026-05-28.xml` atjaunināts.
- Izņemta apņemšanās analīze (`deklaracijas-apnemsanas-0.2.xsd`, piemērs, redaktora sadaļa „Apņemšanās”): tā nav paredzēta normatīvajos aktos. Izņemts `tools/build_examples.py`; piemēri ir galvenais avots.
- Redaktora sadaļa „Shēma” pārveidota: katras shēmas nozīme, identifikatoru veidošanas algoritms soļos ar piemēriem, segmentu tabula, pilni noteikumi. Apzīmējums „AS IS” aizstāts ar „burtiski, kā parakstīts”.
- Redaktorā divas deklarācijas — projekts un avots —, katrai rediģēšana, lasīšana un apņemšanās analīze. Sākumā projektu veido no iepriekšējās valdības deklarācijas. Sadaļa „Par” pārcelta uz beigām.

## 0.1 — 2026-10-08

- Deklarācijas teksts AS IS (`valdibas-deklaracija-0.1.xsd`), identifikatori tikai dokumenta ietvaros (`U001`, `S1-1`).
- Apņemšanās JSON formā (`valdibas-deklaracija-apnemsanas-0.1.schema.json`).
