"""Title, location, freshness and experience filters, plus a rough fit hint.

Every user-specific choice (where, which titles, how many years, which employers to skip,
which skills count towards the fit hint) comes from the filter config: me/radar.yaml, or
filters.example.yaml when that doesn't exist. Nothing about one user is hard-coded here.
"""
from __future__ import annotations

import datetime as dt
import re


def _rx(pattern, flags=re.I):
    """Compile a pattern string, or a list of alternatives, into one regex. Empty -> None."""
    if not pattern:
        return None
    if isinstance(pattern, (list, tuple)):
        pattern = "|".join(f"(?:{p})" for p in pattern if p)
    return re.compile(pattern, flags)


def _words_rx(words, flags=re.I):
    words = [w for w in (words or []) if w]
    if not words:
        return None
    return re.compile(r"\b(" + "|".join(map(re.escape, words)) + r")\b", flags)


class Rules:
    def __init__(self, cfg):
        self.cfg = cfg = cfg or {}
        self.days = int(cfg.get("days") or 45)

        # ---- location
        self.loc_rx = _words_rx(cfg.get("locations"))
        codes = [c for c in cfg.get("location_codes") or [] if c]
        # country codes match case-sensitively ("IN", not the word "in")
        self.code_rx = re.compile(r"\b(" + "|".join(map(re.escape, codes)) + r")\b(?!-)") if codes else None
        self.remote_ok = cfg.get("remote_ok", True)
        self.remote_jd_rx = _words_rx(cfg.get("remote_jd_words"))
        self.remote_exclude_rx = _words_rx(cfg.get("remote_exclude_words"))

        # ---- titles
        self.families = [(f["name"], _rx(f["title"])) for f in cfg.get("families") or []]
        self.jd_check = [(f["name"], _rx(f["title"]), int(f.get("min_jd_hits", 4)))
                         for f in cfg.get("check_jd") or []]
        self.jd_terms_rx = _rx(cfg.get("jd_terms"))
        self.exclude_title_rx = _rx(cfg.get("exclude_titles"))

        # ---- employers
        self.exclude_companies = {_norm_company(c) for c in cfg.get("exclude_companies") or [] if c}

        # ---- experience
        mx = cfg.get("max_required_years")
        self.max_years = None if mx in (None, "") else float(mx)
        self.degree = (cfg.get("degree") or "bachelor").lower()

        # ---- fit hint
        self.fit_terms = {k: _rx(v) for k, v in (cfg.get("fit_terms") or {}).items()}
        self.core_terms = set(cfg.get("core_terms") or [])
        self.flags = [(f["label"], _rx(f["pattern"])) for f in cfg.get("flags") or []]

    # -------------------------------------------------------------- location
    def location_status(self, p):
        """'match', 'remote-check' (remote with no listed place; the JD decides) or None."""
        loc = p.location or ""
        if not self.loc_rx and not self.code_rx:
            return "match"  # no location filter configured
        if (self.loc_rx and self.loc_rx.search(loc)) or (self.code_rx and self.code_rx.search(loc)):
            return "match"
        low = loc.lower()
        if self.remote_ok and (p.remote or "remote" in low or "anywhere" in low):
            if not (self.remote_exclude_rx and self.remote_exclude_rx.search(low)):
                return "remote-check"
        return None

    def remote_ok_for_user(self, p):
        if not self.remote_jd_rx:
            return True
        return bool(self.remote_jd_rx.search(p.description or ""))

    # -------------------------------------------------------------- employer
    def company_excluded(self, company):
        return _norm_company(company) in self.exclude_companies

    # -------------------------------------------------------------- title
    def title_family(self, title):
        """A family label if the title is in scope; 'check:<name>' if the JD must decide; else None."""
        if self.exclude_title_rx and self.exclude_title_rx.search(title):
            return None
        if self.remote_exclude_rx and self.remote_exclude_rx.search(title.lower()):
            return None  # "ML Engineer, US" and the like
        for name, rx in self.families:
            if rx and rx.search(title):
                return name
        for name, rx, _ in self.jd_check:
            if rx and rx.search(title):
                return "check:" + name
        return None

    def jd_check_passes(self, family, text):
        name = family.split(":", 1)[1]
        need = next((n for nm, _, n in self.jd_check if nm == name), 4)
        hits = len(self.jd_terms_rx.findall(text or "")) if self.jd_terms_rx else 0
        return hits >= need, name

    # -------------------------------------------------------------- experience
    def too_senior(self, exp):
        return self.max_years is not None and exp["min"] is not None and exp["min"] > self.max_years

    def parse_experience(self, text, requirements=None):
        return parse_experience(text, requirements, degree=self.degree)

    # -------------------------------------------------------------- fit hint
    def fit_hint(self, p, family, exp):
        text = (p.description or "") + " " + (p.requirements or "")
        hits = [k for k, rx in self.fit_terms.items() if rx and rx.search(text)]
        core = [h for h in hits if h in self.core_terms]
        score = len(core) * 2 + len(hits)
        top = len(self.core_terms) * 2 + len(self.fit_terms) or 1
        level = "strong" if score >= 0.45 * top else "good" if score >= 0.25 * top else "weak"
        bits = [family, level]
        if exp.get("fresher"):
            bits.append("early-career wording")
        for label, rx in self.flags:
            if rx and rx.search(text):
                bits.append("CHECK: " + label)
        bits.append("JD hits: " + (", ".join(hits[:7]) if hits else "none"))
        return "; ".join(bits), score


