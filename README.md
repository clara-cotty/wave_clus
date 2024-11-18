Steps to use wave_clus :

to download wave_clus follow the README of https://github.com/csn-le/wave_clus

1) launch create_matlab_file which take has input neural_data.npy file and gives has output the file filtered_neural_data
and the files C{number_channel}.mat for all the channels.

2) modify wave_clus parameters (file set_parameters.m from https://github.com/csn-le/wave_clus)

3) launch launch_waveclus.py which takes as input the C{number_channel}.mat files and gives as output C{number_channel}_spikes,
times_C{number_channel}.mat and screenshot of wave_clus' spike sorting.
times_C{number_channel}.mat is a matrix where rows are the number of points and each point is defined by [cluster,times].

Note on certain parameters :
  - par.detection = 'neg' It might be a good idea not to choose 'both' because it tends to divide into irrelevant clusters.
  - par.stdmin =  3.5  (the optimum value may vary between 3.5 and 4.5 depending on the signal)
  - par.min_clus = 1000 (to avoid the creation of clusters with very little spike in it)

Temperature serves as an indicator of the quality of the clusters found. The graph is in the figure at bottom left of the screenshots. When wave_clus finds several clusters, they will be relevant if the corresponding colored points are not located at T = 0.

Warning : even if cluster 0 has only very few spikes it will appears in the file times_C{number_channel}.mat





