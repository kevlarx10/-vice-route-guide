# VICE ROUTE — Installable GTA VI guide (Android / PS5 companion)

**What this package does:** preserves the original spoiler-light checklist, savings tracker, purchases, journal, and backup/restore; adds an **Updates** tab. When published as a GitHub Pages site, its scheduled GitHub Action fetches GTA VI links from Rockstar news search, PowerPyx, VGC, and PC Gamer approximately every six hours, and republishes the app with a fresh `updates.json` file. A manual Refresh button loads current published links. Guide titles are hidden by default to reduce accidental spoilers.

**Not included:** automatic edits to mission-by-mission checklist advice, background push notifications, PS5 account integration, or cross-device cloud syncing. New links are not a substitute for checking their accuracy. Publication schedules are best-effort and may be delayed by GitHub or RSS publishers.

## Publish for free (requires your own GitHub account)

1. Create a **public repository** at https://github.com/new (e.g. `vice-route-guide`). Do not initialize it with a README if using drag-and-drop file upload.
2. Extract the ZIP on your computer. Upload the **contents** of this folder preserving paths, including `site/`, `scripts/` and `.github/workflows/publish.yml`, to the new repository. GitHub's website upload does not automatically unpack ZIP files; upload the extracted files. A Git client is easiest for nested directories, though web upload may work when dragging the entire folder contents.
3. In your repository, open **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. Go to **Actions → Refresh GTA VI guide links and publish app → Run workflow** (or push a new commit). Wait for the green deployment check, then open the URL listed under **Settings → Pages**.
5. On your **Android phone**, open that HTTPS link in **Chrome** → three-dot menu → **Add to Home screen** → **Install app**. Your VICE ROUTE icon appears on your home screen.
6. In the old downloaded HTML guide, tap **More → Export my progress**. In the hosted version, tap **More → Restore a backup** and choose your JSON file. Progress in different web origins does NOT transfer automatically.

## How updates work

- News/source links refresh server-side roughly four times daily via the GitHub Actions schedule when the repository is active; GitHub can delay or disable scheduled jobs on inactive repositories.
- Open the installed app and tap **Updates → Refresh** to load the latest deployment. A reliable network connection is required.
- Source headlines from walkthrough sites remain hidden until you choose to reveal them; official titles are visible.
- Checkmarks and financial notes are saved *on that phone/browser*. Use Export periodically as a backup. A browser reset or uninstall can erase local progress.
- The app itself caches the interface for offline use; news needs internet. You do not need a Play Store account.
- This is an independent fan guide; not affiliated with Rockstar Games.

## Optional future upgrade

For actual **reviewed changes to the checklists** (not just auto-published links), someone needs to update the curated `STAGES`, `PURCHASES` and related arrays in `site/index.html`, test, and republish. That can be a separate editorial workflow or a moderator-reviewed contribution process. Automatically treating all internet articles as fact would risk misleading players and introducing spoilers.
