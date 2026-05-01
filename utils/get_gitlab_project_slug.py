import re

import unicodedata


def get_gitlab_project_slug(name: str) -> str:
    """
    Converts a project name string into a GitLab-compatible slug.
    Logic: lowercase, replace non-alphanumeric with hyphens,
    strip consecutive hyphens, and remove leading/trailing hyphens.
    """
    # Normalize Unicode characters
    name = unicodedata.normalize('NFKD', name) # NFKD = separate characters from their accents
    name = "".join([c for c in name if not unicodedata.combining(c)])

    # Convert to lowercase
    slug = name.lower()

    # Replace non-alphanumeric (including spaces) with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)

    # Remove duplicate hyphens and trim edges
    slug = re.sub(r'-+', '-', slug).strip('-')

    return slug