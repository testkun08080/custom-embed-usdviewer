import sys
from PySide6 import QtGui, QtCore, QtWidgets
from pxr import Usd, UsdUtils, Sdf
from pxr.Usdviewq.stageView import StageView
from pxr.Usdviewq.appController import AppController
from pxr.Usdviewq.usdviewApi import UsdviewApi

import sys


class EmmbedUSDWidget(QtWidgets.QWidget):
    def __init__(self, stage=None):
        super(EmmbedUSDWidget, self).__init__()
        self.model = StageView.DefaultDataModel()
        self.stage = stage
        self.view = StageView(dataModel=self.model)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.setContentsMargins(0, 0, 0, 0)

        if self.stage:
            self.setStage(self.stage)

    def imageSave(self):
        print("GetRendererAovs", self.view.GetRendererAovs())
        image = self.view.grabFramebuffer()
        image.save('save.png')

    def setStage(self, stage):
        self.model.stage = stage

    def closeEvent(self, event):
        # Ensure to close the renderer to avoid GlfPostPendingGLErrors
        self.view.closeRenderer()


if __name__ == '__main__':

    app = QtWidgets.QApplication([])

    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # path = r"Sphere.usda"
    path = "OpenUSD/extras/usd/tutorials/convertingLayerFormats/Sphere.usda"

    with Usd.StageCacheContext(UsdUtils.StageCache.Get()):
        stage = Usd.Stage.Open(path)

    window = EmmbedUSDWidget(stage)
    window.setWindowTitle("USD Viewer")
    window.resize(QtCore.QSize(750, 750))
    window.show()

    # カメラをジオメトリにフィット
    window.view.updateView(resetCam=True, forceComputeBBox=True)

    sys.exit(app.exec_())