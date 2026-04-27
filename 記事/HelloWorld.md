# USD Hello World Tutorial
Pixarが開発したフォーマットである[USD(Universal Scene Description)](https://openusd.org/release/index.html)の[公式Tutorial](https://openusd.org/release/tut_usd_tutorials.html)をもとに、USDの構造を解説します。 
まずは、チュートリアルの最初の項目である[Hello World](https://openusd.org/release/tut_helloworld.html)について説明します。

## サンプルUSD
ここでは、チュートリアルで紹介されているサンプルコードをもとに解説します。
```
#usda 1.0

def Xform "hello"
{
    def Sphere "world"
    {
    }
}
```

### Stage：シーン全体
Stageは、USDシーン全体を管理するルートオブジェクトです。
複数のレイヤーや参照関係を解決した結果としての「最終的なシーン」を表します。
このTutorialでは、helloというノードの中に、worldという球体があるシーンということになります。
```
Stage（シーン全体）
 └── /hello
      └── /hello/world
```

### Prim：オブジェクト（ノード）
USDでは、シーン内のすべての要素はPrimという単位で表現されます。
Primは単なるデータではなく、型（Type）と役割を持つ「ノード」として機能し、階層構造の中でシーンを構成します。

この例では、2つのPrimが定義されています。

1つ目は def Xform "hello" で定義されるPrimで、型はXformです。
Xformはトランスフォーム情報（位置・回転・スケール）を持つノードであり、他のPrimをまとめるグループとしての役割も持ちます。
つまり、このPrimはシーン内の親ノードとして機能しています。

2つ目は def Sphere "world" で定義されるPrimで、型はSphereです。
こちらは球体ジオメトリを表すPrimであり、実際に描画される「見えるオブジェクト」です。
このSphereはXformである「hello」の子として配置されることで、親の変換の影響を受けながらシーン内に配置されます。

このようにUSDでは、多様なPrimを用いて階層的にシーンを構築しています。



## Pythonでの構築処理
上記のサンプルUSDを構築する手順について、Pythonを用いて解説します。

```
from pxr import Usd, UsdGeom
stage = Usd.Stage.CreateNew('HelloWorld.usda')
xformPrim = UsdGeom.Xform.Define(stage, '/hello')
spherePrim = UsdGeom.Sphere.Define(stage, '/hello/world')
stage.GetRootLayer().Save()
```

### Stage
StageはUSDシーンを扱うための起点であり、実装ではまずこのStageを生成するところから始まります。新規にシーンを作る場合は、Usd.Stage.CreateNew() を使ってファイルと紐づいたStageを作成します。
```
stage = Usd.Stage.CreateNew("HelloWorld.usda")
```
この1行で「HelloWorld.usda」というUSDファイルに対応するStageが生成され、以降のすべての処理はこのstageを通して行います。

### Prim
Primは、USDシーン内のオブジェクトを定義するための基本単位です。作成はStageを通して行い、型（XformやSphereなど）とパスを指定します。
```
UsdGeom.Xform.Define(stage, "/hello")
UsdGeom.Sphere.Define(stage, "/hello/world")
```
このようにパスを指定することで、親子関係も同時に決まり、「/hello」の中に「/hello/world」がある階層構造が自動的に作られます。

### RootLayer
RootLayerは、Stageに紐づく最上位のレイヤーであり、実際のUSDファイルそのものに対応します。シーンに対して行ったすべての編集は、このRootLayerに書き込まれるため、データの保存先となる基盤になります。
実装では、stage.GetRootLayer() で取得し、その後 Save() を呼ぶことで現在の状態をファイルに保存します。
```
rootLayer = stage.GetRootLayer()
rootLayer.Save()
```
つまり、RootLayerは「最終的な書き込み先」であり、保存処理の起点となる存在です。