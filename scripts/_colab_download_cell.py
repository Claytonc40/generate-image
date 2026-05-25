# @title 2) Download de modelos (presets + SDXL extras)
import json
import os
import subprocess
from pathlib import Path


def civitai_url(base_url: str, token: str) -> str:
    if not token:
        return base_url
    sep = "&" if "?" in base_url else "?"
    return f"{base_url}{sep}token={token}"


def download_one(url: str, dest: str, token: str = ""):
    dest = os.path.abspath(dest)
    if os.path.isfile(dest) and os.path.getsize(dest) > 1_000_000:
        print("[skip]", os.path.basename(dest))
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    url = civitai_url(url, token) if "civitai.com" in url else url
    print("[download]", os.path.basename(dest))
    if "civitai.com" in url:
        cmd = ["wget", "-c", "--content-disposition", "-O", dest, url]
    else:
        cmd = ["wget", "-c", "-O", dest, url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("  wget falhou, tentando curl...")
        subprocess.run(["curl", "-L", "-C", "-", "-o", dest, url], check=False)
    if os.path.isfile(dest):
        gb = os.path.getsize(dest) / 1e9
        print(f"  ok ({gb:.2f} GB)")
    else:
        print("  FALHOU:", dest)


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


EMBEDDED_PRESETS = {
    "pony_v6.json": {
        "default_model": "ponyDiffusionV6XL.safetensors",
        "default_styles": ["Fooocus Pony"],
        "checkpoint_downloads": {
            "ponyDiffusionV6XL.safetensors": "https://huggingface.co/mashb1t/fav_models/resolve/main/fav/ponyDiffusionV6XL.safetensors",
        },
        "vae_downloads": {
            "ponyDiffusionV6XL_vae.safetensors": "https://huggingface.co/mashb1t/fav_models/resolve/main/fav/ponyDiffusionV6XL_vae.safetensors",
        },
    },
    "lustify_v4.json": {
        "default_model": "lustifySDXLNSFW_v40Alpha.safetensors",
        "checkpoint_downloads": {
            "lustifySDXLNSFW_v40Alpha.safetensors": "https://civitai.com/api/download/models/926965",
        },
    },
    "juggernaut_v9.json": {
        "default_model": "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
        "checkpoint_downloads": {
            "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors": "https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
        },
    },
    "epicrealism_xl.json": {
        "default_model": "epicrealismXL_pureFix.safetensors",
        "checkpoint_downloads": {
            "epicrealismXL_pureFix.safetensors": "https://civitai.com/api/download/models/2514955",
            "epicrealismXL_vxFinalkiss.safetensors": "https://civitai.com/api/download/models/1063833",
        },
    },
    "anteros_xxxl.json": {
        "default_model": "anterosXXXL_v10.safetensors",
        "checkpoint_downloads": {
            "anterosXXXL_v10.safetensors": "https://huggingface.co/rosamelanopex/ModelsXL/resolve/e4d1f2bd7fd3078313bc5954ddc8de4760d38b5a/anterosXXXL_v10.safetensors",
        },
    },
    "reed_illustrious_v12.json": {
        "default_model": "reedXXXIllustrious_v120.safetensors",
        "checkpoint_downloads": {
            "reedXXXIllustrious_v120.safetensors": "https://civitai.com/api/download/models/2852255",
        },
    },
}

NSFW_EXTRA_CHECKPOINTS = {
    "lustifySDXLNSFW_v40Alpha.safetensors": "https://civitai.com/api/download/models/926965",
    "Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors": "https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors",
    "epicrealismXL_pureFix.safetensors": "https://civitai.com/api/download/models/2514955",
    "anterosXXXL_v10.safetensors": "https://huggingface.co/rosamelanopex/ModelsXL/resolve/e4d1f2bd7fd3078313bc5954ddc8de4760d38b5a/anterosXXXL_v10.safetensors",
    "reedXXXIllustrious_v120.safetensors": "https://civitai.com/api/download/models/2852255",
    "ponyDiffusionV6XL.safetensors": "https://huggingface.co/mashb1t/fav_models/resolve/main/fav/ponyDiffusionV6XL.safetensors",
}

NSFW_OPTIONAL = {
    "lustifySDXLNSFW_apexV8.safetensors": "https://civitai.com/api/download/models/2808677",
    "reedXXXIllustrious_v140.safetensors": "https://civitai.com/api/download/models/2954011",
}

ANTEROS_CIVITAI = "https://civitai.com/api/download/models/479579"

token = CIVITAI_TOKEN
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
        ckpt_map.update({"lustifySDXLNSFW_apexV8.safetensors": NSFW_OPTIONAL["lustifySDXLNSFW_apexV8.safetensors"]})
    if DOWNLOAD_REED_V14:
        ckpt_map["reedXXXIllustrious_v140.safetensors"] = NSFW_OPTIONAL["reedXXXIllustrious_v140.safetensors"]

if not DOWNLOAD_ALL_PRESET_MODELS:
    keep = set(NSFW_EXTRA_CHECKPOINTS.keys())
    ckpt_map = {k: v for k, v in ckpt_map.items() if k in keep}
    lora_map = {}
    vae_map = {k: v for k, v in vae_map.items() if "pony" in k.lower()}

print("Checkpoints:", len(ckpt_map), "| Loras:", len(lora_map), "| VAE:", len(vae_map))

for fname, url in sorted(ckpt_map.items()):
    download_one(url, os.path.join(CHECKPOINT_DIR, fname), token)

for fname, url in sorted(lora_map.items()):
    download_one(url, os.path.join(LORA_DIR, fname), token)

for fname, url in sorted(vae_map.items()):
    download_one(url, os.path.join(VAE_DIR, fname), token)

anteros_path = os.path.join(CHECKPOINT_DIR, "anterosXXXL_v10.safetensors")
if DOWNLOAD_NSFW_EXTRAS and (not os.path.isfile(anteros_path) or os.path.getsize(anteros_path) < 1_000_000):
    print("Fallback Anteros via Civitai...")
    download_one(ANTEROS_CIVITAI, anteros_path, token)

print("Concluido.")
