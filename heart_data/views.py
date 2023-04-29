from django.shortcuts import render
from rest_framework.views import APIView
import numpy as np
import pandas as pd
import scipy.signal as signal
import matplotlib.pyplot as plt
from django.http import JsonResponse
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

# Create your views here.
class DataReader(APIView):
    def get(self, request):
        
        # Load ECG signal from CSV file
        print('here-------------------------')
        ecg_data = pd.read_csv('Lead2.csv')
        print(ecg_data)
        ecg_signal = ecg_data.iloc[:, 0].values
        print(ecg_signal, type(ecg_signal))
        # we get ecg_data is form of array from the mobile app 

        # Define sampling frequency
        fs = 454.54

        # 1. Amplitude scaling (Normalization)
        normalized_signal = (ecg_signal - np.min(ecg_signal)) / (np.max(ecg_signal) - np.min(ecg_signal))

        # 2. Baseline correction (High-pass filter)
        high_pass_filter = signal.butter(2, 0.5, 'highpass', fs=fs)
        baseline_corrected_signal = signal.filtfilt(high_pass_filter[0], high_pass_filter[1], normalized_signal)
        baseline_corrected_signal = baseline_corrected_signal - np.mean(baseline_corrected_signal)

        # 3. Low-pass filter
        low_pass_filter = signal.butter(4, 100, 'lowpass', fs=fs)
        filtered_signal = signal.filtfilt(low_pass_filter[0], low_pass_filter[1], baseline_corrected_signal)

        # 4. Rescale signal to original range
        rescaled_signal = filtered_signal * 2.93
        print(rescaled_signal,"--------------")
        #  We need to push rescaled_signal in mobile app 

        # # Plot the ECG Signal
        # t = np.arange(len(ecg_signal)) / fs
        # fig, ax = plt.subplots(4, 1, sharex=True, figsize=(12, 6))
        # ax[0].plot(t, ecg_signal, 'b-',linewidth=1, label='Original ECG')
        # ax[0].set_ylabel('Amplitude (mV)')
        # ax[0].legend(loc='best')
        # ax[1].plot(t, normalized_signal, 'g-', linewidth=1, label='Normalised Signal ECG')
        # ax[1].set_xlabel('Time (s)')
        # ax[1].set_ylabel('Amplitude (mV)')
        # ax[1].legend(loc='best')
        # ax[2].plot(t, baseline_corrected_signal, 'r-', linewidth=1,label='Filtered ECG')
        # ax[2].set_ylabel('Amplitude (mV)')
        # ax[2].legend(loc='best')
        # ax[3].plot(t, rescaled_signal, 'y-',linewidth=1, label='rescaled ECG')
        # ax[3].set_ylabel('Amplitude (mV)')
        # ax[3].legend(loc='best')
        # plt.show()
        return JsonResponse(rescaled_signal, stauts=200)