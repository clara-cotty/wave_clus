from functions_get_data import *
import numpy as np
from utils_extraction import get_session_type_final
from utils_tt import *
from spike_sorting import *

# ARGUMENTS
fs = 30e3
t_pre = 0.2#0.2
t_post = 0.50#0.300
bin_width = 0.005
freq_min = 3 #Hz
psth_bins = np.arange(-t_pre, t_post + bin_width, bin_width)

sessions = ['ALTAI_20240806_SESSION_00','ALTAI_20240807_SESSION_00']

for session in sessions:

    # path = 'Z:/eTheremin/OSCYPEK/OSCYPEK/OSCYPEK_20240710_SESSION_00/headstage_0' 
    chemin  = '/mnt/working4/clara/data2/eTheremin/ALTAI/' + session + '/'

    #num_channel = [31, 30, 16, 14,  1, 23, 29,  5, 17, 27, 25,  8, 28, 26,3,  2,  6, 20]
    if os.path.exists(chemin + 'headstage_0' + '/good_clusters.npy'):
        num_channel = np.load(chemin + 'headstage_0' + '/good_clusters.npy', allow_pickle = True)
    else : 
        num_channel = np.arange(32)
    print(num_channel)
    save_path = '/mnt/working4/clara/data6/eTheremin/clara/' + session + '/'#+ 'filtered/std.min =5 bis/'
    nd = np.load(chemin + 'headstage_0/' + 'neural_data.npy', allow_pickle=True)
    # mock=False
    # #session_type = get_session_type_final(path)
    # #print(session_type)
    # #session_type = 'Playback' #TrackingOnly ou PbOnly
    duree_session = len(nd[0])/30000
    nbr_spikes_min = duree_session*freq_min


    # vérifier qu'il n existe pas de tt.pkl, s'il n''existe pas alors on le créée, sinon c'est pas la peine.
    # get_session_type pour le session_type

    
    #2. Créer le data.npy et features.npy
    #create_data_features_mock(path+'headstage_0/', bin_width, sr, mock=False)

    # version test de spike_sorting
    # mat_file = 'Z:/eTheremin/OSCYPEK/OSCYPEK/OSCYPEK_20240710_SESSION_00/spike_sorting/times_C' + str(channel) + '.mat'
    # npy_file = 'Z:/eTheremin/OSCYPEK/OSCYPEK/OSCYPEK_20240710_SESSION_00/spike_sorting/times_C' + str(channel) + '.npy'

    
    create_spikes_clusters(save_path, num_channel,nbr_spikes_min) #créer deux gros fichiers spike_times et spike_cluster
    create_data_features_ss(save_path,  bin_width, fs, mock=False)
