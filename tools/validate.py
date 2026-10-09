"""Pārbaudītājs: XSD + identifikatoru noteikumi + saites starp datnēm + kārtības ruļļa noteikumi.

  python3 tools/validate.py [mape ar XML datnēm]      (noklusējums: data/)

Ziņo: E = kļūda (izejas kods 1), W = brīdinājums, I = informācija.
"""
import os, re, sys
from collections import defaultdict
from lxml import etree

sys.path.insert(0, os.path.dirname(__file__))
import ids

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = "urn:pppa:cac:valdiba:0.2"
N = {"v": NS}
SCHEMAS = {"GovernmentRegistry": "cac-valdiba-kopejie-0.2.xsd", "GovernmentDeclaration": "valdibas-deklaracija-0.2.xsd",
           "GovernmentActionPlan": "valdibas-deklaracijas-ricibas-plans-0.2.xsd",
           "OrganizationRegistry": "organizaciju-registrs-0.2.xsd"}
OUT = []
LINKS = []   # (datne, projekts, avots, [(uzdevums, avota uzdevums)])


def rep(level, where, msg): OUT.append((level, where, msg))
def local(el): return etree.QName(el).localname


def load(folder):
    docs = defaultdict(list)
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".xml"): continue
        p = os.path.join(folder, f)
        try: t = etree.parse(p)
        except etree.XMLSyntaxError as e: rep("E", f, f"XML nav korekts: {e}"); continue
        root = t.getroot(); name = local(root)
        if etree.QName(root).namespace != NS or name not in SCHEMAS: rep("W", f, "nav v0.2 shēmu saimes datne — izlaista"); continue
        sc = etree.XMLSchema(etree.parse(os.path.join(ROOT, "schemas", SCHEMAS[name])))
        if not sc.validate(t):
            for e in sc.error_log: rep("E", f, f"XSD {e.line}: {e.message}")
        if name in ("GovernmentDeclaration", "GovernmentActionPlan") and f != root.get("id") + ".xml": rep("E", f, f"datnes nosaukumam jābūt {root.get('id')}.xml (identifikators)")
        docs[name].append((f, root))
    return docs


def check_registry(f, r):
    govs = {g.get("id"): g for g in r.findall("v:Government", N)}
    orgs = set()
    for gid, g in govs.items():
        vd = g.find("v:ConfidenceVote", N).get("date")
        if not gid.startswith(f"lv-mk-{vd}"): rep("E", f, f"{gid}: ID datums nesakrīt ar uzticības balsojuma datumu {vd}")
    return govs, orgs


def check_orgs(f, r):
    ids_ = {o.get("id"): o for o in r.findall("v:Organization", N)}
    sectors = {s.get("code") for s in r.findall("v:Sector", N)}
    no_reg = 0
    for oid, o in ids_.items():
        sec, kind = oid[:2], o.get("kind")
        if sec not in sectors: rep("E", f, f"{oid}: resors {sec} nav reģistrā")
        if kind in ("ministry", "pm-institution") and not oid.endswith("-0000"): rep("E", f, f"{oid}: resora vadošās institūcijas identifikatoram jābūt {sec}-0000")
        if kind == "subordinate" and o.get("parent", "")[:2] != sec: rep("E", f, f"{oid}: padotības iestāde nav sava resora vadošās institūcijas padotībā")
        if o.get("parent") and o.get("parent") not in ids_: rep("E", f, f"{oid}: augstākā institūcija {o.get('parent')} nav reģistrā")
        if o.get("successor") and o.get("successor") not in ids_: rep("E", f, f"{oid}: pēctecis {o.get('successor')} nav reģistrā")
        if not o.get("regNo") and kind not in ("office", "group"): no_reg += 1
    if r.findtext("v:Metadata/v:Keeper", namespaces=N) not in ids_: rep("E", f, "reģistra uzturētājs nav reģistrā")
    if no_reg: rep("I", f, f"{no_reg} institūcijām nav norādīts reģistrācijas numurs")
    rep("I", f, f"{len(ids_)} ieraksti, {len(sectors)} resori, {sum(1 for o in ids_.values() if o.get('kind') == 'ministry')} ministrijas")
    return set(ids_)


