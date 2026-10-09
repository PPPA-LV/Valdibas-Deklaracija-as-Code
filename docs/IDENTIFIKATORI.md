# Identifikatoru veidošanas noteikumi (v0.2)

Valdībai, deklarācijai, tās sadaļām un uzdevumiem, pielikumiem un rīcības plāna elementiem ir **globāli unikāls, pastāvīgs identifikators**. Rindkopām, sarakstiem, saraksta punktiem un parakstītājiem identifikatoru nepiešķir: uz tiem neatsaucas ne rīcības plāns, ne izpildes informācija. Tas ir vienāds XML datnē, datu noliktavā, tīmekļa adresē un MI aģenta atbildē. Līdz šim deklarāciju uzdevumiem šāda identifikatora nebija; rīcības plāns atsaucās uz „Deklarācijā dotā uzdevuma numuru”, kas ir unikāls tikai vienas deklarācijas ietvaros.

## 1. Pamatprincipi

1. **Viens elements — viens identifikators.** Identifikators nesatur nozīmi, kas var mainīties (ministrijas nosaukumu, sadaļas virsrakstu, statusu).
2. **Pastāvīgums.** Piešķirtu identifikatoru nemaina un nekad neizmanto atkārtoti. Ja elements vairs netiek lietots, tā identifikatoru ieraksta `DataVersion/RetiredId`.
3. **Atvasināms no avota.** Ja avotā ir oficiāls numurs (uzdevuma numurs, pasākuma numurs), identifikators to satur. Ja nav — numuru piešķir pēc secības dokumentā parakstīšanas brīdī.
4. **Pašpietiekams.** Identifikators satur visu ceļu līdz saknei, tāpēc to var saprast bez pārējā dokumenta: `lv-dekl-2026-05-28.u012` ir 2026. gada 28. maija deklarācijas 12. uzdevums.
5. **Atļautās rakstzīmes.** Mazie latīņu burti, cipari, `-` un `.` — der XML `xs:ID`, failu nosaukumos un tīmekļa adresēs.

## 2. Saknes identifikatori

| Objekts | Forma | Datums | Piemērs |
|---|---|---|---|
| Valdība (Ministru kabinets) | `lv-mk-GGGG-MM-DD` | Saeimas uzticības balsojuma datums | `lv-mk-2026-05-28` |
| Institūcija (CaC ID) | `SS-IIII` | — (resors + institūcija resorā; sk. 4.b) | `20-0000` (Klimata un enerģētikas ministrija), `15-0203` (VIAA) |
| Deklarācija | `lv-dekl-GGGG-MM-DD` | Datums dokumentā; ja tā nav vai tas nav pilns — uzticības balsojuma datums; ja balsojuma nav — iesniegšanas datums | `lv-dekl-2026-05-28` |

- Ja vienā datumā ir divi vienāda veida objekti, otrajam pievieno `-2`, trešajam `-3` (līdz `-9`).
- **Valdība un deklarācija ir atsevišķi objekti.** Deklarāciju iesniedz Ministru prezidenta amata kandidāts pirms balsojuma; ja uzticība netiek izteikta, deklarācija pastāv bez valdības (`Government/@status = rejected`).
- **Jauna valdība** ir tad, kad Saeima izsaka uzticību jaunam Ministru kabinetam (arī mainoties Ministru prezidentam). Atsevišķa ministra maiņa jaunu valdību neveido.

Piemēri no pieciem dokumentiem:

| Valdība | Valdības ID | Deklarācijas ID | Piezīme |
|---|---|---|---|
| M. Kučinska | `lv-mk-2016-02-11` | `lv-dekl-2016-02-11` | dokumentā „2016. gada februāris” — lieto balsojuma datumu |
| A. K. Kariņa (2019) | `lv-mk-2019-01-23` | `lv-dekl-2019-01-23` | dokumentā datuma nav — lieto balsojuma datumu |
| A. K. Kariņa (2022) | `lv-mk-2022-12-14` | `lv-dekl-2022-12-14` | |
| E. Siliņas | `lv-mk-2023-09-15` | `lv-dekl-2023-09-15` | |
| A. Kulberga | `lv-mk-2026-05-28` | `lv-dekl-2026-05-28` | |

## 3. Elementu identifikatori

