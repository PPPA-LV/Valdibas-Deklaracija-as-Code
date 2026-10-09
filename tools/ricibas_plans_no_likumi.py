"""Pārveido Valdības rīcības plānu no likumi.lv lapas (saglabāta kā .mhtml vai .html) uz XML (valdibas-deklaracijas-ricibas-plans-0.2.xsd).

  python3 tools/ricibas_plans_no_likumi.py <lapa.mhtml> <deklaracija.xml> <organizacijas.xml> <izvade.xml>

likumi.lv lapā ir četras tabulas: 0 — viss plāns; 1 — rīkojuma 1. pielikums (finansējums rasts);
2 — 2. pielikums (nepieciešams papildu finansējums); 3 — prioritārie pasākumi.
Katrs pasākums tiek ierakstīts vienreiz (no 0. tabulas); 1. un 2. tabula nosaka atribūtu funding.
Plāna ailes 1–3 (sadaļa, uzdevuma numurs, uzdevuma teksts) netiek kopētas — tās aizstāj saite uz deklarācijas uzdevumu.
Ja šīs ailes nesakrīt ar deklarāciju, par to tiek ziņots.
"""
import email, hashlib, os, re, sys
from email import policy
from lxml import etree, html as H

NS = "urn:pppa:cac:valdiba:0.2"; N = {"v": NS}
ALIAS = {}


def page_html(path):
    raw = open(path, "rb").read()
    if raw.lstrip().startswith(b"From:") or b"MIME-Version" in raw[:2000]:
        m = email.message_from_bytes(raw, policy=policy.default)
        for part in m.walk():
            if part.get_content_type() == "text/html": return part.get_payload(decode=True), part.get("Content-Location")
    return raw, None


def cell(c):
    s = re.sub(r"<(p|br|div|li)\b", r"\n<\1", etree.tostring(c, encoding=str))   # rindkopu robežas = jauna rinda
    t = H.fromstring(s).text_content().replace("\xa0", " ")
    return "\n".join(re.sub(r"[ \t]+", " ", l).strip() for l in t.split("\n") if l.strip())


def tables(raw):
    d = H.fromstring(raw, parser=H.HTMLParser(encoding="utf-8"))
    return [[[cell(c) for c in r.xpath("./td|./th")] for r in t.xpath("./tr|./tbody/tr")[1:]] for t in d.xpath("//table") if len(t.xpath(".//tr")) > 1]


def codes(text, known):
    """Institūciju teksts → identifikatori organizāciju reģistrā. known: {saīsinājums vai nosaukums (mazajiem burtiem): SS-IIII}"""
    out = []
    units = [u.strip() for g in re.findall(r"\(([^)]*)\)", text) for u in g.split(",")]   # "IZM (VIAA, LVA)" -> padotības iestādes
    text = re.sub(r"\s*\([^)]*\)", "", text) + "".join("\n" + u for u in units)
    for part in re.split(r"[,;\n]| un ", text):
        part = re.sub(r"^\s*[\d\-–]+\)\s*", "", part)            # "2-4) VK" -> "VK"
        part = part.strip()
        oid = known.get(part.lower())
        if oid and oid not in out: out.append(oid)
        elif not oid and part: UNMATCHED[part] = UNMATCHED.get(part, 0) + 1
    return out


UNMATCHED = {}


