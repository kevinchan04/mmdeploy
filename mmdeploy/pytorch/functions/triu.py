# Copyright (c) OpenMMLab. All rights reserved.
import torch

from mmdeploy.core import FUNCTION_REWRITER


@FUNCTION_REWRITER.register_rewriter(func_name='torch.triu')
def triu(ctx,
         input: torch.Tensor,
         diagonal: int = 0,
         *args,
         **kwargs) -> torch.Tensor:
    """Rewrite `triu` for exporting model to ONNX."""
    assert len(input.shape) >= 2
    height, width = input.shape[-2:]
    arange = torch.arange(width, device=input.device)
    mask = arange.expand(height, width)
    arange0 = torch.arange(width, device=input.device).unsqueeze(0)
    arange1 = torch.arange(height, device=input.device).unsqueeze(-1)
    mask = arange0 >= arange1
    return input * mask
