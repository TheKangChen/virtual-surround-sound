import numpy as np
import sys
import soundfile as sf
import pyaudio
import json

# 5.1 angles = {L: -30, C: 0, R: 30, Ls: -120, Rs: 120}
# which_speaker: (elevation, azimuth)
# L: (0, -30)
# C: (0, 0)
# R: (0, 30)
# Ls: (180, -60)
# Rs: (180, 60)
# 
# wav file 0 degree elevation = impulse_file[::8]
# wav file 180 degree elevation = impulse_file[::40]

sound_file = 'Parking Garage'
signal = './Audio/' + sound_file + '.wav'
impulse_51 = {
    'left_ear': {
        'l_left': {
            'hrir': './HRTF/UCD_wavdb/subject10/neg30azleft.wav',
            'elevation': 8
        },
        'l_center': {
            'hrir': './HRTF/UCD_wavdb/subject10/0azleft.wav',
            'elevation': 8
        },
        'l_right': {
            'hrir': './HRTF/UCD_wavdb/subject10/30azleft.wav',
            'elevation': 8
        },
        'l_left_surround': {
            'hrir': './HRTF/UCD_wavdb/subject10/neg65azleft.wav',
            'elevation': 40
        },
        'l_right_surround': {
            'hrir': './HRTF/UCD_wavdb/subject10/65azleft.wav',
            'elevation': 40
        }
    },
    'right_ear': {
        'r_left': {
            'hrir': './HRTF/UCD_wavdb/subject10/neg30azright.wav',
            'elevation': 8
        },
        'r_center': {
            'hrir': './HRTF/UCD_wavdb/subject10/0azright.wav',
            'elevation': 8
        },
        'r_right': {
            'hrir': './HRTF/UCD_wavdb/subject10/30azright.wav',
            'elevation': 8
        },
        'r_left_surround': {
            'hrir': './HRTF/UCD_wavdb/subject10/neg65azright.wav',
            'elevation': 40
        },
        'r_right_surround': {
            'hrir': './HRTF/UCD_wavdb/subject10/65azright.wav',
            'elevation': 40
        }
    }
}

################################# FUNCTIONS ####################################

def get_impulse():
    # return 3d_array = (row, column, which_array)
    # impulse = (which_speaker, ::, which_ear)

    # Left Ear
    ll = sf.read(impulse_51['left_ear']['l_left']['hrir'])
    lc = sf.read(impulse_51['left_ear']['l_center']['hrir'])
    lr = sf.read(impulse_51['left_ear']['l_right']['hrir'])
    lls = sf.read(impulse_51['left_ear']['l_left_surround']['hrir'])
    lrs = sf.read(impulse_51['left_ear']['l_right_surround']['hrir'])

    # Right Ear
    rl = sf.read(impulse_51['right_ear']['r_left']['hrir'])
    rc = sf.read(impulse_51['right_ear']['r_center']['hrir'])
    rr = sf.read(impulse_51['right_ear']['r_right']['hrir'])
    rls = sf.read(impulse_51['right_ear']['r_left_surround']['hrir'])
    rrs = sf.read(impulse_51['right_ear']['r_right_surround']['hrir'])

    return np.array([[ll[0][8], lc[0][8], lr[0][8], lls[0][40], lrs[0][40]], [rl[0][8], rc[0][8], rr[0][8], rls[0][40], rrs[0][40]]])

def multichannel_convolution(x:np.array, impulse:np.array):
    # spit out shape(5,:,2) 3darray
    multi_convolve = np.zeros((2, 5, (len(x[0,:]) + len(impulse[0, 0, :]) - 1)))

    for i in range(0, 2):
        for k in range(0, 5):
            multi_convolve[i,k,:] = np.convolve(x[k,:], impulse[i,k,:], mode='full')

    return multi_convolve

def convert_to_binaural(x:np.array):
    # Add all left to left, all right to right
    
    binaural = np.zeros((2, len(x[0,0,:])))
    
    for i in range(0, 2):
        for k in range(0, 5):
            binaural[i] += x[i,k,:]

    return binaural / np.amax(binaural) # Normalize

################################################################################


# Process File
signal_read, fs = sf.read(signal)
signal_read = np.swapaxes(signal_read, 1, 0)
hrirs = get_impulse()
multichannel_convolution = multichannel_convolution(signal_read, hrirs)
binaural_out = np.swapaxes(convert_to_binaural(multichannel_convolution), 0, 1)
sf.write(f'{sound_file}_vss.wav', binaural_out, fs)
