"""RefMod Persistent Cache V2 — standalone install, separate node identities."""
import os
import numpy as np
import torch
from PIL import Image
import folder_paths

class _CacheV2:
    SLOT = None
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "execute"
    CATEGORY = "RefMod / Persistent Cache V2"

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "generated_image": ("IMAGE", {"lazy": True}),
            "reuse_saved": ("BOOLEAN", {"default": False}),
        }}

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Ensure a change to files on disk is picked up on the next run.
        return float("nan")

    def check_lazy_status(self, generated_image=None, reuse_saved=False):
        if reuse_saved:
            return []
        return ["generated_image"] if generated_image is None else []

    def _path(self):
        directory = os.path.join(folder_paths.get_output_directory(), "refmod_cache_v2")
        os.makedirs(directory, exist_ok=True)
        return os.path.join(directory, "ultima_foto_" + self.SLOT + ".png")

    def execute(self, generated_image=None, reuse_saved=False):
        path = self._path()
        if reuse_saved:
            if not os.path.isfile(path):
                raise RuntimeError("RefMod Cache V2: falta " + self.SLOT + " en " + path + ". Pon FALSE y ejecuta una vez.")
            with Image.open(path) as im:
                arr = np.asarray(im.convert("RGB"), dtype=np.float32).copy() / 255.0
            print("[RefModCacheV2] REUTILIZANDO " + self.SLOT + ": " + path)
            return (torch.from_numpy(arr).unsqueeze(0),)
        if generated_image is None:
            raise RuntimeError("RefMod Cache V2: imagen " + self.SLOT + " ausente; revisa generador RefMod.")
        arr = (generated_image[0].detach().float().clamp(0, 1).cpu().numpy() * 255).round().astype(np.uint8)
        tmp = path + ".tmp"
        try:
            Image.fromarray(arr).convert("RGB").save(tmp, format="PNG")
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
        print("[RefModCacheV2] GUARDADO " + self.SLOT + ": " + path)
        return (generated_image,)

class RefModV2FaceCache(_CacheV2):
    SLOT = "rostro"

class RefModV2BodyCache(_CacheV2):
    SLOT = "cuerpo"

NODE_CLASS_MAPPINGS = {
    "RefModV2FaceCache": RefModV2FaceCache,
    "RefModV2BodyCache": RefModV2BodyCache,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "RefModV2FaceCache": "RefMod Cache V2 | ROSTRO (nuevo)",
    "RefModV2BodyCache": "RefMod Cache V2 | CUERPO (nuevo)",
}
