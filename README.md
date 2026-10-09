# Valdības deklarācijas datukopa

Mašīnlasāma struktūra valdības deklarācijai un visam, kas no tās izriet: rīcības plānam, izpildes gaitai un saitēm ar tiesību aktiem. Viena datu kopa datu noliktavai, ko vienlīdz var lasīt cilvēks un MI aģents.

Autors: PPP Asociācija (PPPA), Country as Code. Shēmu versija 0.2, melnraksts.

Deklarācijas pamatdokuments ir XML datne atbilstoši shēmai; Word un PDF ir eksports no šiem datiem.

## Datu modelis

```
Valdību reģistrs (valdibas.xml)          dimensijas: Valdība, Organizācija
        │
        ├── Deklarācija            lv-dekl-…            ← parakstītais teksts (1. līmenis), burtiski
        │     Sadaļa → Uzdevums (.uNNN) ← galvenā vienība
        │
        │
        └── Rīcības plāns          lv-mk-….rp           ← MK rīkojums; pasākumi .uNNN.pN (1–5 uz uzdevumu)
              Pasākums → Rezultāts (.dN) · Izpildes gaita (.zGGGGMMDD) · TA lieta · NAP kods
```

Tiesiskais pamats:
- Ministru kabineta iekārtas likuma 14. un 15. pants: deklarācijas saturs un rīcības plāns triju mēnešu laikā.
- Ministru kabineta kārtības rullis (MK noteikumi Nr. 606), 13.–26. punkts un pielikums: rīcības plāna ailes; ne vairāk kā pieci pasākumi uz uzdevumu; apstiprināšana ar MK rīkojumu; izpildes gaitas pārskati.

Deklarācijas formātu neviens normatīvais akts nenosaka. Kārtības rullis paredz tikai to, kas no deklarācijas izriet, un rīcības plāna pirmās trīs ailes ir pati deklarācija: sadaļa, uzdevuma numurs, uzdevuma teksts.

## Saturs

### Dati (`data/`) — autoritatīvās datnes

Datnes nosaukums ir objekta identifikators.

| Datne | Saturs |
|---|---|
| `data/lv-dekl-2026-05-28.xml` | Deklarācija par Andra Kulberga vadītā Ministru kabineta iecerēto darbību (28.05.2026): viss teksts, 11 sadaļas, 52 uzdevumi |
| `data/lv-dekl-2026-10-10.xml` | Jaunas valdības deklarācijas projekts (`status="draft"`): PPPA Latvijas Nacionālā MI stratēģija `pppa-mis-2026-09-10` — 3 pīlāri kā nodaļas, 5 mērķi kā apakšnodaļas, 27 rīcības kā uzdevumi `u053`–`u079`; no Kulberga deklarācijas pārņemti atbilstošie uzdevumi `u015`, `u021`, `u039` (`derivedFrom`) |
| `data/lv-mk-2026-05-28.rp.xml` | Valdības rīcības plāns tās īstenošanai (MK rīkojums Nr. 449, 27.07.2026): 185 pasākumi 52 uzdevumiem, teksts burtiski no likumi.lv; atbildīgās institūcijas ar CaC ID |
| `data/organizacijas.xml` | Valsts institūciju reģistrs (CaC ID): 165 valsts budžeta iestādes un 16 citas institūcijas un grupas; uzturētājs — Valsts kanceleja |
| `data/valdibas.xml` | Valdību reģistrs: piecas valdības (2016–2026) |
| `data/processgit.viewer.json` | ProcessGit skatītāja manifests: atverot deklarāciju, rīcības plānu vai organizāciju reģistru ProcessGit, tie tiek attēloti redaktorā (`editor/`) |

ProcessGit skatītājs ielādē skatīto datni no repozitorija un saistītās datnes no tās pašas mapes pēc identifikatora (deklarācija ↔ rīcības plāns ↔ organizāciju reģistrs). Pievienojot jaunu deklarāciju vai rīcības plānu, tās datnes nosaukums jāpievieno manifesta `edit_allow` sarakstam.

