"""Izveido organizāciju reģistru (organizaciju-registrs-0.2.xsd) no VDVC reģistra (vdvc-register.xml).

  python3 tools/organizacijas_no_vdvc.py source/organizacijas/vdvc-register.xml examples/organizacijas.xml

Avots — Valsts kases „Valsts budžeta iestāžu saraksts” (01.09.2023; iestades_PAS_VBI_01092023.pdf): iestādes kods (ePlāni un eTāmes),
nodokļu maksātāja reģistrācijas numurs, nosaukums, ministrijas kods (budžeta resors saskaņā ar gadskārtējo valsts budžeta likumu).
Avota datnē dažos nosaukumos ir sapludinātas divas rindas (piemēram „FINANŠU MINISTRIJA 13/74 S130110 005190000597275 VALSTS KASE”);
skripts tās sadala un otro institūciju pievieno ar tās kodu un reģistrācijas numuru. Budžeta maksājumu konti („(BUDŽETA MAKSĀJUMI)”) nav institūcijas
un netiek iekļauti. Saīsinājumi — kā tos lieto Ministru kabineta dokumentos (MK rīkojums Nr. 449).
"""
import hashlib, os, re, sys
from lxml import etree

SRC_NS = "http://vdvc.gov.lv/schema/vdvc-register"
NS = "urn:pppa:cac:valdiba:0.2"

SECTORS = {"01": "Valsts prezidenta kanceleja", "02": "Saeima", "03": "Ministru kabinets", "04": "Korupcijas novēršanas un apkarošanas birojs",
           "05": "Tiesībsarga birojs", "08": "Sabiedrības integrācijas fonds", "09": "Sabiedrisko pakalpojumu regulēšanas komisija",
           "10": "Aizsardzības ministrija", "11": "Ārlietu ministrija", "12": "Ekonomikas ministrija", "13": "Finanšu ministrija", "14": "Iekšlietu ministrija",
           "15": "Izglītības un zinātnes ministrija", "16": "Zemkopības ministrija", "17": "Satiksmes ministrija", "18": "Labklājības ministrija",
           "19": "Tieslietu ministrija", "20": "Klimata un enerģētikas ministrija", "21": "Viedās administrācijas un reģionālās attīstības ministrija",
           "22": "Kultūras ministrija", "24": "Valsts kontrole", "28": "Augstākā tiesa", "29": "Veselības ministrija", "30": "Satversmes tiesa",
           "32": "Prokuratūra", "35": "Centrālā vēlēšanu komisija", "46": "Sabiedrisko elektronisko plašsaziņas līdzekļu padome",
           "47": "Nacionālā elektronisko plašsaziņas līdzekļu padome",
           "00": "Amati un institūciju grupas", "90": "Pašvaldības", "91": "Valsts kapitālsabiedrības", "92": "Atvasinātas publiskas personas",
           "93": "Biedrības un sociālie partneri"}
# institūcijas, kas nav valsts budžeta iestādes, un grupas (MK rīkojums Nr. 449); identifikatorus piešķir reģistra uzturētājs: (id, veids, nosaukums, saīsinājumi, augstākā)
EXTRA = [("00-0001", "office", "Ministru prezidents", ["MP"], None),
         ("00-0002", "group", "Visas ministrijas", ["Visas ministrijas", "ministrijas"], None),
         ("00-0003", "group", "Pašvaldības", ["pašvaldības"], None),
         ("00-0004", "group", "Pašvaldību policijas", ["Pašvaldību policijas"], None),
         ("00-0005", "group", "Nevalstiskās organizācijas", ["NVO"], None),
         ("90-0001", "municipality", "Daugavpils valstspilsētas pašvaldība", ["Daugavpils pašvaldība"], None),
         ("90-0002", "municipality", "Liepājas valstspilsētas pašvaldība", ["Liepājas pašvaldība"], None),
         ("90-0003", "municipality", "Ventspils valstspilsētas pašvaldība", ["Ventspils pašvaldība"], None),
         ("91-0001", "company", "VAS „Valsts nekustamie īpašumi”", ["VNĪ"], "13-0000"),
         ("91-0002", "company", "VSIA „Autotransporta direkcija”", ["ATD"], "17-0000"),
         ("91-0003", "company", "VSIA „Bērnu klīniskā universitātes slimnīca”", ["BKUS"], "29-0000"),
         ("92-0001", "public-person", "Latvijas Universitāte", ["LU"], None),
         ("92-0002", "public-person", "Rīgas Tehniskā universitāte", ["RTU"], None),
         ("93-0001", "association", "Latvijas Tirdzniecības un rūpniecības kamera", ["LTRK"], None),
         ("93-0002", "association", "Latvijas Darba devēju konfederācija", ["LDDK"], None),
         ("93-0003", "association", "Latvijas Pašvaldību savienība", ["LPS"], None)]
