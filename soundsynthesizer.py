# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_slider2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import soundfile as sf
import pygame
import librosa
import numpy as np
import matplotlib.pyplot as plt
import copy

class Ui_MainWindow(object):

    def __init__(self):
        super().__init__()
        self.data = 0
        self.rate = 44100
        self._play = None
        self.tar_sr = 0
        self.temp_data = 0
        self.length_flag = 0
        self.y =0
        self.got_bin_value =0

    def load(self):
        dialog = QtWidgets.QFileDialog()
        self.fname = dialog.getOpenFileName(None, "Window name", "", "Wav Files (*.wav)")
        self.data, self.rate = sf.read(self.fname[0])
        self.temp_fname = self.fname[0]
        print(self.fname[0])

    def saveFileDialog(self):

        dialog = QtWidgets.QFileDialog()
        name = dialog.getSaveFileName(None, "Window name", "", "Wav Files (*.wav)")
        print(name[0])
        sf.write(name[0], self.y, self.tar_sr)



    def play_original(self):
        pygame.init()
        self._play = pygame.mixer.Sound(self.fname[0])
        self._play.play()
        print(self.fname[0])

    def display_length(self):
        self.duration = librosa.core.get_duration(y=self.data, sr=self.rate)
        print(self.duration, "seconds")

    def set_sampling_rate(self, text):
        t = text
        if t == "8000":
            self.tar_sr = 8000
        elif t == '11025':
            self.tar_sr = 11025
        elif t == '16000':
            self.tar_sr = 16000
        elif t == '22050':
            self.tar_sr = 22050
        elif t == '44100':
            self.tar_sr = 44100
        elif t == '48000':
            self.tar_sr = 48000
        elif t == '88200':
            self.tar_sr = 88200
        elif t == '96000':
            self.tar_sr = 96000
        else:
            self.tar_sr == self.rate
        print(self.tar_sr)

    def get_length(self, text):
        self.new_length = self.length_line_edit.text()

    def set_length(self):
        """
        This function Provides the Duration of the signal that needs to be set for the the audio.
        Takes the input from the linetext which is the duration that the signal needs to cut.

        # """
        self.length_flag = 1
        self.x = self.length_line_edit.text()
        print(type(self.x))
        self.i = float(self.x)  # Convert the string to float
        self.temp_data, self.lib_rate = librosa.core.load(self.fname[0], duration=self.i)
        self.duration = librosa.core.get_duration(y=self.temp_data, sr=self.lib_rate)
        print(self.duration)

    def ply_resampled(self):
        print("Start playing Changed ")

        if self.tar_sr == 0:
            self.tar_sr = self.rate
        print(self.tar_sr)
        if self.length_flag == 0:
            self.tar_data = librosa.core.resample(self.data, self.rate, self.tar_sr, res_type='kaiser_best')
            print("data")
        else:
            self.tar_data = librosa.core.resample(self.data, self.rate, self.tar_sr, res_type='kaiser_best')
            print("temp_data")
        sf.write('file_changed.wav', self.tar_data, self.tar_sr)
        pygame.init()
        _play = pygame.mixer.Sound("file_changed.wav")
        _play.play()

    def fft(self):

        self.data, self.rate = sf.read("file_changed.wav")
        self.N = len(self.data)  # length of the data
        self.T = 1.0 / self.rate  # delta T

        # Fourier transform
        self.FFT_data = np.fft.rfft(self.data)
        self.xf = np.linspace(0.0, 1.0 / (2.0 * self.T), self.N // 2)
        self.FFT_plot_data = copy.deepcopy(self.FFT_data)
        self.a = 2.0 / self.N * np.abs(self.FFT_plot_data[0:self.N // 2])
        # plt.plot(self.xf, self.a, 'r')
        # plt.grid()
        # plt.show()
        self.freq = np.fft.rfftfreq(self.N, d=1. / self.rate)
        self.magnitude_slider.setMaximum(np.abs(self.FFT_plot_data.max()))
        print("FFT")
        print(np.abs(self.FFT_plot_data.max()))

    def get_bins(self, text):

        self.got_bin_value = self.bin_line_edit.text()

    def get_mag_2(self):
        self.mag_2= self.mag_line_edit.text()
        print(self.mag_2)


    def get_freq_2(self):
        self.freq_2= self.freq_line_edit_2.text()
        print(self.freq_2)

    def number_samples_2(self):
        self.y =0
        self.num_samp = self.number_samples_line_edit.text()

    def set_y_data_2(self):
        self.num_samp = int(self.num_samp)
        print(self.num_samp)
        self.freq_2 = float(self.freq_2)
        self.mag_2 = float(self.mag_2)
        self.x_2 = np.linspace(0.0, self.num_samp * (1.0 / self.tar_sr), self.num_samp)
        self.y += (self.mag_2 * np.sin(self.freq_2 * 2.0 * np.pi * self.x_2))
        print(self.y)
        sf.write("test.wav", self.y, self.tar_sr)
        pygame.init()
        self._play = pygame.mixer.Sound("test.wav")
        self._play.play()
        # self.freq_2 =0
        # self.mag_2 =0

    def set_bin_value(self):
        self.got_bin_value = int(self.got_bin_value)
        print(self.got_bin_value)

    def amp_plot_2(self):
        T = 1.0/self.tar_sr
        self.yf_2 = np.fft.rfft(self.y)
        self.xf_2=np.linspace(0.0,1.0/(2.0*T),self.num_samp//2)
        plt.plot(self.xf_2, 2.0/self.num_samp *np.abs(self.yf_2[0:self.num_samp//2]))
        plt.grid()
        plt.show()


    def get_freq_idx(self):
        x = self.freq_line_edit.text()
        x = int(x)
        print(x)
        self.idx = (np.abs(self.freq - x)).argmin()
        print(self.freq[self.idx])

    def set_amplitude(self):
        if self.got_bin_value != 0:
            self.start_idx = self.idx
            self.stop_idx = self.idx + self.got_bin_value
            self.value = self.magnitude_slider.value()
            self.FFT_data[self.start_idx:self.stop_idx] = self.value
            print(self.FFT_data[self.start_idx:self.stop_idx])
        else:
            self.value = self.magnitude_slider.value()
            self.FFT_data[self.idx] = self.value
            print(self.FFT_data[self.idx], self.value)

    def replay_new_fft_data(self):

        # Convert back to time domain
        self.newdata = np.fft.irfft(self.FFT_data)

        # And save it to a new wave file
        sf.write(file="test.wav", data=self.newdata, samplerate=self.rate)
        self.b = 2.0 / self.N * np.abs(self.FFT_data[0:self.N // 2])
        print("IFFT")
        # plt.plot(self.xf,self.b)
        # plt.grid()
        # plt.show()

        pygame.init()
        _play = pygame.mixer.Sound("test.wav")
        _play.play()

    def plot_spectrums(self):
        plt.bar(self.xf, self.b)
        plt.bar(self.xf, self.a)
        plt.show()

    def amp_plot(self):

        plt.plot(self.xf, self.a)
        plt.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(844, 625)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.freq_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.freq_line_edit.setGeometry(QtCore.QRect(50, 360, 112, 27))
        self.freq_line_edit.setObjectName("freq_line_edit")
        self.btn_save_file = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save_file.setGeometry(QtCore.QRect(50, 470, 91, 31))
        self.btn_save_file.clicked.connect(self.saveFileDialog)
        self.btn_save_file.setObjectName("btn_save_file")
        self.sub_app_name = QtWidgets.QLabel(self.centralwidget)
        self.sub_app_name.setGeometry(QtCore.QRect(10, 230, 291, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.sub_app_name.setFont(font)
        self.sub_app_name.setObjectName("sub_app_name")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(390, 380, 56, 17))
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(600, 60, 101, 61))
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.length_text = QtWidgets.QLabel(self.widget)
        self.length_text.setObjectName("length_text")
        self.gridLayout_2.addWidget(self.length_text, 0, 0, 1, 1)
        self.length_line_edit = QtWidgets.QLineEdit(self.widget)
        self.length_line_edit.setObjectName("length_line_edit")
        self.gridLayout_2.addWidget(self.length_line_edit, 1, 0, 1, 1)
        self.magnitude_slider = QtWidgets.QSlider(self.centralwidget)
        self.magnitude_slider.setGeometry(QtCore.QRect(50, 393, 741, 18))
        self.magnitude_slider.setOrientation(QtCore.Qt.Horizontal)
        self.magnitude_slider.setObjectName("magnitude_slider")
        self.freq_text = QtWidgets.QLabel(self.centralwidget)
        self.freq_text.setGeometry(QtCore.QRect(18, 360, 25, 17))
        self.freq_text.setObjectName("freq_text")
        self.mag_text = QtWidgets.QLabel(self.centralwidget)
        self.mag_text.setGeometry(QtCore.QRect(18, 393, 26, 17))
        self.mag_text.setObjectName("mag_text")
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(20, 140, 298, 54))
        self.widget1.setObjectName("widget1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btn_FFT = QtWidgets.QPushButton(self.widget1)
        self.btn_FFT.setObjectName("btn_FFT")
        self.btn_FFT.clicked.connect(self.fft)
        self.gridLayout_3.addWidget(self.btn_FFT, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.bin_text = QtWidgets.QLabel(self.widget1)
        self.bin_text.setObjectName("bin_text")
        self.gridLayout.addWidget(self.bin_text, 0, 0, 1, 1)
        self.bin_line_edit = QtWidgets.QLineEdit(self.widget1)
        self.bin_line_edit.setObjectName("bin_line_edit")
        self.gridLayout.addWidget(self.bin_line_edit, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 1, 1, 1)
        self.btn_set_bins = QtWidgets.QPushButton(self.widget1)
        self.btn_set_bins.setObjectName("btn_set_bins")
        self.gridLayout_3.addWidget(self.btn_set_bins, 0, 2, 1, 1)
        self.widget2 = QtWidgets.QWidget(self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(22, 90, 565, 29))
        self.widget2.setObjectName("widget2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.btn_play_resampled_audio = QtWidgets.QPushButton(self.widget2)
        self.btn_play_resampled_audio.setObjectName("btn_play_resampled_audio")
        self.btn_play_resampled_audio.clicked.connect(self.ply_resampled)
        self.gridLayout_4.addWidget(self.btn_play_resampled_audio, 0, 0, 1, 1)
        self.btn_amplitude_plot = QtWidgets.QPushButton(self.widget2)
        self.btn_amplitude_plot.setObjectName("btn_amplitude_plot")
        self.btn_amplitude_plot.clicked.connect(self.amp_plot)
        self.gridLayout_4.addWidget(self.btn_amplitude_plot, 0, 2, 1, 1)
        self.btn_compare = QtWidgets.QPushButton(self.widget2)
        self.btn_compare.setObjectName("btn_compare")
        self.btn_compare.clicked.connect(self.plot_spectrums)
        self.gridLayout_4.addWidget(self.btn_compare, 0, 3, 1, 1)
        self.btn_PlaySythesizedAudio = QtWidgets.QPushButton(self.widget2)
        self.btn_PlaySythesizedAudio.setObjectName("btn_PlaySythesizedAudio")
        self.gridLayout_4.addWidget(self.btn_PlaySythesizedAudio, 0, 1, 1, 1)
        self.widget3 = QtWidgets.QWidget(self.centralwidget)
        self.widget3.setGeometry(QtCore.QRect(22, 52, 351, 35))
        self.widget3.setObjectName("widget3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget3)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.btn_load_audio = QtWidgets.QPushButton(self.widget3)
        self.btn_load_audio.setObjectName("btn_load_audio")
        self.btn_load_audio.clicked.connect(self.load)
        self.gridLayout_5.addWidget(self.btn_load_audio, 0, 0, 1, 1)
        self.btn_play = QtWidgets.QPushButton(self.widget3)
        self.btn_play.setObjectName("btn_play")
        self.btn_play.clicked.connect(self.play_original)
        self.gridLayout_5.addWidget(self.btn_play, 0, 1, 1, 1)
        self.btn_show_length = QtWidgets.QPushButton(self.widget3)
        self.btn_show_length.setObjectName("btn_show_length")
        self.btn_show_length.clicked.connect(self.display_length)
        self.gridLayout_5.addWidget(self.btn_show_length, 0, 2, 1, 1)
        self.sampling_rate_combo_box = QtWidgets.QComboBox(self.widget3)
        self.sampling_rate_combo_box.setObjectName("sampling_rate_combo_box")
        self.sampling_rate_combo_box.addItem("")
        self.sampling_rate_combo_box.addItem("")
        self.sampling_rate_combo_box.addItem("")
        self.sampling_rate_combo_box.addItem("")
        self.sampling_rate_combo_box.addItem("")
        self.sampling_rate_combo_box.addItem("")
        self.sampling_rate_combo_box.addItem("")
        self.sampling_rate_combo_box.addItem("")
        self.gridLayout_5.addWidget(self.sampling_rate_combo_box, 0, 3, 1, 1)
        self.sampling_rate_combo_box.activated[str].connect(self.set_sampling_rate)
        self.app_Name = QtWidgets.QLabel(self.centralwidget)
        self.app_Name.setGeometry(QtCore.QRect(208, 11, 204, 34))
        font = QtGui.QFont()
        font.setFamily("AnjaliOldLipi")
        font.setPointSize(18)
        font.setItalic(True)
        self.app_Name.setFont(font)
        self.app_Name.setObjectName("app_Name")
        self.widget4 = QtWidgets.QWidget(self.centralwidget)
        self.widget4.setGeometry(QtCore.QRect(50, 430, 206, 29))
        self.widget4.setObjectName("widget4")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.widget4)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.btn_set_freq = QtWidgets.QPushButton(self.widget4)
        self.btn_set_freq.setObjectName("btn_set_freq")
        self.btn_set_freq.clicked.connect(self.get_freq_idx)

        self.gridLayout_7.addWidget(self.btn_set_freq, 0, 0, 1, 1)
        self.btn_set_mag = QtWidgets.QPushButton(self.widget4)
        self.btn_set_mag.setObjectName("pushButton_3")
        self.gridLayout_7.addWidget(self.btn_set_mag, 0, 1, 1, 1)
        self.widget5 = QtWidgets.QWidget(self.centralwidget)
        self.widget5.setGeometry(QtCore.QRect(21, 262, 419, 87))
        self.widget5.setObjectName("widget5")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.widget5)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.samples_text = QtWidgets.QLabel(self.widget5)
        self.samples_text.setObjectName("samples_text")
        self.gridLayout_6.addWidget(self.samples_text, 0, 0, 1, 1)
        self.freq_mag_text = QtWidgets.QLabel(self.widget5)
        self.freq_mag_text.setObjectName("freq_mag_text")
        self.gridLayout_6.addWidget(self.freq_mag_text, 0, 1, 1, 2)
        self.number_samples_line_edit = QtWidgets.QLineEdit(self.widget5)
        self.number_samples_line_edit.setObjectName("number_samples_line_edit")
        self.gridLayout_6.addWidget(self.number_samples_line_edit, 1, 0, 1, 1)
        self.freq_line_edit_2 = QtWidgets.QLineEdit(self.widget5)
        self.freq_line_edit_2.setObjectName("freq_line_edit_2")
        self.gridLayout_6.addWidget(self.freq_line_edit_2, 1, 1, 1, 1)
        self.mag_line_edit = QtWidgets.QLineEdit(self.widget5)
        self.mag_line_edit.setObjectName("mag_line_edit")
        self.gridLayout_6.addWidget(self.mag_line_edit, 1, 2, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_6, 0, 0, 1, 3)
        self.btn_PlaySythesizedAudio_2 = QtWidgets.QPushButton(self.widget5)
        self.btn_PlaySythesizedAudio_2.clicked.connect(self.set_y_data_2)
        self.btn_PlaySythesizedAudio_2.setObjectName("btn_PlaySythesizedAudio_2")
        self.gridLayout_8.addWidget(self.btn_PlaySythesizedAudio_2, 1, 0, 1, 1)
        self.btn_amplitude_plot_2 = QtWidgets.QPushButton(self.widget5)
        self.btn_amplitude_plot_2.setObjectName("btn_amplitude_plot_2")
        self.btn_amplitude_plot_2.clicked.connect(self.amp_plot_2)
        self.gridLayout_8.addWidget(self.btn_amplitude_plot_2, 1, 1, 1, 1)
        self.btn_compare_2 = QtWidgets.QPushButton(self.widget5)
        self.btn_compare_2.setObjectName("btn_compare_2")
        self.gridLayout_8.addWidget(self.btn_compare_2, 1, 2, 1, 1)
        self.freq_line_edit.raise_()
        self.btn_PlaySythesizedAudio.raise_()
        self.btn_FFT.raise_()
        self.btn_set_bins.raise_()
        self.bin_line_edit.raise_()
        self.bin_text.raise_()
        self.btn_set_freq.raise_()
        self.btn_set_mag.raise_()
        self.btn_save_file.raise_()
        self.number_samples_line_edit.raise_()
        self.sub_app_name.raise_()
        self.samples_text.raise_()
        self.freq_line_edit_2.raise_()
        self.freq_mag_text.raise_()
        self.btn_PlaySythesizedAudio.raise_()
        self.btn_PlaySythesizedAudio_2.raise_()
        self.btn_amplitude_plot_2.raise_()
        self.btn_compare_2.raise_()
        self.label.raise_()
        self.mag_line_edit.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 844, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.magnitude_slider.valueChanged['int'].connect(self.label.setNum)
        self.number_samples_line_edit.textEdited['QString'].connect(self.number_samples_2)
        self.freq_line_edit_2.textEdited['QString'].connect(self.get_freq_2)
        self.mag_line_edit.textEdited['QString'].connect(self.get_mag_2)
        self.freq_line_edit.textEdited['QString'].connect(self.get_freq_idx)
        self.length_line_edit.textEdited['QString'].connect(self.get_length)
        self.bin_line_edit.textEdited['QString'].connect(self.get_bins)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_save_file.setText(_translate("MainWindow", "Save File"))
        self.sub_app_name.setText(_translate("MainWindow", "Create Audio with certain Parameters"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.length_text.setText(_translate("MainWindow", "Set Length"))
        self.freq_text.setText(_translate("MainWindow", "freq"))
        self.mag_text.setText(_translate("MainWindow", "Mag"))
        self.btn_FFT.setText(_translate("MainWindow", "Apply FT  "))
        self.bin_text.setText(_translate("MainWindow", "Enter the bin value"))
        self.btn_set_bins.setText(_translate("MainWindow", "Set bins"))
        self.btn_set_bins.clicked.connect(self.set_bin_value)
        self.btn_play_resampled_audio.setText(_translate("MainWindow", "Play resampled Audio"))
        self.btn_amplitude_plot.setText(_translate("MainWindow", "Amplitude Spectrum"))
        self.btn_compare.setText(_translate("MainWindow", "Compare Spectrums"))
        self.btn_PlaySythesizedAudio.setText(_translate("MainWindow", "Play Sythesized Audio"))
        self.btn_PlaySythesizedAudio.clicked.connect(self.replay_new_fft_data)
        self.btn_load_audio.setText(_translate("MainWindow", "Load Audio"))
        self.btn_play.setText(_translate("MainWindow", "Play"))
        self.btn_show_length.setText(_translate("MainWindow", "Show Length"))
        self.sampling_rate_combo_box.setItemText(0, _translate("MainWindow", "8000"))
        self.sampling_rate_combo_box.setItemText(1, _translate("MainWindow", "11025"))
        self.sampling_rate_combo_box.setItemText(2, _translate("MainWindow", "16000"))
        self.sampling_rate_combo_box.setItemText(3, _translate("MainWindow", "22050"))
        self.sampling_rate_combo_box.setItemText(4, _translate("MainWindow", "44100"))
        self.sampling_rate_combo_box.setItemText(5, _translate("MainWindow", "48000"))
        self.sampling_rate_combo_box.setItemText(6, _translate("MainWindow", "88200"))
        self.sampling_rate_combo_box.setItemText(7, _translate("MainWindow", "96000"))
        self.app_Name.setText(_translate("MainWindow", "Sound Synthesizer"))
        self.btn_set_freq.setText(_translate("MainWindow", "Set Frequency"))
        self.btn_set_mag.setText(_translate("MainWindow", "Set Magnitude"))
        self.btn_set_mag.clicked.connect(self.set_amplitude)
        self.samples_text.setText(_translate("MainWindow", "Enter The Number of samples "))
        self.freq_mag_text.setText(_translate("MainWindow", "Enter Freqencies and magnitudes "))
        self.btn_PlaySythesizedAudio_2.setText(_translate("MainWindow", "Play Sythesized Audio"))
        self.btn_amplitude_plot_2.setText(_translate("MainWindow", "Amplitude Spectrum"))
        self.btn_compare_2.setText(_translate("MainWindow", "Compare Spectrums"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

