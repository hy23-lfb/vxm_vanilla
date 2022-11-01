#!/usr/bin/env python

"""
Example script to train a VoxelMorph model in a semi-supervised
fashion by providing ground-truth segmentation data for training images.

If you use this code, please cite the following
    Unsupervised Learning for Probabilistic Diffeomorphic Registration for Images and Surfaces
    A.V. Dalca, G. Balakrishnan, J. Guttag, M.R. Sabuncu. 
    MedIA: Medical Image Analysis. (57). pp 226-236, 2019 

Copyright 2020 Adrian V. Dalca

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in 
compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is
distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or 
implied. See the License for the specific language governing permissions and limitations under 
the License.
"""
import os
import sys

if os.name == 'nt': # windows system
    sys.path.append('Y:\\repo\Masterarbeit\\voxelmorph')
elif os.name == 'posix': # nic system
    sys.path.append('/home/students/yogeshappa/repo/Masterarbeit/voxelmorph')

import random
import argparse
import numpy as np
import tensorflow as tf
import voxelmorph_custom as vxm


# disable eager execution
# tf.compat.v1.disable_eager_execution()


# parse the commandline
parser = argparse.ArgumentParser()

parser.add_argument('--config-file', required=True, help='json file to read the parameters')
spec = parser.parse_args()

if 0:
    # data organization parameters
    parser.add_argument('--img-list', required=True, help='line-seperated list of training files')
    parser.add_argument('--seg-suffix', help='input seg file suffix')
    parser.add_argument('--seg-prefix', help='input seg file prefix')
    parser.add_argument('--model-dir', default='models',
                        help='model output directory (default: models)')
    parser.add_argument('--atlas', help='optional atlas to perform scan-to-atlas training')
    
    # training parameters
    parser.add_argument('--gpu', default='0', help='GPU ID numbers (default: 0)')
    parser.add_argument('--epochs', type=int, default=1500,
                        help='number of training epochs (default: 1500)')
    parser.add_argument('--steps-per-epoch', type=int, default=100,
                        help='frequency of model saves (default: 100)')
    parser.add_argument('--load-weights', help='optional weights file to initialize with')
    parser.add_argument('--initial-epoch', type=int, default=0,
                        help='initial epoch number (default: 0)')
    parser.add_argument('--lr', type=float, default=1e-4, help='learning rate (default: 1e-4)')
    
    # network architecture parameters
    parser.add_argument('--enc', type=int, nargs='+',
                        help='list of unet encoder filters (default: 16 32 32 32)')
    parser.add_argument('--dec', type=int, nargs='+',
                        help='list of unet decorder filters (default: 32 32 32 32 32 16 16)')
    parser.add_argument('--int-steps', type=int, default=7,
                        help='number of integration steps (default: 7)')
    parser.add_argument('--int-downsize', type=int, default=2,
                        help='flow downsample factor for integration (default: 2)')
    
    # loss hyperparameters
    parser.add_argument('--image-loss', default='mse',
                        help='image reconstruction loss - can be mse or ncc (default: mse)')
    parser.add_argument('--grad-loss-weight', type=float, default=0.01,
                        help='weight of gradient loss (lamba) (default: 0.01)')
    args = parser.parse_args()
else:
    import json
    class ArgParser():
        def __init__(self, data):
            self.img_list           = data['img_list']
            self.seg_suffix         = data['seg_suffix']
            self.seg_prefix         = data['seg_prefix']
            self.model_dir          = data['model_dir']
            self.atlas_file         = data['atlas_file']
            self.gpu                = data['gpu']
            self.epochs             = data['epochs']
            self.steps_per_epoch    = data['steps_per_epoch']
            self.load_weights       = data['load_weights']
            self.initial_epoch      = data['initial_epoch']
            self.lr                 = data['lr']
            self.enc                = data['enc']
            self.dec                = data['dec']
            self.int_steps          = data['int_steps']
            self.int_downsize       = data['int_downsize']
            self.image_loss         = data['image_loss']
            self.grad_loss_weight   = data['grad_loss_weight']
            self.n_gradients        = data['n_gradients']
            self.max_pool           = data['max_pool']
    
    # Opening JSON file
    f = open(spec.config_file)
    data = json.load(f)
    args = ArgParser(data)
    f.close()

