#!/usr/bin/env python3
from __future__ import annotations

import html
import posixpath
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
REPO_URL = "https://github.com/anhtnt90dev/ai-solution-architecture"


@dataclass(frozen=True)
class Page:
    source_rel: str
    output_rel: str
    section: str
    markdown: str | None = None
    virtual: bool = False


def norm(path: str) -> str:
    return posixpath.normpath(path.replace("\\", "/")).lstrip("./")


def repo_rel(path: Path) -> str:
    return norm(path.relative_to(ROOT).as_posix())


def title_from_markdown(markdown: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", markdown, flags=re.MULTILINE)
    if not match:
        return fallback
    title = re.sub(r"`([^`]+)`", r"\1", match.group(1))
    return re.sub(r"\s+", " ", title).strip()


def output_for_source(source_rel: str) -> str:
    source_rel = norm(source_rel)

    exact = {
        "learn-ai-solution-architecture/README.md": "site/learn/index.html",
        "learn-ai-solution-architecture/docs/en/README.md": "site/learn/en/index.html",
        "learn-ai-solution-architecture/docs/en/curriculum.md": "site/learn/en/curriculum.html",
        "learn-ai-solution-architecture/docs/en/projects.md": "site/learn/en/projects.html",
        "learn-ai-solution-architecture/docs/en/reference-atlas.md": "site/learn/en/reference-atlas.html",
        "learn-ai-solution-architecture/docs/en/glossary.md": "site/learn/en/glossary.html",
        "learn-ai-solution-architecture/docs/vi/README.md": "site/learn/vi/index.html",
        "learn-ai-solution-architecture/docs/vi/curriculum.md": "site/learn/vi/curriculum.html",
        "learn-ai-solution-architecture/docs/vi/projects.md": "site/learn/vi/projects.html",
        "learn-ai-solution-architecture/docs/vi/reference-atlas.md": "site/learn/vi/reference-atlas.html",
        "learn-ai-solution-architecture/docs/vi/glossary.md": "site/learn/vi/glossary.html",
        "templates/README.md": "site/templates/index.html",
        "templates/architecture-decision-record.md": "site/templates/architecture-decision-record.html",
        "templates/runtime-decision-matrix.md": "site/templates/runtime-decision-matrix.html",
        "templates/rag-data-contract.md": "site/templates/rag-data-contract.html",
        "templates/llmops-evaluation-scorecard.md": "site/templates/llmops-evaluation-scorecard.html",
        "templates/production-readiness-checklist.md": "site/templates/production-readiness-checklist.html",
        "templates/security-governance-review.md": "site/templates/security-governance-review.html",
        "capstone/README.md": "site/capstone/index.html",
        "assessments/README.md": "site/assessments/index.html",
        "assessments/en/architecture-review-exam.md": "site/assessments/en/architecture-review-exam.html",
        "assessments/en/answer-key.md": "site/assessments/en/answer-key.html",
        "assessments/vi/bai-kiem-tra-kien-truc.md": "site/assessments/vi/bai-kiem-tra-kien-truc.html",
        "assessments/vi/dap-an.md": "site/assessments/vi/dap-an.html",
        "repo-architecture-docs/README.md": "site/deep-dives/index.html",
        "repo-architecture-docs/DOCUMENTATION_STANDARD.md": "site/deep-dives/documentation-standard.html",
    }
    if source_rel in exact:
        return exact[source_rel]

    deep_dive = re.match(
        r"repo-architecture-docs/([^/]+)/([^/]+)/README\.(en|vi)\.md$",
        source_rel,
    )
    if deep_dive:
        group, repo, language = deep_dive.groups()
        return f"site/deep-dives/{group}/{repo}/{language}.html"

    raise ValueError(f"No output mapping for {source_rel}")


def collect_pages() -> list[Page]:
    fixed_sources = [
        "learn-ai-solution-architecture/README.md",
        "learn-ai-solution-architecture/docs/en/README.md",
        "learn-ai-solution-architecture/docs/en/curriculum.md",
        "learn-ai-solution-architecture/docs/en/projects.md",
        "learn-ai-solution-architecture/docs/en/reference-atlas.md",
        "learn-ai-solution-architecture/docs/en/glossary.md",
        "learn-ai-solution-architecture/docs/vi/README.md",
        "learn-ai-solution-architecture/docs/vi/curriculum.md",
        "learn-ai-solution-architecture/docs/vi/projects.md",
        "learn-ai-solution-architecture/docs/vi/reference-atlas.md",
        "learn-ai-solution-architecture/docs/vi/glossary.md",
        "templates/README.md",
        "templates/architecture-decision-record.md",
        "templates/runtime-decision-matrix.md",
        "templates/rag-data-contract.md",
        "templates/llmops-evaluation-scorecard.md",
        "templates/production-readiness-checklist.md",
        "templates/security-governance-review.md",
        "capstone/README.md",
        "assessments/README.md",
        "assessments/en/architecture-review-exam.md",
        "assessments/en/answer-key.md",
        "assessments/vi/bai-kiem-tra-kien-truc.md",
        "assessments/vi/dap-an.md",
        "repo-architecture-docs/README.md",
        "repo-architecture-docs/DOCUMENTATION_STANDARD.md",
    ]

    pages: list[Page] = []
    for source in fixed_sources:
        section = "Deep Dives" if source.startswith("repo-architecture-docs/") else "Docs"
        pages.append(Page(source, output_for_source(source), section))

    for path in sorted((ROOT / "repo-architecture-docs").glob("*/*/README.*.md")):
        source = repo_rel(path)
        pages.append(Page(source, output_for_source(source), "Deep Dives"))

    group_dirs = sorted(
        path
        for path in (ROOT / "repo-architecture-docs").iterdir()
        if path.is_dir() and re.match(r"^\d\d-", path.name)
    )
    for group_dir in group_dirs:
        group_rel = repo_rel(group_dir)
        repos = sorted(path for path in group_dir.iterdir() if path.is_dir())
        group_title = group_dir.name.replace("-", " ").title()
        lines = [
            f"# {group_title}",
            "",
            "Repository deep dives in this architecture domain.",
            "",
            "| Repository | English | Vietnamese |",
            "| --- | --- | --- |",
        ]
        for repo_dir in repos:
            repo_name = repo_dir.name
            lines.append(
                f"| {repo_name} | [English]({repo_name}/README.en.md) | "
                f"[Vietnamese]({repo_name}/README.vi.md) |"
            )
        lines.extend(
            [
                "",
                "## Back To Index",
                "",
                "- [All repository deep dives](../README.md)",
                "- [English course](../../learn-ai-solution-architecture/docs/en/README.md)",
                "- [Vietnamese course](../../learn-ai-solution-architecture/docs/vi/README.md)",
            ]
        )
        source_rel = f"{group_rel}/README.md"
        pages.append(
            Page(
                source_rel=source_rel,
                output_rel=f"site/deep-dives/{group_dir.name}/index.html",
                section="Deep Dives",
                markdown="\n".join(lines),
                virtual=True,
            )
        )

    return pages


PAGES = collect_pages()
LINK_MAP: dict[str, str] = {}

for page in PAGES:
    source = norm(page.source_rel)
    output = norm(page.output_rel)
    LINK_MAP[source] = output
    if source.endswith("/README.md"):
        directory = source[: -len("/README.md")]
        LINK_MAP[directory] = output
        LINK_MAP[directory + "/"] = output


def rel_href(from_output_rel: str, to_repo_rel: str) -> str:
    current_dir = posixpath.dirname(norm(from_output_rel))
    return posixpath.relpath(norm(to_repo_rel), current_dir)


def map_url(url: str, current_source_rel: str, current_output_rel: str) -> str:
    if not url:
        return url
    if re.match(r"^(https?:|mailto:|tel:)", url) or url.startswith("#"):
        return url

    path_part, anchor = (url.split("#", 1) + [""])[:2] if "#" in url else (url, "")
    query = ""
    if "?" in path_part:
        path_part, query = path_part.split("?", 1)

    if not path_part:
        return f"#{anchor}" if anchor else url

    source_dir = posixpath.dirname(norm(current_source_rel))
    target = norm(posixpath.join(source_dir, path_part))

    candidates = [target]
    if target.endswith("/"):
        candidates.append(target[:-1])
    if not posixpath.basename(target).startswith("README"):
        candidates.append(f"{target}/README.md")

    mapped = None
    for candidate in candidates:
        if candidate in LINK_MAP:
            mapped = LINK_MAP[candidate]
            break

    if mapped:
        href = rel_href(current_output_rel, mapped)
    else:
        href = rel_href(current_output_rel, target)

    if query:
        href += f"?{query}"
    if anchor:
        href += f"#{anchor}"
    return href


def render_inline(text: str, current_source_rel: str, current_output_rel: str) -> str:
    code_spans: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        code_spans.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"@@CODE{len(code_spans) - 1}@@"

    escaped = re.sub(r"`([^`]+)`", stash_code, text)
    escaped = html.escape(escaped)

    def image_repl(match: re.Match[str]) -> str:
        alt = match.group(1)
        url = html.unescape(match.group(2))
        href = map_url(url, current_source_rel, current_output_rel)
        return f'<img src="{html.escape(href, quote=True)}" alt="{alt}">'

    def link_repl(match: re.Match[str]) -> str:
        label = match.group(1)
        url = html.unescape(match.group(2))
        href = map_url(url, current_source_rel, current_output_rel)
        return f'<a href="{html.escape(href, quote=True)}">{label}</a>'

    escaped = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image_repl, escaped)
    escaped = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", link_repl, escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", escaped)

    for index, code in enumerate(code_spans):
        escaped = escaped.replace(f"@@CODE{index}@@", code)
    return escaped