# resora vadošā iestāde (ministrija vai Valsts kanceleja): pārējās resora iestādes ir tās padotībā
HEADS = {"10": "90000022632", "11": "90000069065", "12": "90000086008", "13": "90000014724", "14": "90000282046", "15": "90000022399",
         "16": "90000064161", "17": "90000088687", "18": "90000022064", "19": "90000070045", "20": "40900039891", "21": "90000028508",
         "22": "90000042963", "29": "90001474921", "03": "90000055313"}
INDEPENDENT_IN_SECTOR = {"90010248231"}          # Fiskālās disciplīnas padome — budžets FM resorā, bet neatkarīga
ABBR = {"90000022632": ["AizM"], "90000069065": ["ĀM"], "90000086008": ["EM"], "90000014724": ["FM"], "90000282046": ["IeM"],
        "90000022399": ["IZM"], "40900039891": ["KEM"], "90000042963": ["KM"], "90000022064": ["LM"], "90000088687": ["SM", "SAM"],
        "90000070045": ["TM"], "90001474921": ["VM"], "90000028508": ["VARAM"], "90000064161": ["ZM"], "90000055313": ["VK"],
        "90000433377": ["KP"], "90000069830": ["CSP"], "90000068854": ["PTAC"], "90001739473": ["LIAA"], "90000069281": ["VID"],
        "90001263305": ["IUB"], "40900025406": ["FID"], "90001427791": ["KNAB"], "90000054163": ["PMLP"], "90001634668": ["NVA"],
        "90001669496": ["VSAA"], "90001800413": ["VIAA"], "90009113250": ["LVA"], "90000270634": ["UR"], "90009649337": ["NVD"],
        "90001237779": ["SIF"], "90000081852": ["NEPLP"], "90000049726": ["LNKC"], "90000048222": ["LZP"], "90010248231": ["FDP"],
        "90000812928": ["CFLA"], "90001162258": ["SPRK"], "90001733697": ["VRAA"], "90000049834": ["VUGD"], "90000054712": ["VDD"]}
RENAMED = {"90000028508": ("VIEDĀS ADMINISTRĀCIJAS UN REĢIONĀLĀS ATTĪSTĪBAS MINISTRIJA", None)}
MERGE = re.compile(r"^(.*?)\s*(\d{2})(?:/\d{2})? (S13\d{4}) (\d{4})(\d{11}) (.+)$")


