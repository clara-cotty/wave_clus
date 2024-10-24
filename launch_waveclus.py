import subprocess
import os
import time
import numpy as np

sessions = ['ALTAI_20240822_SESSION_00']

for session in sessions:
    print(session)
    path = 'Y:/eTheremin/clara/' + session + '/'  
    if os.path.exists('Z:/eTheremin/ALTAI/' + session + '/' + 'headstage_0/good_clusters.npy'):
        good_channels = np.load('Z:/eTheremin/ALTAI/' + session + '/' + 'headstage_0/good_clusters.npy', allow_pickle = True)
    else : 
        good_channels = np.arange(32)
    

    print(good_channels)

    interval_verification = 0.5
    timeout_creation = 300  

    for channel in good_channels:


        fichier_mat = path +  'C' + str(channel) + '.mat'
        fichier_spikes = path + 'C' + str(channel) + '_spikes.mat'
        fichier_times = path + 'times_C' + str(channel) + '.mat'  # file created by Do_clustering

        # Commands for MATLAB
        wave_clus_get_spikes = f"matlab -nodesktop -nosplash -batch \"cd('{path}'); Get_spikes('{fichier_mat}');\""
        wave_clus_do_clustering = f"matlab -nodesktop -nosplash -batch \"cd('{path}'); Do_clustering('{fichier_spikes}');\""

        # Run the first wave_clus command with error redirection to a log file
        try:
            print("execution of Get_spikes for channel {channel}...")
            with open('log_get_spikes.txt', 'a') as log_file:
                subprocess.run(wave_clus_get_spikes, shell=True, check=True, stdout=log_file, stderr=log_file)
            print(f"Get_spikes has been executed successfully for channel {channel}.")
        except subprocess.CalledProcessError as e:
            print(f"Error during execution of Get_spikes for channel {channel} : {e}")
            exit(1)

        # Wait for the spikes file to be generated before launching Do_clustering
        while not os.path.exists(fichier_spikes):
            print(f"Waiting for the creation of {fichier_spikes} for channel {channel}...")
            time.sleep(interval_verification)

        # Execute the second wave_clus command with error redirection to a log file
        try:
            print(f"Executing Do_clustering for channel {channel}...")
            with open('log_do_clustering.txt', 'a') as log_file:
                subprocess.run(wave_clus_do_clustering, shell=True, check=True, stdout=log_file, stderr=log_file)
            print(f"Do_clustering executed successfully for channel {channel}.")
        except subprocess.CalledProcessError as e:
            print(f"Error during the execution of Do_clustering for channel {channel}: {e}")
            exit(1)

        # Wait for the "times_C" file to be created
        time_start = time.time()
        while not os.path.exists(fichier_times):
            if time.time() - time_start > timeout_creation:
                print(f"The file {fichier_times} was not created for channel {channel} after {timeout_creation} seconds.")
                exit(1)
            print(f"Waiting for the creation of {fichier_times} for channel {channel}...")
            time.sleep(interval_verification)

        print(f"The file {fichier_times} has been created successfully for channel {channel}.")
