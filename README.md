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

| Mape / datne | Saturs |
|---|---|
| `schemas/cac-valdiba-kopejie-0.2.xsd` | Kopīgie tipi (identifikatori, organizācijas, termiņi) un valdību reģistrs |
| `schemas/valdibas-deklaracija-0.2.xsd` | Deklarācijas teksts |
| `schemas/valdibas-deklaracijas-ricibas-plans-0.2.xsd` | Valdības deklarācijas rīcības plāns: pasākumi, rezultāti, atbildīgie, termiņi, izpildes gaita; katrs pasākums norāda deklarācijas uzdevumu |
| `docs/IDENTIFIKATORI.md` | Identifikatoru veidošanas noteikumi |
| `examples/valdibas.xml` | Piecas valdības (2016–2026) |
| `schemas/organizaciju-registrs-0.2.xsd` | Organizāciju reģistrs: institūcijas identifikators (`SS-IIII`: resors + institūcija, ministrija — `SS-0000`), reģistrācijas numurs, nosaukums, saīsinājumi, resors, augstākā iestāde; uztur Valsts kanceleja |
| `examples/organizacijas.xml` | 165 valsts budžeta iestādes (VDVC reģistrs, Valsts kases saraksts 01.09.2023) un 16 citas institūcijas un grupas no MK rīkojuma Nr. 449 (resori 00, 90–93) |
| `tools/organizacijas_no_vdvc.py` | Izveido organizāciju reģistru no VDVC reģistra (`source/organizacijas/`) |
| `examples/lv-dekl-2026-05-28.xml` | A. Kulberga valdības deklarācija, viss teksts, 11 sadaļas, 52 uzdevumi; identifikatori tikai sadaļām un uzdevumiem |
| `examples/lv-mk-2026-05-28.rp.xml` | Valdības rīcības plāns (MK rīkojums Nr. 449, 27.07.2026): 185 pasākumi 52 uzdevumiem, teksts burtiski no likumi.lv |
| `source/ricibas-plans/` | Rīkojuma Nr. 449 avoti: likumi.lv lapa (.mhtml) un PDF |
| `tools/ricibas_plans_no_likumi.py` | Pārveido rīcības plānu no likumi.lv lapas uz XML un salīdzina plāna ailes 1–3 ar deklarāciju |
| `editor/Valdibas_deklaracijas_datukopa.html` | Redaktors vienā HTML datnē: valdības deklarācija (lasīšana, rediģēšana), rīcības plāns — pasākumi pie katra uzdevuma ar CaC ID, institūciju reģistrs („Organizācijas”); projekts, shēmas, apraksts („Par”); eksportē XML v0.2 un Word |
| `source/pdf/` | Avota PDF |
| `source/v0.1/` | Iepriekšējā (v0.1) shēma un dati, no kuriem veidoti piemēri |
| `tools/ids.py` | Identifikatoru veidošana |
| `tools/validate.py` | Pārbaude: XSD, identifikatori, saites starp datnēm, kārtības ruļļa 18. un 20. punkts, termiņi |
| `tools/test_validate.py` | Negatīvie testi pārbaudītājam |

## Pārbaude

```
pip install lxml
python3 tools/validate.py            # examples/
python3 tools/test_validate.py
```

Pārbaudītājs ziņo `E` (kļūda), `W` (brīdinājums), `I` (informācija). Pašreizējie piemēri: 0 kļūdas, 1 brīdinājums — 10 deklarācijas uzdevumiem rīcības plānā ir vairāk nekā pieci pasākumi (kārtības ruļļa 18. punkts).

## Ko shēma nodrošina

- Uzdevumam ir divas paralēlas numerācijas: drukātais numurs (`@number`) un pastāvīgs identifikators (`@id`); jaunas deklarācijas projektā katrs uzdevums norāda avota uzdevumu (`@derivedFrom`).
- Katram elementam ir globāli unikāls identifikators, piemēram `lv-dekl-2026-05-28.u012`, `lv-mk-2026-05-28.rp.u001.p3`.
- Rīcības plāns ir salīdzināms arī tad, ja ailes atšķiras no pielikuma: `Metadata/Column` sasaista avota aili ar shēmas lauku.
- Izpildes gaita ir laika rinda: viens ieraksts katrā pārskata periodā, ar pierādījumu (dokumenta numurs un datums, TA lieta).
- Ārējie identifikatori ir saglabāti: TA lietas numurs, publikāciju sistēmas ID, NAP kodi.
