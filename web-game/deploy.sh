#!/bin/bash
# Puts the browser version online on Vercel. No server code and no keys:
# every player adds their own free Gemini key in settings.
# Run from anywhere:  bash web-game/deploy.sh
# First run: signs you in to Vercel, links this folder to a Vercel project,
# deploys. Later runs: just deploy.
set -e
cd "$(dirname "$0")"

if ! npx vercel whoami >/dev/null 2>&1; then
  echo "signing in to Vercel (a browser window opens)"
  npx vercel login
fi

if [ ! -f .vercel/project.json ]; then
  echo "linking this folder to a Vercel project called pylevels"
  npx vercel link --yes --project pylevels
fi

# Fresh version numbers on the page's files, so browsers never keep an old copy.
STAMP=$(date +%s)
sed -i '' -E "s/style\.css(\?v=[0-9]+)?/style.css?v=$STAMP/; s/game\.js(\?v=[0-9]+)?/game.js?v=$STAMP/" index.html

npx vercel --prod --yes
