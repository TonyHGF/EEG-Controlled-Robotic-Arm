import numpy as np

from pylsl import StreamInlet, resolve_stream

streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])
while True:
    sample, timestamp = inlet.pull_sample()
    # sample = np.array(sample)
    # print(sample[0])
    # print(sample.shape)
    print(sample)
    break
