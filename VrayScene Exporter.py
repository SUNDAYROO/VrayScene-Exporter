import winreg
import os
import subprocess
import time
import psutil
import threading

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFileDialog, QStatusBar, QMessageBox, QComboBox, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"VrScene Exporter")
        Dialog.resize(474, 235)
        self.OutputPath_T = QLabel(Dialog)
        self.OutputPath_T.setObjectName(u"OutputPath_T")
        self.OutputPath_T.setGeometry(QRect(10, 80, 71, 16))
        self.Title_T = QLabel(Dialog)
        self.Title_T.setObjectName(u"Title_T")
        self.Title_T.setGeometry(QRect(160, 10, 121, 16))
        self.StartF_T = QLabel(Dialog)
        self.StartF_T.setObjectName(u"StartF_T")
        self.StartF_T.setGeometry(QRect(10, 140, 71, 16))
        self.EndF_T = QLabel(Dialog)
        self.EndF_T.setObjectName(u"EndF_T")
        self.EndF_T.setGeometry(QRect(220, 140, 61, 16))
        self.MayaScene_E = QLineEdit(Dialog)
        self.MayaScene_E.setObjectName(u"MayaScene_E")
        self.MayaScene_E.setGeometry(QRect(90, 50, 321, 21))
        self.StartF_E = QLineEdit(Dialog)
        self.StartF_E.setObjectName(u"StartF_E")
        self.StartF_E.setGeometry(QRect(90, 140, 110, 21))
        self.EndF_E = QLineEdit(Dialog)
        self.EndF_E.setObjectName(u"EndF_E")
        self.EndF_E.setGeometry(QRect(300, 140, 110, 21))
        self.MayaScene_B = QPushButton(Dialog)
        self.MayaScene_B.setObjectName(u"MayaScene_B")
        self.MayaScene_B.setGeometry(QRect(420, 50, 31, 24))
        self.OuputPath_E = QLineEdit(Dialog)
        self.OuputPath_E.setObjectName(u"OuputPath_E")
        self.OuputPath_E.setGeometry(QRect(90, 80, 321, 21))
        self.MayaScene_T = QLabel(Dialog)
        self.MayaScene_T.setObjectName(u"MayaScene_T")
        self.MayaScene_T.setGeometry(QRect(10, 50, 71, 16))
        self.Camera_T = QLabel(Dialog)
        self.Camera_T.setObjectName(u"Camera_T")
        self.Camera_T.setGeometry(QRect(10, 110, 71, 16))
        self.Camera_E = QComboBox(Dialog)
        self.Camera_E.setObjectName(u"comboBox")
        self.Camera_E.setGeometry(QRect(90, 110, 321, 21))

        self.OuputPath_B = QPushButton(Dialog)
        self.OuputPath_B.setObjectName(u"OuputPath_B")
        self.OuputPath_B.setGeometry(QRect(420, 80, 31, 24))
        self.Camera_B = QPushButton(Dialog)
        self.Camera_B.setObjectName(u"Camera_B")
        self.Camera_B.setGeometry(QRect(420, 110, 31, 24))
        self.Run_B = QPushButton(Dialog)
        self.Run_B.setObjectName(u"Run_B")
        self.Run_B.setGeometry(QRect(300, 190, 51, 24))
        self.Stop_B = QPushButton(Dialog)
        self.Stop_B.setObjectName(u"Stop_B")
        self.Stop_B.setGeometry(QRect(360, 190, 51, 24))
        QWidget.setTabOrder(self.MayaScene_E, self.MayaScene_B)
        QWidget.setTabOrder(self.MayaScene_B, self.OuputPath_E)
        QWidget.setTabOrder(self.OuputPath_E, self.OuputPath_B)
        QWidget.setTabOrder(self.OuputPath_B, self.StartF_E)
        QWidget.setTabOrder(self.StartF_E, self.EndF_E)
        QWidget.setTabOrder(self.EndF_E, self.Run_B)


        self.MayaScene_B.clicked.connect(self.selectMayaScene)
        self.OuputPath_B.clicked.connect(self.selectOutputPath)
        self.Run_B.clicked.connect(self.onRunClicked)
        self.Stop_B.clicked.connect(self.onStopClicked)
        self.Camera_B.clicked.connect(self.addCustomCamera)


        # 상태바 추가
        self.statusBar = QStatusBar(Dialog)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.setGeometry(QRect(0, 215, 474, 20))
        self.statusBar.showMessage("Ready")

        self.process = None  # 프로세스 저장을 위한 변수 추가


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.OutputPath_T.setText(QCoreApplication.translate("Dialog", u"Output Path", None))
        self.Title_T.setText(QCoreApplication.translate("Dialog", u"VrayScene Exporter", None))
        self.StartF_T.setText(QCoreApplication.translate("Dialog", u"Start Frame", None))
        self.EndF_T.setText(QCoreApplication.translate("Dialog", u"End Frame", None))
        self.MayaScene_B.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.MayaScene_T.setText(QCoreApplication.translate("Dialog", u"Maya Scene", None))
        self.OuputPath_B.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.Camera_B.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.Camera_T.setText(QCoreApplication.translate("Dialog", u"Camera", None))
        self.Run_B.setText(QCoreApplication.translate("Dialog", u"Run", None))
        self.Stop_B.setText(QCoreApplication.translate("Dialog", u"Stop", None))

    # retranslateUi

    def selectMayaScene(self):
        file_name, _ = QFileDialog.getOpenFileName(None, "Select Maya Scene", "", "Maya Files (*.ma *.mb)")
        if file_name:
            print(f"선택된 마야 파일: {file_name}")  # 파일 선택 디버깅
            self.MayaScene_E.setText(file_name)
            self.populateCameraComboBox(file_name)  # 카메라 목록을 채우기 위해 파일 경로 전달

    def populateCameraComboBox(self, maya_file):
        file_extension = os.path.splitext(maya_file)[1].lower()
        if file_extension == ".ma":
            cameras = self.getMayaFileCameras(maya_file)
            if cameras:
                self.updateCameraComboBox(cameras)
        elif file_extension == ".mb":
            # .mb 파일의 경우, getMayaFileCameras 함수 내에서
            # 카메라 목록이 준비되면 updateCameraComboBox 함수가 자동으로 호출됩니다.
            self.getMayaFileCameras(maya_file)
    def updateCameraComboBox(self, cameras):
        self.Camera_E.clear()
        for camera in cameras:
            self.Camera_E.addItem(camera)

    def getMayaFileCameras(self, maya_file):
        file_extension = os.path.splitext(maya_file)[1].lower()
        if file_extension == ".ma":
            # .ma 파일 처리 로직
            try:
                with open(maya_file, 'r') as file:
                    cameras = []
                    for line in file:
                        if "createNode camera" in line:
                            parent_name = line.split('-p')[1].split(';')[0].strip(' "')
                            cameras.append(parent_name)
                    return cameras
            except Exception as e:
                print(f"마야 파일(.ma) 읽기 중 오류 발생: {e}")
        elif file_extension == ".mb":
            # 스레드를 시작하여 Maya 스크립트를 비동기적으로 실행
            thread = threading.Thread(target=self.runMayaScript, args=(maya_file,))
            thread.start()

    def runMayaScript(self, maya_file):
        try:
            self.statusBar.showMessage("Loading Cameras...")
            script = f'''
import maya.standalone
import maya.cmds as cmds

maya.standalone.initialize(name='python')

cmds.file("{maya_file}", open=True, force=True, prompt=False, loadNoReferences=True)

cameras = cmds.ls(type='camera')
camera_names = [cam[:-5] if cam.endswith('Shape') else cam for cam in cameras]

print("Cam List :")
for cam in camera_names:
    print(cam)
print("Cam List End")

maya.standalone.uninitialize()
'''
            # Windows에서 콘솔 창을 숨기기 위한 설정
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            script_path = 'temp_maya_script.py'
            with open(script_path, 'w') as file:
                file.write(script)

            process = subprocess.Popen(['mayapy', script_path],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       startupinfo=startupinfo)
            stdout, stderr = process.communicate()  # 프로세스의 결과를 받아옴

            if process.returncode == 0:
                output = stdout.decode('utf-8', errors='ignore').strip()
                camera_list_start = output.find("Cam List :") + len("Cam List :")
                camera_list_end = output.find("Cam List End", camera_list_start)
                camera_lines = output[camera_list_start:camera_list_end].strip().split('\n')
                cameras = [line.strip() for line in camera_lines if line.strip() and not line.startswith("00:00")]
                if "Came List End" in cameras:
                    cameras.remove("Came List End")
                self.updateCameraComboBox(cameras)

            else:
                print(f"마야 스크립트 실행 중 오류 발생: {stderr.decode('utf-8', errors='ignore')}")

            os.remove(script_path)
            self.statusBar.showMessage("Ready")

        except Exception as e:
            print(f"스크립트 실행 중 예외 발생: {e}")
            self.statusBar.showMessage("Error")

    def addCustomCamera(self):
        dialog = CameraDialog()
        if dialog.exec():
            camera_name = dialog.getCameraName()
            if camera_name:
                self.Camera_E.addItem(camera_name)
    def selectOutputPath(self):
        # 파일 저장 대화 상자를 열어 사용자가 파일 이름을 입력하고 저장 위치를 선택하게 합니다.
        file_name, _ = QFileDialog.getSaveFileName(None, "Save VrayScene File", "", "VrayScene Files (*.vrscene)")
        if file_name:
            # 파일 이름에 .vrscene 확장자가 없으면 추가합니다.
            if not file_name.endswith(".vrscene"):
                file_name += ".vrscene"
            self.OuputPath_E.setText(file_name)

    def find_maya_install_path(self):
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, '.ma') as key:
                program_name = winreg.QueryValue(key, None)

            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, f'{program_name}\\shell\\open\\command') as key:
                command_path, _ = winreg.QueryValueEx(key, "")
                maya_bin_path = command_path.split('"')[1]
                return os.path.dirname(maya_bin_path)
        except Exception as e:
            print(f"Maya 실행 파일 경로를 찾는 데 실패했습니다: {e}")
            return None

    def set_environment_variable(self, name, value):
        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Environment")
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)
            return True
        except Exception as e:
            print(f"환경 변수 설정 실패: {e}")
            return False

    def add_to_system_path(self, new_path):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ) as key:
                current_path, _ = winreg.QueryValueEx(key, "PATH")
            if new_path not in current_path:
                updated_path = f"{new_path};{current_path}"
                self.set_environment_variable("PATH", updated_path)
                print(f"시스템 PATH에 추가됨: {new_path}")
            else:
                print("이미 시스템 PATH에 존재함")
        except Exception as e:
            print(f"시스템 PATH 업데이트 실패: {e}")

    def onRunClicked(self):
        # Maya 설치 경로를 환경변수로 설정
        maya_path = self.find_maya_install_path()
        if maya_path:
            self.set_environment_variable("MAYA_DIR", maya_path)
            self.add_to_system_path(maya_path)

        # 사용자 입력에 따라 명령어 생성
        output_path = self.OuputPath_E.text()
        maya_scene = self.MayaScene_E.text()
        selected_camera = self.Camera_E.currentText()
        start_frame = self.StartF_E.text()
        end_frame = self.EndF_E.text()

        command = f'Render.exe -r vray -cam "{selected_camera}" -exportFileName "{output_path}" -noRender -s {start_frame} -e {end_frame} -exportFramesSeparate "{maya_scene}"'

        base_output_path = os.path.splitext(output_path)[0]
        final_output_file = f"{base_output_path}_{end_frame.zfill(4)}.vrscene"
        self.statusBar.showMessage("Running...")
        threading.Thread(target=self.runCommand, args=(command, final_output_file)).start()
        print(final_output_file)

        # 명령어 실행
        try:
            self.process = subprocess.Popen(command, shell=True)

            print("명령어 실행 중...")
        except Exception as e:
            print(f"명령어 실행 중 오류 발생: {e}")

    def runCommand(self, command, final_output_file):
        try:
            # 최종 파일의 존재 여부를 체크
            while not os.path.exists(final_output_file):
                time.sleep(5)  # 5초 간격으로 체크

            # 파일이 존재하면 Done 메시지 표시
            self.statusBar.showMessage("Done")

        except Exception as e:
            print(f"명령어 실행 중 오류 발생: {e}")
            self.statusBar.showMessage("Error")

    def onStopClicked(self):
        if self.process and self.process.poll() is None:
            try:
                parent = psutil.Process(self.process.pid)
                for child in parent.children(recursive=True):  # 모든 자식 프로세스 찾기
                    child.terminate()  # 자식 프로세스 종료
                parent.terminate()  # 부모 프로세스 종료
            except psutil.NoSuchProcess:
                print("프로세스가 이미 종료되었습니다.")
            finally:
                self.process = None
                self.statusBar.showMessage("Stopped")
        else:
            print("실행 중인 프로세스가 없습니다.")

class CameraDialog(QDialog):
    def __init__(self, parent=None):
        super(CameraDialog, self).__init__(parent)
        self.setWindowTitle("Camera")
        self.setGeometry(100, 100, 239, 119)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.setGeometry(80, 70, 51, 24)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setGeometry(150, 70, 61, 24)

        self.camera_name_edit = QLineEdit(self)
        self.camera_name_edit.setGeometry(80, 20, 131, 20)

        self.label = QLabel("Camera", self)
        self.label.setGeometry(10, 20, 71, 16)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def getCameraName(self):
        return self.camera_name_edit.text()


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

# QApplication 인스턴스 생성
app = QApplication([])

# MyDialog 인스턴스 생성 및 실행
dialog = MyDialog()
dialog.show()

# 애플리케이션 이벤트 루프 시작
app.exec()