import subprocess
import datetime as dt

dt_string = dt.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
normal_filename = 'profiles/{}profile_{}.txt'.format('normal_', dt_string)
fast_filename = 'profiles/{}profile_{}.txt'.format('fast_', dt_string)

normal_command = 'python -m cProfile -m cellpose --dir exemplar-001/ --pretrained_model nuclei --save_tif --channel_axis 0 --chan 1 --verbose > {}'.format(normal_filename)
fast_command = 'python -m cProfile -m cellpose --dir exemplar-001/ --pretrained_model nuclei --save_tif --channel_axis 0 --chan 1 --verbose --fast_mode > {}'.format(fast_filename)
subprocess.run(fast_command, shell=True)