def X(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def XA(s): return X(s).replace('"', "&quot;")


def main(page, decl_path, reg_path, out_path):
    raw, url = page_html(page)
    T = tables(raw)
    full, fin, add = T[0], {r[3] for r in T[1]}, {r[3] for r in T[2]}
    dx = etree.parse(decl_path).getroot(); did = dx.get("id")
    gov = dx.find("v:Metadata/v:Government", N).get("ref"); pid = gov + ".rp"
    tasks = {}
    for s in dx.iter(f"{{{NS}}}Section"):
        for t in s.findall("v:Task", N): tasks[int(t.get("number"))] = (t.get("id"), t.findtext("v:Text", namespaces=N), s.findtext("v:Heading", namespaces=N))
    known = {}
    for o in etree.parse(reg_path).getroot().findall("v:Organization", N):
        for ab in o.findall("v:Abbreviation", N): known[ab.text.strip().lower()] = o.get("id")
        known[o.findtext("v:Name", namespaces=N).strip().lower()] = o.get("id")
    title = H.fromstring(raw, parser=H.HTMLParser(encoding="utf-8")).findtext(".//title").strip()

    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         f'<GovernmentActionPlan xmlns="{NS}" id="{pid}" government="{gov}" declaration="{did}" schemaVersion="0.2">',
         "  <Metadata>", f"    <Title>Valdības rīcības plāns Deklarācijas par Andra Kulberga vadītā Ministru kabineta iecerēto darbību īstenošanai</Title>",
         f'    <Approval id="{pid}.v1" kind="approval">', "      <Act>Ministru kabineta rīkojums Nr. 449</Act>", "      <Date>2026-07-27</Date>",
         "      <Protocol>prot. Nr. 39 39. §</Protocol>", "      <Publication>Latvijas Vēstnesis, 143, 29.07.2026., OP numurs: 2026/143.33</Publication>",
         "      <URL>https://likumi.lv/ta/id/369925</URL>", "    </Approval>",
         "    <Source>", f"      <FileName>{X(os.path.basename(page))}</FileName>", f"      <SHA256>{hashlib.sha256(open(page, 'rb').read()).hexdigest()}</SHA256>",
         f"      <URL>{X(url or 'https://likumi.lv/ta/id/369925')}</URL>", "    </Source>",
         f'    <DataVersion number="1" date="2026-10-09"/>', "  </Metadata>"]
    report = {}
    for sec, tno, ttext, num, text, result, resp, co, dl, prio in full:
        n = int(tno.rstrip(".")); tid, dtext, dsec = tasks[n]
        if re.sub(r"\s+", " ", ttext).strip() != re.sub(r"\s+", " ", dtext).strip(): report[("uzdevuma teksts", n)] = (ttext, dtext)
        if sec.strip() != dsec.strip(): report[("sadaļa", n)] = (sec, dsec)
        mm = re.fullmatch(r"(\d+)\.(\d+)\.?", num); assert mm and int(mm.group(1)) == n, num
        mid = f"{pid}.u{n:03d}.p{int(mm.group(2))}"
        funding = "allocated" if num in fin else "additional" if num in add else None; assert funding, num
        a = f' priority="{XA(prio)}"' if prio.strip() else ""
        L.append(f'  <Measure id="{mid}" number="{num}" task="{tid}" funding="{funding}"{a}>')
        L.append(f"    <Text>{X(text)}</Text>"); L.append(f"    <Result>{X(result)}</Result>")
        c = codes(resp, known); L.append(f'    <Responsible{f" orgs=\"{" ".join(c)}\"" if c else ""}>{X(resp)}</Responsible>')
        if co.strip(): c = codes(co, known); L.append(f'    <CoResponsible{f" orgs=\"{" ".join(c)}\"" if c else ""}>{X(co)}</CoResponsible>')
        vals = ["-".join(reversed(x.split("."))) for x in re.findall(r"\b(\d{2}\.\d{2}\.\d{4})", dl)]
        L.append(f'    <Deadline{f" values=\"{" ".join(vals)}\"" if vals else ""}>{X(dl)}</Deadline>')
        L.append("  </Measure>")
    L.append("</GovernmentActionPlan>")
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"{len(full)} pasākumi, {len({r[1] for r in full})} uzdevumi → {out_path}")
    if UNMATCHED: print("institūcijas, kuru nav organizāciju reģistrā:", ", ".join(f"{k} ({v})" for k, v in sorted(UNMATCHED.items())))
    for (kind, n), (a, b) in report.items(): print(f"NESAKRĪT {kind}, {n}. uzdevums:\n  plānā:       {a}\n  deklarācijā: {b}")


if __name__ == "__main__":
    main(*sys.argv[1:5])
