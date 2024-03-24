import numpy as np
import torch # 如果pytorch安装成功即可导入


print(torch.cuda.is_available()) # 查看CUDA是否可用
print(torch.cuda.device_count()) # 查看可用的CUDA数量
print(torch.version.cuda) # 查看CUDA的版本号
print(torch.cuda.get_device_name(1))
print(torch.cuda.get_device_capability(1))
print(torch.cuda.get_device_properties(1))