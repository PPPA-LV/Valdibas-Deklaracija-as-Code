"""Identifikatoru veidošana — viena vieta, ko lieto gan pārveidotāji, gan pārbaudītājs.

Noteikumi: docs/IDENTIFIKATORI.md. Funkcijas ir tīras: tās nesaskaņo ar datiem, tikai veido virkni.
"""
import re

ROOT_RE = r"lv-(?:dekl|mk)-\d{4}-\d{2}-\d{2}(?:-[2-9])?"
ITEM_RE = re.compile(rf"^{ROOT_RE}(?:\.[a-z]{{1,2}}\d*(?:-\d+)*)+$")


def declaration_id(date_iso, seq=1):
    """lv-dekl-GGGG-MM-DD[-n]; date_iso = datums dokumentā vai, ja tā nav, uzticības balsojuma datums."""
    return f"lv-dekl-{date_iso}" + (f"-{seq}" if seq > 1 else "")


def government_id(vote_date_iso, seq=1):
    """lv-mk-GGGG-MM-DD[-n]; datums = Saeimas uzticības balsojuma datums."""
    return f"lv-mk-{vote_date_iso}" + (f"-{seq}" if seq > 1 else "")


def section(parent, n, top):
    """Augstākā līmeņa sadaļa: <dekl>.sNN; apakšsadaļa: <vecāksadaļa>-NN."""
    return f"{parent}.s{n:02d}" if top else f"{parent}-{n:02d}"


def task(decl, number, dup=1):
    """Uzdevums: <dekl>.uNNN — numurs, kā drukāts. Dublikāts avotā: -2, -3…"""
    return f"{decl}.u{number:03d}" + (f"-{dup}" if dup > 1 else "")


def paragraph(sec, n): return f"{sec}.t{n:02d}"
def list_(parent, n): return f"{parent}.l{n:02d}"
def item(lst, n): return f"{lst}.i{n:02d}"
def signatory(decl, n): return f"{decl}.m{n:02d}"          # m00 = Ministru prezidenta amata kandidāts
def annex(decl, n): return f"{decl}.pi{n}"
def goal(sec, n): return f"{sec}.g{n}"
def result(sec, n): return f"{sec}.rz{n}"
def commitment(source, n): return f"{source}.a{n}"
def plan(gov): return f"{gov}.rp"
def plan_version(pl, n): return f"{pl}.v{n}"
def measure(pl, task_number, n): return f"{pl}.u{task_number:03d}.p{n}"
def new_measure(pl, n): return f"{pl}.j{n:03d}"
def measure_result(m, n): return f"{m}.d{n}"
def progress(m, period_iso): return f"{m}.z{period_iso.replace('-', '')}"


def valid(item_id):
    return bool(ITEM_RE.match(item_id))
