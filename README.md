# はじめに
USDのビルドからusdviewerのローカル起動までを行います

## 開発環境
- macOS Sequoia 15.5
- VsCode
- zsh 5.9 (arm64-apple-darwin24.0)

## 前提条件

システムに以下がインストールされていることを確認してください:

- Python 3.11
- uv pip (インストールは[こちら](https://docs.astral.sh/uv/getting-started/installation/))

## ローカルへクローン
- サブモジュールを使う場合
```zsh
git submodule add https://github.com/PixarAnimationStudios/OpenUSD OpenUSD         
```
or
- クローン
```zsh
git clone https://github.com/PixarAnimationStudios/OpenUSD.git        
```

## UVを使用してVENVの作成
```zsh
uv init -p 3.11
uv add PyOpenGL PySide6
#python OpenUSD/build_scripts/build_usd.py BuildUSD
uv run OpenUSD/build_scripts/build_usd.py BuildUSD
```

## 環境パスの設定

- PYTHONPATHの設定

  ```zsh
  cat > .env <<EOL
  PYTHONPATH=/Users/$USER/Git/test-USD/BuildUSD/lib/python
  EOL
  ```

- PATHの設定

  ```zsh
  export PATH=/Users/$USER/Git/test-USD/BuildUSD/bin:$PATH
  ```

## usdviewerの起動
```zsh
uv run --env-file=.env usdview OpenUSD/extras/usd/tutorials/convertingLayerFormats/Sphere.usda
```