### Shēmas (`schemas/`)

| Datne | Saturs |
|---|---|
| `schemas/valdibas-deklaracija-0.2.xsd` | Deklarācija |
| `schemas/valdibas-deklaracijas-ricibas-plans-0.2.xsd` | Valdības deklarācijas rīcības plāns: pasākumi, rezultāti, atbildīgie, termiņi, izpildes gaita; katrs pasākums norāda deklarācijas uzdevumu |
| `schemas/organizaciju-registrs-0.2.xsd` | Organizāciju reģistrs: CaC ID (`SS-IIII`; ministrija — `SS-0000`), reģistrācijas numurs, nosaukums, saīsinājumi, augstākā institūcija |
| `schemas/cac-valdiba-kopejie-0.2.xsd` | Kopīgie tipi (identifikatori, datumi) un valdību reģistrs |

### Rīki, dokumentācija, avoti

| Mape / datne | Saturs |
|---|---|
| `docs/IDENTIFIKATORI.md` | Identifikatoru veidošanas noteikumi |
| `tools/validate.py` | Pārbaude: XSD, datņu nosaukumi, identifikatori, saites starp datnēm, kārtības ruļļa 18. un 20. punkts, termiņi |
| `tools/test_validate.py` | Negatīvie testi pārbaudītājam |
| `tools/projekts_no_mi_strategijas.py` | Veido deklarācijas projektu no MI stratēģijas XML un pārņem atbilstošos avota deklarācijas uzdevumus |
| `tools/ricibas_plans_no_likumi.py` | Pārveido rīcības plānu no likumi.lv lapas uz XML un salīdzina plāna ailes 1–3 ar deklarāciju |
| `tools/organizacijas_no_vdvc.py` | Izveido organizāciju reģistru no VDVC reģistra un Valsts kases saraksta |
| `tools/ids.py` | Identifikatoru veidošana |
| `editor/Valdibas_deklaracijas_datukopa.html` | Redaktors vienā HTML datnē: valdības deklarācija (lasīšana, rediģēšana), rīcības plāns ar CaC ID, institūciju reģistrs, jaunas deklarācijas projekts, shēmas, apraksts; eksportē XML un Word |
| `source/pdf/` | Deklarācijas avota PDF |
| `source/ricibas-plans/` | MK rīkojuma Nr. 449 avoti: likumi.lv lapa (.mhtml) un PDF |
| `source/organizacijas/` | VDVC reģistrs un Valsts kases „Valsts budžeta iestāžu saraksts” (01.09.2023) |
| `source/v0.1/` | Iepriekšējā (v0.1) shēma un dati |

## Pārbaude

```
pip install lxml
python3 tools/validate.py            # data/
python3 tools/test_validate.py
```

Pārbaudītājs ziņo `E` (kļūda), `W` (brīdinājums), `I` (informācija). Pašreizējie dati: 0 kļūdas, 1 brīdinājums — 10 deklarācijas uzdevumiem rīcības plānā ir vairāk nekā pieci pasākumi (kārtības ruļļa 18. punkts).

## Ko shēma nodrošina

- Uzdevumam ir divas paralēlas numerācijas: drukātais numurs (`@number`) un pastāvīgs identifikators (`@id`); jaunas deklarācijas projektā katrs uzdevums norāda avota uzdevumu (`@derivedFrom`).
- Katram elementam ir globāli unikāls identifikators, piemēram `lv-dekl-2026-05-28.u012`, `lv-mk-2026-05-28.rp.u001.p3`.
- Rīcības plāns ir salīdzināms arī tad, ja ailes atšķiras no pielikuma: `Metadata/Column` sasaista avota aili ar shēmas lauku.
- Izpildes gaita ir laika rinda: viens ieraksts katrā pārskata periodā, ar pierādījumu (dokumenta numurs un datums, TA lieta).
- Ārējie identifikatori ir saglabāti: TA lietas numurs, publikāciju sistēmas ID, NAP kodi.
