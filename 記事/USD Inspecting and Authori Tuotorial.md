# USD Tuotorial --Inspecting and Authoring Properties--

Pixarが開発したフォーマットである[USD(Universal Scene Description)](https://openusd.org/release/index.html)の[公式Tutorial](https://openusd.org/release/tut_usd_tutorials.html)の項目である[Inspecting and Authoring Properties](https://openusd.org/release/tut_inspect_and_author_props.html)と以下のサンプルUSDをもとに、
USDのPrimにおいて情報を管理するPropertyについて、AttributeとRelationShipについて解説するとともに、Pythonによる実装方法についても説明します。

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
Propertyは、Primが保持する情報を表す要素で、PropertyにはAttribute と RelationShipの二種類があります。
USDでは、Primの中にさまざまなPropertyが格納され、Primに関する情報を管理します。

このサンプルでは、Sphere Primである /hello/world に対して以下のPropertyが存在しています。
```
/hello/world
 ├── extent
 ├── radius
 └── primvars:displayColor
```


## Attribute
Attributeは、値を保持するPropertyです。
数値・色・ベクトル・文字列など、実際のデータを管理します。

このサンプルでは、3つのAttributeが定義されています。

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
このTutorialには含まれていませんがPropertyにはRelationShipという種類もあります。
RelationShipは、値を実態と持つのではなく、参照として持たせるPropertyです。
例えると、textureを別usdから参照するなどです。


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

