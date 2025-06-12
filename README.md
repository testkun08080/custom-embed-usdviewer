# test-USD

```zsh
git submodule add https://github.com/PixarAnimationStudios/OpenUSD OpenUSD         
```

```zsh
uv init -p 3.11
uv add PyOpenGL PySide6
#python OpenUSD/build_scripts/build_usd.py BuildUSD
uv run OpenUSD/build_scripts/build_usd.py BuildUSD
```

export PATH=/Users/dangpee/Git/test-USD/BuildUSD/bin:$PATH

uv run --env-file=.env usdview OpenUSD/extras/usd/tutorials/convertingLayerFormats/Sphere.usda

