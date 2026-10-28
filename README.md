# ComfyUI RefMod Persistent Cache V2 (repositorio NUEVO)

Nombre recomendado del repositorio: `ComfyUI-RefMod-Persistent-Cache-V2`.
No es una actualización del plugin anterior: instala esta carpeta NUEVA en `ComfyUI/custom_nodes/ComfyUI_RefMod_PersistentCache_V2/` y reinicia ComfyUI.

Dos clases independientes y NUEVAS:
- `RefModV2FaceCache`: `output/refmod_cache_v2/ultima_foto_rostro.png`
- `RefModV2BodyCache`: `output/refmod_cache_v2/ultima_foto_cuerpo.png`

El booleano compartido controla ambos nodos:
- FALSE: genera y GUARDA las dos fotos (una ejecución).
- TRUE: LEE las dos fotos guardadas. `generated_image` es una entrada lazy para que no solicite la generación de las fotos al reutilizar.

Nota: en instalaciones con `SaveImage` conectados directamente a los generadores, desactiva esos SaveImage si quieres evitar que se vuelvan a ejecutar. El workflow V91 ya los deja silenciados.

Los archivos de V2 se guardan en una carpeta DIFERENTE a V89/V90 para evitar contaminación con fotos guardadas incorrectamente. La primera ejecución de V2 debe ser FALSE.

Requisitos: torch, numpy, Pillow, folder_paths (provistos por ComfyUI). Compatible con la API de nodos lazy en versiones recientes de ComfyUI.
