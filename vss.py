import numpy as np
import soundfile as sf

# which_speaker: (elevation, azimuth)
# L: (0, -65)
# R: (0, 65)
# C: (0, 0)
# LFE: -
# Ls: (180, -20)
# Rs: (180, 20)
# RLS: (180, -55)
# RRS: (180, 55)
# FLU: (45, -30)
# FRU: (45, 30)
# RLU: (135, -30)
# RRU: (135, 30)
# 
# wav file 0 degree elevation = impulse_file[::8]
# wav file 180 degree elevation = impulse_file[::40]

################################# FUNCTIONS ####################################

def get_impulse():
    # return 3d_array = (row, column, which_array)
    # impulse = (which_speaker, ::, which_ear)

    # Left Ear
    ll, _ = sf.read(impulse_51['left_ear']['l_L']['hrir'])
    lr, _ = sf.read(impulse_51['left_ear']['l_R']['hrir'])
    lc, _ = sf.read(impulse_51['left_ear']['l_C']['hrir'])
    lls, _ = sf.read(impulse_51['left_ear']['l_LS']['hrir'])
    lrs, _ = sf.read(impulse_51['left_ear']['l_RS']['hrir'])
    lrls, _ = sf.read(impulse_51['left_ear']['l_RLS']['hrir'])
    lrrs, _ = sf.read(impulse_51['left_ear']['l_RRS']['hrir'])
    lflu, _ = sf.read(impulse_51['left_ear']['l_FLU']['hrir'])
    lfru, _ = sf.read(impulse_51['left_ear']['l_FRU']['hrir'])
    lrlu, _ = sf.read(impulse_51['left_ear']['l_RLU']['hrir'])
    lrru, _ = sf.read(impulse_51['left_ear']['l_RRU']['hrir'])

    # Right Ear
    rl, _ = sf.read(impulse_51['right_ear']['r_L']['hrir'])
    rr, _ = sf.read(impulse_51['right_ear']['r_R']['hrir'])
    rc, _ = sf.read(impulse_51['right_ear']['r_C']['hrir'])
    rls, _ = sf.read(impulse_51['right_ear']['r_LS']['hrir'])
    rrs, _ = sf.read(impulse_51['right_ear']['r_RS']['hrir'])
    rrls, _ = sf.read(impulse_51['right_ear']['r_RLS']['hrir'])
    rrrs, _ = sf.read(impulse_51['right_ear']['r_RRS']['hrir'])
    rflu, _ = sf.read(impulse_51['right_ear']['r_FLU']['hrir'])
    rfru, _ = sf.read(impulse_51['right_ear']['r_FRU']['hrir'])
    rrlu, _ = sf.read(impulse_51['right_ear']['r_RLU']['hrir'])
    rrru, _ = sf.read(impulse_51['right_ear']['r_RRU']['hrir'])

    # Get rid of lfe
    lfe = np.zeros(ll[8,:].shape)

    return np.array([[ll[8,:], lr[8,:], lc[8,:], lfe, lls[40,:], lrs[40,:], lrls[40,:], lrrs[40,:], lflu[16,:], lfru[16,:], lrlu[32,:], lrru[32,:]], [rl[8,:], rr[8,:], rc[8,:], lfe, rls[40,:], rrs[40,:], rrls[40,:], rrrs[40,:], rflu[16,:], rfru[16,:], rrlu[32,:], rrru[32,:]]])

def multichannel_convolution(x:np.array, impulse:np.array, channels:int):
    convolution_length = len(x[0,:]) + len(impulse[0, 0, :]) - 1
    multi_convolve = np.zeros((2, channels, convolution_length))

    for i in range(0, 2):
        for k in range(0, channels):
            multi_convolve[i,k,:] = np.convolve(x[k,:], impulse[i,k,:], mode='full')

    return multi_convolve

def convert_to_binaural(x:np.array, channels:int):
    # Add all left to left, all right to right
    
    binaural = np.zeros((2, len(x[0,0,:])))
    
    for i in range(0, 2):
        for k in range(0, channels):
            binaural[i] += x[i,k,:]

    return binaural * np.amax(signal_read) / np.amax(binaural) # Normalize to original volume

