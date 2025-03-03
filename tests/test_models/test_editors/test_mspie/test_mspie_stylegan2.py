# Copyright (c) OpenMMLab. All rights reserved.
import platform
from unittest import TestCase

import pytest
import torch
from mmengine import MessageHub
from mmengine.optim import OptimWrapper, OptimWrapperDict

from mmedit.models import EditDataPreprocessor, MSPIEStyleGAN2
from mmedit.structures import EditDataSample
from mmedit.utils import register_all_modules

register_all_modules()


class TestMSPIEStyleGAN2(TestCase):

    @classmethod
    def setup_class(cls):
        cls.generator_cfg = dict(
            type='MSStyleGANv2Generator', out_size=32, style_channels=16)
        cls.disc_cfg = dict(type='MSStyleGAN2Discriminator', in_size=32)

        # reg params
        d_reg_interval = 16
        g_reg_interval = 4
        ema_half_life = 10.  # G_smoothing_kimg

        cls.ema_config = dict(
            type='ExponentialMovingAverage',
            interval=1,
            momentum=1. - (0.5**(32. / (ema_half_life * 1000.))))

        cls.loss_config = dict(
            r1_loss_weight=10. / 2. * d_reg_interval,
            r1_interval=d_reg_interval,
            norm_mode='HWC',
            g_reg_interval=g_reg_interval,
            g_reg_weight=2. * g_reg_interval,
            pl_batch_shrink=2)

    @pytest.mark.skipif(
        ('win' in platform.system().lower() and 'cu' in torch.__version__)
        or not torch.cuda.is_available(),
        reason='skip on windows-cuda due to limited RAM.')
    def test_stylegan2_cpu(self):
        accu_iter = 1
        message_hub = MessageHub.get_instance('test-mspie-s2')
        gan = MSPIEStyleGAN2(
            self.generator_cfg,
            self.disc_cfg,
            data_preprocessor=EditDataPreprocessor(),
            ema_config=self.ema_config,
            loss_config=self.loss_config,
            train_settings=dict(num_upblocks=3))

        optimizer_g = torch.optim.SGD(gan.generator.parameters(), lr=0.01)
        optimizer_d = torch.optim.SGD(gan.discriminator.parameters(), lr=0.01)

        optim_wrapper_dict = OptimWrapperDict(
            generator=OptimWrapper(optimizer_g, accumulative_counts=accu_iter),
            discriminator=OptimWrapper(
                optimizer_d, accumulative_counts=accu_iter))

        # prepare inputs
        img = torch.randn(3, 32, 32)
        data = dict(inputs=dict(), data_samples=[EditDataSample(gt_img=img)])

        # simulate train_loop here
        message_hub.update_info('iter', 0)
        _ = gan.train_step(data, optim_wrapper_dict)
