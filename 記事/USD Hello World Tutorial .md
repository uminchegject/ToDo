# USD Tuotorial --Hello World--

Pixarが開発したフォーマットである[USD(Universal Scene Description)](https://openusd.org/release/index.html)の[公式Tutorial](https://openusd.org/release/tut_usd_tutorials.html)の最初の項目である[Hello World](https://openusd.org/release/tut_helloworld.html)と以下のサンプルUSDをもとに、USDにおける重要な要素であるStageとPrimについて解説するとともに、Pythonによる実装手順についても説明します。
```
#usda 1.0

def Xform "hello"
{
    def Sphere "world"
    {
    }
}
```

## Stage
Stageは、USDシーン全体を管理するルートオブジェクトです。
複数のレイヤーや参照関係を解決した結果としての「最終的なシーン」を表します。
このTutorialではhelloというノードの中に、worldという球体があるシーンということになります。
```
Stage（シーン全体）
 └── /hello
      └── /hello/world
```

## Prim
Primは、型情報を持つシーン内のオブジェクトであり、階層構造の中で管理される基本単位です。
このサンプルコードでは、2つのPrimが定義されています。

1つ目は def Xform "hello" で定義されるPrimで型はXformです。Xformはトランスフォーム情報（位置・回転・スケール）を持つPrimであり、他のPrimをまとめるグループとしての役割も持ちます。

2つ目は def Sphere "world" で定義されるPrimで型はSphereです。こちらは球体ジオメトリを表すPrimであり、実際に描画されるオブジェクトです。
このSphereはXformである「hello」の子として配置されることで、親の変換の影響を受けながらシーン内に配置されます。

このようにUSDでは多様なPrimを用いて階層的にシーンを構築しています。

## Pythonでの構築処理
以上を踏まえて、実際にサンプルUSDを構築する手順を、以下のPythonコードをもとに解説します。
```
from pxr import Usd, UsdGeom
stage = Usd.Stage.CreateNew('HelloWorld.usda')
xformPrim = UsdGeom.Xform.Define(stage, '/hello')
spherePrim = UsdGeom.Sphere.Define(stage, '/hello/world')
stage.GetRootLayer().Save()
```

### Stage
まず、Usd.Stage.CreateNew() を使って、ファイルと紐づいたStageを作成します。
```
stage = Usd.Stage.CreateNew("HelloWorld.usda")
```
この1行で「HelloWorld.usda」というUSDファイルに対応するStageが生成され、以降のすべての処理はこのstageを通して行います。

### Prim
次に、2つのPrimを定義します。
Primの作成はStageを通して行い、型（Xform / Sphere）とパスを指定します。
```
UsdGeom.Xform.Define(stage, "/hello")
UsdGeom.Sphere.Define(stage, "/hello/world")
```
のようにパスを指定することで、階層構造（親子関係）も同時に定義されます。
ここでは「/hello」が親となり、「/hello/world」がその子として自動的に配置されます。

### RootLayer
最後に、stage.GetRootLayer() でRootLayerを取得し、Save() を呼び出して内容をファイルに保存します。
```
rootLayer = stage.GetRootLayer()
rootLayer.Save()
```
RootLayerは、Stageが参照する最上位のレイヤーであり、
シーンに対する編集内容はこのRootLayerに書き込まれ、Save() を実行することでファイルとして出力されます。