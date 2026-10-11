import re
import sys

ZL_PATH = r"C:/git/voynich-collective/data/ZL3b-n.txt"
RF_PATH = r"C:/git/voynich-collective/data/RF1b-er.txt"  # resolved variant, matches ZL's own
                                                           # "resolve to first option" normalization policy


def strip_markup_zl(text):
    # remove <...> tags (paragraph/line markers, comments), keep word content
    text = re.sub(r'<[^>]*>', '', text)
    # resolve [a:b] alternatives to the FIRST option, per this project's own established
    # normalization policy (data/scripts/normalize_eva.py)
    text = re.sub(r'\[([^:\]]+):[^\]]*\]', r'\1', text)
    # resolve {a} (rare alt marker if present) similarly - keep content
    text = re.sub(r'\{([^}]*)\}', r'\1', text)
    # normalize word-boundary punctuation: , and other intra-line separators behave like .
    text = text.replace(',', '.')
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
                continue  # folio header line, not a text locus
            out[locus] = stripper(rest)
    return out


zl = parse(ZL_PATH, strip_markup_zl)
rf = parse(RF_PATH, strip_markup_rf)

common = sorted(set(zl) & set(rf), key=lambda k: (k.split('.')[0], k))
print(f"ZL loci: {len(zl)}  RF loci: {len(rf)}  common: {len(common)}")

total_words = 0
matched_words = 0
mismatches = []
line_mismatch_count = 0
locus_missing_on_one_side = (set(zl) ^ set(rf))

for locus in common:
    zwords = [w for w in zl[locus].split('.') if w]
    rwords = [w for w in rf[locus].split('.') if w]
    if len(zwords) != len(rwords):
        line_mismatch_count += 1
        continue  # word-count mismatch at this locus; counted separately, not word-aligned
    for zw, rw in zip(zwords, rwords):
        total_words += 1
        if zw == rw:
            matched_words += 1
        else:
            mismatches.append((locus, zw, rw))

print(f"Loci with matching word-count: {len(common) - line_mismatch_count} / {len(common)}")
print(f"Loci with DIFFERENT word-count (not word-aligned, excluded from word comparison): {line_mismatch_count}")
print(f"Total words compared: {total_words}")
print(f"Matched: {matched_words} ({100*matched_words/total_words:.2f}%)")
print(f"Mismatched: {len(mismatches)} ({100*len(mismatches)/total_words:.2f}%)")
print(f"Loci missing on exactly one side: {len(locus_missing_on_one_side)}")
print()
print("First 25 word-level mismatches (locus, ZL, RF-resolved):")
for m in mismatches[:25]:
    print(" ", m)
