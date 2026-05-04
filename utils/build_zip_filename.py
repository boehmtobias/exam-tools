import datetime


def build_zip_filename(ns_name: str) -> str:
    """Build filename in YYYYMMDD_HHMM_namespace format."""
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d_%H%M")
    safe_name = ns_name.replace("/", "_").replace(" ", "_")
    return f"{date_str}_{safe_name}.zip"
