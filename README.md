# paraview-cube-height

ParaView 用の Python プラグインのサンプルです。読み込んだ VTK メッシュに対して、

- **スライダー**で定義したパラメタ（立方体の高さ）を変更し、
- それに応じて**メッシュを動的に変形**し、
- **ユーザ定義関数**（表面積に相当するスカラー）で**コンターカラー**を付ける

という一連の流れを、1 つのフィルタとして実装しています。

## 必要環境

- ParaView 6.x（Windows 11 / macOS / Linux 共通）
- 追加ライブラリ不要（ParaView 同梱の Python と VTK のみ使用）

## ファイル構成

- `cube_height_plugin.py` — プラグイン本体（Cube Height Filter）
- `data/sample_grid.vtk` — デモ用の六面体メッシュ（そのまま読み込めます）
- `data/make_sample.py` — 上記サンプルを再生成するスクリプト（標準ライブラリのみ）

## 使い方

1. ParaView を起動し、`File > Open` で `data/sample_grid.vtk` を開いて **Apply**。
2. `Tools > Manage Plugins/Extensions` から `cube_height_plugin.py` を読み込む。
3. パイプラインで読み込んだメッシュを選択し、`Filters > Alphabetical > Cube Height Filter` を適用。
4. Properties パネルに現れる **Height** スライダーを動かすと、Z 方向の高さが変化する。
5. ツールバーの `Color By` で **SurfaceAreaLike** を選ぶと、関数値に応じたカラーマップが表示される。

> **ヒント:** `Edit > Settings > General > Auto Apply` を有効にしておくと、スライダーの
> ドラッグでビューがライブ更新されます。

## サンプルデータの再生成

```bash
python data/make_sample.py
```

`make_sample.py` 冒頭の `NX, NY, NZ` を編集すればメッシュ解像度を変えられます。

## 設計メモ

データ変換ロジックは副作用のない純粋関数として切り出し、再代入を避けています。
ParaView / VTK のアルゴリズムモデル上どうしても必要になる「パラメタの保持」
「`Modified()` 呼び出し」「出力オブジェクトへの書き込み」だけを `RequestData` 内の
手続き的境界に閉じ込めています。`surface_area_like()` を差し替えれば、任意の
ユーザ定義関数でのカラーリングに拡張できます。

## ライセンス

MIT License（`LICENSE` を参照）。
