# Distanța Levenshtein: de câte operații (inserare, ștergere, înlocuire
# de caracter) e nevoie ca dintr-un text să obții celălalt.
# E scrisă de mână, fără bibliotecă, ca să se vadă cum funcționează.


def distance(a: str, b: str) -> int:
    # ținem minte doar două rânduri din matrice, nu toată matricea
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i]
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            cur.append(min(
                prev[j] + 1,         # ștergere
                cur[j - 1] + 1,      # inserare
                prev[j - 1] + cost,  # înlocuire
            ))
        prev = cur
    return prev[-1]


def similarity(a: str, b: str) -> float:
    # 1 = identice, 0 = complet diferite
    longest = max(len(a), len(b))
    if longest == 0:
        return 1.0
    return 1 - distance(a, b) / longest
