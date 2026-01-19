---
marp: true
theme: uncover
---

<style>
/* 全体の基本文字サイズ */
section {
  font-size: 20px;
}

/* 見出しサイズ調整（uncover対策） */
h1 { font-size: 44px; }
h2 { font-size: 34px; }
h3 { font-size: 26px; }
h4 { font-size: 22px; }

/* 本文・リスト */
p, li {
  font-size: 20px;
  line-height: 1.4;
}

/* フッター少し小さめ */
footer {
  font-size: 14px;
}
</style>

<!--
_color: white
-->

![bg brightness:0.6](Picture/FacadeGenerator_Cover.jpg)

# ファザード生成ツール

---

![bg left:40%](Picture/FacadeGenerator_Overview.jpg)

### 概要

Houdiniのプロシージャルモデリングを用いて、  
ファサード設計をルールとして定義し、  
パネル形状・配置ロジックを切り替え可能なツールを実装した。

パネル形状を入力として受け取り、  
スケール・位置・回転などをパラメーター制御することで、  
多様なファサードバリエーションを効率的に生成できる。


---

![bg left:40%](Picture/FacadeGenerator_ObjectiveBackground.jpg)

### 目的・背景（Background）

設計初期段階において、  
配置密度・リズム・不均質性の検討を  
繰り返し行うことは困難である。

本制作では、ファサードを「形状」ではなく  
**生成ルール**として扱うことを前提に、  
以下の3項目を目的として実装した。

- ファサード設計における  
  反復作業・バリエーション検討のコスト削減
- コンピュテーショナルデザインにおける  
  ルール設計と形状生成の関係性の整理
- 「形状」ではなく  
  生成プロセスそのものを再利用可能にすること


---

<!--
_color: white
-->

![bg brightness:0.6](Picture/CityGenerator_Cover.jpg)

# 街生成ツール

---


![bg left:40%](Picture/CityGenerator_Overview.jpg)

### 概要

本ツールは、Houdini上で動作する  
**プロシージャルな街ジェネレーターHDA**である。

道路・区画・建物ボリュームの生成を  
段階的に行う構成とし、  
パラメーター操作によって  
街並みのスケールや密度を  
柔軟に制御できる。

---

![bg left:40%](Picture/CityGenerator_ObjectiveBackground.jpg)

### 目的・背景

街並みの制作では、  
試行錯誤を繰り返しながら  
スケール感や密度を調整する必要がある。

その過程において、  
手作業による修正は作業コストが高く、  
破壊的な変更になりやすいという  
課題が存在する。

本制作では、  
**非破壊かつ再利用可能な形で  
街生成を行えるツールの構築**を目的とし、  
設計段階から  
プロシージャルワークフローを前提とした  
実装を行った。