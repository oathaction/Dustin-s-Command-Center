#!/usr/bin/env python3
"""Pixel-fit check for icons, run under the name the stage B drawings brief gives it.

The check itself is icon_pixel_fit_check.js beside this file: it needs Chromium through Playwright, which this
environment has for Node only. This wrapper passes every argument through and returns the check's exit code.

    python3 -I work/build/scripts/phase-2/icon_pixel_fit_check.py --size 24 a.svg [b.svg ...]
    python3 -I work/build/scripts/phase-2/icon_pixel_fit_check.py --size 16,24 --weight 1.5,2 folder/
    python3 -I work/build/scripts/phase-2/icon_pixel_fit_check.py --self-test
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if __name__ == "__main__":
    js = os.path.join(HERE, "icon_pixel_fit_check.js")
    env = dict(os.environ)
    if "NODE_PATH" not in env and os.path.isdir("/opt/node-tools/node_modules"):
        env["NODE_PATH"] = "/opt/node-tools/node_modules"
    sys.exit(subprocess.call(["node", js] + sys.argv[1:], env=env))
