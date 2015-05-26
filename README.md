# The PYCCLE corpus

The Penn-York Computer-annotated Corpus of a Large Amount of English
based on the TCP (PYCCLE-TCP) corpus is a part-of-speech tagged version
of the Early English Books Online
([EEBO](http://www.textcreationpartnership.org/tcp-eebo/)) and
Eighteenth Century Collections Online
([ECCO](http://www.textcreationpartnership.org/tcp-ecco/)) corpora, as
digitized by the Text Creation Partnership (TCP).

You can download the corpus from the following links:

- [EEBO Phase 1](https://s3.amazonaws.com/pyccle/pyccle-eebo.tgz)
- [ECCO](https://s3.amazonaws.com/pyccle/pyccle-ecco.tgz)

Please be advised that these are large downloads (1GB for the EEBO;
100MB for ECCO)

## Composition

The EEBO portion of the corpus (1473–1700) comprises 25,363 texts in
Phase 1 and 22,967 texts in Phase 2, for a total of roughly 900 million
words.  The ECCO portion of the corpus contains 2,473 texts for a total
of roughly 100 million words.

The EEBO-Phase1 and ECCO texts are publicly available from the TCP, and
in an annotated form through PYCCLE.  The EEBO-Phase2 texts are only
available to the faculty, staff, and students of institutions which
partner with the TCP, and thus cannot be made publicly available here.
Please contact Aaron Ecay if you qualify for access to EEBO-Phase2 and
would like to access the PYCCLE versions of those texts.

## Annotation

The texts have been acquired in their TEI-annotated XML format.  They
have been stripped of metadata, including footnotes, marginalia, and
**any verse material** (text occurring in `<L>...</L>` XML tags).  The
texts were then tagged using a POS tagger trained on the PPCEME.

### Accuracy

The PYCCLE texts have not been hand-corrected.  There are several
conceivable sources of error:
- Uncorrected OCR errors in the texts.
- Annotation differences between the TCP and PPCEME
  - PPCEME contractions are split manually.  The PYCCLE uses an
    automatic tokenizer which splits contractions based on Modern
    English rules.  Thus, non-standard contractions such as “shalbe” (=
    “shall be”) are not identified, and are often tagged incorrectly.
  - The PPCEME and TCP projects differ in their use of diacritics and
    Unicode characters to indicate non-standard orthographic variants,
    such as the superscript characters in words like M<sup>r</sup> or
    y<sup>rs</sup>; the diacritic representing a final “n” in words like
    “conditiõ”; and others.  Thus, these words may be incorrectly
    identified and tagged.
  - The TCP includes texts (or parts of texts) in foreign languages such
    as Latin and Welsh.
- Inherent limitations of automatic POS tagging

## Metadata

The files are supplied with a csv file listing their code name (A or B
followed by 5 digits for the EEBO; K followed by 6 digits for the ECCO).
This information has been automatically scraped from metadata supplied
with the corpus, and may in rare cases be incorrect or incomplete.  More
complete metadata is available on the
[Oxford Text Archive website](http://ota.ox.ac.uk/tcp/).  I have not
been able to locate this metadata in a machine-readable format.  **If
you are able to supply this information please get in touch with me.**

## Searching

You can use the
[Weihnachsgurke](https://github.com/aecay/weihnachtsgurke) program for
searching the PYCCLE.

## Licensing

The original texts from the TCP are licensed under the
[CC0](https://creativecommons.org/about/cc0) license.  The
PYCCLE-annotated versions are licensed under the
[CC Attribution](https://creativecommons.org/licenses/by/4.0/) license.
This means that you must cite the PYCCLE when you create materials based
off of it, but you are otherwise free to use it as you see fit.  For
academic publications, an appropriate citation is:

> Ecay, Aaron.  (2015).  “The Penn-York Computer-annotated Corpus of a
> Large amount of English based on the TCP (PYCCLE-TCP)”.  Public
> release 1.  <https://github.com/uoy-linguistics/pyccle>.

As a courtesy, **I would appreciate being notified if you create a
publication or resource based on PYCCLE** (including a conference
presentation or poster, academic article, online resource, further
annotated database, etc.)
