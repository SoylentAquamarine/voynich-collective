"""Extends compare_rf1b_zl3b_boundary_aware.py by normalizing ZL's @NNN; special-character
notation to RF's own plain '?' for the same "uncertain character" concept, per the next step
named in logs/2026-10-11-sq1-boundary-aware-realignment.md.

RF1b-er.txt contains zero @NNN; instances (confirmed via grep before writing this script) --
only ZL3b-n.txt uses this notation, so normalization is one-directional.
"""
import re

ZL_PATH = r"C:/git/voynich-collective/data/ZL3b-n.txt"
RF_PATH = r"C:/git/voynich-collective/data/RF1b-er.txt"


def strip_markup_zl(text):
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
    text = re.sub(r'\{([^}]*)\}', r'\1', text)
    text = text.replace(',', '.')
    # Normalize ZL's @NNN; numbered special-character references to RF's own plain '?'
    # for the identical underlying concept (an attested-but-unreadable character).
    text = re.sub(r'@\d+;', '?', text)
    return text.strip()


def strip_markup_rf(text):
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\{([^}]*)\}', r'\1', text)
    text = text.replace(',', '.')
    return text.strip()


def parse(path, stripper):
    out = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            m = re.match(r'^<(f[^,>]+(?:,[^>]+)?)>\s*(.*)$', line)
            if not m:
                continue
            locus, rest = m.groups()
            if '.' not in locus:
                continue
            out[locus] = stripper(rest)
    return out


def despace(text):
    return text.replace('.', '')


def levenshtein(a, b):
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        for j in range(1, lb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[lb]


zl = parse(ZL_PATH, strip_markup_zl)
rf = parse(RF_PATH, strip_markup_rf)

common = sorted(set(zl) & set(rf), key=lambda k: (k.split('.')[0], k))

pure_boundary_shift = 0
genuine_difference = 0
total_edit_distance = 0
total_chars = 0
worst_cases = []

for locus in common:
    z_despaced = despace(zl[locus])
    r_despaced = despace(rf[locus])
    total_chars += max(len(z_despaced), len(r_despaced))
    if z_despaced == r_despaced:
        pure_boundary_shift += 1
    else:
        genuine_difference += 1
        d = levenshtein(z_despaced, r_despaced)
        total_edit_distance += d
        worst_cases.append((d, locus, z_despaced, r_despaced))

worst_cases.sort(reverse=True)

print(f"Common loci: {len(common)}")
print(f"Loci with IDENTICAL despaced glyph sequence (pure boundary-shift, zero content disagreement): "
      f"{pure_boundary_shift} ({100*pure_boundary_shift/len(common):.2f}%)")
print(f"Loci with a GENUINE glyph-level content difference (despaced sequences differ): "
      f"{genuine_difference} ({100*genuine_difference/len(common):.2f}%)")
print()
print(f"Total despaced characters (max of the two sides, summed across all common loci): {total_chars}")
print(f"Total edit distance across all genuinely-differing loci: {total_edit_distance}")
print(f"Corpus-wide glyph-level agreement rate (1 - edit_distance/total_chars), AFTER @NNN;->? "
      f"normalization: {100*(1 - total_edit_distance/total_chars):.2f}%")
print()
print("Worst 15 genuinely-differing loci by edit distance (distance, locus, ZL-despaced, RF-despaced):")
for d, locus, zd, rd in worst_cases[:15]:
    print(f"  {d:3d}  {locus:12s}  {zd!r:40s}  {rd!r}")