Elementa identifikators = vecākelementa identifikators + `.` + segments. Segments = burtu kods + numurs.

### Deklarācija (`lv-dekl-…`)

| Segments | Elements | Numurs | Piemērs |
|---|---|---|---|
| `sNN` | Sadaļa (augstākā līmeņa) | secība dokumentā, 2 cipari | `lv-dekl-2026-05-28.s02` |
| `-NN` | Apakšsadaļa (pievieno sadaļas segmentam) | secība sadaļā | `lv-dekl-2026-05-28.s02-01` |
| `uNNN` | **Uzdevums** | **numurs, kā drukāts**, kad uzdevums izveidots; 3 cipari (projektā sk. 4.a) | `lv-dekl-2026-05-28.u012` |
| `gN` / `rzN` | Sasniedzamais mērķis / rezultāts (jaunām deklarācijām) | secība sadaļā | `lv-dekl-2030-01-15.s03.g1` |
| `piN` | Pielikums | secība | `lv-dekl-2019-01-23.pi1` |

Uzdevuma identifikators **nav atkarīgs no sadaļas**: `u012` paliek `u012`, lai kurā sadaļā uzdevums atrastos. Tāpēc uzdevumu var atrast tikai pēc deklarācijas ID un numura — tieši tā, kā to dara rīcības plāna 2. aile.

### Rīcības plāns (`lv-mk-…`)

| Segments | Elements | Numurs | Piemērs |
|---|---|---|---|
| `rp` | Rīcības plāns (viens valdībai) | — | `lv-mk-2026-05-28.rp` |
| `vN` | Plāna versija = katrs MK rīkojums (apstiprināšana, grozījumi) | secība | `lv-mk-2026-05-28.rp.v1` |
| `uNNN.pN` | Pasākums I sadaļā: uzdevuma numurs + pasākuma numurs | **pasākuma numurs, kā drukāts** („1.3” → `u001.p3`) | `lv-mk-2026-05-28.rp.u001.p3` |
| `zGGGGMMDD` | Izpildes gaitas ieraksts | pārskata perioda beigu datums | `lv-mk-2026-05-28.rp.u001.p3.z20260830` |

## 4. Īpašie gadījumi

| Gadījums | Noteikums |
|---|---|
| Avotā izlaists uzdevuma numurs (piemēram, nav 17.) | `u017` neveido; pārbaudītājs ziņo par iztrūkumu. |
| Projektā uzdevums pārvietots vai pirms tā pievienots jauns uzdevums | Mainās tikai `@number`; identifikators paliek (sk. 4.a). |
| Avotā divreiz drukāts viens numurs | Otrajam `u017-2`; `number` atribūtā paliek drukātais numurs. |
| Vēsturiskā deklarācijā ievadā ir sava numerācija (piemēram 1–5 prioritātes) | Tie nav uzdevumi: numurēts saraksts bez identifikatora, nevis `u`. |
| Pasākums izņemts no plāna ar grozījumiem | Identifikatoru ieraksta `DataVersion/RetiredId`; atkārtoti to neizmanto. |
| Jauns pasākums plāna grozījumos | Nākamais brīvais numurs uzdevumā (pēc 1.1–1.5 → 1.6), arī ja aktīvo pasākumu skaits nepārsniedz piecus. |
| Plānā nav drukāta pasākuma numura | Numuru piešķir pēc secības uzdevumā pirmajā apstiprinātajā versijā. |
| Pārnešanas kļūda (piemēram, divas rindkopas apvienotas kļūdas pēc) | Labo datus, palielina `DataVersion/@number`; lieko identifikatoru ieraksta `RetiredId`. |

## 4.a Projekts un divas numerācijas

Jaunas deklarācijas projektu veido no iepriekšējās deklarācijas (atvasina). Projektam ir savs identifikators (`lv-dekl-` + projekta izveides datums), `Government/@status = draft` un `Metadata/DerivedFrom` — avota deklarācijas identifikators.

Uzdevumam ir divas paralēlas numerācijas:

