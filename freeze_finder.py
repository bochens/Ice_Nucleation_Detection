import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy import signal
from os.path import isfile, join, basename
from scipy.signal import savgol_filter
from scipy.fft import fft, ifft, rfft, irfft



input_file = "/Users/bochen/TAMU/Ice nucleation detection/fucoxanthin 5mgml/output_brightness/gss_table_brightness_corrected.csv"
output_dir = "/Users/bochen/TAMU/Ice nucleation detection/fucoxanthin 5mgml/output_brightness/brightness_corrected_result"


str_array = np.loadtxt(input_file, delimiter = ",", dtype=str)

print(str_array.shape)

filename_array = str_array[:, 0]
datetime_array = str_array[:, 1]
grayscale_data = str_array[:, 2:].astype(float)

print(grayscale_data.shape)


for j in np.arange(grayscale_data.shape[1]):

    with open(join(output_dir, "freezing_output.csv"), 'a') as the_file:
        the_file.write(str(j))
        the_file.write("\n")

    g_data = grayscale_data[:, j]

    #fig = plt.figure()
    #plt.plot(np.arange(len(g_data)), g_data)e

    kernel_size = 20
    kernel = np.ones(kernel_size) / kernel_size

    g_daray = np.convolve(g_data, kernel, mode='same') # moving average
    #g_daray = savgol_filter(g_data, 51, polyorder = 2, deriv=0)
    #g_daray = g_data

    g_daray -= np.average(g_daray)
    g_data_centered = g_data - np.average(g_data)

    step = np.hstack((np.ones(len(g_daray)), -1*np.ones(len(g_daray))))
    up_step = np.hstack((-1*np.ones(len(g_daray)), np.ones(len(g_daray))))
    slant_step = np.hstack(((np.arange(len(g_daray))*(-1/len(g_daray))+2), (np.arange(len(g_daray))*(1/len(g_daray))-1) ))

    g_daray_step = np.convolve(g_daray, step, mode='valid')
    #g_daray_step = np.convolve(g_data_centered, step, mode='valid')
    

    y = g_daray
    dy = np.diff(y)
    dy_mv = np.convolve(dy, kernel, mode='same') # moving average
    ddy = np.diff(dy_mv) * 10000

    dy_convolve = np.convolve(dy, slant_step, mode='valid')

    #peaks = signal.find_peaks(-g_daray, width=10, prominence=1E4)[0]
    peaks = signal.find_peaks(-g_daray_step, width=10, prominence=1E5)[0]
    #peaks = signal.find_peaks(-dy, width=10, prominence=1E3)[0]
    #peaks = signal.find_peaks(-ddy, width=20, prominence=1E3)[0]

    fig1 = plt.figure(figsize=[10, 5])
    plt.plot(np.arange(len(g_daray)), g_data_centered*100)
    plt.plot(np.arange(len(g_daray)), g_daray*100)
    plt.plot(np.arange(len(g_daray_step)), g_daray_step)
    #plt.plot(np.arange(len(dy)), dy*1000, color = 'y')
    #plt.plot(np.arange(len(ddy)), ddy)
    
    
    print(peaks)
    for i in range(len(peaks)):
        plt.axvline(x = peaks[i], color='r')
        with open(join(output_dir, "freezing_output.csv"), 'a') as the_file:
            the_file.write(str(peaks[i]))
            the_file.write(" ,")
            the_file.write(str(filename_array[peaks[i]]))
            the_file.write(" ,")
            the_file.write(str(datetime_array[peaks[i]]))
            the_file.write("\n")

    plt.savefig(join(output_dir, str(j)+".png"), dpi=300)

plt.show()