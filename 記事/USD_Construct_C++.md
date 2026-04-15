SdfLayerRefPtr
UsdObjTranslateObjToUsd(const UsdObjStream &objStream)
{
    // objStream の内容を表す USD データを持つ SdfLayer を作成する。
    // 手順としては：
    // 1. 匿名のインメモリレイヤーを作成
    // 2. それをルートレイヤーとして UsdStage を生成
    // 3. Usd / UsdGeom API を使ってメッシュを構築
    // 4. 最終的にレイヤーだけ返す（Stage は破棄）

    // 書き込み先となる匿名レイヤーを作成
    SdfLayerRefPtr layer = SdfLayer::CreateAnonymous(".usda");

    // 上記レイヤーをルートとする UsdStage を作成
    UsdStageRefPtr stage = UsdStage::Open(layer);
	
	

    // objStream から頂点データを取得
    const std::vector<GfVec3f> &objVerts = objStream.GetVerts();
    if (objVerts.empty())
        return layer; // 頂点がなければ空レイヤーを返す

    // UV 座標を取得
    const std::vector<GfVec2f> &objUVs = objStream.GetUVs();

    // std::vector → USD 用配列 (VtArray) に変換
    VtVec3fArray usdPoints;
    VtVec2fArray usdUVs;
    usdPoints.assign(objVerts.begin(), objVerts.end());
    usdUVs.assign(objUVs.begin(), objUVs.end());

    // OBJ のポイント情報（頂点インデックスや UV インデックス）
    const std::vector<UsdObjStream::Point> &objPoints = objStream.GetPoints();

    // USD ではバウンディングボックス（extent）が必要
    GfRange3f extent;
    for (const auto& pt : usdPoints) {
        extent.UnionWith(pt); // 範囲を更新
    }



    // extent を min / max の配列として格納
    VtVec3fArray extentArray(2);
    extentArray[0] = extent.GetMin();
    extentArray[1] = extent.GetMax();



    // OBJ の各グループごとにメッシュを生成
    for (const auto& group : objStream.GetGroups()) {

        // グループ名が USD の識別子として無効ならスキップ
        if (!TfIsValidIdentifier(group.name)) {
            TF_WARN("Omitting OBJ group with invalid name '%s'",
                    group.name.c_str());
            continue;
        }

        // 面が存在しないグループはスキップ
        if (group.faces.empty()) {
            TF_WARN("Omitting OBJ group with no faces '%s'",
                    group.name.c_str());
            continue;
        }



        // グループごとに UsdGeomMesh を作成
        UsdGeomMesh mesh =
            UsdGeomMesh::Define(stage, SdfPath("/" + group.name));

        // 頂点座標を設定
        // ※簡易実装のため、すべての頂点をそのまま使用している
        mesh.GetPointsAttr().Set(usdPoints);



        // フェース情報（ポリゴン構成）を作成
        VtArray<int> faceVertexCounts;   // 各フェースの頂点数
        VtArray<int> faceVertexIndices;  // 頂点インデックス
        VtArray<int> faceUVIndices;      // UV インデックス

        for (const auto& face : group.faces) {
            faceVertexCounts.push_back(face.size());

            for (int p = face.pointsBegin; p != face.pointsEnd; ++p) {
                // 頂点インデックス
                faceVertexIndices.push_back(objPoints[p].vertIndex);

                // UV があればインデックスを追加
                if (objPoints[p].uvIndex >= 0) {
                    faceUVIndices.push_back(objPoints[p].uvIndex);
                }
            }
        }



        // フェース情報をメッシュに設定
        mesh.GetFaceVertexCountsAttr().Set(faceVertexCounts);
        mesh.GetFaceVertexIndicesAttr().Set(faceVertexIndices);



        // UV 情報がある場合は Primvar を作成
        if (!usdUVs.empty() || !faceUVIndices.empty()) {

            // faceVarying（頂点ごとに異なる）UV を定義
            UsdGeomPrimvar uvPrimVar =
                UsdGeomPrimvarsAPI(mesh).CreatePrimvar(
                    TfToken("uv"),
                    SdfValueTypeNames->TexCoord2fArray,
                    UsdGeomTokens->faceVarying);

            // UV 座標を設定
            if (!usdUVs.empty()) {
                uvPrimVar.GetAttr().Set(usdUVs);
            }

            // インデックス付き UV（indexed primvar）を設定
            if (!faceUVIndices.empty()) {
                uvPrimVar.CreateIndicesAttr().Set(faceUVIndices);
            }
        }



        // バウンディングボックスを設定
        mesh.GetExtentAttr().Set(extentArray);
    }

    // 作成したレイヤーを返す
    return layer;
}