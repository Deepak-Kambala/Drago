"""
Deploys generated dragon assets to an independent 'gh-pages' orphan branch.
Uses a single squashed commit with git push --force so git history never bloats,
guaranteeing 0 MB historical binary overhead regardless of how many users join.
"""

import os
import shutil
import tempfile
import subprocess
import sys

def deploy_assets(assets_dir: str = "assets"):
    if not os.path.exists(assets_dir):
        print(f"[Drago Deploy] Error: {assets_dir} does not exist.")
        return False

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY", "Deepak-Kambala/Drago")

    # If running locally via gh auth token
    if not token:
        try:
            token = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
        except Exception:
            pass

    if not token:
        print("[Drago Deploy] Error: GITHUB_TOKEN or gh auth token required to push to gh-pages.")
        return False

    temp_dir = tempfile.mkdtemp(prefix="drago_gh_pages_")
    try:
        # Copy all assets to temp_dir
        for item in os.listdir(assets_dir):
            src = os.path.join(assets_dir, item)
            dst = os.path.join(temp_dir, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        # Also create a duplicate copy inside 'assets/' folder within gh-pages
        # so both https://.../users/... AND https://.../assets/users/... resolve cleanly
        assets_subdir = os.path.join(temp_dir, "assets")
        os.makedirs(assets_subdir, exist_ok=True)
        for item in os.listdir(assets_dir):
            src = os.path.join(assets_dir, item)
            dst = os.path.join(assets_subdir, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)

        # Disable Jekyll processing on GitHub Pages
        with open(os.path.join(temp_dir, ".nojekyll"), "w") as f:
            f.write("")

        # Create landing index.html redirecting to main repo
        with open(os.path.join(temp_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Drago - Animated GitHub Profile Dragons</title>
  <meta http-equiv="refresh" content="0; url=https://github.com/{repo}">
</head>
<body>
  <p>Redirecting to <a href="https://github.com/{repo}">Drago on GitHub</a>...</p>
</body>
</html>
""")

        # Initialize single-commit orphan repo
        subprocess.run(["git", "init", "-b", "gh-pages"], cwd=temp_dir, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=temp_dir, check=True)
        subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], cwd=temp_dir, check=True)
        subprocess.run(["git", "add", "-A"], cwd=temp_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Drago: Deploy latest squashed dragon assets [skip ci]"], cwd=temp_dir, check=True)

        remote_url = f"https://x-access-token:{token}@github.com/{repo}.git"
        subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=temp_dir, check=True)
        
        print(f"[Drago Deploy] Force-pushing squashed single commit to {repo}:gh-pages...")
        subprocess.run(["git", "push", "--force", "origin", "gh-pages"], cwd=temp_dir, check=True)
        print("[Drago Deploy] Successfully deployed to gh-pages with 0 MB historical bloat!")
        return True
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    success = deploy_assets()
    sys.exit(0 if success else 1)
