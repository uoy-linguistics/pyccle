import re
import lxml.etree as ET
from statistics import mean
from tqdm import tqdm

DATERE = "(^|[^0-9])([1l][4-8][0-9lI]\\[?[0-9lI-]\\??\\]?)($|[^0-9])"


def str_to_date(ss):
    s = ss[1]
    s = s.replace("l", "1")
    s = s.replace("I", "1")
    s = s.replace("[", "")
    s = s.replace("]", "")
    s = s.replace("?", "")
    if s[-1] == "-":
        # Unknown ones-place
        s = s[:-1] + "5"
    return int(s)


def date_file(f, min_date, max_date):
    founddates = set()
    with open(f) as fin:
        content = fin.read()
    doc = ET.fromstring(content)
    idnos = doc.iter("IDNO")
    for idno in idnos:
        idno.getparent().remove(idno)
    notes = doc.iter("NOTE")
    for note in notes:
        note.getparent().remove(note)
    terms = doc.iter("TERM")
    for term in terms:
        term.getparent().remove(term)
    ps = doc.iter("PUBLICATIONSTMT")
    for p in ps:
        s = ET.tostring(p, method="text", encoding="unicode")
        if "Michigan" in s:
            # Bogus PUBLICATIONSTMT
            p.getparent().remove(p)
    dates = doc.iter("DATE")
    for date in dates:
        matches = re.findall(DATERE, ET.tostring(date,
                                                 method="text",
                                                 encoding="unicode"))
        founddates.update(map(str_to_date, matches))
    if len(founddates) == 0:
        ps = doc.iter("PUBLICATIONSTMT")
        for p in ps:
            s = ET.tostring(p, method="text", encoding="unicode")
            matches = re.findall(DATERE, s)
            founddates.update(map(str_to_date, matches))
    if len(founddates) == 0:
        matches = re.findall(DATERE, ET.tostring(doc, method="text", encoding="unicode"))
        founddates.update(map(str_to_date, matches))
    founddates = set(filter(lambda d: d < max_date and d > min_date, founddates))
    if len(founddates) > 1:
        if max(founddates) - min(founddates) < 31:
            return int(mean(founddates))
        else:
            print("found too many matches for: %s; %s" % (f, founddates))
    elif len(founddates) == 0:
        print("found no matches for: %s" % f)
    else:
        return founddates.pop()


def date_files(files, min_date, max_date, progress=True):
    datesdict = {}
    if progress:
        coll = tqdm(files)
    else:
        coll = files
    for f in coll:
        name = f.split("/")[-1].split(".")[0]
        datesdict[name] = date_file(f, min_date, max_date)
    return datesdict
