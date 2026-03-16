"""Two-pass MDX chunker: MarkdownHeaderTextSplitter → RecursiveCharacterTextSplitter."""

import re

import frontmatter
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


def _preprocess_mdx(raw: str) -> str:
    """Strip YAML frontmatter and JSX import lines."""
    post = frontmatter.loads(raw)
    lines = post.content.splitlines()
    filtered = [line for line in lines if not line.strip().startswith("import ")]
    return "\n".join(filtered)


def _slugify(text: str) -> str:
    """Convert heading text to a URL-safe slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    return slug.strip("-")


def chunk_chapter(
    raw_mdx: str,
    chapter_id: str,
    module_id: str,
    base_url: str,
    chunk_size: int = 750,
    chunk_overlap: int = 100,
) -> list[tuple[str, dict]]:
    """
    Chunk a chapter MDX file into (text, metadata) tuples.

    Returns a list of (chunk_text, metadata_dict) where metadata contains:
    chapter_id, module_id, section_id, section_heading, source_url, chunk_index, heading_level.
    """
    clean_text = _preprocess_mdx(raw_mdx)

    # Pass 1: split by markdown headers
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ]
    )
    header_docs = header_splitter.split_text(clean_text)

    # Pass 2: split each header section by token count
    token_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    results: list[tuple[str, dict]] = []
    chunk_index = 0

    for doc in header_docs:
        # Determine heading info
        heading_text = doc.metadata.get("h3") or doc.metadata.get("h2") or doc.metadata.get("h1") or chapter_id
        heading_level = 3 if doc.metadata.get("h3") else (2 if doc.metadata.get("h2") else 1)
        section_id = _slugify(heading_text)
        source_url = f"{base_url}#{section_id}"

        sub_chunks = token_splitter.split_text(doc.page_content)

        for text in sub_chunks:
            if not text.strip():
                continue
            metadata = {
                "chapter_id": chapter_id,
                "module_id": module_id,
                "section_id": section_id,
                "section_heading": heading_text,
                "source_url": source_url,
                "chunk_index": chunk_index,
                "heading_level": heading_level,
            }
            results.append((text, metadata))
            chunk_index += 1

    return results