################################################################################


# Process File
if __name__ == "__main__":

    # sound_file = 'AMBIX-003_48k_7.1.4'
    sound_file = 'AMBIX-004_48k_7.1.4'
    signal = './Audio/Ambisonics/' + sound_file + '.wav'
    impulse_51 = {
        'left_ear': {
            'l_L': {
                'hrir': './HRTF/UCD_wavdb/subject10/neg65azleft.wav',
                'elevation': 8
            },
            'l_R': {
                'hrir': './HRTF/UCD_wavdb/subject10/65azleft.wav',
                'elevation': 8
            },
            'l_C': {
                'hrir': './HRTF/UCD_wavdb/subject10/0azleft.wav',
                'elevation': 8
            },
            'l_LS': {
                'hrir': './HRTF/UCD_wavdb/subject10/neg20azleft.wav',
                'elevation': 40
            },
            'l_RS': {
                'hrir': './HRTF/UCD_wavdb/subject10/20azleft.wav',
                'elevation': 40
            },
            'l_RLS': {
                'hrir': './HRTF/UCD_wavdb/subject10/neg55azleft.wav',
                'elevation': 40
            },
            'l_RRS': {
                'hrir': './HRTF/UCD_wavdb/subject10/55azleft.wav',
                'elevation': 40
            },
            'l_FLU': {
                'hrir': './HRTF/UCD_wavdb/subject10/neg30azleft.wav',
                'elevation': 16
            },
            'l_FRU': {
                'hrir': './HRTF/UCD_wavdb/subject10/30azleft.wav',
                'elevation': 16
            },
            'l_RLU': {
                'hrir': './HRTF/UCD_wavdb/subject10/neg30azleft.wav',
                'elevation': 32
            },
            'l_RRU': {
                'hrir': './HRTF/UCD_wavdb/subject10/30azleft.wav',
                'elevation': 32
            }
        },
        'right_ear': {
            'r_L': {
                'hrir': './HRTF/UCD_wavdb/subject10/neg65azright.wav',
                'elevation': 8
            },
            'r_R': {
                'hrir': './HRTF/UCD_wavdb/subject10/65azright.wav',
                'elevation': 8
            },
            'r_C': {
                'hrir': './HRTF/UCD_wavdb/subject10/0azright.wav',
                'elevation': 8
            },
            'r_LS': {
                'hrir': './HRTF/UCD_wavdb/subject10/neg20azright.wav',
                'elevation': 40
            },
            'r_RS': {
                'hrir': './HRTF/UCD_wavdb/subject10/20azright.wav',
                'elevation': 40
            },
            'r_RLS': {
                'hrir': './HRTF/UCD_wavdb/subject10/neg55azright.wav',
                'elevation': 40
            },
            'r_RRS': {
                'hrir': './HRTF/UCD_wavdb/subject10/55azright.wav',
                'elevation': 40
            },
            'r_FLU': {
                'hrir': './HRTF/UCD_wavdb/subject10/neg30azright.wav',
                'elevation': 16
            },
            'r_FRU': {
                'hrir': './HRTF/UCD_wavdb/subject10/30azright.wav',
                'elevation': 16
            },
            'r_RLU': {
                'hrir': './HRTF/UCD_wavdb/subject10/neg30azright.wav',
                'elevation': 32
            },
            'r_RRU': {
                'hrir': './HRTF/UCD_wavdb/subject10/30azright.wav',
                'elevation': 32
            }
        }
    }


    signal_read, sr = sf.read(signal)
    signal_read = np.swapaxes(signal_read, 1, 0)
    n_channel = signal_read.shape[0]
    hrirs = get_impulse()
    multi_convolve = multichannel_convolution(signal_read, hrirs, n_channel)
    binaural_out = np.swapaxes(convert_to_binaural(multi_convolve, n_channel), 0, 1)
    sf.write(f'{sound_file}_vss.wav', binaural_out, sr)