def _norm_company(s):
    s = re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()
    return re.sub(r"\b(inc|pvt|private|ltd|limited|llc|corp|corporation|technologies|technology|labs|"
                  r"software|careers)\b", "", s).strip()


# ------------------------------------------------------------------ freshness
def age_days(posted, today=None):
    if not posted:
        return None
    today = today or dt.date.today()
    try:
        return (today - dt.date.fromisoformat(posted)).days
    except ValueError:
        return None


# ------------------------------------------------------------------ experience
_NUMWORDS = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6",
             "seven": "7", "eight": "8", "nine": "9", "ten": "10", "twelve": "12", "fifteen": "15"}
_NUM = r"(\d{1,2}(?:\.\d)?)"
_YRS = r"\s*\+?\s*(?:years?|yrs?)"
_PATTERNS = [
    re.compile(_NUM + r"\s*\+?\s*(?:-|–|—|to)\s*" + _NUM + _YRS, re.I),                   # 1-3 years
    re.compile(_NUM + r"\s*\+\s*(?:years?|yrs?)", re.I),                                     # 2+ years
    re.compile(r"(?:minimum|min\.?|at least|atleast|over|more than)\s*(?:of\s*)?" + _NUM + _YRS, re.I),
    re.compile(_NUM + r"\s*(?:years?|yrs?)\s*(?:or more|and above|minimum|\(?min)", re.I),
    re.compile(_NUM + r"\s*(?:years?|yrs?)(?:'|’)?\s*(?:of\s+)?(?:\w+[\s-]+){0,4}?experience", re.I),
    re.compile(r"experience\s*(?:of|:)?\s*" + _NUM + _YRS, re.I),
]
_EXP_CONTEXT = re.compile(r"experien|\bexp\b|work(ing)?\b|industry|professional|hands-on|background|track record", re.I)
_NOISE = re.compile(r"founded|years? (ago|old)|history|decade|over the (past|last)|journey|anniversary|"
                    r"years? in business|age\b|warranty|contract of|for \d+ years? (running|in a row)|"
                    r"\b(19|20)\d\d\b.*(founded|since)", re.I)
_PREFERRED = re.compile(r"prefer|nice[- ]to[- ]have|good[- ]to[- ]have|bonus|desir|a plus|is a plus|plus if", re.I)
_PREF_HEADING = re.compile(r"(preferred|nice[- ]to[- ]have|good[- ]to[- ]have|bonus|desired)\s*(qualifications|skills|points|requirements|experience)?\s*:?\s*$", re.I)
_FRESHER = re.compile(r"\b(fresher|freshers|new grad|new-grad|recent graduate|graduating in 20\d\d|20\d\d (batch|graduates?|pass-?outs?)|"
                      r"0\s*(?:-|–|to)\s*\d+\s*years?|entry[- ]level|early[- ]career)\b", re.I)
