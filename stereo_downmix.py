import numpy as np
import soundfile as sf


# 5.0 format = (L, C, R, Ls, Rs)
# Down mix method reference Dolby website: https://professionalsupport.dolby.com/s/article/How-do-the-5-1-and-Stereo-downmix-settings-work?language=en_US
# Lo = L + (–3 dB × C) + (–3 dB × Ls)
# Ro = R + (–3 dB × C) + (–3 dB × Rs)

def minus_x_db(input, db):
    def db_to_amplitude(x):
        return 10 ** (x / 20)
    
    return input * ((np.amax(input) - db_to_amplitude(db)) / np.amax(input))

def downmix_to_stereo(x):
    length = len(x[0,:])

    stereo = np.zeros((2, length))
    stereo[0,:] = x[0,:] + minus_x_db(x[1,:], 3) + minus_x_db(x[3,:], 3)
    stereo[1,:] = x[2,:] + minus_x_db(x[1,:], 3) + minus_x_db(x[4,:], 3)

    return stereo *  np.amax(signal_read) / np.amax(stereo) # normalize


# Process File
if __name__ == "__main__":
    sound_file = 'Parking Garage'
    signal = './Audio/' + sound_file + '.wav'

    signal_read, fs = sf.read(signal)
    signal_read = np.swapaxes(signal_read, 1, 0)
    stereo_downmix = np.swapaxes(downmix_to_stereo(signal_read), 0, 1)
    sf.write(f'{sound_file}_stereo.wav', stereo_downmix, fs)