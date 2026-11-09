Rebuilds `banner.gif` using [Terminal Text Effects](https://github.com/ChrisBuilds/terminaltexteffects) (`tte`).

    python -m venv venv && venv/bin/pip install terminaltexteffects pillow pyfiglet
    cd tools && ../venv/bin/python build_gif.py ../banner.gif 70
