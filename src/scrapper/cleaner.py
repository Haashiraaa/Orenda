

from bs4 import BeautifulSoup


class Cleaner:


    @classmethod
    def clean_html(cls, raw_html: str, max_chars: int = 15000) -> str:
        
        STRIP_TAGS = ["script", "style", "noscript", "svg", "iframe", "nav",
                  "footer", "header", "aside", "form", "button"]

        # Common ad/tracking/junk class or id substrings
        STRIP_HINTS = ["cookie", "banner", "advert", "sidebar", "popup", "modal",
                   "newsletter", "social-share", "breadcrumb"]

        soup = BeautifulSoup(raw_html, "lxml")

        for tag in soup(STRIP_TAGS):
            tag.decompose()

        # Decide what to remove first, then remove it in a separate pass.
        # Decomposing a parent detaches its children (their .attrs becomes
        # None), so calling .decompose() mid-iteration over the same
        # find_all() snapshot crashes once the loop reaches an
        # already-orphaned child. Splitting decide/act avoids that.
        to_remove = []
        for el in soup.find_all(True):
            if el.attrs is None: # type: ignore[reportUnnecessaryComparison]
                continue
            attrs = " ".join([
                str(el.get("class", "")),
                str(el.get("id", "")),
            ]).lower()
            if any(hint in attrs for hint in STRIP_HINTS):
                to_remove.append(el)

        for el in to_remove:
            if el.parent is not None:  # skip if an ancestor already removed it
                el.decompose()

        # Prefer <main> or <article> if present - usually where the real content is
        main = soup.find("main") or soup.find("article")
        target = main if main else soup.body if soup.body else soup

        # Strip attributes we don't need for extraction (keep href/src for links/images)
        for el in target.find_all(True):
            keep = {}
            if el.has_attr("href"):
                keep["href"] = el["href"]
            if el.has_attr("src"):
                keep["src"] = el["src"]
            el.attrs = keep

        text = str(target)

        # Collapse whitespace
        text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        if len(text) > max_chars:
            text = text[:max_chars] + "\n<!-- truncated -->"

        return text

    
    @classmethod
    def looks_js_rendered(cls, raw_html: str) -> bool:
        """
        Cheap heuristic: SPA shells often have a near-empty body with just
        a root div and a pile of <script> tags. If we see that, we need a
        headless browser instead of requests.
        """
        soup = BeautifulSoup(raw_html, "lxml")
        body = soup.body
        if not body:
            return True
        text_len = len(body.get_text(strip=True))
        script_count = len(soup.find_all("script"))
        return text_len < 200 and script_count > 5

