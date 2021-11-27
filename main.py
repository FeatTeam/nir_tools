import re
import sys
from decimal import Decimal
from PyQt5.Qt import *
import config as Config
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
        self.init_from_config()
        self.setWindowTitle(f"布眼科技智能AI实时监测系统")
        self.setWindowIcon(QIcon("nir_tools.ico"))
        self.widget = QWidget(self)
        self.layout = QVBoxLayout(self.widget)

        self.input_temp_addr = QLineEdit(self)
        self.input_temp_addr.setText(self.tmp_path)
        self.input_temp_addr.move(170, 50)
        self.input_temp_addr.resize(450, 30)

        self.label_temp_addr = QLabel(self)
        self.label_temp_addr.setText(u"采集数据临时地址：")
        self.label_temp_addr.move(15, 50)
        self.label_temp_addr.resize(150, 30)

        self.input_relocate_dir = QLineEdit(self)
        self.input_relocate_dir.setText(self.rootPath)
        self.input_relocate_dir.move(170, 100)
        self.input_relocate_dir.resize(450, 30)

        self.label_relocate_dir = QLabel(self)
        self.label_relocate_dir.setText(u"采样数据存放地址：")
        self.label_relocate_dir.move(15, 100)
        self.label_relocate_dir.resize(150, 30)

        self.input_fabric = QLineEdit(self)
        self.input_fabric.setText(self.fabric)
        self.input_fabric.move(170, 150)
        self.input_fabric.resize(450, 30)

        self.label_fabric = QLabel(self)
        self.label_fabric.setText(u"布匹编号和成分\n（编号在前以'_'隔开）：")
        self.label_fabric.move(15, 150)
        self.label_fabric.resize(150, 30)

        self.input_device_id = QLineEdit(self)
        self.input_device_id.setText(self.device_id)
        self.input_device_id.move(170, 200)
        self.input_device_id.resize(100, 30)

        self.label_device_id = QLabel(self)
        self.label_device_id.setText(u"采集设备编号：")
        self.label_device_id.move(15, 200)
        self.label_device_id.resize(150, 30)

        self.input_collector_name = QLineEdit(self)
        self.input_collector_name.setText(self.name)
        self.input_collector_name.move(170, 250)
        self.input_collector_name.resize(100, 30)

        self.label_collector_name = QLabel(self)
        self.label_collector_name.setText(u"采集员的姓名：")
        self.label_collector_name.move(15, 250)
        self.label_collector_name.resize(150, 30)

        self.input_collect_date = QLineEdit(self)
        self.input_collect_date.setText(self.date)
        self.input_collect_date.move(170, 300)
        self.input_collect_date.resize(100, 30)

        self.label_collect_date = QLabel(self)
        self.label_collect_date.setText(u"采集日期：")
        self.label_collect_date.move(15, 300)
        self.label_collect_date.resize(150, 30)

        self.input_collected_loc = QLineEdit(self)
        self.input_collected_loc.setText(self.location)
        self.input_collected_loc.move(170, 350)
        self.input_collected_loc.resize(100, 30)

        self.label_collected_loc = QLabel(self)
        self.label_collected_loc.setText(u"采集地点：")
        self.label_collected_loc.move(15, 350)
        self.label_collected_loc.resize(150, 30)

        self.input_waving_type = QLineEdit(self)
        self.input_waving_type.setText(self.waving_type)
        self.input_waving_type.move(520, 250)
        self.input_waving_type.resize(100, 30)

        self.label_waving_type = QLabel(self)
        self.label_waving_type.setText(u"布样所用织法：")
        self.label_waving_type.move(350, 250)
        self.label_waving_type.resize(150, 30)

        self.input_batch_size = QLineEdit(self)
        self.input_batch_size.setText(str(self.batch_size))
        self.input_batch_size.move(520, 300)
        self.input_batch_size.resize(100, 30)

        self.label_batch_size = QLabel(self)
        self.label_batch_size.setText(u"单批布采样次数：")
        self.label_batch_size.move(350, 300)
        self.label_batch_size.resize(150, 30)

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
        self.detect_thread = DetectTheard("undefined path", self.batch_size)
        self.detect_thread.chan.connect(self.Alert)
        self.detect_thread.proc.connect(self.ShowProc)
        self.detect_thread.finished_num.connect(self.ShowFinished)

    def init_from_config(self):
        self.tmp_path = Config.tmp_path
        self.rootPath = Config.rootPath
        self.device_id = Config.device_id
        self.name = Config.name
        self.date = Config.date
        self.location = Config.location
        self.fabric = Config.fabric
        self.waving_type = Config.waving_type
        self.batch_size = int(Config.batch_size)

    def save_config(self):
        self.tmp_path = self.input_temp_addr.text()
        self.rootPath = self.input_relocate_dir.text()
        self.device_id = self.input_device_id.text()
        self.name = self.input_collector_name.text()
        self.date = self.input_collect_date.text()
        self.location = self.input_collected_loc.text()
        self.fabric = self.input_fabric.text()
        self.waving_type = self.input_waving_type.text()
        self.batch_size = int(self.input_batch_size.text())
        with open("config.py", "w", encoding='utf-8') as f:
            f.write(f"tmp_path='{self.tmp_path }'\n")
            f.write(f"rootPath='{self.rootPath }'\n")
            f.write(f"device_id='{self.device_id }'\n")
            f.write(f"name='{self.name}'\n")
            f.write(f"date='{self.date}'\n")
            f.write(f"location='{self.location }'\n")
            f.write(f"fabric='{self.fabric}'\n")
            f.write(f"waving_type='{self.waving_type}'\n")
            f.write(f"batch_size='{self.batch_size}'\n")

    def Test(self):
        self.save_config()

        # if running, terminate background task
        if self.detect_thread.isRunning():
            self.DestroyDetectThread()
            return

        # if not running, start background task
        err_msg = self.detectConfigErr()
        if err_msg:
            QMessageBox.warning(self, "ERROR", err_msg)
            return
        self.RunDetectThread()

    def DestroyDetectThread(self):
        self.detect_thread.terminate()
        self.btn_start_detect.setStyleSheet("QpushButton{background:white}")

    def RunDetectThread(self):
        self.DestroyDetectThread()
        self.btn_start_detect.setStyleSheet('''QPushButton{background:red;}''')
        self.detect_thread.setConfig(self.tmp_path, self.batch_size)

        self.detect_thread.start()

    def ShowFinished(self, finished_num):
        self.DestroyDetectThread()
        reply = QMessageBox.warning(self,
                                    "消息框标题",
                                    f"{finished_num}个采样点已检测，是否转移？",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
                                    )

        if reply == QMessageBox.Yes:
            if self.Move():
                self.Test()
        else:
            pass

    def ShowProc(self, title):
        self.setWindowTitle(title)

    def Alert(self, notValidFile):
        self.DestroyDetectThread()
        reply = QMessageBox.warning(self,
                                    "消息框标题",
                                    f"{notValidFile}采样点出错，是否删除并重新检测？",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
                                    )

        if reply == QMessageBox.Yes:
            self.detect_thread.delete()
            self.Test()
        else:
            pass

    def make_despath(self):
        self.save_config()
        return make_despath(self.rootPath, self.device_id, self.name,
                            self.date, self.location, self.fabric, self.waving_type)

    # return err_msg,can_ignore
    def detectConfigErr(self):
        self.save_config()
        despath, dirname = self.make_despath()

        if not os.path.exists(self.rootPath):
            return "采样数据存放地址不存在！"
        if not self.device_id:
            return "采集设备编号不存在！"
        if not self.name:
            return "采集员姓名不存在！"
        if not self.date:
            return "采集日期不存在！"
        if not self.location:
            return "采集地点不存在！"
        if not self.device_id:
            return "采集设备编号不存在！"
        if not self.fabric:
            return "布匹成分不存在！"
        if not self.waving_type:
            return "编织方式不存在！"
        if not self.batch_size:
            return "采样次数不存在！"
        comp_err = self.checkCompErr()
        if comp_err:
            return comp_err
        if len(dirname.split("_")) != 10:
            return "组合的文件夹名未能以_分为10组"
        return None

    def checkCompErr(self):
        seg = self.fabric.split("_")
        if len(seg) != 5:
            return "布匹编号成分 未以_分为5组"
        comp, isLegal, total = get_components(seg[-1])
        if not isLegal:
            return f'布匹成分之和非100,而是{total}'
        return None

