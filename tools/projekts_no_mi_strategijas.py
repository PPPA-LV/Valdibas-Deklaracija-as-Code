#!/usr/bin/env python3
"""Jaunas valdības deklarācijas projekts no PPPA MI stratēģijas + atbilstošie Kulberga deklarācijas uzdevumi.

Lietojums:
    python3 tools/projekts_no_mi_strategijas.py <pppa-mis-….xml> data/lv-dekl-2026-05-28.xml 2026-10-10 data/

Struktūra (teksts pārņemts burtiski):
    ievads                 = stratēģijas vīzija
    principi               = stratēģijas īstenošanas principi
    prioritātes → nodaļa   = stratēģijas pīlārs (I, II, III)
              → apakšnodaļa = stratēģijas mērķis (Goal = mērķa apraksts)
              → uzdevums    = stratēģijas rīcība („Nosaukums. Teksts”)
Identifikatori:
    stratēģijas rīcība rNN    → uzdevums u(052+NN)  (avota deklarācijā 52 uzdevumi; nākamie brīvie numuri)
    pārņemtais avota uzdevums → tas pats uNNN + @derivedFrom
"""
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape, quoteattr

S = {"s": "urn:pppa:cac:mi-strategija:0.1"}
V = {"v": "urn:pppa:cac:valdiba:0.2"}

# Kulberga deklarācijas uzdevumi, kas atbilst stratēģijai: avota uzdevums -> stratēģijas mērķis (pievieno mērķa sākumā)
FROM_SOURCE = {"u021": 1, "u015": 2, "u039": 5}


def sentence(t):
    t = t.strip()
    return t if t[-1:] in ".!?" else t + "."


def main(mis_path, src_path, day, out_dir):
    mis = ET.parse(mis_path).getroot()
    src = ET.parse(src_path).getroot()
    src_id = src.get("id")
    did = f"lv-dekl-{day}"
    src_tasks = {t.get("id").rsplit(".", 1)[1]: t for t in src.iterfind(".//v:Task", V)}
    max_src = max(int(k[1:]) for k in src_tasks)
    assert max_src == 52, max_src

    n = 0  # drukātais numurs dokumentā
    L = []
    add = L.append

    def task(uid, text, derived=None):
        nonlocal n
        n += 1
        d = f" derivedFrom={quoteattr(derived)}" if derived else ""
        add(f'            <Task id="{did}.{uid}" number="{n}"{d}>')
        add(f"              <Text>{escape(text)}</Text>")
        add("            </Task>")

    vision = mis.findtext("s:Vision", namespaces=S)
    pr = mis.find("s:Principles", S)
    add(f'    <Section id="{did}.s01" kind="introduction">')
    add(f"      <Paragraph>{escape(vision)}</Paragraph>")
    add("    </Section>")
    add(f'    <Section id="{did}.s02" kind="principles">')
    add(f"      <Heading>{escape(pr.findtext('s:Heading', namespaces=S))}</Heading>")
    add(f"      <Paragraph>{escape(pr.findtext('s:Intro', namespaces=S))}</Paragraph>")
    add('      <List style="bullet">')
    for p in pr.iterfind("s:Principle", S):
        add(f"        <Item>{escape(p.findtext('s:Label', namespaces=S))}: {escape(p.findtext('s:Text', namespaces=S))}</Item>")
    add("      </List>")
    add("    </Section>")
    add(f'    <Section id="{did}.s03" kind="priorities">')
    add("      <Heading>Ministru kabineta iecerētās darbības prioritātes</Heading>")
    mapping = []
    for pi, p in enumerate(mis.iterfind("s:Pillar", S), 1):
        cid = f"{did}.s03-{pi:02d}"
        add(f'      <Section id="{cid}" kind="chapter" label="{p.get("number")}">')
        add(f"        <Heading>{escape(p.findtext('s:Name', namespaces=S))} — {escape(p.findtext('s:Heading', namespaces=S))}</Heading>")
        add(f"        <Paragraph>{escape(p.findtext('s:Description', namespaces=S))}</Paragraph>")
        for gi, g in enumerate(p.iterfind("s:Goal", S), 1):
            gn = int(g.get("number").rstrip("."))
            sid = f"{cid}-{gi:02d}"
            add(f'        <Section id="{sid}" kind="subchapter" label="{g.get("number")}">')
            add(f"          <Heading>{escape(g.findtext('s:Title', namespaces=S))}</Heading>")
            add(f'          <Goal id="{sid}.g1">{escape(g.findtext("s:Description", namespaces=S))}</Goal>')
            for u, goal in FROM_SOURCE.items():
                if goal == gn:
                    task(u, src_tasks[u].findtext("v:Text", namespaces=V), f"{src_id}.{u}")
                    mapping.append((n, u, f"{src_id}.{u}"))
            for a in g.iterfind("s:Action", S):
                an = int(a.get("number"))
                u = f"u{max_src + an:03d}"
                task(u, sentence(a.findtext("s:Title", namespaces=S)) + " " + a.findtext("s:Text", namespaces=S))
                mapping.append((n, u, a.get("id")))
            add("        </Section>")
        add("      </Section>")
    add("    </Section>")

    mis_id = mis.get("id")
    head = f"""<?xml version="1.0" encoding="UTF-8"?>
<GovernmentDeclaration xmlns="urn:pppa:cac:valdiba:0.2" id="{did}" schemaVersion="0.2">
  <Metadata>
    <Title>Deklarācija par Ministru kabineta iecerēto darbību</Title>
    <Subtitle>Projekts</Subtitle>
    <Date>{day}</Date>
    <Place>Rīga</Place>
    <Language>lv</Language>
    <LegalBasis>Ministru kabineta iekārtas likums, 14. un 15. pants</LegalBasis>
    <Government status="draft"/>
    <DerivedFrom>{src_id}</DerivedFrom>
    <Source>
      <FileName>{mis_id}.xml</FileName>
      <URL>https://processgit.org/Country-as-Code/AI-Strategija/src/branch/main/data/{mis_id}.xml</URL>
    </Source>
    <DataVersion number="1" date="{day}">
      <Change>Projekts izveidots no PPPA Latvijas Nacionālās MI stratēģijas {mis_id} ({mis.get("version")}): pīlāri — nodaļas, mērķi — apakšnodaļas, rīcības r01–r{max(int(a.get("number")) for a in mis.iterfind(".//s:Action", S)):02d} — uzdevumi u{max_src + 1:03d}–u{max_src + len(list(mis.iterfind(".//s:Action", S))):03d} (uNNN = 052 + rīcības numurs).</Change>
      <Change>No {src_id} pārņemti atbilstošie uzdevumi {", ".join(sorted(FROM_SOURCE))} (Task/@derivedFrom).</Change>
    </DataVersion>
  </Metadata>
  <Body>"""
    tail = """  </Body>
  <Composition>
    <PrimeMinisterCandidate><Office>Ministru prezidenta amata kandidāts</Office><Name>Nav noteikts</Name></PrimeMinisterCandidate>
    <InvitedMinisters heading="Aicinātie ministri:">
      <Minister><Office>Nav noteikts</Office><Name>Nav noteikts</Name></Minister>
    </InvitedMinisters>
  </Composition>
</GovernmentDeclaration>
"""
    out = Path(out_dir) / f"{did}.xml"
    out.write_text(head + "\n" + "\n".join(L) + "\n" + tail, encoding="utf-8")
    print("->", out, f"({n} uzdevumi)")
    for num, u, ref in mapping:
        print(f"  {num:>2}. {u} ← {ref}")


if __name__ == "__main__":
    main(*sys.argv[1:5])
