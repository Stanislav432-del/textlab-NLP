# Experiment: rulează ambele metode pe perechile din pairs.json și
# salvează rezultatele în results.csv, plus mediile pe categorii.
# Se pornește din folderul proiectului:  python -m experiment.run
import csv
import json
from pathlib import Path

from backend.main import Texts, compare

FOLDER = Path(__file__).parent
CATEGORIES = ["identice", "modificari mici", "reformulate", "diferite"]

pairs = json.loads((FOLDER / "pairs.json").read_text(encoding="utf-8"))
rows = []
for nr, pair in enumerate(pairs, start=1):
    res = compare(Texts(text_a=pair["a"], text_b=pair["b"], language="ro"))
    rows.append({
        "nr": nr,
        "categorie": pair["category"],
        "cosinus_%": res["similarity"],
        "levenshtein_%": res["levenshtein"]["similarity"],
        "distanta": res["levenshtein"]["distance"],
        "timp_cosinus_ms": res["time_ms"]["cosine"],
        "timp_levenshtein_ms": res["time_ms"]["levenshtein"],
    })

with open(FOLDER / "results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"{'Categorie':<17}{'Cosinus %':>11}{'Levenshtein %':>15}")
for cat in CATEGORIES:
    part = [r for r in rows if r["categorie"] == cat]
    cos = sum(r["cosinus_%"] for r in part) / len(part)
    lev = sum(r["levenshtein_%"] for r in part) / len(part)
    print(f"{cat:<17}{cos:>11.1f}{lev:>15.1f}")

t_cos = sum(r["timp_cosinus_ms"] for r in rows) / len(rows)
t_lev = sum(r["timp_levenshtein_ms"] for r in rows) / len(rows)
print(f"\nTimp mediu: cosinus {t_cos:.2f} ms, Levenshtein {t_lev:.2f} ms")
print("Rezultatele complete sunt în experiment/results.csv")
