# USD Tuotorial --Property--

Pixarが開発したフォーマットである[USD(Universal Scene Description)](https://openusd.org/release/index.html)の[公式Tutorial](https://openusd.org/release/tut_usd_tutorials.html)の項目である[Inspecting and Authoring Properties](https://openusd.org/release/tut_inspect_and_author_props.html)と以下のサンプルUSDをもとに、
USDのPrimにおいて情報を管理するPropertyについて、Attribute と Relationship の役割を解説するとともに、Python による実装方法についても説明します。

```
#usda 1.0

def Xform "hello"
{
    def Sphere "world"
    {
        float3[] extent = [(-2, -2, -2), (2, 2, 2)]
        color3f[] primvars:displayColor = [(0, 0, 1)]
        double radius = 2
    }
}
```


## Property
Property は、Prim が保持する情報を表す要素であり、USD では Attribute と Relationship の 2 種類に分類されます。
Prim にはさまざまな Property が格納されており、オブジェクトの状態や他の Prim との関連情報を管理します。
このサンプルでは、Sphere Prim である /hello/world に対して、以下の Property が存在しています。
```
/hello/world
 ├── extent
 ├── radius
 └── primvars:displayColor
```


## Attribute
Attribute は、値を保持するための Property です。
数値・色・ベクトル・文字列など、Prim が持つ実際のデータを管理します。
このサンプルでは、以下の 3 つの Attribute が定義されています。

### extent
primのboundを表すattributeです。
球体の半径が2なので4 × 4 × 4のbound値を定義します
```
float3[] extent = [(-2, -2, -2), (2, 2, 2)]
```

### radius
Sphereの半径を表すAttributeです。
球体の半径を2で定義しています。
```
double radius = 2
```

### primvars:displayColor
Sphereの表示色を表すAttributeです。
RGB形式で定義されており、 青色を定義しています
```
color3f[] primvars:displayColor = [(0, 0, 1)]
```


## RelationShip
この Tutorial には含まれていませんが、Property には Relationship という種類も存在します。
Relationship は、Attribute のように実際の値を保持するのではなく、他の Prim やデータへの参照関係を管理するための Property です。
例えば、別の USD に存在する Texture や Material を参照する場合などに使用されます。


## Pythonでの構築処理
以上を踏まえて、実際にサンプルUSDを構築する手順を、以下のPythonコードをもとに解説します。
```
from pxr import Usd, UsdGeom

# USDを開く
stage = Usd.Stage.Open("HelloWorld.usda")

# Sphere取得
sphere = stage.GetPrimAtPath("/hello/world")

# radius
sphere.GetAttribute("radius").Set(2)

# extent
sphere.GetAttribute("extent").Set([(-2, -2, -2), (2, 2, 2)])

# 色（青）
UsdGeom.Sphere(sphere).GetDisplayColorAttr().Set([(0, 0, 1)])

# 保存
stage.GetRootLayer().Save()
```

まず、Attribute を設定する対象となる world の球体 Prim を取得します。
```
# USDを開く
stage = Usd.Stage.Open("HelloWorld.usda")

# Sphere取得
sphere = stage.GetPrimAtPath("/hello/world")
```

world（球体 Prim）を取得したら、各 Attribute を設定します。
```
# radius
sphere.GetAttribute("radius").Set(2)

# extent
sphere.GetAttribute("extent").Set([(-2, -2, -2), (2, 2, 2)])

# 色（青）
UsdGeom.Sphere(sphere).GetDisplayColorAttr().Set([(0, 0, 1)])
```

最後に Stage を保存して完了です。
```
# 保存
stage.GetRootLayer().Save()
````