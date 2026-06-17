# USD Tuotorial --Traversing a Stage--

## Traverse()
`Usd.Stage.Traverse()` は、USDステージ内の Prim を深さ優先順で巡回するためのジェネレータです。
最も基本的なステージ走査方法であり、Python のジェネレータとして扱えるため、特定の型の Prim だけを抽出するなどのフィルタリングも簡単に行えます。

ただし、`Traverse()` はステージ上のすべての Prim を返しているわけではありません。
実際には、**Active（有効）・Defined（定義済み）・Loaded（ロード済み）・Concrete（実体を持つ）** という条件を満たす Prim だけを対象に巡回します。
そのため、非アクティブな Prim や未ロードの Payload、クラス定義用の Abstract Prim などは結果に含まれません。

一方、`Usd.Stage.TraverseAll()` はこれらの条件を適用せず、ステージ上に存在する Prim をそのまま巡回するためのメソッドです。
通常の `Traverse()` では見えない非アクティブ Prim なども取得できます。
ただし、非アクティブ化された Prim の子要素は合成済みシーングラフ（composed scenegraph）から取り除かれるため、親 Prim は見えてもその子 Prim は存在しない場合があります。

そのため、普段のシーン処理では `Traverse()` を使うことが多く、特定の Prim が見つからない原因を調査したり、USD の内部状態を確認したりするときには `TraverseAll()` を利用します。


## PrimRange()
`Usd.PrimRange()` は、指定した Prim を起点として、その Prim と子孫 Prim を巡回するためのイテレータです。
`Usd.Stage.Traverse()` がステージ全体を対象とするのに対し、`Usd.PrimRange()` は特定の Prim 以下の階層だけを対象に走査したい場合に使用します。

巡回はデフォルトで **深さ優先（Depth First）かつ pre-order（親→子の順）** で行われます。
そのため、まず親 Prim が返され、その後に子 Prim、孫 Prim へと順番に処理が進みます。

また、`Usd.PrimRange()` の大きな特徴は、巡回対象を細かく制御できることです。
Predicate（条件）を指定することで、Active な Prim のみ、Loaded な Prim のみ、といった条件付きの走査が可能です。
実際には `Usd.Stage.Traverse()` も内部的には `Usd.PrimRange()` を利用しており、**Active・Defined・Loaded・Concrete** な Prim を対象とする Predicate があらかじめ設定された便利メソッドと考えることができます。

さらに、`Usd.PrimRange()` では巡回中に特定の Prim 以下の探索を打ち切る（Prune）こともできます。
これにより、大規模なシーンの中で不要なサブツリーをスキップしながら効率的に走査できます。

そのため、`Usd.Stage.Traverse()` が「ステージ全体を手軽に巡回するための高レベル API」であるのに対し、`Usd.PrimRange()` は「巡回範囲や条件を細かく制御するための低レベルで柔軟な API」と言えます。
特定の階層だけを対象にした処理や、大規模シーンの最適化、カスタムな走査条件が必要な場合に利用されます。
