import re
import lxml.etree as ET
from statistics import mean

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

HONORIFICS = ["saint", "sir", "rector", "master of arts"]


def parse_single_date(s):
    if s.startswith("ca. "):
        s = s[4:]
    if re.match("1[0-9]{3}\\??($|[. ])", s):
        if s.endswith("?"):
            s = s[:-1]
        return int(s[0:4])
    print("could not parse date %s" % s)
    return


def parse_date(s):
    birth = death = None
    if s.startswith("b. "):
        birth = parse_single_date(s[3:])
    elif s.startswith("d. "):
        death = parse_single_date(s[3:])
    elif s.startswith("fl. "):
        return None, None
    else:
        parts = s.split("-")
        if len(parts) == 2:
            birth = parse_single_date(parts[0])
            death = parse_single_date(parts[1])
    return birth, death


def parse_author(s):
    date = first = last = dob = dod = None
    # Lose a final period
    if s.endswith("."):
        s = s[:-1]
    if s.endswith(", aut"):
        s = s[:-5]
    parts = s.split(",")
    last = parts.pop(0).strip()
    if len(parts) > 0:
        first = parts.pop(0).strip()
        if re.match("1[0-9]{3}|fl\\.|b\\.|d\\.|ca\\.", first):
            date = first
            first = None
    if date is None:
        for p in parts:
            p = p.strip()
            if re.match("1[0-9]{3}", p):
                date = p
                break
    if date is not None:
        dob, dod = parse_date(date)
    if first is None:
        name = last
    else:
        name = first + " " + last
    return name, dob, dod


def get_tree(f):
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
    return doc


def date_file(filename, doc, min_date, max_date):
    founddates = set()
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
        matches = re.findall(DATERE, ET.tostring(doc,
                                                 method="text",
                                                 encoding="unicode"))
        founddates.update(map(str_to_date, matches))
    founddates = set(filter(lambda d: d < max_date and d > min_date,
                            founddates))
    if len(founddates) > 1:
        if max(founddates) - min(founddates) < 31:
            return int(mean(founddates))
        else:
            print("found too many matches for: %s; %s" %
                  (filename, founddates))
    elif len(founddates) == 0:
        print("found no matches for: %s" % filename)
    else:
        return founddates.pop()

