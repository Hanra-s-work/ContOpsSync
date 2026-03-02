#!/bin/bash
FILE_PATH="./tools.sh"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR/files"
chmod +x "$FILE_PATH"
exec "$FILE_PATH" "$@"
