# @title 2) Download de modelos (Lustify v4 + essenciais Fooocus)
import json
import os
import subprocess
import sys
from pathlib import Path

# Tamanho mínimo para checkpoints SDXL (~100 MB; Civitai sem token devolvia HTML ~0 GB)
MIN_CHECKPOINT_BYTES = 100_000_000
MIN_VAE_BYTES = 10_000_000
MIN_SMALL_FILE_BYTES = 100_000

# Colab ~114 GB: só lustify + auxiliares que o launch baixa na 1ª execução
PRESET_FILES_FOR_DOWNLOAD = ("lustify_v4.json",)

HF_LUSTIFY_V40 = (
    "https://huggingface.co/xxxpo13/LUSTIFY_SDXL/resolve/main/lustifySDXLNSFWSFW_v40.safetensors"
)

EMBEDDED_PRESETS = {
    "lustify_v4.json": {
        "default_model": "lustifySDXLNSFW_v40Alpha.safetensors",
        "default_styles": ["Fooocus V2", "Fooocus Photograph"],
        "checkpoint_downloads": {
            "lustifySDXLNSFW_v40Alpha.safetensors": HF_LUSTIFY_V40,
        },
    },
}

# vae_approx + prompt expansion (launch.py também baixa; pré-fetch evita surpresa de disco)
FOOOCUS_LAUNCH_ESSENTIALS = [
    (
        "models/vae_approx/xlvaeapp.pth",
        "https://huggingface.co/lllyasviel/misc/resolve/main/xlvaeapp.pth",
        MIN_SMALL_FILE_BYTES,
    ),
    (
        "models/vae_approx/vaeapp_sd15.pth",
        "https://huggingface.co/lllyasviel/misc/resolve/main/vaeapp_sd15.pt",
        MIN_SMALL_FILE_BYTES,
    ),
    (
        "models/vae_approx/xl-to-v1_interposer-v4.0.safetensors",
        "https://huggingface.co/mashb1t/misc/resolve/main/xl-to-v1_interposer-v4.0.safetensors",
        MIN_SMALL_FILE_BYTES,
    ),
    (
        "models/prompt_expansion/fooocus_expansion/pytorch_model.bin",
        "https://huggingface.co/lllyasviel/misc/resolve/main/fooocus_expansion.bin",
        MIN_SMALL_FILE_BYTES,
    ),
]


def download_one(url: str, dest: str, min_bytes: int = MIN_CHECKPOINT_BYTES):
    dest = os.path.abspath(dest)
    if os.path.isfile(dest) and os.path.getsize(dest) >= min_bytes:
        print("[skip]", os.path.basename(dest))
        return
    if "civitai.com" in url:
        raise RuntimeError(
            f"URL Civitai bloqueado no fluxo principal: {url}\n"
            "Use HuggingFace (COLAB-MODELS.md) ou a célula opcional de upload manual."
        )
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    print("[download]", os.path.basename(dest))
    cmd = ["wget", "-c", "-O", dest, url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("  wget falhou, tentando curl...")
        subprocess.run(["curl", "-L", "-C", "-", "-o", dest, url], check=False)
    if not os.path.isfile(dest):
        raise RuntimeError(f"Download falhou (arquivo ausente): {dest}")
    size = os.path.getsize(dest)
    if size < min_bytes:
        try:
            os.remove(dest)
        except OSError:
            pass
        raise RuntimeError(
            f"Download inválido para {os.path.basename(dest)}: {size / 1e6:.1f} MB "
            f"(mínimo {min_bytes / 1e6:.0f} MB). Verifique a URL ou espaço em disco."
        )
    print(f"  ok ({size / 1e9:.2f} GB)")


def collect_preset_downloads(presets_dir: str, only_names=PRESET_FILES_FOR_DOWNLOAD):
    ckpt, lora, vae = {}, {}, {}
    for name in only_names:
        p = Path(presets_dir) / name
        if not p.is_file():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print("preset ignorado", name, e)
            continue
        ckpt.update(data.get("checkpoint_downloads", {}))
        lora.update(data.get("lora_downloads", {}))
        vae.update(data.get("vae_downloads", {}))
    return ckpt, lora, vae


presets_path = os.path.join(FOOOCUS_DIR, "presets")
Path(presets_path).mkdir(parents=True, exist_ok=True)

for name, body in EMBEDDED_PRESETS.items():
    p = Path(presets_path) / name
    if not p.exists():
        full = {
            "default_refiner": "None",
            "default_refiner_switch": 0.5,
            "default_loras": [[True, "None", 1.0]] * 5,
            "default_cfg_scale": 4.0,
            "default_sample_sharpness": 2.0,
            "default_sampler": "dpmpp_2m_sde_gpu",
            "default_scheduler": "karras",
            "default_performance": "Speed",
            "default_prompt": "",
            "default_prompt_negative": "",
            "default_aspect_ratio": "896*1152",
            "default_overwrite_step": -1,
            "embeddings_downloads": {},
            "lora_downloads": {},
            **body,
        }
        p.write_text(json.dumps(full, indent=4), encoding="utf-8")
        print("preset escrito:", name)

if DOWNLOAD_ALL_PRESET_MODELS or DOWNLOAD_NSFW_EXTRAS:
    print(
        "[aviso] DOWNLOAD_ALL_PRESET_MODELS / DOWNLOAD_NSFW_EXTRAS ignorados: "
        "Colab lustify-only (~10-15 GB)."
    )

ckpt_map, lora_map, vae_map = collect_preset_downloads(presets_path)

print("Checkpoints:", len(ckpt_map), "| Loras:", len(lora_map), "| VAE:", len(vae_map))
print("Essenciais launch:", len(FOOOCUS_LAUNCH_ESSENTIALS))

failed = []
for fname, url in sorted(ckpt_map.items()):
    try:
        download_one(url, os.path.join(CHECKPOINT_DIR, fname))
    except Exception as e:
        print(f"  ERRO {fname}: {e}")
        failed.append(fname)

for fname, url in sorted(lora_map.items()):
    try:
        download_one(url, os.path.join(LORA_DIR, fname), min_bytes=1_000_000)
    except Exception as e:
        print(f"  ERRO {fname}: {e}")
        failed.append(fname)

for fname, url in sorted(vae_map.items()):
    try:
        download_one(url, os.path.join(VAE_DIR, fname), min_bytes=MIN_VAE_BYTES)
    except Exception as e:
        print(f"  ERRO {fname}: {e}")
        failed.append(fname)

for rel_path, url, min_b in FOOOCUS_LAUNCH_ESSENTIALS:
    dest = os.path.join(FOOOCUS_DIR, rel_path)
    try:
        download_one(url, dest, min_bytes=min_b)
    except Exception as e:
        print(f"  ERRO {rel_path}: {e}")
        failed.append(rel_path)

if failed:
    print("\nFalharam:", ", ".join(failed))
    sys.exit(1)

print("Concluido (lustify + essenciais). Controlnet/inpaint baixam sob demanda na UI.")
