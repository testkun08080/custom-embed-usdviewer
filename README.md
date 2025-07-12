# 概要
USD viewerをwidgetに埋め込んで、UIと通してディスプレイの内容をコントロールできるようにしたものです。  
不必要なuiを消しているので、ビューワーとして使いたいだけの場合などに有効かと思います。  
以下のサンプルを参考にして、作成しています（ここで感謝申し上げます！）  
https://gist.github.com/BigRoy/5ac50208969fdc69a722d66874faf8a2#file-usdviewport_qt-py  

USDのビルドからusdviewerのローカル起動までを行います。
詳しいドキュメントは以下公式のgithub ページをご覧ください。  
https://github.com/PixarAnimationStudios/OpenUSD

![サンプルGIF](/docs/sample.gif)

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
uv add PyOpenGL PySide6 numpy
uv run OpenUSD/build_scripts/build_usd.py BuildUSD
```

## 環境パスの設定

- PYTHONPATHの設定

  ```zsh
  cat > .env <<EOL
  PYTHONPATH=./BuildUSD/lib/python
  EOL
  ```

- PATHの設定

  ```zsh
  export PATH=./BuildUSD/bin:$PATH
  ```

## usdviewerの起動

- uvでusdviewを直接起動
  ```zsh
  uv run --env-file=.env usdview OpenUSD/extras/usd/tutorials/convertingLayerFormats/Sphere.usda
  ```
- pythonファイル経由で起動
  ```zsh
  uv run --env-file=.env open_usd_viewer.py
  ```
- Shell scriptでの起動
  ```zsh
  source ./run_usd_viewer.sh 
  ```


## Embed USD Viewerの起動

- uvでapp.pyの起動
  ```zsh
  uv run --env-file=.env app.py
  ```

## 📒参考
https://gist.github.com/BigRoy/5ac50208969fdc69a722d66874faf8a2#file-usdviewport_qt-py


## 💬 補足
- 利用に関して問題があれば[Issue](https://github.com/testkun08080/kanpo-rss/issues)からご連絡ください。

---

## 📄 ライセンス

MIT License © [testkun08080](https://github.com/testkun08080)

## 😀 貢献
バグ報告や機能リクエスト、プルリクエストは大歓迎です。問題や提案がある場合は、GitHubのIssueを作成してください。
その他に、いいなと思ったらスターもらえるとシンプルに喜びます。もしくはコーヒー奢ってもらえるとより喜びます。