_DEGREE = {
    "bachelor": re.compile(r"bachelor|b\.?tech|b\.?e\b|b\.?s\b|undergrad", re.I),
    "master": re.compile(r"master|m\.?tech|m\.?s\b|m\.?sc\b", re.I),
    "phd": re.compile(r"ph\.?d|doctora", re.I),
}


def _norm(text):
    t = text.replace("–", "-").replace("—", "-")
    return re.sub(r"\b(" + "|".join(_NUMWORDS) + r")\b(?=\s*(?:\(\d+\)\s*)?\+?\s*(?:-|to|or|years?|yrs?))",
                  lambda m: _NUMWORDS[m.group(1).lower()], t, flags=re.I)


def _sentences(text):
    # keep line structure: headings matter for "preferred" detection
    lines = [l.strip() for l in text.split("\n")]
    out, heading_pref = [], False
    for l in lines:
        if not l:
            continue
        if len(l) < 70 and _PREF_HEADING.search(l):
            heading_pref = True
            continue
        if len(l) < 70 and re.search(r"(minimum|basic|required|requirements|qualifications|what you|you have|must)", l, re.I) \
                and not re.search(r"\d", l):
            heading_pref = False
        for s in re.split(r"(?<=[.;!?])\s+|•", l):
            if s.strip():
                out.append((s.strip(), heading_pref))
    return out


def parse_experience(text, requirements=None, degree="bachelor"):
    """Return dict(min=float|None, quote=str, fresher=bool, mentions=[(min, sentence, preferred)]).

    The binding minimum is the largest minimum among required mentions (within one sentence, an
    "X or Y" alternative takes the smaller). Mentions under a "preferred / nice to have" heading or
    inline "preferred" are ignored. When the feed separates basic qualifications (amazon.jobs),
    only that block is parsed. In "Bachelor's + 3 years, or Master's + 1 year", the figure after
    the user's own degree (config: degree) binds.
    """
    src = _norm(requirements if requirements else (text or ""))
    deg_rx = _DEGREE.get(degree, _DEGREE["bachelor"])
    mentions = []
    for sent, pref_heading in _sentences(src):
        if not re.search(r"years?|yrs?", sent, re.I):
            continue
        if _NOISE.search(sent):
            continue
        # "1-3 years" and "2+ years" are experience asks on their own; weaker shapes need context
        pats = _PATTERNS if _EXP_CONTEXT.search(sent) else _PATTERNS[:2]
        mins = []
        for pat in pats:
            for m in pat.finditer(sent):
                try:
                    v = float(m.group(1))
                except (TypeError, ValueError):
                    continue
                if v <= 25:
                    mins.append((m.start(), v))
        if not mins:
            continue
        degrees_named = sum(1 for rx in _DEGREE.values() if rx.search(sent))
        own = deg_rx.search(sent)
        if own and degrees_named > 1 and len({v for _, v in mins}) > 1:
            after = [mv for mv in mins if mv[0] > own.start()] or mins
            val = min(after, key=lambda mv: mv[0])[1]
        else:
            val = min(v for _, v in mins)
        preferred = pref_heading or bool(_PREFERRED.search(sent))
        mentions.append((val, sent[:220], preferred))
    required = [m for m in mentions if not m[2]]
    fresher = bool(_FRESHER.search(_norm(text or "") + " " + _norm(requirements or "")))
    if required:
        binding = max(required, key=lambda m: m[0])
        return {"min": binding[0], "quote": binding[1], "fresher": fresher, "mentions": mentions}
    return {"min": None, "quote": "not stated" + (" (only in preferred: " + mentions[0][1][:120] + ")" if mentions else ""),
            "fresher": fresher, "mentions": mentions}