# These authors erroneously appear to be a corporate body, thus we have to
# override them specifically.
AUTH_EXCEPTIONS = {
    "Barbon, Nicholas, d. 1698. Letter to a gentleman in the country giving an account of the two insurance-offices, the Fire-Office & Friendly-Society.": "Barbon, Nicholas, d. 1698.",
    "Du Moulin, Lewis, 1606-1680. Motions for reforming the Church of England in this present Parliament.": "Du Moulin, Lewis, 1606-1680.",
    "Elliot, John, Parliament-Commissioner.": "Elliot, John",
    "Adamson, Patrick, 1537-1592. Declaration of the Kings Majesties intentioun and meaning toward the lait actis of Parliament. aut": "Adamson, Patrick, 1537-1592.",
    "Bishop, George, gentleman in the Parliamentary army.": "Bishop, George",
    "Burnet, Gilbert, 1643-1715. Reflections on a late pamphlet entituled Parliamentum pacificum.":"Burnet, Gilbert, 1643-1715.",
    "Cowley, Abraham, 1618-1667. To the Royal Society.": "Cowley, Abraham, 1618-1667.",
    "Dryden, John, 1631-1700. Poem upon the death of his late Highness Oliver, Lord Protector of England, Scotland, and Ireland.": "Dryden, John, 1631-1700.",
    "Findlater, James Ogilvy, Earl of, 1663-1730. Speech of James Viscount of Seafield ... president to the Parliament of Scotland, on Tuesday the nineteenth of July 1698.": "Findlater, James Ogilvy, Earl of, 1663-1730.",
    "Fletcher, Robert, with the Army at Dublin.": "Fletcher, Robert",
    "Ford, John, Mayor of Bath.": "Ford, John",
    "Fowler, Edward, 1632-1714. A vindication of the divines of the Church of England.": "Fowler, Edward, 1632-1714.",
    "Gander, Joseph. Sovereignty of the British-seas asserted.": "Gander, Joseph.",
    "Harding, Thomas, 1516-1572. Confutation of a booke intituled An apologie of the Church of England.": "Harding, Thomas, 1516-1572.",
    "Hart, Richard, Friend to all the conformable clergy and laity of the true and apostolical Church of England.": "Hart, Richard",
    "I. I., faithful subject to his King and welwisher to his Parliament.": "I. I.",
    "J. G., member of the Church of England.": "J. G.",
    "J. S., Minister of the Church of England.": "J. S.",
    "L. D., member of the late Parliament.": "L. D.",
    "Lauderdale, John Maitland, Duke of, 1616-1682. Speech of His Grace the Earl of Lauderdaill ... delivered in Parliament the ninteenth day of October, 1669.": "Lauderdale, John Maitland, Duke of, 1616-1682.",
    "Lauderdale, John Maitland, Duke of, 1616-1682. Speech of His Grace the Earle of Lauderdale, His Majesties high-commissioner for the Parliament of Scotland.": "Lauderdale, John Maitland, Duke of, 1616-1682.",
    "Lilburne, Elizabeth. To the chosen and betrusted knights, citizens and burgesses, assembled in the high and supream court of Parliament.": "Lilburne, Elizabeth",
    "Luce, Richard, Presbyter of the Church of England.": "Luce, Richard",
    "Mayor, William.": "Mayor, William.",
    "Merke, Thomas, d. 1409. Speech in the last Parliament of King Richard II.": "Merke, Thomas, d. 1409.",
    "N. N., Protestant and declared dissenter from the Church of England.": "N. N.",
    "Northleigh, John, 1657-1705. Parliamentum pacificum.": "Northleigh, John, 1657-1705.",
    "R. C., Minister of the Church of England.": "R. C.",
    "R. T., Presbyter of the Church of England.": "R. T.",
    "Robinson, William, member of the Society of Friends.": "Robinson, William",
    "S. J., Minister of the Church of England.": "S. J.",
    "Sprat, Thomas, 1635-1713. History of the Royal Society of London.": "Sprat, Thomas, 1635-1713.",
    "Sprat, Thomas, 1635-1713. To the happie memory of the most renowned Prince Oliver, Lord Protector.": "Sprat, Thomas, 1635-1713.",
    "Stoppa, Giovanni Battista. Collection or narative sent to His Highness the Lord Protector ... concerning the bloody and barbarous massacres and other cruelties.": "Stoppa, Giovanni Battista.",
    "T. B., countrey minister of the Church of England.": "T. B.",
    "T. N., True member of the Church of England.": "T. N.",
    "Tenison, Thomas, 1636-1715. Present state of the controversie between the Church of England and the Church of Rome. aut": "Tenison, Thomas, 1636-1715.",
    "Wake, William, 1657-1737. Continuation of the present state of controversy, between the Church of England, and the Church of Rome. aut": "Wake, William, 1657-1737.",
    "Wake, William, 1657-1737. Defence of the Exposition of the doctrine of the Church of England. aut": "Wake, William, 1657-1737.",
    "Wake, William, 1657-1737. Exposition of the doctrine of the Church of England. aut": "Wake, William, 1657-1737.",
    "Wake, William, 1657-1737. Second defence of the Exposition of the doctrine of the Church of England. aut": "Wake, William, 1657-1737.",
    "Walker, Clement, 1595-1651. Relations and observations, historical and politick, upon the Parliament.": "Walker, Clement, 1595-1651.",
    "Walton, J., of the Parliamentary Army.": "Walton, J.",
    "Whitby, Daniel, b. 1609 or 10. Vindication of the forme of common prayers vsed in the Church of England.": "Whitby, Daniel, b. 1609 or 10",
    "Wilkinson, Robert, member of the Army.": "Wilkinson, Robert"
}


def author_file(filename, doc):
    authors = doc.iter("AUTHOR")
    author_set = set()
    for author in authors:
        author = ET.tostring(author,
                             method="text",
                             encoding="unicode")
        if author in AUTH_EXCEPTIONS:
            author = AUTH_EXCEPTIONS[author]
        elif "Parliament" in author or \
           "England and Wales" in author or \
           "Church of England" in author or \
           "Church of Scotland" in author or \
           "Privy Council" in author or \
           "Army " in author or \
           "Society" in author or \
           "Committee" in author or \
           "Mayor" in author or \
           "Synod" in author or \
           "Lord Lieutenant" in author or \
           "Eglises" in author or \
           "City of London" in author or \
           "Lord Protector" in author or \
           "Sovereign" in author or \
           "East India Company" in author or \
           "Staaten" in author:
            # Skip institutional authors, including Dutch parliaments
            # (staaten)
            print("Skipping author %s" % author)
            continue
        author_tuple = parse_author(author)
        author_set.add(author_tuple)
    if len(author_set) > 1:
        print("too many authors: %s, %s" % (filename, author_set))
    elif len(author_set) == 0:
        print("no author %s" % filename)
    else:
        return author_set.pop()


def date_files(files, min_date, max_date, progress=False):
    # TODO: implement progress indication
    dates = []
    for f in files:
        name = f.split("/")[-1].split(".")[0]
        tree = get_tree(f)
        author_info = author_file(f, tree)
        if author_info is None:
            author = dob = dod = None
        else:
            author, dob, dod = author_info
        dates.append({'file': name,
                      'date': date_file(f, tree, min_date, max_date),
                      'author': author,
                      'dob': dob,
                      'dod': dod})
    return dates
