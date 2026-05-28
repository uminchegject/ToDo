# USD Tuotorial --Over & Reference--

Pixarが開発したフォーマットである[USD(Universal Scene Description)](https://openusd.org/release/index.html)の[公式Tutorial](https://openusd.org/release/tut_usd_tutorials.html)の項目である[Referencing Layers](https://openusd.org/release/tut_referencing_layers.html)をもとに、非破壊的に情報を参照する方法について、Over と Reference の役割を解説するとともに、Python による実装方法についても説明します。
```
#usda 1.0

over "refSphere" (
    prepend references = @./HelloWorld.usda@
)
{
    uniform token[] xformOpOrder = []
}

over "refSphere2" (
    prepend references = @./HelloWorld.usda@
)
{
    over "world"
    {
        color3f[] primvars:displayColor = [(1, 0, 0)]
    }
}
```

## over
`over` は、既に存在している Prim に対して、差分だけを非破壊で上書きするための仕組みです。
これまで使用していた def は、Scene 上に実体を持つ Prim を定義するものであり、レンダリングや DCC ツールで読み込まれる対象になります。
一方 `over` は、別レイヤーで定義された Prim に対して、後から設定を追加・変更するための Prim です。
元データを直接編集するのではなく、位置・Visibility・Material などの設定だけを差分として重ねることで、非破壊に編集を行うことができます。
USDでは「後から適用された強い意見が優先される」という Layer Composition の仕組みがあり、`over` はその仕組みを利用して既存データに変更を加えています。

サンプルソースだと HelloWorld.usda を参照した refSphere2 に対して、world Prim の displayColor だけを上書きしています。
```
over "refSphere2" (
    prepend references = @./HelloWorld.usda@
)
{
    over "world"
    {
        color3f[] primvars:displayColor = [(1, 0, 0)]
    }
}
```
この場合、元の HelloWorld.usda は変更されません。
しかし、Compose 後の Stage では world Prim の色が赤 (1, 0, 0) に変更された状態として扱われます。
また、次の例のように xformOpOrder を空にすることで、元アセットの Transform 情報を無効化することもできます。
```
over "refSphere" (
    prepend references = @./HelloWorld.usda@
)
{
    uniform token[] xformOpOrder = []
}
```
このように over は、「元データは保持したまま、一部だけ差し替えたい」という用途で非常に重要な仕組みです。


## refenrece
`reference` は、別の USD ファイルを現在の Stage に読み込むための仕組みです。
これはデータをコピーするのではなく、外部USDを参照として合成（Compose）する形で読み込みます。
例えば、Tree.usda のようなアセットを Scene.usda に配置したい場合、`reference` を使用してアセットを読み込みます。
参照元のUSDが更新された場合、その変更を参照先にも反映できるため、Prefab や外部アセット参照のような運用が可能になります。
また、`reference` では通常、参照先USDの defaultPrim が入口として利用されます。
そのため、「どのPrimをアセットの代表として扱うか」を defaultPrim に設定しておくことが重要になります。

サンプルソースだと、以下の例では HelloWorld.usda を refSphere として読み込んでいます。
```
over "refSphere" (
    prepend references = @./HelloWorld.usda@
)
{
    uniform token[] xformOpOrder = []
}
```
prepend references に指定された @./HelloWorld.usda@ が外部USDファイルへの参照です。
この記述により、HelloWorld.usda の内容が現在の Stage に合成され、refSphere 配下に展開されます。
同様に、次の例でも HelloWorld.usda を参照していますが、こちらでは over を組み合わせて色だけを変更しています。
```
over "refSphere2" (
    prepend references = @./HelloWorld.usda@
)
{
    over "world"
    {
        color3f[] primvars:displayColor = [(1, 0, 0)]
    }
}
```
このように reference と over を組み合わせることで、

* アセット本体は共通利用する
* Sceneごとに見た目やTransformだけ変更する
* 元データを壊さず差分管理する 
 
といった USD らしい非破壊ワークフローを実現できます。


## Pythonでの構築処理
```
from pxr import Usd, UsdGeom

# =========================================================
# HelloWorld.usda 作成
# =========================================================

helloStage = Usd.Stage.CreateNew("HelloWorld.usda")

helloXform = UsdGeom.Xform.Define(helloStage, "/hello")

sphere = UsdGeom.Sphere.Define(helloStage, "/hello/world")
sphere.GetRadiusAttr().Set(2)
sphere.GetDisplayColorAttr().Set([(0, 0, 1)])

helloStage.SetDefaultPrim(helloXform.GetPrim())

UsdGeom.XformCommonAPI(helloXform).SetTranslate((4, 5, 6))

helloStage.GetRootLayer().Save()


# =========================================================
# Reference Stage 作成
# =========================================================

refStage = Usd.Stage.CreateNew("RefExample.usda")

# over Prim 作成
refSphere = refStage.OverridePrim("/refSphere")

# reference 追加
refSphere.GetReferences().AddReference("./HelloWorld.usda")

# transform override
refXform = UsdGeom.Xformable(refSphere)
refXform.SetXformOpOrder([])


# =========================================================
# 2つ目の reference
# =========================================================

refSphere2 = refStage.OverridePrim("/refSphere2")

refSphere2.GetReferences().AddReference("./HelloWorld.usda")

# displayColor override
overSphere = UsdGeom.Sphere.Get(refStage, "/refSphere2/world")
overSphere.GetDisplayColorAttr().Set([(1, 0, 0)])


# 保存
refStage.GetRootLayer().Save()
```


DefaultPrim設定
```
helloStage = Usd.Stage.CreateNew("HelloWorld.usda")

helloXform = UsdGeom.Xform.Define(helloStage, "/hello")

sphere = UsdGeom.Sphere.Define(helloStage, "/hello/world")
sphere.GetRadiusAttr().Set(2)
sphere.GetDisplayColorAttr().Set([(0, 0, 1)])

helloStage.SetDefaultPrim(helloXform.GetPrim())

UsdGeom.XformCommonAPI(helloXform).SetTranslate((4, 5, 6))

helloStage.GetRootLayer().Save()
```

Override設定
```
refStage = Usd.Stage.CreateNew("RefExample.usda")

# over Prim 作成
refSphere = refStage.OverridePrim("/refSphere")
```

reference設定
```
# reference 追加
refSphere.GetReferences().AddReference("./HelloWorld.usda")
```

値を上書き
```
# transform override
refXform = UsdGeom.Xformable(refSphere)
refXform.SetXformOpOrder([])
```

同様の手順
```
refSphere2 = refStage.OverridePrim("/refSphere2")

refSphere2.GetReferences().AddReference("./HelloWorld.usda")

# displayColor override
overSphere = UsdGeom.Sphere.Get(refStage, "/refSphere2/world")
overSphere.GetDisplayColorAttr().Set([(1, 0, 0)])


# 保存
refStage.GetRootLayer().Save()
```