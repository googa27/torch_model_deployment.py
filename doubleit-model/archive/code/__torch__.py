import torch as tc
import torch.nn as nn
import typing as tp



class Model(nn.Module):
    __parameters__ = []
    __buffers__ = []
    training: bool
    _is_full_backward_hook: tp.Optional[bool]

    def forward(self,
                x: tc.Tensor) -> tc.Tensor:
        return tc.mul(x, 2)