def X(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main(src, out):
    root = etree.parse(src).getroot()
    orgs, skipped, split = [], [], []
    for m in root:
        for o in m:
            items = [(m.get("code"), o.get("code"), o.get("nmr"), o.findtext(f"{{{SRC_NS}}}name").strip())]
            while True:
                sec, code, nmr, name = items[-1]
                mm = MERGE.match(name)
                if not mm: break
                items[-1] = (sec, code, nmr, mm.group(1).strip())
                items.append((mm.group(2), mm.group(4), mm.group(5), mm.group(6).strip())); split.append(mm.group(6).strip())
            for it in items:
                if "BUDŽETA MAKSĀJUMI" in it[3]: skipped.append(it[3]); continue
                orgs.append(it)
    # avota sapludinātajās rindās nozaudētas institūcijas — no Valsts kases saraksta (iestades_PAS_VBI_01092023.pdf)
    ADD = [("10", "0032", "90000056893", "LATVIJAS REPUBLIKAS AIZSARDZĪBAS MINISTRIJAS NACIONĀLO BRUŅOTO SPĒKU NODROŠINĀJUMA PAVĒLNIECĪBAS 3.REĢIONĀLAIS NODROŠINĀJUMA CENTRS")]
    have = {o[2] for o in orgs}
    for a in ADD:
        if a[2] not in have: orgs.append(a); split.append(a[3])
    per_sector = {}
    for o in orgs: per_sector.setdefault(o[0], set()).add(o[2])
    def oid(sec, code, nmr):
        if HEADS.get(sec) == nmr or (sec not in HEADS and len(per_sector[sec]) == 1): return f"{sec}-0000"   # resora vadošā institūcija
        return f"{sec}-{code}"
    seen = set(); L = []
    for sec, code, nmr, name in sorted(orgs, key=lambda x: (x[0], oid(*x[:3]))):
        if nmr in seen: continue
        seen.add(nmr)
        head = HEADS.get(sec); i = oid(sec, code, nmr)
        if nmr == head: kind, parent = ("pm-institution" if sec == "03" else "ministry"), None
        elif head and nmr not in INDEPENDENT_IN_SECTOR: kind, parent = "subordinate", f"{sec}-0000"
        else: kind, parent = "independent", None
        former = None
        if nmr in RENAMED: former, name = name, RENAMED[nmr][0]
        a = f' parent="{parent}"' if parent else ""
        L.append(f'  <Organization id="{i}" regNo="{nmr}" kind="{kind}"{a}>')
        L.append(f"    <Name>{X(name)}</Name>")
        for ab in ABBR.get(nmr, []): L.append(f"    <Abbreviation>{X(ab)}</Abbreviation>")
        L.append(f'    <BudgetCode year="2023">{code}</BudgetCode>')
        if former: L.append(f"    <FormerName>{X(former)}</FormerName>")
        L.append("  </Organization>")
    for i, kind, name, abbr, parent in EXTRA:
        L.append(f'  <Organization id="{i}" kind="{kind}"{f" parent=\"{parent}\"" if parent else ""}>\n    <Name>{X(name)}</Name>' + "".join(f"\n    <Abbreviation>{X(a)}</Abbreviation>" for a in abbr) + "\n  </Organization>")
    head = ['<?xml version="1.0" encoding="UTF-8"?>', f'<OrganizationRegistry xmlns="{NS}" schemaVersion="0.2">', "  <Metadata>",
            "    <Title>Valsts institūciju reģistrs</Title>", "    <Keeper>03-0000</Keeper>",
            f"    <Source>\n      <FileName>{os.path.basename(src)}</FileName>\n      <SHA256>{hashlib.sha256(open(src, 'rb').read()).hexdigest()}</SHA256>\n    </Source>",
            f"    <Source>\n      <FileName>iestades_PAS_VBI_01092023.pdf</FileName>\n      <SHA256>{hashlib.sha256(open(os.path.join(os.path.dirname(src), 'iestades_PAS_VBI_01092023.pdf'), 'rb').read()).hexdigest()}</SHA256>\n    </Source>",
            '    <DataVersion number="1" date="2026-10-10">',
            f"      <Change>Izveidots no VDVC reģistra un Valsts kases „Valsts budžeta iestāžu saraksta” (01.09.2023): {len(seen)} valsts budžeta iestādes; {len(split)} atgūtas no sapludinātām avota rindām; {len(skipped)} budžeta maksājumu konti nav iekļauti.</Change>",
            "      <Change>Identifikatori SS-IIII; resora vadošā institūcija SS-0000; Valsts kases 2023. gada kodi — BudgetCode.</Change>",
            f"      <Change>Pievienotas {len(EXTRA)} institūcijas un grupas, kas minētas MK rīkojumā Nr. 449 un nav valsts budžeta iestādes (resori 00, 90–93); reģistrācijas numuri jāpapildina.</Change>",
            "      <Change>Nosaukumi valsts budžeta iestādēm — kā avotā (lielajiem burtiem).</Change>",
            "    </DataVersion>", "  </Metadata>"]
    head += [f'  <Sector code="{c}">{X(n)}</Sector>' for c, n in sorted(SECTORS.items())]
    open(out, "w", encoding="utf-8").write("\n".join(head + L + ["</OrganizationRegistry>"]) + "\n")
    print(f"{len(seen)} valsts budžeta iestādes + {len(EXTRA)} citas institūcijas un grupas → {out}")
    print("atgūtas no sapludinātām rindām:", split)
    print("izlaisti budžeta maksājumu konti:", skipped)

if __name__ == "__main__":
    main(*sys.argv[1:3])