print()
print("##############################################################")
print("img_list         type: {} and value: {}".format(type(args.img_list), args.img_list))
print("seg_suffix       type: {} and value: {}".format(type(args.seg_suffix), args.seg_suffix))
print("seg_prefix       type: {} and value: {}".format(type(args.seg_prefix), args.seg_prefix))
print("model_dir        type: {} and value: {}".format(type(args.model_dir), args.model_dir))
print("atlas_file       type: {} and value: {}".format(type(args.atlas_file), args.atlas_file))
print("gpu              type: {} and value: {}".format(type(args.gpu), args.gpu))
print("epochs           type: {} and value: {}".format(type(args.epochs), args.epochs))
print("steps_per_epoch  type: {} and value: {}".format(type(args.steps_per_epoch), args.steps_per_epoch))
print("load_weights     type: {} and value: {}".format(type(args.load_weights), args.load_weights))
print("initial_epoch    type: {} and value: {}".format(type(args.initial_epoch), args.initial_epoch))
print("lr               type: {} and value: {}".format(type(args.lr), args.lr))
print("enc              type: {} and value: {}".format(type(args.enc), args.enc))
print("dec              type: {} and value: {}".format(type(args.dec), args.dec))
print("int_steps        type: {} and value: {}".format(type(args.int_steps), args.int_steps))
print("int_downsize     type: {} and value: {}".format(type(args.int_downsize), args.int_downsize))
print("image_loss       type: {} and value: {}".format(type(args.image_loss), args.image_loss))
print("grad_loss_weight type: {} and value: {}".format(type(args.grad_loss_weight), args.grad_loss_weight))
print("n_gradients      type: {} and value: {}".format(type(args.n_gradients), args.n_gradients))
print("max_pool         type: {} and value: {}".format(type(args.max_pool), args.max_pool))
print("##############################################################")
print()



train_imgs      = vxm.py.utils.read_file_list(args.img_list, prefix=None,
                                         suffix=None)
train_landmarks = vxm.py.utils.read_file_list(args.img_list, prefix=None,
                                         suffix=args.seg_suffix)
assert len(train_imgs) > 0, 'Could not find any training data.'

# generator (scan-to-scan unless the atlas cmd argument was provided)

generator = vxm.generators.semisupervised_landmarks(
    train_imgs,
    train_landmarks,
    atlas_file=args.atlas_file,
    steps_per_epoch=args.steps_per_epoch)

# extract shape from sampled input
inshape = next(generator)[0][0].shape[1:-1] # (256, 512, 64) := (row, columns, slices)

# prepare model folder
model_dir = args.model_dir
os.makedirs(model_dir, exist_ok=True)

# tensorflow device handling
device, nb_devices = vxm.tf.utils.setup_device(args.gpu)

# unet architecture
enc_nf = args.enc if args.enc else [16, 32, 32, 32]
dec_nf = args.dec if args.dec else [32, 32, 32, 32, 32, 16, 16]

# prepare model checkpoint save path
save_filename = os.path.join(model_dir, '{epoch:04d}.h5')

print("Harsha, inshape is {}".format(inshape))
# build the model
model = vxm.networks.VxmDenseLandmarksAuxiliaryLoss(
    n_gradients=args.n_gradients,
    max_pool=args.max_pool,
    inshape=inshape,
    nb_unet_features=[enc_nf, dec_nf],
    int_steps=args.int_steps,
    int_resolution=args.int_downsize
)

# load initial weights (if provided)
if args.load_weights:
    model.load_weights(args.load_weights)

# prepare image loss
if args.image_loss == 'ncc':
    image_loss_func = vxm.losses.NCC().loss
elif args.image_loss == 'mse':
    image_loss_func = vxm.losses.MSE().loss
else:
    raise ValueError('Image loss should be "mse" or "ncc", but found "%s"' % args.image_loss)

# losses
losses = [image_loss_func, vxm.losses.Grad(
    'l2', loss_mult=args.int_downsize).loss]
weights = [1, args.grad_loss_weight]

# multi-gpu support
if nb_devices > 1:
    save_callback = vxm.networks.ModelCheckpointParallel(save_filename)
    model = tf.keras.utils.multi_gpu_model(model, gpus=nb_devices)
else:
    save_callback = tf.keras.callbacks.ModelCheckpoint(save_filename, period=20)

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=args.lr), loss=losses, loss_weights=weights)

# save starting weights
model.save(save_filename.format(epoch=args.initial_epoch))

model.fit(generator,
          initial_epoch=args.initial_epoch,
          epochs=args.epochs,
          steps_per_epoch=args.steps_per_epoch,
          callbacks=[save_callback],
          verbose=1
         )
