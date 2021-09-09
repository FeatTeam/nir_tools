import sys
from PyQt5.Qt import *
import os
import time
import pandas as pd
import shutil
import numpy as np
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from denoise import denoise


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(f"布眼科技智能AI实时监测系统")
        self.setWindowIcon(QIcon("nir_tools.ico"))
        self.widget = QWidget(self)
        self.layout = QVBoxLayout(self.widget)

        self.input_temp_addr = QLineEdit(self)
        self.input_temp_addr.move(170, 50)
        self.input_temp_addr.resize(450, 30)

        self.label_relocate_dir = QLabel(self)
        self.label_relocate_dir.setText(u"请输入采集数据临时地址：")
        self.label_relocate_dir.move(15, 50)
        self.label_relocate_dir.resize(150, 30)

        self.input_relocate_dir = QLineEdit(self)
        self.input_relocate_dir.move(170, 150)
        self.input_relocate_dir.resize(450, 30)

        self.label_relocate_dir = QLabel(self)
        self.label_relocate_dir.setText(u"请输入采样数据存放地址：")
        self.label_relocate_dir.move(15, 150)
        self.label_relocate_dir.resize(150, 30)

        self.input_device_id = QLineEdit(self)
        self.input_device_id.move(170, 200)
        self.input_device_id.resize(100, 30)

        self.label_device_id = QLabel(self)
        self.label_device_id.setText(u"请输入采集设备编号：")
        self.label_device_id.move(15, 200)
        self.label_device_id.resize(150, 30)

        self.input_collector_name = QLineEdit(self)
        self.input_collector_name.move(170, 250)
        self.input_collector_name.resize(100, 30)

        self.label_collector_name = QLabel(self)
        self.label_collector_name.setText(u"请输入采集员的姓名：")
        self.label_collector_name.move(15, 250)
        self.label_collector_name.resize(150, 30)

        self.input_collect_date = QLineEdit(self)
        self.input_collect_date.move(170, 300)
        self.input_collect_date.resize(100, 30)

        self.label_collect_date = QLabel(self)
        self.label_collect_date.setText(u"请输入采集日期：")
        self.label_collect_date.move(15, 300)
        self.label_collect_date.resize(150, 30)

        self.input_collected_loc = QLineEdit(self)
        self.input_collected_loc.move(170, 350)
        self.input_collected_loc.resize(100, 30)

        self.label_collected_loc = QLabel(self)
        self.label_collected_loc.setText(u"请输入采集地点：")
        self.label_collected_loc.move(15, 350)
        self.label_collected_loc.resize(150, 30)

        self.input_fabric = QLineEdit(self)
        self.input_fabric.move(520, 200)
        self.input_fabric.resize(100, 30)

        self.label_fabric = QLabel(self)
        self.label_fabric.setText(u"请输入布匹编号和成分\n（编号在前以'_'隔开）：")
        self.label_fabric.move(350, 200)
        self.label_fabric.resize(150, 30)

        self.input_waving_type = QLineEdit(self)
        self.input_waving_type.move(520, 250)
        self.input_waving_type.resize(100, 30)

        self.label_waving_type = QLabel(self)
        self.label_waving_type.setText(u"请输入布样所用织法：")
        self.label_waving_type.move(350, 250)
        self.label_waving_type.resize(150, 30)

        self.btn_start_detect = QPushButton(self)
        self.btn_start_detect.move(650, 50)
        self.btn_start_detect.setText("开始检测")
        self.btn_start_detect.setStyleSheet("QpushButton{background:white}")
        self.btn_start_detect.clicked.connect(self.Test)

        self.btn_finish_detect = QPushButton(self)
        self.btn_finish_detect.move(450, 350)
        self.btn_finish_detect.setText("本匹布采样完成")
        self.btn_start_detect.setStyleSheet("QpushButton{background:white}")
        self.btn_finish_detect.clicked.connect(self.Move)
        self.detect_thread = DetectTheard("undefined path")

    def Test(self):
        # if running, terminate background task
        if self.detect_thread.isRunning():
            self.DestroyDetectThread()
            return

        # if not running, start background task
        self.tmp_path = self.input_temp_addr.text()
        if not os.path.exists(self.tmp_path):
            reply = QMessageBox.warning(self,
                                        "ERROR",
                                        f"采集数据临时地址不存在！",
                                        )
            return
        self.btn_start_detect.setStyleSheet('''QPushButton{background:red;}''')
        self.detect_thread.ChangePath(self.tmp_path)
        self.detect_thread.chan.connect(self.Alert)
        self.detect_thread.proc.connect(self.ShowProc)
        self.detect_thread.start()

    def DestroyDetectThread(self):
        self.detect_thread.terminate()
        self.btn_start_detect.setStyleSheet("QpushButton{background:white}")

    def ShowProc(self, title):
        self.setWindowTitle(title)

    def Alert(self, notValidFile):
        reply = QMessageBox.warning(self,
                                    "消息框标题",
                                    f"{notValidFile}采样点出错，是否删除并重新检测？",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
                                    )

        if reply == QMessageBox.Yes:
            self.detect_thread.delete()
        self.DestroyDetectThread()

    def Move(self):
        rootPath = self.input_relocate_dir.text()
        device_id = self.input_device_id.text()
        name = self.input_collector_name.text()
        date = self.input_collect_date.text()
        location = self.input_collected_loc.text()
        fabric = self.input_fabric.text()
        waving_type = self.input_waving_type.text()
        if not os.path.exists(rootPath):
            reply = QMessageBox.warning(self,
                                        "ERROR",
                                        f"采样数据存放地址不存在！",
                                        )
            return
        if not device_id:
            reply = QMessageBox.warning(self,
                                        "ERROR",
                                        f"采集设备编号不存在！",
                                        )
            return
        if not name:
            reply = QMessageBox.warning(self,
                                        "ERROR",
                                        f"采集员姓名不存在！",
                                        )
            return
        if not date:
            reply = QMessageBox.warning(self,
                                        "ERROR",
                                        f"采集日期不存在！",
                                        )
            return
        if not location:
            reply = QMessageBox.warning(self,
                                        "ERROR",
                                        f"采集地点不存在！",
                                        )
            return
        if not device_id:
            reply = QMessageBox.warning(self,
                                        "ERROR",
                                        f"采集设备编号不存在！",
                                        )
            return
        if not fabric:
            reply = QMessageBox.warning(self,
                                        "ERROR",
                                        f"布匹成分不存在！",
                                        )
            return
        if not waving_type:
            reply = QMessageBox.warning(self,
                                        "ERROR",
                                        f"布匹编号不存在！",
                                        )
            return
        move(self.tmp_path, rootPath, device_id, name,
             date, location, fabric, waving_type)

    def closeEvent(self, event):

        reply = QMessageBox.question(self, '信息', '确认退出吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class DetectTheard(QThread):
    """该线程用于计算耗时的累加操作"""
    chan = pyqtSignal(str)  # 信号类型 str
    proc = pyqtSignal(str)

    def __init__(self, tmp_path):
        super().__init__()
        self.tmp_path = tmp_path

    def ChangePath(self, tmp_path):
        self.tmp_path = tmp_path

    def run(self):
        s = self.WaitForNotValidFile()
        self.chan.emit(s)  # 计算结果完成后，发送结果

    def WaitForNotValidFile(self):
        cache = set()
        while True:
            self.proc.emit(f"布眼科技智能AI实时监测系统")
            files = os.listdir(self.tmp_path)
            for file in files:
                if file in cache:
                    continue
                self.proc.emit(f"布眼科技智能AI实时监测系统 正在处理{file}")
                if '_r' in file or '_a' in file:
                    if not check(os.path.join(self.tmp_path, file)):
                        self.bad_files = [file, file.replace('_r', '_a'), file.replace('_r', '_i'), file.replace('_r', ''),
                                          file.replace('_r', '').replace('.csv', '.dat')]
                        return file
                cache.add(file)
            time.sleep(1)

    def delete(self):
        for bad_file in self.bad_files:
            os.remove(os.path.join(self.tmp_path, bad_file))
        return


def check(p):
    with open(p, encoding='utf-8') as f:
        col = np.loadtxt(f, str, delimiter=",", usecols=(1))
        data = np.array(col[29:], dtype=float)
        if float(max(data)) < 0.1 or not denoise(data):
            return False
    return True


def move(tmp_path, rootPath, device_id, name, date, location, fabric, waving_type):
    b = f"{device_id}_{fabric}_{waving_type}_{name}_{date}_{location}"
    despath = os.path.join(rootPath, b)
    if not os.path.exists(rootPath):
        os.mkdir(rootPath)
    os.mkdir(despath)
    currentList = os.listdir(tmp_path)
    for file in currentList:
        shutil.move(os.path.join(tmp_path, file), despath)


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    m = Main()
    m.show()
    m.resize(800, 500)
    app.exec()
