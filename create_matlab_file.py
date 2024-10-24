import numpy as np
from scipy.io import savemat
import scipy.io as sio
import os
import spikeinterface.full as si
import spikeinterface.extractors as se
import spikeinterface.preprocessing as spiketoolkit
import spikeinterface.widgets as sw
from convert_positions_in_tones import *
from utils_extraction import *
import spikeinterface
import zarr as zr
from  pathlib import Path
import tqdm
import spikeinterface.full as si
from spikeinterface.sortingcomponents.peak_detection import detect_peaks
from probeinterface import Probe, ProbeGroup
import matplotlib
import pickle

chemin = '/mnt/working4/clara/data2/eTheremin/ALTAI/' 
sessions = ['ALTAI_20240918_SESSION_00']  #list of sessions to be processed
save_path = '/mnt/working4/clara/data6/eTheremin/clara/'
nbr_channel = 32

chunk_size = 10**6  # ex: 1 million sample
fs = 30e3  # sampling frequency

matplotlib.use('Agg')

for session in sessions:
    print(session)
    path = chemin + session
    print(f"processing of {session}")
    final_save_path =  save_path + session +'/'
    path_f = path + '/headstage_0/'

    if os.path.exists(path_f + 'good_clusters.npy'):
        num_channel = np.load(path_f + 'good_clusters.npy', allow_pickle=True)
    else:
        num_channel = np.arange(nbr_channel)

    all_files_exist = all(os.path.exists(save_path + 'C' + str(k) + '.mat') for k in num_channel)
    if all_files_exist:
        print(f"All 'C' files for {session} already exist. Proceed to the next session.")
        continue  

    if os.path.exists(path_f + 'neural_data.npy'):

        neural_data = np.load(path_f + 'neural_data.npy')
        sig = neural_data
        full_raw_rec = se.NumpyRecording(traces_list=np.transpose(sig), sampling_frequency=fs)
        full_raw_rec = full_raw_rec.astype('float32')
        recording_cmr = si.common_reference(full_raw_rec, reference='global', operator='median')
        recording_f = si.bandpass_filter(recording_cmr, freq_min=300, freq_max=3000)  
        filtered_neural_signal = np.empty((neural_data.shape[1], neural_data.shape[0]), dtype=np.float32) 

        for start in range(0, neural_data.shape[1], chunk_size):

            end = min(start + chunk_size, neural_data.shape[1])  
            print(f"chunk processing from {start} to {end}")
            chunk_filtered = recording_f.get_traces(start_frame=start, end_frame=end).astype(np.float32)
            filtered_neural_signal[start:end, :] = chunk_filtered

        np.save(save_path + 'filtered_neural_data.npy', filtered_neural_signal)

        data_t = np.load(save_path + 'filtered_neural_data.npy', allow_pickle=True)
        data = data_t.transpose()  

        print(f"shape of filtered data : {data.shape}")
        print(f"Channel : {num_channel}")

        # Form of filtered data
        for k in num_channel:
            print(f"processing of channel {k}")
            data_C = data[k, :]
            print(f"data shape for channel {k} : {data_C.shape}")

            # Save as a .mat file
            data_dict = {'data': data_C, 'sr': fs}
            savemat(save_path + 'C' + str(k) + '.mat', data_dict)
            print(f"file C{k}.mat saved succesfully.")

    else:
        print(f"The neural data for the session {session} does not exist in {path_f}")
