import re
import unicodedata
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langdetect import detect as ld_detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.languages import LANGUAGES

DetectorFactory.seed = 0  # rezultate stabile la detectare
app = FastAPI(title="TextLab")


class Texts(BaseModel):
    text_a: str
    text_b: str
    language: str = "auto"


def normalize(text: str) -> str:
    """litere mici, fără punctuație; diacriticele se scot doar la literele
    latine (ș, ă, é...), iar chirilica rămâne intactă (й rămâne й)"""
    text = unicodedata.normalize("NFD", text.lower())
    out = []
    for ch in text:
        if unicodedata.category(ch) == "Mn" and out and out[-1].isascii() and out[-1].isalpha():
            continue
        out.append(ch)
    text = unicodedata.normalize("NFC", "".join(out)).replace("ё", "е")
    return re.sub(r"[^\w\s]", " ", text)


def detect_code(text: str):
    try:
        code = ld_detect(text)
    except LangDetectException:
        return None
    return code if code in LANGUAGES else None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/languages")
def languages():
    return [{"code": c, "name": v["name"]} for c, v in LANGUAGES.items()]


@app.post("/api/compare")
def compare(data: Texts):
    a, b = normalize(data.text_a), normalize(data.text_b)
    if not a.strip() or not b.strip():
        raise HTTPException(status_code=400, detail="Completează ambele texte.")

    if data.language == "auto":
        codes = {detect_code(data.text_a), detect_code(data.text_b)} - {None}
    elif data.language in LANGUAGES:
        codes = {data.language}
    else:
        raise HTTPException(status_code=400, detail="Limbă necunoscută.")

    stop = sorted({normalize(w).strip() for c in codes
                   for w in LANGUAGES[c]["stop_words"]})

    vectorizer = TfidfVectorizer(stop_words=stop or None)
    try:
        matrix = vectorizer.fit_transform([a, b])
    except ValueError:
        raise HTTPException(status_code=400, detail="Textele sunt prea scurte.")

    score = float(cosine_similarity(matrix[0], matrix[1])[0][0])

    words = vectorizer.get_feature_names_out()
    row_a, row_b = matrix[0].toarray()[0], matrix[1].toarray()[0]
    common = sorted(
        [(w, min(x, y)) for w, x, y in zip(words, row_a, row_b) if x > 0 and y > 0],
        key=lambda t: t[1], reverse=True,
    )

    if score >= 0.75:
        verdict = "Foarte asemănătoare"
    elif score >= 0.4:
        verdict = "Parțial asemănătoare"
    else:
        verdict = "Diferite"

    return {
        "similarity": round(score * 100, 1),
        "verdict": verdict,
        "languages": [LANGUAGES[c]["name"] for c in sorted(codes)],
        "common_words": [w for w, _ in common],
        "stats": {
            "words_a": len(a.split()),
            "words_b": len(b.split()),
            "shared_unique": len(common),
        },
    }


# trebuie să fie ULTIMA linie
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")