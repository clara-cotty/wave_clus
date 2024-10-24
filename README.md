Steps to use wave_clus :

to download wave_clus follow the README of https://github.com/csn-le/wave_clus

1) launch create_matlab_file which take has input neural_data.npy file and gives has output the file filtered filtered_neural_data
and the files C{number_channel}.mat for all the channels.

2) modify wave_clus parameters (file set_parameters.m from https://github.com/csn-le/wave_clus)

3) launch launch_waveclus.py which takes as input the C{number_channel}.mat files and gives as output C{number_channel}_spikes,
times_C{number_channel}.mat and screenshot of wave_clus' spike sorting.
times_C{number_channel}.mat is a matrix where rows are the number of points and each point is defined by [cluster,times].

note on certain parameters :
  - par.detection = 'neg' It might be a good idea not to choose 'both' this as it tends to divide into irrelevant clusters.
  - par.stdmin =  3.5  (the optimum value may vary between 3.5 and 4.5 depending on the signal)
  - par.min_clus = 1000 (to avoid the creation of clusters with very little spike in it)