def check_declaration(f, r, govs):
    did = r.get("id"); texts = {}
    for el in r.iter():
        i = el.get("id") if isinstance(el.tag, str) else None
        if i and el is not r and not i.startswith(did + "."): rep("E", f, f"{i}: nesākas ar deklarācijas ID {did}")
    gov = r.find("v:Metadata/v:Government", N); gref = gov.get("ref")
    if gov.get("status") == "confidence_granted" and not gref: rep("E", f, "status confidence_granted, bet nav valdības atsauces")
    if gref and govs:
        if gref not in govs: rep("E", f, f"valdība {gref} nav reģistrā")
        elif (govs[gref].findtext("v:Declaration", namespaces=N) or "") != did: rep("E", f, f"reģistrā valdībai {gref} norādīta cita deklarācija")
    date = r.findtext("v:Metadata/v:Date", namespaces=N)
    if date and not did.startswith(f"lv-dekl-{date}"): rep("W", f, f"ID datums nesakrīt ar dokumenta datumu {date}")

    def lists(parent_el, parent_id):
        for k, l in enumerate(parent_el.findall("v:List", N), 1):
            if l.get("id") or any(it.get("id") for it in l.findall("v:Item", N)):
                rep("W", f, f"{parent_id}: sarakstiem un saraksta punktiem identifikatoru nepiešķir")

    def section(s, exp):
        if s.get("id") != exp: rep("E", f, f"{s.get('id')}: sagaidīts {exp} (secība dokumentā)")
        if any(p.get("id") for p in s.findall("v:Paragraph", N)): rep("W", f, f"{exp}: rindkopām identifikatoru nepiešķir")
        lists(s, exp)
        for k, g in enumerate(s.findall("v:Goal", N), 1):
            if g.get("id") != ids.goal(exp, k): rep("E", f, f"{g.get('id')}: sagaidīts {ids.goal(exp, k)}")
        for k, g in enumerate(s.findall("v:Result", N), 1):
            if g.get("id") != ids.result(exp, k): rep("E", f, f"{g.get('id')}: sagaidīts {ids.result(exp, k)}")
        for t in s.findall("v:Task", N):
            num = int(t.get("number")); tid = t.get("id"); idn = int(re.search(r"\.u(\d+)", tid).group(1))
            if not re.fullmatch(re.escape(ids.task(did, num)) + r"(-\d+)?", tid):
                if draft: renumbered.append(num)
                else: rep("E", f, f"{tid}: sagaidīts {ids.task(did, num)} (numurs {num})")
            src = t.get("derivedFrom")
            if src:
                if not derived: rep("E", f, f"{tid}: derivedFrom norādīts, bet nav Metadata/DerivedFrom")
                elif not src.startswith(derived + ".u"): rep("E", f, f"{tid}: derivedFrom {src} nav no {derived}")
                else: links.append((tid, src))
            idnums.append(idn); texts[tid] = t.findtext("v:Text", namespaces=N); lists(t, tid)
        for k, c in enumerate(s.findall("v:Section", N), 1): section(c, ids.section(exp, k, top=False))

    draft = gov.get("status") == "draft"; derived = r.findtext("v:Metadata/v:DerivedFrom", namespaces=N)
    renumbered, links, idnums = [], [], []
    for k, s in enumerate(r.findall("v:Body/v:Section", N), 1): section(s, ids.section(did, k, top=True))
    if renumbered: rep("I", f, f"projekts: {len(renumbered)} uzdevumiem drukātais numurs atšķiras no identifikatora (pārnumurēts; identifikators nemainās)")
    if derived: LINKS.append((f, did, derived, links))
    nums = sorted(int(t.get("number")) for t in r.iter(f"{{{NS}}}Task"))
    gaps = sorted(set(range(1, (nums[-1] if nums else 0) + 1)) - set(nums))
    if gaps: rep("W", f, f"uzdevumu numerācijā trūkst: {gaps}")
    cp = r.find("v:Composition", N)
    if any(m.get("id") for m in cp.iter(f"{{{NS}}}PrimeMinisterCandidate", f"{{{NS}}}Minister")): rep("W", f, "parakstītājiem identifikatoru nepiešķir")
    rep("I", f, f"{did}: {len(r.findall('.//v:Section', N))} sadaļas, {len(nums)} uzdevumi")
    return did, texts, idnums


