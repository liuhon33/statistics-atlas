# SciNet's DAT112, Neural Network Programming.
# Lecture 7, 13 May 2025. Original code: Erik Spence.
# PyTorch translation. Images use NCHW rather than TensorFlow's NHWC.

import torch
from torch import nn


class Conv3Layer(nn.Module):
    def __init__(self, num_in_channels, num_out_channels, is_res=False):
        super().__init__()
        self.Conv2D_1 = nn.Conv2d(num_in_channels, num_out_channels, 3, padding=1)
        # Keras GroupNormalization defaults to epsilon=0.001.
        self.GroupNorm_1 = nn.GroupNorm(8, num_out_channels, eps=1e-3)
        self.Conv2D_2 = nn.Conv2d(num_out_channels, num_out_channels, 3, padding=1)
        self.GroupNorm_2 = nn.GroupNorm(8, num_out_channels, eps=1e-3)
        self.is_res = is_res

    def forward(self, inputs):
        x = self.Conv2D_1(inputs)
        x = self.GroupNorm_1(x)
        x1 = torch.relu(x)
        x = self.Conv2D_2(x1)
        x = self.GroupNorm_2(x)
        x = torch.relu(x)
        if self.is_res:
            x = x1 + x
        return x


class UnetDownLayer(nn.Module):
    def __init__(self, num_in_channels, num_out_channels):
        super().__init__()
        self.Conv3 = Conv3Layer(num_in_channels, num_out_channels)
        self.MaxPool2D = nn.MaxPool2d(2, stride=2)

    def forward(self, inputs):
        return self.MaxPool2D(self.Conv3(inputs))


class UnetUpLayer(nn.Module):
    def __init__(self, num_in_channels, num_out_channels):
        super().__init__()
        self.Conv2DTranspose = nn.ConvTranspose2d(num_in_channels, num_out_channels, 2, stride=2)
        self.Conv3_1 = Conv3Layer(num_out_channels, num_out_channels)
        self.Conv3_2 = Conv3Layer(num_out_channels, num_out_channels)

    def forward(self, inputs):
        img_input, skip = inputs
        x = torch.cat([img_input, skip], dim=1)
        x = torch.relu(self.Conv2DTranspose(x))
        x = self.Conv3_1(x)
        return self.Conv3_2(x)


class TimeSirenLayer(nn.Module):
    def __init__(self, emb_dim):
        super().__init__()
        self.Dense_1 = nn.Linear(1, emb_dim)
        self.Dense_2 = nn.Linear(emb_dim, emb_dim)

    def forward(self, inputs):
        x = self.Dense_1(inputs)
        x = torch.sin(x)
        return self.Dense_2(x)


class NaiveUnet(nn.Module):
    def __init__(self, input_shape, n_feat):
        super().__init__()
        if tuple(input_shape) != (64, 64, 3):
            raise ValueError('This lecture model expects input_shape=(64, 64, 3).')
        if n_feat < 8 or n_feat % 8:
            raise ValueError('n_feat must be a positive multiple of 8.')
        self.input_shape = tuple(input_shape)
        self.n_feat = n_feat
        self.init_conv = Conv3Layer(3, n_feat, is_res=True)
        self.down1 = UnetDownLayer(n_feat, n_feat)
        self.down2 = UnetDownLayer(n_feat, 2 * n_feat)
        self.down3 = UnetDownLayer(2 * n_feat, 2 * n_feat)
        self.to_vec = nn.AvgPool2d(4)
        self.timeemb = TimeSirenLayer(2 * n_feat)
        self.up0 = nn.ConvTranspose2d(2 * n_feat, 2 * n_feat, 4, stride=4)
        self.up0_norm = nn.GroupNorm(8, 2 * n_feat, eps=1e-3)
        self.up1 = UnetUpLayer(4 * n_feat, 2 * n_feat)
        self.up2 = UnetUpLayer(4 * n_feat, n_feat)
        self.up3 = UnetUpLayer(2 * n_feat, n_feat)
        self.out = nn.Conv2d(2 * n_feat, 3, 3, padding=1)
        self.apply(self._keras_initialization)

    @staticmethod
    def _keras_initialization(layer):
        # Match Keras' Glorot-uniform kernels and zero biases, not random draws.
        if isinstance(layer, (nn.Conv2d, nn.ConvTranspose2d, nn.Linear)):
            nn.init.xavier_uniform_(layer.weight)
            nn.init.zeros_(layer.bias)

    def forward(self, inputs):
        img_input, t_input = inputs
        x = self.init_conv(img_input)
        down1 = self.down1(x)
        down2 = self.down2(down1)
        down3 = self.down3(down2)
        thro = torch.relu(self.to_vec(down3))
        timeemb = self.timeemb(t_input.reshape(-1, 1)).reshape(-1, 2 * self.n_feat, 1, 1)
        thro = torch.relu(self.up0_norm(self.up0(thro + timeemb)))
        up1 = self.up1([thro, down3])
        up2 = self.up2([up1, down2])
        up3 = self.up3([up2, down1])
        return self.out(torch.cat([up3, x], dim=1))
