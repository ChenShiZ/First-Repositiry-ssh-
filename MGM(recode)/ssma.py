import torch
import torch.nn as nn


class SSMA(nn.Module):
    """PyTorch Module for SSMA"""

    def __init__(self, features, bottleneck):
        """Constructor

        :param features: number of feature maps
        :param bottleneck: bottleneck compression rate
        """
        super(SSMA, self).__init__()
        reduce_size = bottleneck
        double_features = int(2 * features)
        self.link = nn.Sequential(
            nn.Conv2d(double_features, reduce_size, kernel_size=1, stride=1),
            nn.ReLU(),
            nn.Conv2d(reduce_size, double_features, kernel_size=1, stride=1),
            nn.Sigmoid()
        )
        self.final_conv = nn.Sequential(
            nn.Conv2d(double_features, features, kernel_size=1, stride=1),
            nn.BatchNorm2d(features)
        )

        nn.init.kaiming_uniform_(self.link[0].weight, nonlinearity="relu")
        nn.init.kaiming_uniform_(self.link[2].weight, nonlinearity="relu")
        nn.init.kaiming_uniform_(self.final_conv[0].weight, nonlinearity="relu")

    def forward(self, x1, x2):
        """Forward pass

        :param x1: input data from encoder 1
        :param x2: input data from encoder 2
        :return: Fused feature maps
        """
        x1
        tensorx1=torch.unsqueeze(x1, dim=1)
        x2
        tensorx2 = torch.unsqueeze(x2, dim=1)

        x_12 = torch.cat((tensorx1, tensorx2), dim=1)

        x_12_est = self.link(x_12)
        x_12 = x_12 * x_12_est
        x_12 = self.final_conv(x_12)
        x_12 = torch.squeeze(x_12)

        return x_12