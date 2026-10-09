"""Negatīvie testi: sabojā piemērus un pārbauda, ka pārbaudītājs to pamana.

  python3 tools/test_validate.py
"""
import os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "data")

CASES = [
    ("pasākums neesošam uzdevumam", "lv-mk-2026-05-28.rp.xml", 'id="lv-mk-2026-05-28.rp.u014.p1" number="14.1." task="lv-dekl-2026-05-28.u014"', 'id="lv-mk-2026-05-28.rp.u099.p1" number="99.1." task="lv-dekl-2026-05-28.u099"', "uzdevums 99 deklarācijā nav"),
    ("pasākuma numurs neatbilst uzdevumam", "lv-mk-2026-05-28.rp.xml", 'number="1.3." task="lv-dekl-2026-05-28.u001"', 'number="2.3." task="lv-dekl-2026-05-28.u001"', "neatbilst uzdevumam"),
    ("nezināma organizācija", "lv-mk-2026-05-28.rp.xml", '<Responsible orgs="10-0000">', '<Responsible orgs="10-0999">', "nav organizāciju reģistrā"),
    ("ministrijas ID nav SS-0000", "organizacijas.xml", 'id="20-0000" regNo="40900039891"', 'id="20-0699" regNo="40900039891"', "jābūt 20-0000"),
    ("padotības iestāde citā resorā", "organizacijas.xml", 'id="10-0033" regNo="90002065000" kind="subordinate" parent="10-0000"', 'id="10-0033" regNo="90002065000" kind="subordinate" parent="14-0000"', "nav sava resora"),
    ("uzdevuma ID neatbilst numuram", "lv-dekl-2026-05-28.xml", 'id="lv-dekl-2026-05-28.u012" number="12"', 'id="lv-dekl-2026-05-28.u013" number="12"', "sagaidīts lv-dekl-2026-05-28.u012"),
    ("dublēts uzdevuma numurs", "lv-dekl-2026-05-28.xml", 'id="lv-dekl-2026-05-28.u013" number="13"', 'id="lv-dekl-2026-05-28.u013" number="12"', "XSD"),
    ("sadaļas ID ārpus secības", "lv-dekl-2026-05-28.xml", 'id="lv-dekl-2026-05-28.s02-03"', 'id="lv-dekl-2026-05-28.s02-07"', "sagaidīts lv-dekl-2026-05-28.s02-03"),
    ("deklarācija nesakrīt ar reģistru", "valdibas.xml", "<Declaration>lv-dekl-2026-05-28</Declaration>", "<Declaration>lv-dekl-2026-05-29</Declaration>", "cita deklarācija"),
    ("termiņš pēc pilnvaru beigām", "valdibas.xml", "<ActionPlan>lv-mk-2026-05-28.rp</ActionPlan>", '<ActionPlan>lv-mk-2026-05-28.rp</ActionPlan>\n    <TermEnd value="2026-09-01">pārbaudes vērtība</TermEnd>', "pēc valdības pilnvaru beigām"),
]


def run(folder):
    return subprocess.run([sys.executable, os.path.join(ROOT, "tools/validate.py"), folder], capture_output=True, text=True)


def main():
    base = run(EX)
    ok = base.returncode == 0; print(("PASS" if ok else "FAIL") + "  dati ir derīgi")
    for name, fname, old, new, expect in CASES:
        d = tempfile.mkdtemp()
        for f in os.listdir(EX): shutil.copy(os.path.join(EX, f), d)
        p = os.path.join(d, fname); t = open(p, encoding="utf-8").read()
        assert old in t, f"testa šablons nav atrasts: {name}"
        open(p, "w", encoding="utf-8").write(t.replace(old, new, 1))
        r = run(d); hit = expect in r.stdout and (r.returncode == 1 or expect.startswith("uzdevumam"))
        ok &= hit; print(("PASS" if hit else "FAIL") + f"  {name}")
        if not hit: print(r.stdout)
        shutil.rmtree(d)
    print("\nVisi testi izdevās" if ok else "\nIr neizdevušies testi"); return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
