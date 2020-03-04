import sys
from PyQt5.QtWidgets import QApplication,  QWidget, QVBoxLayout, QHBoxLayout, QPushButton, \
    QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file system view - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        operatorLayout = QHBoxLayout()
        addBtn = QPushButton("添加节点")
        updateBtn = QPushButton("修改节点")
        delBtn = QPushButton("删除节点")
        operatorLayout.addWidget(addBtn)
        operatorLayout.addWidget(updateBtn)
        operatorLayout.addWidget(delBtn)
        # 按钮的信号槽连接
        addBtn.clicked.connect(self.addTreeNodeBtn)
        updateBtn.clicked.connect(self.updateTreeNodeBtn)
        delBtn.clicked.connect(self.delTreeNodeBtn)

        self.tree = QTreeWidget(self)
        # 设置列数
        # self.tree.setColumnCount(2)
        self.tree.setColumnCount(1)
        # 设置头的标题
        # self.tree.setHeaderLabels(['Key', 'Value'])
        self.tree.setHeaderLabels(['Key'])
        self.root = QTreeWidgetItem(self.tree)
        self.root.setText(0, 'root')
        self.root.setText(1, '0')

        child1 = QTreeWidgetItem(self.root)
        child1.setText(0, 'child1')
        child1.setText(1, '1')

        child2 = QTreeWidgetItem(self.root)
        child2.setText(0, 'child2')
        child2.setText(1, '2')

        child3 = QTreeWidgetItem(self.root)
        child3.setText(0, 'child3')
        child3.setText(1, '3')

        child4 = QTreeWidgetItem(child3)
        child4.setText(0, 'child4')
        child4.setText(1, '4')

        child5 = QTreeWidgetItem(child3)
        child5.setText(0, 'child5')
        child5.setText(1, '5')

        self.tree.addTopLevelItem(self.root)
        self.tree.clicked.connect(self.onTreeClicked)

        mainLayout = QVBoxLayout(self);
        mainLayout.addLayout(operatorLayout);
        mainLayout.addWidget(self.tree);
        self.setLayout(mainLayout)
        self.show()

    def onTreeClicked(self, qmodelindex):
        item = self.tree.currentItem()
        print("key=%s ,value=%s" % (item.text(0), item.text(1)))

    def addTreeNodeBtn(self):
        print('--- addTreeNodeBtn ---')
        item = self.tree.currentItem()
        node = QTreeWidgetItem(item)
        node.setText(0, 'newNode')
        node.setText(1, '10')

    def updateTreeNodeBtn(self):
        print('--- updateTreeNodeBtn ---')
        item = self.tree.currentItem()
        item.setText(0, 'updateNode')
        item.setText(1, '20')

    def delTreeNodeBtn(self):
        print('--- delTreeNodeBtn ---')
        item = self.tree.currentItem()
        root = self.tree.invisibleRootItem()
        # print(item.parent())
        # root.removeChild(self.root)
        root.removeChild(self.tree.topLevelItem(0))
        # for item in self.tree.selectedItems():
        #     (item.parent() or root).removeChild(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

