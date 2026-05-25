# @title 2) Download de modelos (presets + SDXL extras)
import json
import os
import subprocess
import sys
from pathlib import Path

# Tamanho mínimo para checkpoints SDXL (~100 MB; Civitai sem token devolvia HTML ~0 GB)
MIN_CHECKPOINT_BYTES = 100_000_000
MIN_VAE_BYTES = 10_000_000


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


def collect_preset_downloads(presets_dir: str):
    ckpt, lora, vae = {}, {}, {}
    for p in Path(presets_dir).glob("*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print("preset ignorado", p.name, e)
            continue
        ckpt.update(data.get("checkpoint_downloads", {}))
        lora.update(data.get("lora_downloads", {}))
        vae.update(data.get("vae_downloads", {}))
    return ckpt, lora, vae


HF_LUSTIFY_V40 = (
    "https://huggingface.co/xxxpo13/LUSTIFY_SDXL/resolve/main/lustifySDXLNSFWSFW_v40.safetensors"
)
HF_EPIC_PUREFIX = (
    "https://huggingface.co/123543o/124052/resolve/main/checkpoints/XL/epicrealismXL_pureFix.safetensors"
)
HF_EPIC_VXFINALKISS = (
    "https://huggingface.co/John6666/epicrealism-xl-v8kiss-sdxl/resolve/main/"
    "epicrealismXL_vx1Finalkiss.safetensors"
)

EMBEDDED_PRESETS = {
    "pony_v6.json": {
        "default_model": "ponyDiffusionV6XL.safetensors",
        "default_styles": ["Fooocus Pony"],
        "checkpoint_downloads": {
            "ponyDiffusionV6XL.safetensors": (
                "https://huggingface.co/mashb1t/fav_models/resolve/main/fav/ponyDiffusionV6XL.safetensors"
            ),
        },
        "vae_downloads": {
            "ponyDiffusionV6XL_vae.safetensors": (
                "https://huggingface.co/mashb1t/fav_models/resolve/main/fav/ponyDiffusionV6XL_vae.safetensors"
            ),
        },
    },
    "lustify_v4.json": {
        "default_model": "lustifySDXLNSFW_v40Alpha.safetensors",
        "checkpoint_downloads": {
            "lustifySDXLNSFW_v40Alpha.safetensors": HF_LUSTIFY_V40,
        },
    },
    "juggernaut_v9.json": {
        "default_model": "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
        "checkpoint_downloads": {
            "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors": (
                "https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/"
                "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
            ),
        },
    },
    "epicrealism_xl.json": {
        "default_model": "epicrealismXL_pureFix.safetensors",
        "checkpoint_downloads": {
            "epicrealismXL_pureFix.safetensors": HF_EPIC_PUREFIX,
            "epicrealismXL_vxFinalkiss.safetensors": HF_EPIC_VXFINALKISS,
        },
    },
    "anteros_xxxl.json": {
        "default_model": "anterosXXXL_v10.safetensors",
        "checkpoint_downloads": {
            "anterosXXXL_v10.safetensors": (
                "https://huggingface.co/rosamelanopex/ModelsXL/resolve/"
                "e4d1f2bd7fd3078313bc5954ddc8de4760d38b5a/anterosXXXL_v10.safetensors"
            ),
        },
    },
    "reed_illustrious_v12.json": {
        "default_model": "reedXXXIllustrious_v120.safetensors",
        "checkpoint_downloads": {},
    },
}

NSFW_EXTRA_CHECKPOINTS = {
    "lustifySDXLNSFW_v40Alpha.safetensors": HF_LUSTIFY_V40,
    "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors": (
        "https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/"
        "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors"
    ),
    "epicrealismXL_pureFix.safetensors": HF_EPIC_PUREFIX,
    "anterosXXXL_v10.safetensors": (
        "https://huggingface.co/rosamelanopex/ModelsXL/resolve/"
        "e4d1f2bd7fd3078313bc5954ddc8de4760d38b5a/anterosXXXL_v10.safetensors"
    ),
    "ponyDiffusionV6XL.safetensors": (
        "https://huggingface.co/mashb1t/fav_models/resolve/main/fav/ponyDiffusionV6XL.safetensors"
    ),
}

# Sem espelho HF de checkpoint único (só Civitai / diffusers fragmentado)
MANUAL_ONLY_CHECKPOINTS = {
    "reedXXXIllustrious_v120.safetensors",
    "reedXXXIllustrious_v140.safetensors",
    "lustifySDXLNSFW_apexV8.safetensors",
}

presets_path = os.path.join(FOOOCUS_DIR, "presets")
Path(presets_path).mkdir(parents=True, exist_ok=True)

for name, body in EMBEDDED_PRESETS.items():
    p = Path(presets_path) / name
    if not p.exists():
        full = {
            "default_refiner": "None",
            "default_refiner_switch": 0.5,
            "default_loras": [[True, "None", 1.0]] * 5,
            "default_cfg_scale": 7.0,
            "default_sample_sharpness": 2.0,
            "default_sampler": "dpmpp_2m_sde_gpu",
            "default_scheduler": "karras",
            "default_performance": "Speed",
            "default_prompt": "",
            "default_prompt_negative": "",
            "default_styles": ["Fooocus V2"],
            "default_aspect_ratio": "896*1152",
            "default_overwrite_step": -1,
            "embeddings_downloads": {},
            "lora_downloads": {},
            **body,
        }
        p.write_text(json.dumps(full, indent=4), encoding="utf-8")
        print("preset escrito:", name)

ckpt_map, lora_map, vae_map = collect_preset_downloads(presets_path)

if DOWNLOAD_NSFW_EXTRAS:
    ckpt_map.update(NSFW_EXTRA_CHECKPOINTS)
    if DOWNLOAD_LUSTIFY_APEX_V8:
        print(
            "[aviso] lustifySDXLNSFW_apexV8: sem URL HF de checkpoint único; "
            "use upload manual (COLAB-MODELS.md)."
        )
    if DOWNLOAD_REED_V14:
        print(
            "[aviso] reedXXXIllustrious_v140: sem URL HF; use upload manual."
        )

if not DOWNLOAD_EPIC_VX_FINALKISS:
    ckpt_map.pop("epicrealismXL_vxFinalkiss.safetensors", None)

if not DOWNLOAD_ALL_PRESET_MODELS:
    keep = set(NSFW_EXTRA_CHECKPOINTS.keys())
    ckpt_map = {k: v for k, v in ckpt_map.items() if k in keep}
    lora_map = {}
    vae_map = {k: v for k, v in vae_map.items() if "pony" in k.lower()}

for name in sorted(MANUAL_ONLY_CHECKPOINTS):
    if name in ckpt_map and ckpt_map[name] and "civitai.com" in ckpt_map[name]:
        ckpt_map.pop(name, None)

print("Checkpoints:", len(ckpt_map), "| Loras:", len(lora_map), "| VAE:", len(vae_map))

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

if failed:
    print("\nFalharam:", ", ".join(failed))
    sys.exit(1)

if "reed_illustrious_v12" in FOOOCUS_PRESET and not os.path.isfile(
    os.path.join(CHECKPOINT_DIR, "reedXXXIllustrious_v120.safetensors")
):
    print(
        "\n[aviso] Preset reed_illustrious_v12 sem download automático: "
        "faça upload manual de reedXXXIllustrious_v120.safetensors "
        f"em {CHECKPOINT_DIR}"
    )

print("Concluido.")
