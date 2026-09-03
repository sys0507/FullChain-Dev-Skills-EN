#!/usr/bin/env bash
# Open the user-journey view in one step: start a local server and open the browser with data loaded.
# Usage:
#   bash view.sh            # View the demo by default
#   bash view.sh alpha      # View journeys derived from AlphaProject
#   bash view.sh out/any-path-inventory.json   # View a specific inventory
#   bash view.sh demo 8900  # Choose a port (default: 8731)
DIR="$(cd "$(dirname "$0")" && pwd)"; cd "$DIR"
SRC="${1:-demo}"; PORT="${2:-8731}"
case "$SRC" in
  demo)  REL="out/demo-path-inventory.json" ;;
  alpha) REL="out/alpha-path-inventory.json" ;;
  *)     REL="$SRC" ;;
esac
if [ ! -f "$REL" ]; then echo "Data file not found: $DIR/$REL"; echo "Run run_pipeline.sh first to generate out/*.json"; exit 1; fi
# Start a background server when the port is unused; otherwise reuse the existing server.
if ! curl -s "http://localhost:$PORT/" >/dev/null 2>&1; then
  ( python3 -m http.server "$PORT" >/tmp/jv_server_$PORT.log 2>&1 & )
fi
URL="http://localhost:$PORT/knife6_viewer.html?src=$REL"
echo "→ Opening: $URL"
open "$URL" 2>/dev/null || xdg-open "$URL" 2>/dev/null || echo "Open the URL above manually in a browser"