| Numerācija | Kur glabā | Mainās? | Piemērs |
|---|---|---|---|
| Drukātais numurs — dokumenta teksts | `Task/@number` | jā: pievienojot, dzēšot vai pārvietojot uzdevumus, numurē no jauna pēc secības | `13.` |
| Identifikators — datu atslēga | `Task/@id` | nē: piešķirts, uzdevumu izveidojot | `lv-dekl-2026-10-09.u012` |
| Avota uzdevums | `Task/@derivedFrom` | nē | `lv-dekl-2026-05-28.u012` (avotā — 12. uzdevums) |

- Pārņemtais uzdevums saglabā avota uzdevuma numuru identifikatorā (`u012` → `u012`), tāpēc uzdevumus starp deklarācijām var salīdzināt arī pēc pārnumurēšanas.
- Jaunam uzdevumam piešķir nākamo brīvo numuru (`u053`, ja avotā bija 52 uzdevumi); `derivedFrom` nenorāda.
- Dzēsta uzdevuma identifikatoru atkārtoti neizmanto.
- Projektā drukātais numurs un identifikators var atšķirties; pārbaudītājs to norāda kā informāciju. Iesniegtā deklarācijā (`status` nav `draft`) identifikators atbilst drukātajam numuram.

## 4.b Institūcijas identifikators — CaC ID

CaC ID ir vienots, pastāvīgs identifikators katrai valsts institūcijai. To piešķir organizāciju reģistra (`organizacijas.xml`) uzturētājs — Valsts kanceleja. Reģistrs ir vienīgais institūciju identifikatoru avots; citās datnēs institūcijas norāda tikai ar šo identifikatoru.

| Daļa | Nozīme | Piemērs |
|---|---|---|
| `SS` | Resors: ministrija vai cita centrālā valsts institūcija ar savu kodu (sākotnēji — kā gadskārtējā valsts budžeta likumā) | `20` — Klimata un enerģētikas ministrija |
| `IIII` | Institūcija resorā; resora vadošā institūcija — `0000` | `20-0000` — pati ministrija; `15-0203` — VIAA Izglītības un zinātnes ministrijas resorā |

- Sākotnējie kodi ņemti no Valsts kases „Valsts budžeta iestāžu saraksta” (01.09.2023). Turpmāk identifikatorus piešķir reģistra uzturētājs neatkarīgi no gadskārtējā budžeta; Valsts kases kodi glabājas kā sasaiste pa gadiem (`BudgetCode year="2023"`).
- Rezervētie resori: `00` — amati un institūciju grupas (`00-0001` Ministru prezidents); `90` — pašvaldības; `91` — valsts kapitālsabiedrības; `92` — atvasinātas publiskas personas; `93` — biedrības un sociālie partneri.
- Identifikatoru nemaina un atkārtoti neizmanto. Ja institūciju pārceļ uz citu resoru vai apvieno, tai piešķir jaunu identifikatoru; vecajam norāda `validTo` un `successor`. Slēgta resora kodu atkārtoti neizmanto.
- Reģistrācijas numurs (`regNo`, 11 cipari) — sasaistei ar VID un Uzņēmumu reģistru; identifikatorā to nelieto. Ārpus datu kopas — `urn:lv:gov:org:20-0000`.

## 5. Saistība ar citiem identifikatoriem

| Ārējs identifikators | Kur glabā | Piemērs |
|---|---|---|
| Rīkojums, ar kuru plāns apstiprināts | `Approval` (akts, datums, protokols, publikācija, URL) | MK rīkojums Nr. 449, likumi.lv/ta/id/369925 |
| Organizācija | `Responsible/@orgs`, `CoResponsible/@orgs` — identifikators no `organizacijas.xml`; saīsinājums (`AizM`, `SM`/`SAM`) ir tikai `Abbreviation` | `10-0000` (Aizsardzības ministrija) |

## 6. Tīmekļa adrese

Katram identifikatoram paredzēta adrese `{bāze}/id/{identifikators}`, piemēram `{bāze}/id/lv-dekl-2026-05-28.u012`. Bāzes adresi nosaka repozitorija publicēšanas vieta.

## 7. Pārbaude

`tools/ids.py` veido identifikatorus, `tools/validate.py` pārbauda, ka katrs identifikators atbilst šiem noteikumiem un ka atsauces starp datnēm (reģistrs ↔ deklarācija ↔ rīcības plāns) ir derīgas. `tools/test_validate.py` pārbauda, ka pārbaudītājs pamana kļūdas.
