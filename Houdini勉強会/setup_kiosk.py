import hou

# 指定パスのノードを選択状態にする
def select_node(node_path):
    node = hou.node(node_path)
    
    # すべての選択を解除
    hou.clearAllSelected()
    
    # 対象ノードを選択（他を解除しない設定も一応付与）
    node.setSelected(True, clear_all_selected=False)
    

# 指定パスのノードを表示（Display FlagをON）
def display_node(node_path):
    node = hou.node(node_path)
    
    # ビューポートで表示されるようにする
    node.setDisplayFlag(True)
    

# UI（Houdiniのパネル構成）を整理する関数
def setup_gui():
    
    # すべてのPane（画面分割領域）をループ
    for pane in hou.ui.panes():
        
        # パネルタブ（上のタブUI）を非表示
        pane.setShowPaneTabs(False)
        
        # Network Editorがある場合、Scene Viewerタブを追加
        if pane.tabOfType(hou.paneTabType.NetworkEditor, 0):
            pane.createTab(hou.paneTabType.SceneViewer)
                    
    # すべてのPane Tabをループ
    for tab in hou.ui.paneTabs():
    
        # パラメータパネルのUI調整
        if tab.type() == hou.paneTabType.Parm:
            # ネットワーク操作バーを非表示
            tab.setShowNetworkControls(False)
                
        # シーンビューアのUI調整
        elif tab.type() == hou.paneTabType.SceneViewer:

            tab.setShowNetworkControls(False)     # ネットワーク操作バー非表示
            tab.showDisplayOptionsBar(False)      # 表示オプションバー非表示
            tab.showOperationBar(False)           # 操作バー非表示
            tab.showSelectionBar(False)           # 選択バー非表示
            
            # カラコレバーが存在する場合は非表示
            if tab.includeColorCorrectionBar():
                tab.showColorCorrectionBar(False)
                    
            # メモリバーが存在する場合は非表示
            if tab.includeMemoryBar():
                tab.showMemoryBar(False)
                    
        # Parm / SceneViewer以外のタブは閉じる
        else:
            tab.close()
                        
    # シェルフ（ツールバー）を非表示
    hou.ui.curDesktop().shelfDock().show(False)
    
    # メニューバー表示設定（Falseで非表示）
    hou.setPreference('showmenu.val', ['0', '1'][False])
        
    # 最小化されたストウバー（UIの折りたたみ）をすべて隠す
    hou.ui.setHideAllMinimizedStowbars(True)
        

# ノード選択
select_node("/obj/box_object/box")

# ノード表示（ビューポート表示対象にする）
display_node("/obj/box_object/box")

# UIレイアウト整理
setup_gui()