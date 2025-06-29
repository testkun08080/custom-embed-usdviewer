import sys
from PySide6 import QtWidgets, QtCore, QtUiTools
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice
from pxr import Usd, UsdUtils
from embedUSDViewer import EmmbedUSDWidget

def get_ui_widget(ui_file_name):
    """Get a UI widget from a UI file."""

    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    uiWidget = loader.load(ui_file)
    ui_file.close()

    return uiWidget

class UsdViewerContoler:
    def __init__(self):
        self.ui = get_ui_widget("form.ui")

        # USD Stageの読み込み
        path = "Sphere.usda"
        with Usd.StageCacheContext(UsdUtils.StageCache.Get()):
            self.stage = Usd.Stage.Open(path)

        # USD Viewerウィジェットの埋め込み
        self.usd_widget = EmmbedUSDWidget(self.stage)
        self.ui.mainLayout.addWidget(self.usd_widget)

        # AOVs選択用のUIをセットアップ
        self.setup_aov_ui()

        # Save Imageボタンのイベント接続
        self.ui.saveImage_Button.clicked.connect(self.usd_widget.imageSave)

    def setup_aov_ui(self):
        # AOVsリストを取得してコンボボックスに追加
        aovs = self.usd_widget.view.GetRendererAovs()
        print("aovs", aovs)
        if not aovs:
            # AOVsが空の場合、デフォルトのAOVを追加
            default_aovs = ['color', 'primId', 'depth', 'Neye']
            for aov in default_aovs:
                self.ui.aovs_comboBox.addItem(aov)
        else:
            for aov in aovs:
                self.ui.aovs_comboBox.addItem(aov)

        # AOV選択時のイベント接続
        self.ui.aovs_comboBox.currentTextChanged.connect(self.on_aov_changed)

    def on_aov_changed(self, aov_name):
        print(aov_name)
        # 選択されたAOVにビューを更新
        if aov_name:
            self.usd_widget.view.SetRendererAov(aov_name)
            self.usd_widget.view.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = UsdViewerContoler()
    window.ui.show()
    # window.usd_widget.view.updateView(resetCam=True, forceComputeBBox=True)
    sys.exit(app.exec_())
