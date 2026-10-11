# Aici sunt limbile suportate. Pentru fiecare limbă avem o listă de
# cuvinte frecvente (stop words) care se ignoră la comparare.
LANGUAGES = {
    "ro": {"name": "Română", "stop_words": [
        "si", "de", "la", "in", "a", "o", "un", "cu", "pe", "ca", "este", "sunt",
        "se", "nu", "din", "pentru", "al", "ale", "care", "sa", "mai", "dar",
        "sau", "ce", "le", "lui", "fi", "fost", "prin", "dupa", "ei", "ea", "el",
        "acest", "aceasta", "va", "au", "am"]},
    "en": {"name": "Engleză", "stop_words": [
        "the", "and", "is", "are", "of", "to", "in", "an", "that", "for", "with",
        "on", "it", "as", "this", "was", "be", "by", "at", "or", "from", "not",
        "but", "have", "has", "they", "we", "you"]},
    "ru": {"name": "Rusă", "stop_words": [
        "и", "в", "во", "не", "что", "он", "на", "я", "с", "со", "как", "а", "то",
        "все", "она", "так", "его", "но", "да", "ты", "к", "у", "же", "вы", "за",
        "бы", "по", "только", "ее", "мне", "было", "вот", "от", "меня", "еще",
        "нет", "о", "из", "ему", "это", "для", "они", "мы", "был", "быть"]},
}