# return if continue to Test()

    def Move(self):

        despath, _ = self.make_despath()
        err_msg = self.detectConfigErr()
        if err_msg:
            QMessageBox.warning(self, "ERROR", err_msg)
            return False
        if os.path.exists(despath):
            reply = QMessageBox.warning(
                self, "ERROR", "目标地址地址已存在！可能是布样号重复,是否继续归档?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply != QMessageBox.Yes:
                return False
        move(self.tmp_path, self.rootPath, despath)
        return True

    def closeEvent(self, event):

        reply = QMessageBox.question(self, '信息', '确认退出吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class DetectTheard(QThread):
    chan = pyqtSignal(str)  # 损坏文件名
    proc = pyqtSignal(str)  # 处理进度,windowTitle
    finished_num = pyqtSignal(str)  # 已检测数量

    def __init__(self, tmp_path, batch_size):
        super().__init__()
        self.tmp_path = tmp_path
        self.batch_size = batch_size

    def setConfig(self, tmp_path, batch_size):
        self.tmp_path = tmp_path
        self.batch_size = batch_size

    def run(self):
        s = self.WaitForNotValidFile()
        if s:
            self.chan.emit(s)  # 计算结果完成后，发送结果

    def WaitForNotValidFile(self):
        cache = set()
        while True:
            self.proc.emit(f"布眼科技智能AI实时监测系统")
            # 检测文件数量达标
            if len(cache) >= 4*self.batch_size:
                self.finished_num.emit(str(len(cache)))
                return

            files = os.listdir(self.tmp_path)
            for file in files:
                if file in cache:
                    continue
                self.proc.emit(f"布眼科技智能AI实时监测系统 正在处理{file}")
                if '_r' in file or '_a' in file:
                    if not check(os.path.join(self.tmp_path, file)):
                        base_name = file.replace('_r', '').replace('_a', '')
                        self.bad_files = [base_name, base_name.replace('.', '_a.'), base_name.replace(
                            '.', '_i.'), base_name.replace('.', '_r.'), base_name.replace('.csv', '.dat')]
                        return file
                cache.add(file)
            time.sleep(1)

    def delete(self):
        for bad_file in self.bad_files:
            try:
                os.remove(os.path.join(self.tmp_path, bad_file))
            except Exception:
                pass
        return


def check(p):
    with open(p, encoding='utf-8') as f:
        col = np.loadtxt(f, str, delimiter=",", usecols=(1))
        data = np.array(col[29:], dtype=float)
        if float(max(data)) < 0.1 or not denoise(data):
            return False
    return True


def make_despath(rootPath, device_id, name, date, location, fabric, waving_type):
    dirname = f"{device_id}_{fabric}_{waving_type}_{name}_{date}_{location}"
    return os.path.join(rootPath, dirname), dirname


def move(tmp_path, rootPath, despath):

    if not os.path.exists(rootPath):
        os.mkdir(rootPath)
    if not os.path.exists(despath):
        os.mkdir(despath)
    currentList = os.listdir(tmp_path)
    for file in currentList:
        old_path = os.path.join(tmp_path, file)
        new_path = os.path.join(despath, file)
        if os.path.exists(new_path):
            os.remove(new_path)
        shutil.move(old_path, despath)


def get_components(seg):
    pattern = re.compile(r'([a-zA-Z]+[(\-|\+)?\d+(\.\d+)?]+)')  # 查找数字
    total = Decimal('0')
    components = pattern.findall(seg)
    dict = {}
    for i in range(len(components)):
        j = 0
        key = ""
        while j < len(components[i]) and components[i][j].isdigit() == False:
            key = "".join((key, components[i][j]))
            j += 1
        dict[key] = "".join((components[i][j:]))

    components = sorted(dict.items(), key=lambda k: float(k[1]), reverse=True)
    for k, v in components:
        total += Decimal(v)
    isLegal = True if total == Decimal('100') else False
    return components, isLegal, total


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    m = Main()
    m.show()
    m.resize(800, 500)
    app.exec()