def check_plan(f, r, decls, govs, orgs):
    pid, gid, did = r.get("id"), r.get("government"), r.get("declaration")
    if pid != ids.plan(gid): rep("E", f, f"{pid}: jābūt {ids.plan(gid)}")
    if govs:
        if gid not in govs: rep("E", f, f"valdība {gid} nav reģistrā")
        elif govs[gid].findtext("v:Declaration", namespaces=N) != did: rep("E", f, "reģistrā valdībai norādīta cita deklarācija")
    term = govs.get(gid).find("v:TermEnd", N) if govs.get(gid) is not None else None
    term_end = term.get("value") if term is not None else None
    for k, a in enumerate(r.findall("v:Metadata/v:Approval", N), 1):
        if a.get("id") != ids.plan_version(pid, k): rep("E", f, f"{a.get('id')}: sagaidīts {ids.plan_version(pid, k)}")
    tasks = set(decls[did][1]) if did in decls else None
    if tasks is None: rep("W", f, f"deklarācija {did} nav šajā mapē — saite ar uzdevumiem netiek pārbaudīta")
    per_task = defaultdict(int)
    for m in r.findall("v:Measure", N):
        mid, num, t = m.get("id"), m.get("number"), m.get("task")
        if not t.startswith(did + ".u"): rep("E", f, f"{mid}: uzdevums {t} nav no deklarācijas {did}"); continue
        tn = int(re.search(r"\.u(\d+)", t).group(1))
        if tasks is not None and tn not in tasks: rep("E", f, f"{mid}: uzdevums {tn} deklarācijā nav")
        mm = re.fullmatch(r"(\d+)\.(\d+)\.?", num)
        if not mm or int(mm.group(1)) != tn: rep("E", f, f"{mid}: numurs „{num}” neatbilst uzdevumam {tn}")
        elif mid != ids.measure(pid, tn, int(mm.group(2))): rep("E", f, f"{mid}: sagaidīts {ids.measure(pid, tn, int(mm.group(2)))}")
        per_task[tn] += 1
        for o in m.findall("v:Responsible", N) + m.findall("v:CoResponsible", N):
            for c in (o.get("orgs") or "").split():
                if orgs and c not in orgs: rep("E", f, f"{mid}: organizācija {c} nav organizāciju reģistrā")
        for v in (m.find("v:Deadline", N).get("values") or "").split():
            if term_end and v > term_end: rep("E", f, f"{mid}: termiņš {v} pēc valdības pilnvaru beigām {term_end}")
        for p in m.findall("v:Progress", N):
            if p.get("id") != ids.progress(mid, p.get("period")): rep("E", f, f"{p.get('id')}: sagaidīts {ids.progress(mid, p.get('period'))}")
    over = {tn: n for tn, n in sorted(per_task.items()) if n > 5}
    if over: rep("W", f, f"{len(over)} uzdevumiem vairāk nekā pieci pasākumi (kārtības ruļļa 18. punkts): " + ", ".join(f"{tn}. — {n}" for tn, n in over.items()))
    if tasks is not None:
        without = sorted(tasks - set(per_task))
        if without: rep("W", f, f"uzdevumi bez pasākumiem (kārtības ruļļa 20. punkts): {without}")
    rep("I", f, f"{sum(per_task.values())} pasākumi {len(per_task)} uzdevumiem")


def main(folder):
    docs = load(folder)
    govs, orgs = {}, set()
    for f, r in docs["GovernmentRegistry"]: g, o = check_registry(f, r); govs.update(g)
    for f, r in docs["OrganizationRegistry"]: orgs |= check_orgs(f, r)
    decls = {}
    for f, r in docs["GovernmentDeclaration"]:
        did, texts, nums = check_declaration(f, r, govs); decls[did] = (texts, nums)
    for f, did, derived, links in LINKS:
        if derived not in decls: rep("I", f, f"avota deklarācija {derived} nav šajā mapē — saites netiek pārbaudītas"); continue
        src_ids = {ids.task(derived, n) for n in decls[derived][1]}
        bad = [s for _, s in links if re.sub(r"-\d+$", "", s) not in src_ids]
        if bad: rep("E", f, f"derivedFrom norāda uz neesošiem avota uzdevumiem: {bad}")
        taken = {s for _, s in links}
        rep("I", f, f"projekts no {derived}: pārņemti {len(taken)}, jauni {len(decls[did][1]) - len(links)}, izņemti {len(src_ids - taken)}")
    for f, r in docs["GovernmentActionPlan"]: check_plan(f, r, decls, govs, orgs)
    for lvl in "EWI":
        for l, w, m in OUT:
            if l == lvl: print(f"{l}  {w}: {m}")
    e = sum(1 for l, *_ in OUT if l == "E"); w = sum(1 for l, *_ in OUT if l == "W")
    print(f"\n{e} kļūdas, {w} brīdinājumi")
    return 1 if e else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data")))
