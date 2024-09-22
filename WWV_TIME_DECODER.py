#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: WWV TIME SIGNAL DECODER
# Author: vhmg
# Copyright: 2024 Vicente Montecinos
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import WWV_TIME_DECODER_python_mod as python_mod  # embedded python module
import sip
import time
import threading



class WWV_TIME_DECODER(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "WWV TIME SIGNAL DECODER", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("WWV TIME SIGNAL DECODER")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "WWV_TIME_DECODER")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.prob1 = prob1 = 0
        self.time_date = time_date = python_mod.www_decoder(prob1)
        self.samp_rate = samp_rate = 48e3
        self.offset = offset = 1
        self.filter_taps = filter_taps = 64
        self.decoded = decoded = time_date
        self.decimation = decimation = 48

        ##################################################
        # Blocks
        ##################################################

        self.probSign1 = blocks.probe_signal_f()
        self._offset_range = qtgui.Range(0, 3, 0.01, 1, 200)
        self._offset_win = qtgui.RangeWidget(self._offset_range, self.set_offset, "Offset", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._offset_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._filter_taps_range = qtgui.Range(1, 64, 1, 64, 200)
        self._filter_taps_win = qtgui.RangeWidget(self._filter_taps_range, self.set_filter_taps, "Filter", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._filter_taps_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.root_raised_cosine_filter_0 = filter.fir_filter_fff(
            1,
            firdes.root_raised_cosine(
                1,
                (samp_rate/decimation),
                4,
                0.001,
                filter_taps))
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            (int(samp_rate/decimation*3)), #size
            samp_rate/decimation, #samp_rate
            "Signal Scope", #name
            3, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Before RRCF', 'After RRCF', 'Binary', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 2, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 0, 3, 4, 6)
        for r in range(0, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 9):
            self.top_grid_layout.setColumnStretch(c, 1)
        def _prob1_probe():
          while True:

            val = self.probSign1.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_prob1,val))
              except AttributeError:
                self.set_prob1(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (50))
        _prob1_thread = threading.Thread(target=_prob1_probe)
        _prob1_thread.daemon = True
        _prob1_thread.start()
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcc(decimation, firdes.low_pass_2(1,samp_rate,110,5,50), (-100), samp_rate)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self._decoded_tool_bar = Qt.QToolBar(self)

        if None:
            self._decoded_formatter = None
        else:
            self._decoded_formatter = lambda x: str(x)

        self._decoded_tool_bar.addWidget(Qt.QLabel("Decoded Time / Date:"))
        self._decoded_label = Qt.QLabel(str(self._decoded_formatter(self.decoded)))
        self._decoded_tool_bar.addWidget(self._decoded_label)
        self.top_grid_layout.addWidget(self._decoded_tool_bar, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-offset))
        self.audio_source_0 = audio.source(48000, 'BlackHole 2ch', True)
        self.audio_sink_0 = audio.sink(48000, 'HDMI', True)
        self.analog_agc_xx_0 = analog.agc_ff((2e-3), 1, 1.0, 65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.audio_source_0, 0), (self.audio_sink_0, 0))
        self.connect((self.audio_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.probSign1, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_add_const_vxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "WWV_TIME_DECODER")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_prob1(self):
        return self.prob1

    def set_prob1(self, prob1):
        self.prob1 = prob1
        self.set_time_date(python_mod.www_decoder(self.prob1))

    def get_time_date(self):
        return self.time_date

    def set_time_date(self, time_date):
        self.time_date = time_date
        self.set_decoded(self.time_date)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass_2(1,self.samp_rate,110,5,50))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate/self.decimation)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, (self.samp_rate/self.decimation), 4, 0.001, self.filter_taps))

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.blocks_add_const_vxx_0.set_k((-self.offset))

    def get_filter_taps(self):
        return self.filter_taps

    def set_filter_taps(self, filter_taps):
        self.filter_taps = filter_taps
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, (self.samp_rate/self.decimation), 4, 0.001, self.filter_taps))

    def get_decoded(self):
        return self.decoded

    def set_decoded(self, decoded):
        self.decoded = decoded
        Qt.QMetaObject.invokeMethod(self._decoded_label, "setText", Qt.Q_ARG("QString", str(self._decoded_formatter(self.decoded))))

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate/self.decimation)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, (self.samp_rate/self.decimation), 4, 0.001, self.filter_taps))




def main(top_block_cls=WWV_TIME_DECODER, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
