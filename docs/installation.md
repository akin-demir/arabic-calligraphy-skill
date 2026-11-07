# Installation

Supported and locally tested: Linux x86-64, Python 3.12.14, Pango 1.56.3, Cairo 1.18.4, HarfBuzz 10.2.0 and bundled Debian Noto fonts 20201225-2. Python 3.11+ is the package target; remote CI verifies additional runtimes. macOS and Windows are not tested.

On Debian/Ubuntu, install native libraries with your system package manager:

```bash
sudo apt-get update
sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0 libcairo2 libfontconfig1 libharfbuzz0b
python -m venv .venv
. .venv/bin/activate
python -m pip install .
arabic-calligraphy --version
```

For development use `python -m pip install '.[dev]'`. Native libraries and Python dependencies must be installed before running the renderer. The four bundled fonts register privately inside this process; no system font installation or network request is performed during rendering. If a bundled file is absent or modified, reinstall rather than silently falling back.

Use the development branch until merged. The package has not been published to PyPI; do not assume a same-name package on an index is this project. Build a wheel with `python -m build` after installing development tooling. `requirements-dev.txt` pins the local Python verification toolchain. Native system libraries remain platform-managed; CI records their versions rather than claiming bit-identical output on all systems.

The root SKILL.md, references, scripts and Python sources travel together when installed as a skill. Run `python -m pip install /path/to/arabic-calligraphy-skill` from that skill directory. A Python wheel installs the renderer and font data, but does not itself install an agent skill.
