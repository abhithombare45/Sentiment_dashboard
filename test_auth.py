import torch

x = torch.rand(5, 3)
print(x)

print(torch.backends.mps.is_available())