def slugify(text: str, counts: dict[str, int]) -> str:
    base = re.sub(r"`([^`]+)`", r"\1", text).lower()
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    if not base:
        base = "section"
    count = counts.get(base, 0)
    counts[base] = count + 1
    return base if count == 0 else f"{base}-{count + 1}"


def split_table_row(row: str) -> list[str]:
    row = row.strip().strip("|")
    return [cell.strip() for cell in row.split("|")]


def is_table_separator(row: str) -> bool:
    row = row.strip()
    return bool(re.match(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$", row))


def render_markdown(markdown: str, current_source_rel: str, current_output_rel: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None
    heading_counts: dict[str, int] = {}
    i = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(item.strip() for item in paragraph).strip()
            out.append(f"<p>{render_inline(text, current_source_rel, current_output_rel)}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    def close_blocks() -> None:
        flush_paragraph()
        close_list()

    while i < len(lines):
        raw = lines[i].rstrip()
        stripped = raw.strip()

        if not stripped:
            close_blocks()
            i += 1
            continue

        fence = re.match(r"^```([A-Za-z0-9_-]*)\s*$", stripped)
        if fence:
            close_blocks()
            language = fence.group(1)
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i].rstrip("\n"))
                i += 1
            if i < len(lines):
                i += 1
            code = "\n".join(code_lines)
            if language == "mermaid":
                out.append(f'<div class="mermaid">{html.escape(code)}</div>')
            else:
                class_name = f' class="language-{html.escape(language, quote=True)}"' if language else ""
                out.append(f"<pre><code{class_name}>{html.escape(code)}</code></pre>")
            continue

        if (
            stripped.startswith("|")
            and i + 1 < len(lines)
            and is_table_separator(lines[i + 1])
        ):
            close_blocks()
            headers = split_table_row(stripped)
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_table_row(lines[i]))
                i += 1
            out.append("<div class=\"table-scroll\"><table>")
            out.append(
                "<thead><tr>"
                + "".join(
                    f"<th>{render_inline(cell, current_source_rel, current_output_rel)}</th>"
                    for cell in headers
                )
                + "</tr></thead>"
            )
            out.append("<tbody>")
            for row in rows:
                out.append(
                    "<tr>"
                    + "".join(
                        f"<td>{render_inline(cell, current_source_rel, current_output_rel)}</td>"
                        for cell in row
                    )
                    + "</tr>"
                )
            out.append("</tbody></table></div>")
            continue

        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", stripped)
        if heading:
            close_blocks()
            level = len(heading.group(1))
            text = heading.group(2)
            slug = slugify(text, heading_counts)
            out.append(
                f'<h{level} id="{slug}">{render_inline(text, current_source_rel, current_output_rel)}</h{level}>'
            )
            i += 1
            continue

        if re.match(r"^-{3,}$", stripped):
            close_blocks()
            out.append("<hr>")
            i += 1
            continue

        quote = re.match(r"^>\s*(.+)$", raw)
        if quote:
            close_blocks()
            quote_lines = [quote.group(1)]
            i += 1
            while i < len(lines):
                next_quote = re.match(r"^>\s*(.+)$", lines[i].rstrip())
                if not next_quote:
                    break
                quote_lines.append(next_quote.group(1))
                i += 1
            quote_text = " ".join(quote_lines)
            out.append(
                f"<blockquote><p>{render_inline(quote_text, current_source_rel, current_output_rel)}</p></blockquote>"
            )
            continue

        unordered = re.match(r"^\s*[-*+]\s+(.+)$", raw)
        ordered = re.match(r"^\s*\d+[.)]\s+(.+)$", raw)
        if unordered or ordered:
            flush_paragraph()
            target_list = "ul" if unordered else "ol"
            if list_type != target_list:
                close_list()
                out.append(f"<{target_list}>")
                list_type = target_list
            item = (unordered or ordered).group(1)
            item = re.sub(
                r"^\[( |x|X)\]\s+",
                lambda match: (
                    '<input type="checkbox" disabled> '
                    if match.group(1) == " "
                    else '<input type="checkbox" checked disabled> '
                ),
                item,
            )
            out.append(f"<li>{render_inline(item, current_source_rel, current_output_rel)}</li>")
            i += 1
            continue

        close_list()
        paragraph.append(raw)
        i += 1

    close_blocks()
    return "\n".join(out)


CSS = """
:root {
  --ink: #172033;
  --muted: #566179;
  --line: #d9e0ea;
  --paper: #ffffff;
  --soft: #f5f7fb;
  --blue: #0a66c2;
  --green: #047857;
  --red: #c1121f;
  --amber: #b45309;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  color: var(--ink);
  background: var(--paper);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.65;
}

a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }

.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 1px solid var(--line);
  background: rgba(251, 252, 255, 0.96);
  backdrop-filter: blur(8px);
}

.topbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  width: min(1180px, calc(100% - 32px));
  min-height: 66px;
  margin: 0 auto;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: var(--ink);
  font-weight: 800;
}

.mark {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  color: #fff;
  background: var(--blue);
  border-radius: 8px;
  font-weight: 900;
}

.navlinks {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 14px;
  font-size: 14px;
  font-weight: 650;
}

.layout {
  display: grid;
  grid-template-columns: 250px minmax(0, 1fr);
  gap: 34px;
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
  padding: 34px 0 58px;
}

.sidebar {
  position: sticky;
  top: 92px;
  align-self: start;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--soft);
}

.sidebar strong {
  display: block;
  margin-bottom: 10px;
}

.sidebar a {
  display: block;
  padding: 6px 0;
  color: var(--ink);
  font-size: 14px;
}

.doc {
  min-width: 0;
  padding-bottom: 32px;
}

.crumb {
  margin: 0 0 12px;
  color: var(--green);
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
}

.source-link {
  display: inline-flex;
  margin: 0 0 20px;
  padding: 7px 10px;
  border: 1px solid var(--line);
  border-radius: 8px;
  color: var(--ink);
  background: #fff;
  font-size: 13px;
  font-weight: 700;
}

h1, h2, h3, h4, h5, h6 {
  line-height: 1.2;
  letter-spacing: 0;
}

h1 {
  margin: 0 0 14px;
  font-size: clamp(34px, 6vw, 56px);
}

h2 {
  margin-top: 34px;
  padding-top: 20px;
  border-top: 1px solid var(--line);
  font-size: 28px;
}

h3 { margin-top: 26px; font-size: 22px; }
p { max-width: 880px; }

img {
  max-width: 100%;
  height: auto;
}

pre, .mermaid {
  max-width: 100%;
  overflow-x: auto;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fbfcff;
}

code {
  padding: 2px 5px;
  border-radius: 5px;
  background: #eef2f7;
  font-family: "Cascadia Mono", Consolas, "Liberation Mono", monospace;
  font-size: 0.92em;
}

pre code {
  padding: 0;
  background: transparent;
}

blockquote {
  margin: 20px 0;
  padding: 12px 18px;
  border-left: 4px solid var(--blue);
  background: var(--soft);
}

.table-scroll { overflow-x: auto; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 18px 0;
  font-size: 15px;
}

th, td {
  padding: 10px 12px;
  border: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
}

th {
  background: var(--soft);
}

hr {
  border: 0;
  border-top: 1px solid var(--line);
  margin: 28px 0;
}

footer {
  border-top: 1px solid var(--line);
  background: var(--soft);
}

.footer-inner {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
  padding: 22px 0;
  color: var(--muted);
  font-size: 14px;
}

@media (max-width: 860px) {
  .topbar-inner {
    align-items: flex-start;
    flex-direction: column;
    padding: 14px 0;
  }

  .navlinks {
    justify-content: flex-start;
  }

  .layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
  }
}
""".strip()


def nav_href(current_output_rel: str, target_repo_rel: str) -> str:
    return rel_href(current_output_rel, target_repo_rel)


def render_page(page: Page) -> str:
    if page.markdown is None:
        markdown = (ROOT / page.source_rel).read_text(encoding="utf-8")
    else:
        markdown = page.markdown

    title = title_from_markdown(markdown, page.section)
    body = render_markdown(markdown, page.source_rel, page.output_rel)
    css_href = rel_href(page.output_rel, "site/assets/site.css")
    lang = "vi" if "/vi/" in page.source_rel or page.source_rel.endswith(".vi.md") else "en"
    source_url = (
        f"{REPO_URL}/tree/main/{page.source_rel[:-len('/README.md')]}"
        if page.virtual
        else f"{REPO_URL}/blob/main/{page.source_rel}"
    )

    links = {
        "home": nav_href(page.output_rel, "index.html"),
        "en": nav_href(page.output_rel, "site/learn/en/index.html"),
        "vi": nav_href(page.output_rel, "site/learn/vi/index.html"),
        "curriculum": nav_href(page.output_rel, "site/learn/en/curriculum.html"),
        "projects": nav_href(page.output_rel, "site/learn/en/projects.html"),
        "toolkit": nav_href(page.output_rel, "site/templates/index.html"),
        "capstone": nav_href(page.output_rel, "site/capstone/index.html"),
        "assessments": nav_href(page.output_rel, "site/assessments/index.html"),
        "deep": nav_href(page.output_rel, "site/deep-dives/index.html"),
    }

    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | AI Solution Architecture</title>
  <meta name="description" content="AI solution architecture documentation page.">
  <link rel="stylesheet" href="{css_href}">
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="{links["home"]}">
        <span class="mark">AI</span>
        <span>Solution Architecture</span>
      </a>
      <nav class="navlinks" aria-label="Documentation navigation">
        <a href="{links["en"]}">English</a>
        <a href="{links["vi"]}">Tiếng Việt</a>
        <a href="{links["curriculum"]}">Curriculum</a>
        <a href="{links["toolkit"]}">Toolkit</a>
        <a href="{links["deep"]}">Deep Dives</a>
        <a href="{REPO_URL}">GitHub</a>
      </nav>
    </div>
  </header>
  <main class="layout">
    <aside class="sidebar">
      <strong>Documentation</strong>
      <a href="{links["en"]}">English course</a>
      <a href="{links["vi"]}">Trang tiếng Việt</a>
      <a href="{links["curriculum"]}">Curriculum</a>
      <a href="{links["projects"]}">Projects</a>
      <a href="{links["toolkit"]}">Architecture toolkit</a>
      <a href="{links["capstone"]}">Capstone</a>
      <a href="{links["assessments"]}">Assessments</a>
      <a href="{links["deep"]}">Repository deep dives</a>
    </aside>
    <article class="doc">
      <p class="crumb">{html.escape(page.section)}</p>
      <a class="source-link" href="{html.escape(source_url, quote=True)}">View source</a>
      {body}
    </article>
  </main>
  <footer>
    <div class="footer-inner">
      AI Solution Architecture Knowledge System. Published from <a href="{REPO_URL}">anhtnt90dev/ai-solution-architecture</a>.
    </div>
  </footer>
  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
    mermaid.initialize({{ startOnLoad: true, theme: "base" }});
  </script>
</body>
</html>
"""


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)

    (SITE / "assets").mkdir(parents=True, exist_ok=True)
    (SITE / "assets" / "site.css").write_text(CSS + "\n", encoding="utf-8", newline="\n")

    for page in PAGES:
        target = ROOT / page.output_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_page(page), encoding="utf-8", newline="\n")

    print(f"Generated {len(PAGES)} documentation pages under {repo_rel(SITE)}")


if __name__ == "__main__":
    main()
