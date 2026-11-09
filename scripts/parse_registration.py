"""
Helper script to parse GitHub Issue or Comment registrations for Drago.
"""

import os
import re
import sys

def parse_registration():
    event_name = os.environ.get("EVENT_NAME", "")
    issue_user = os.environ.get("ISSUE_USER", "")
    comment_user = os.environ.get("COMMENT_USER", "")
    title = os.environ.get("ISSUE_TITLE", "")
    issue_body = os.environ.get("ISSUE_BODY", "")
    comment_body = os.environ.get("COMMENT_BODY", "")

    target_user = comment_user if event_name == "issue_comment" else issue_user
    relevant_text = comment_body if event_name == "issue_comment" else f"{title}\n{issue_body}"

    palettes = [
        "crimson-fury",
        "arctic-frost",
        "cyberpunk-neon",
        "toxic-emerald",
        "solar-flare",
        "obsidian-gold",
    ]
    palette = "obsidian-gold"

    # 0. Check GitHub Issue Form fields: ### GitHub Username \n <username>
    m_form_user = re.search(r"###\s*GitHub Username\s*\n+([a-zA-Z0-9_-]+)", relevant_text, re.IGNORECASE)
    if m_form_user:
        target_user = m_form_user.group(1).strip()

    m_form_pal = re.search(r"###\s*Color Palette\s*\n+([a-zA-Z0-9_-]+)", relevant_text, re.IGNORECASE)
    if m_form_pal:
        pal_cand = m_form_pal.group(1).strip().lower()
        if pal_cand in palettes:
            palette = pal_cand

    # 1. Check title format: Register <username> or Register: <username>
    m_title = re.search(r"Register(?::|\s)\s*([a-zA-Z0-9_-]+)", title, re.IGNORECASE)
    if m_title and event_name != "issue_comment" and not m_form_user:
        cand = m_title.group(1).strip()
        if cand.lower() not in palettes and cand.lower() not in ("[your", "username]"):
            target_user = cand

    # 2. Check /register command format: /register [arg1] [arg2]
    m_cmd = re.search(r"/register\s+([a-zA-Z0-9_-]+)(?:\s+([a-zA-Z0-9_-]+))?", relevant_text, re.IGNORECASE)
    if m_cmd:
        arg1 = m_cmd.group(1).strip()
        arg2 = m_cmd.group(2).strip() if m_cmd.group(2) else None
        if arg1.lower() in palettes:
            palette = arg1.lower()
        else:
            target_user = arg1
            if arg2 and arg2.lower() in palettes:
                palette = arg2.lower()

    # 3. Check palette mentions in relevant text
    for p in palettes:
        if re.search(rf"\b{re.escape(p)}\b", relevant_text, re.IGNORECASE):
            palette = p
            break

    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path and os.path.exists(os.path.dirname(os.path.abspath(output_path))):
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(f"user={target_user}\n")
            f.write(f"palette={palette}\n")

    print(f"Extracted Registration -> User: {target_user}, Palette: {palette}")
    return target_user, palette

if __name__ == "__main__":
    parse_registration()

