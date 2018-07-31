#!/usr/bin/env python
import os, sys
import subprocess

caffe_bin = '/home/Working/caffe/build/tools/caffe' # PLEASE MODIFY TO YOUR LOCAL DIRECTORY
template  = 'model/train.template.quad.prototxt'

subprocess.call('mkdir -p tmp/tmp_model', shell=True)

batch_size_train = 4
batch_size_test  = 1
crop_width       = 768
crop_height      = 384
# crop_width       = 960
# crop_height      = 512
input_width      = 960
input_height     = 540
train_data_lmdb  = "/home/Working/data/FlyingThingsLMDB"
test_data_lmdb   = "/home/Working/data/FlyingThingsLMDB"

replacement_list = {
    '$BATCH_SIZE_TRAIN': ('%d' % batch_size_train),
    '$BATCH_SIZE_TEST' : ('%d' % batch_size_test),
    '$TRAIN_DATA_LMDB' : ('%s' % train_data_lmdb),
    '$TEST_DATA_LMDB'  : ('%s' % test_data_lmdb),
    '$CROP_WIDTH'      : ('%d' % crop_width),
    '$CROP_HEIGHT'     : ('%d' % crop_height),
    '$INPUT_WIDTH'     : ('%d' % input_width),
    '$INPUT_HEIGHT'    : ('%d' % input_height)
}

proto = ''
with open(template, "r") as tfile:
    proto = tfile.read()

for r in replacement_list:
    proto = proto.replace(r, replacement_list[r])

with open('tmp/tmp_model/train.prototxt', "w") as tfile:
    tfile.write(proto)



os.system('mkdir training') 
os.chdir('training') 

# =========================================================

my_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(my_dir)

if not os.path.isfile(caffe_bin):
    print('Caffe tool binaries not found. Did you compile caffe with tools (make all tools)?')
    sys.exit(1)

print('args:', sys.argv[1:])


trained_filenames = os.listdir('./')

if len(trained_filenames)==0:
	# start from scratch
	args = [caffe_bin, 'train', '-solver', '../model/solver.prototxt'] + sys.argv[1:]
else:
	# start from the latest training result
	iters = []
	for i in range(len(trained_filenames)):
		i0 = trained_filenames[i].find('iter_')
		if  i0==-1:
			continue
		i1 = trained_filenames[i].find('.')
		iters.append(int(trained_filenames[i][i0+5:i1]))		
	latest_iter = max(iters)
	args = [caffe_bin, 
		'train', 
		'-solver', '../model/solver.prototxt', 
		'-snapshot', 'disp_iter_'+ str(latest_iter) + '.solverstate',
		] + sys.argv[1:]
	
cmd = str.join(' ', args)
print('Executing %s' % cmd)

subprocess.call(args)
