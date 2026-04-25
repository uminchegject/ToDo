## サンプルUSD

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
* USDシーン全体を管理するルートオブジェクト
* レイヤー群やPrim階層を統合して扱う
* 例えると「3Dシーンのコンテナ」

### Prim：オブジェクト（ノード）
* シーンを構成する基本単位
* 3Dモデル、グループ、ライトなどを表す
* 階層構造のノードとして機能する

### 階層構造：パス（/hello/world）で管理
* USDではすべてのオブジェクトを「パス」で識別
* UNIXディレクトリのようなツリー構造


## Pythonでの構築処理
上記USDを構築するための処理

```
from pxr import Usd, UsdGeom
stage = Usd.Stage.CreateNew('HelloWorld.usda')
xformPrim = UsdGeom.Xform.Define(stage, '/hello')
spherePrim = UsdGeom.Sphere.Define(stage, '/hello/world')
stage.GetRootLayer().Save()
```

### Stage
* USDシーンの生成・読み込みの起点
* Usd.Stage.CreateNew() で新規作成
* 全Primやレイヤーを統合管理
```
stage = Usd.Stage.CreateNew("HelloWorld.usda")
```

### Prim
* シーン内のオブジェクトを定義
* 型付き（UsdGeomなど）または汎用で作成可能
* パスを指定して階層構造を構築
```
UsdGeom.Xform.Define(stage, "/hello")
UsdGeom.Sphere.Define(stage, "/hello/world")
```

### RootLayer
* Stageの最上位レイヤー（実ファイルに対応）
* すべての編集結果が書き込まれる基盤
* 保存処理の起点
```
rootLayer = stage.GetRootLayer()
rootLayer.Save()
```