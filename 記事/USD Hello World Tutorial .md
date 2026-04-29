# USD Tuotorial --Hello World--

Pixarが開発したフォーマットである[USD(Universal Scene Description)](https://openusd.org/release/index.html)の[公式Tutorial](https://openusd.org/release/tut_usd_tutorials.html)をもとに、USDの構造を解説します。まずは、チュートリアルの最初の項目である[Hello World](https://openusd.org/release/tut_helloworld.html)について説明します。

## サンプルUSD

ここではチュートリアルで紹介されている下記サンプルコードをもとに、Stage・Primの2つの要素を解説します。

```
#usda 1.0

def Xform "hello"
{
    def Sphere "world"
    {
    }
}
```

### Stage

StageはUSDシーン全体を管理するルートオブジェクトです。

複数のレイヤーや参照関係を解決した結果としての「最終的なシーン」を表します。

このTutorialではhelloというノードの中に、worldという球体があるシーンということになります。

```
Stage（シーン全体）
 └── /hello
      └── /hello/world
```

### Prim

USDではシーン内のオブジェクトはPrimという単位で表現されます。Primはオブジェクトの型として機能し、階層構造の中でシーンを構成する要素となります。

このサンプルコードでは、2つのPrimが定義されています。

1つ目は def Xform "hello" で定義されるPrimで型はXformです。Xformはトランスフォーム情報（位置・回転・スケール）を持つノードであり、他のPrimをまとめるグループとしての役割も持ちます。つまりこのPrimはシーン内の親ノードとして機能しています。

2つ目は def Sphere "world" で定義されるPrimで型はSphereです。こちらは球体ジオメトリを表すPrimであり、実際に描画されるオブジェクトです。このSphereはXformである「hello」の子として配置されることで、親の変換の影響を受けながらシーン内に配置されます。

このようにUSDでは多様なPrimを用いて階層的にシーンを構築しています。

## Pythonでの構築処理

上記のサンプルUSDを構築する手順について、Pythonを用いた実装を解説します。

```
from pxr import Usd, UsdGeom
stage = Usd.Stage.CreateNew('HelloWorld.usda')
xformPrim = UsdGeom.Xform.Define(stage, '/hello')
spherePrim = UsdGeom.Sphere.Define(stage, '/hello/world')
stage.GetRootLayer().Save()
```

### Stage

StageはUSDシーンを扱うための起点であり、実装ではこのStageを生成するところから始まります。新規にシーンを作る場合はUsd.Stage.CreateNew() を使ってファイルと紐づいたStageを作成します。

```
stage = Usd.Stage.CreateNew("HelloWorld.usda")
```

この1行で「HelloWorld.usda」というUSDファイルに対応するStageが生成され、以降のすべての処理はこのstageを通して行います。

### Prim

PrimはUSDシーン内のオブジェクトを定義するための基本単位です。作成はStageを通して行い、型（XformやSphereなど）とパスを指定します。

```
UsdGeom.Xform.Define(stage, "/hello")
UsdGeom.Sphere.Define(stage, "/hello/world")
```

このようにパスを指定することで親子関係も同時に決まり、「/hello」の中に「/hello/world」がある階層構造が自動的に作られます。

### RootLayer

RootLayerはStageに紐づく最上位のレイヤーであり、実際のUSDファイルそのものに対応します。シーンに対して行ったすべての編集はこのRootLayerに書き込まれるため、データの保存先となる基盤になります。

実装ではstage.GetRootLayer() で取得し、その後 Save() を呼ぶことで現在の状態をファイルに保存します。

```
rootLayer = stage.GetRootLayer()
rootLayer.Save()
```