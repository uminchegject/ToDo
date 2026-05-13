# USD Tuotorial --Inspecting and Authoring Properties--

Pixarが開発したフォーマットである[USD(Universal Scene Description)](https://openusd.org/release/index.html)の[公式Tutorial](https://openusd.org/release/tut_usd_tutorials.html)の項目である[Inspecting and Authoring Properties](https://openusd.org/release/tut_inspect_and_author_props.html)と以下のサンプルUSDをもとに、USDのPrimにおいて情報を管理するPropertyと、その値を保持するAttributeについて解説するとともに、Pythonによる実装方法についても説明します。

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
Propertyは、Primが保持する情報を表す要素です。
USDでは、Primの中にさまざまなPropertyが格納されています。

このサンプルでは、Sphere Primである /hello/world に対して以下のPropertyが存在しています。
```
/hello/world
 ├── radius
 └── primvars:displayColor
```


## Attribute
Attributeは、値を保持するPropertyです。
数値・色・ベクトル・文字列など、実際のデータを管理します。

このサンプルでは、2つのAttributeが定義されています。
