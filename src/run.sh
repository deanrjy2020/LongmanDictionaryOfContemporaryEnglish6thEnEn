#!/usr/bin/env bash
set -e

#check py version.
REQUIRED_PY_VER=3.14
PYTHON=${PYTHON:-python}
PY_VER=$($PYTHON - <<'EOF'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
EOF
)
if [[ "$PY_VER" != "$REQUIRED_PY_VER" ]]; then
    echo "❌ Python $REQUIRED_PY_VER is required, but got $PY_VER"
    echo "👉 Try: py -$REQUIRED_PY_VER run.sh  (or activate your venv)"
    exit 1
fi
echo "✅ Python version OK: $PY_VER"

/c/Python314/python src/generate_ldoce6enen_bugfix.py 2>&1 |& tee l6_log.txt
md5sum.exe data/*