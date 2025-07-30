import os
import math
from typing import Optional, Tuple

import torch
from diffusers import MochiPipeline
from diffusers.utils import export_to_video

# Simple singleton cache keyed by (device_id, precision)
_MODELS = {}

def _parse_resolution(resolution: str) -> Tuple[int, int]:
    # "512x512" -> (512, 512)
    try:
        w, h = resolution.lower().split("x")
        return int(w), int(h)
    except Exception:
        # Fallback to model default (roughly 480p per README)
        return 480, 480


class MochiModel:
    """
    Thin wrapper around genmo/mochi-1-preview via diffusers.MochiPipeline.

    Features:
    - bfloat16 (default) to reduce VRAM (README suggests ~22GB vs 42GB full precision)
    - enable_model_cpu_offload + enable_vae_tiling for memory savings
    - resolution parsing (width/height)
    - deterministic seeding (optional)
    """
    def __init__(
        self,
        device: torch.device,
        precision: str = os.getenv("MOCHI_PRECISION", "bf16"),  # "bf16" or "fp32"
        enable_offload: bool = True,
        fps: int = int(os.getenv("MOCHI_FPS", "30")),
    ):
        self.device = device
        self.precision = precision
        self.enable_offload = enable_offload
        self.fps = fps

        kwargs = {}
        if precision.lower() == "bf16":
            # per README, use variant="bf16", torch_dtype=torch.bfloat16
            kwargs.update(dict(variant="bf16", torch_dtype=torch.bfloat16))

        # Load pipeline
        # NOTE: If you need to pin a specific diffusers commit, do it in requirements.
        self.pipe: MochiPipeline = MochiPipeline.from_pretrained(
            "genmo/mochi-1-preview", **kwargs
        )

        # Memory savings recommended by README
        if enable_offload:
            # Will move modules to GPU on-the-fly (needs accelerate installed)
            self.pipe.enable_model_cpu_offload()
        self.pipe.enable_vae_tiling()

        # Move to device if not offloading
        if not enable_offload:
            self.pipe.to(device)

    @torch.inference_mode()
    def generate(
        self,
        prompt: str,
        length_sec: int,
        resolution: str,
        out_path: str,
        num_frames: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> str:
        """
        Generate a video and save it to `out_path`.
        Returns the output path.
        """
        width, height = _parse_resolution(resolution)

        if num_frames is None:
            num_frames = max(1, int(math.ceil(length_sec * self.fps)))

        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)

        # torch.autocast block recommended by README for bf16
        # cache_enabled=False avoids some CUDA graph cache issues sometimes seen with long videos
        dtype_ctx = (
            torch.autocast("cuda", torch.bfloat16, cache_enabled=False)
            if (self.device.type == "cuda" and self.precision.lower() == "bf16")
            else torch.no_grad()
        )

        with dtype_ctx:
            # diffusers' MochiPipeline signature per README:
            # frames = pipe(prompt, num_frames=84).frames[0]
            result = self.pipe(
                prompt,
                num_frames=num_frames,
                height=height,
                width=width,
                generator=generator,
            )
            frames = result.frames[0]

        export_to_video(frames, out_path, fps=self.fps)
        return out_path


def get_model_for_device(device_id: int, precision: Optional[str] = None):
    """
    Returns a cached MochiModel for (device_id, precision).
    """
    if precision is None:
        precision = os.getenv("MOCHI_PRECISION", "bf16")

    key = (device_id, precision)
    if key not in _MODELS:
        device = torch.device(f"cuda:{device_id}" if torch.cuda.is_available() else "cpu")
        _MODELS[key] = MochiModel(device=device, precision=precision)

    return _MODELS[key]
