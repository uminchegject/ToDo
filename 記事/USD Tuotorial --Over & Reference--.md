# USD Tuotorial --Over & Reference--

Pixarが開発したフォーマットである[USD(Universal Scene Description)](https://openusd.org/release/index.html)の[公式Tutorial](https://openusd.org/release/tut_usd_tutorials.html)の項目である[Referencing Layers](https://openusd.org/release/tut_referencing_layers.html)をもとに、非破壊的に情報を参照する方法について、Over と Reference の役割を解説するとともに、Python による実装方法についても説明します。


## over
`over` は、既に存在している Prim に対して、差分だけを非破壊で上書きするための仕組みです。
これまで使用していた def は、Scene 上に実体を持つ Prim を定義するものであり、レンダリングや DCC ツールで読み込まれる対象になります。
一方 `over` は、別レイヤーで定義された Prim に対して、後から設定を追加・変更するための Prim です。
元データを直接編集するのではなく、位置・Visibility・Material などの設定だけを差分として重ねることで、非破壊に編集を行うことができます。
USDでは「後から適用された強い意見が優先される」という Layer Composition の仕組みがあり、`over` はその仕組みを利用して既存データに変更を加えています。


## refenrece
`reference` は、別の USD ファイルを現在の Stage に読み込むための仕組みです。
これはデータをコピーするのではなく、外部USDを参照として合成（Compose）する形で読み込みます。
例えば、Tree.usda のようなアセットを Scene.usda に配置したい場合、`reference` を使用してアセットを読み込みます。
参照元のUSDが更新された場合、その変更を参照先にも反映できるため、Prefab や外部アセット参照のような運用が可能になります。
また、`reference` では通常、参照先USDの defaultPrim が入口として利用されます。
そのため、「どのPrimをアセットの代表として扱うか」を defaultPrim に設定しておくことが重要になります。
