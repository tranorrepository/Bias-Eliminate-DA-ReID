# encoding: utf-8
"""
@author:  sherlock
@contact: sherlockliao01@gmail.com
"""

import argparse
import os
import sys
import torch
import time
import numpy as np

from torch.backends import cudnn

sys.path.append('.')
from config import cfg
from data import make_test_data_loader
from data.datasets import init_dataset
from engine.tester import tester
from modeling import build_model, build_camera_model
from layers import make_loss
from solver import make_optimizer, WarmupMultiStepLR

from utils.logger import setup_logger

def test(cfg):
    logger = setup_logger("reid_baseline", cfg.OUTPUT_DIR)
    logger.info("Running with config:\n{}".format(cfg))

    # prepare dataset
    test_data_loader, num_query = make_test_data_loader(cfg)

    # prepare model
    model = build_model(cfg, num_classes=[700,500])
    logger.info('Path to the checkpoint of model:%s' %(cfg.TEST.WEIGHT))
    model.load_param(cfg.TEST.WEIGHT, 'self')
    camera_model = build_camera_model(cfg, num_classes=5)
    logger.info('Path to the checkpoint of model:%s' %(cfg.TEST.CAMERA_WEIGHT))
    camera_model.load_param(cfg.TEST.CAMERA_WEIGHT, 'self')
    tester(cfg,
            model,
            camera_model,
            test_data_loader,
            num_query
            )

def main():

    parser = argparse.ArgumentParser(description="ReID Baseline Training")
    parser.add_argument(
        "--config_file", default="", help="path to config file", type=str
    )
    parser.add_argument("opts", help="Modify config options using the command-line", default=None,
                        nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.config_file != "":
        cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()

    output_dir = cfg.OUTPUT_DIR
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if cfg.MODEL.DEVICE == "cuda":
        os.environ['CUDA_VISIBLE_DEVICES'] = cfg.MODEL.DEVICE_ID
    cudnn.benchmark = True

    test(cfg)

if __name__ == '__main__':
    main()
