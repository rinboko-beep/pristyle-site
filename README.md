# Pristyle site

Live: https://pristyle-il.netlify.app (Netlify project `pristyle-il`, Rin's account, deployed from a zip, not linked to Git).

Update:
1. Edit `CONFIG` / content in `build.py` or the layout in `template.html`.
2. `python3 build.py` -> `public/`.
3. `cd public && zip -qr ../deploy/site.zip . && cd ..`, commit and push to `main`.
4. In the built-in browser open https://app.netlify.com/projects/pristyle-il/deploys and run in the page:
   fetch the zip from `https://raw.githubusercontent.com/rinboko-beep/pristyle-site/main/deploy/site.zip`,
   wrap it in a `File`, put it on the zip `input[type=file]` with a `DataTransfer`, dispatch `change`.
