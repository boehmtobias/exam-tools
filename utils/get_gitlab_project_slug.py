import re

def get_gitlab_project_slug(name: str) -> str:
    """
    Converts a project name string into a GitLab-compatible slug.
    Logic: lowercase, replace non-alphanumeric with hyphens,
    strip consecutive hyphens, and remove leading/trailing hyphens.
    """
    # Convert to lowercase and replace non-alphanumeric (including spaces) with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower())

    # Remove duplicate hyphens and trim edges
    slug = re.sub(r'-+', '-', slug).strip('-')

    return slug