#!/usr/bin/env python3
"""Download local Fooocus models from presets + launch essentials (HuggingFace only)."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = ROOT / "presets"

MIN_CHECKPOINT = 100_000_000
MIN_VAE = 10_000_000
MIN_LORA = 1_000_000
MIN_SMALL = 100_000

# Presets the user cares about (+ all presets when --all-presets)
FOCUS_PRESETS = {
    "default.json",
    "lustify_v4.json",
    "juggernaut_v9.json",
    "epicrealism_xl.json",
    "anteros_xxxl.json",
    "reed_illustrious_v12.json",
    "pony_v6.json",
}

# REED: no HF URL in preset; optional mirrors (may be wrong version — verify manually)
REED_HF_CANDIDATES: list[tuple[str, str]] = [
    # ("reedXXXIllustrious_v120.safetensors", "https://huggingface.co/..."),
]

FOOOCUS_LAUNCH_ESSENTIALS: list[tuple[str, str, int]] = [
    ("models/vae_approx/xlvaeapp.pth", "https://huggingface.co/lllyasviel/misc/resolve/main/xlvaeapp.pth", MIN_SMALL),
    ("models/vae_approx/vaeapp_sd15.pth", "https://huggingface.co/lllyasviel/misc/resolve/main/vaeapp_sd15.pt", MIN_SMALL),
    (
        "models/vae_approx/xl-to-v1_interposer-v4.0.safetensors",
        "https://huggingface.co/mashb1t/misc/resolve/main/xl-to-v1_interposer-v4.0.safetensors",
        MIN_SMALL,
    ),
    (
        "models/prompt_expansion/fooocus_expansion/pytorch_model.bin",
        "https://huggingface.co/lllyasviel/misc/resolve/main/fooocus_expansion.bin",
        MIN_SMALL,
    ),
]

FOOOCUS_AUX: list[tuple[str, str, int]] = [
    ("models/inpaint/fooocus_inpaint_head.pth", "https://huggingface.co/lllyasviel/fooocus_inpaint/resolve/main/fooocus_inpaint_head.pth", MIN_SMALL),
    ("models/inpaint/inpaint.fooocus.patch", "https://huggingface.co/lllyasviel/fooocus_inpaint/resolve/main/inpaint.fooocus.patch", MIN_SMALL),
    ("models/inpaint/inpaint_v25.fooocus.patch", "https://huggingface.co/lllyasviel/fooocus_inpaint/resolve/main/inpaint_v25.fooocus.patch", MIN_SMALL),
    ("models/inpaint/inpaint_v26.fooocus.patch", "https://huggingface.co/lllyasviel/fooocus_inpaint/resolve/main/inpaint_v26.fooocus.patch", MIN_SMALL),
    ("models/loras/sdxl_lcm_lora.safetensors", "https://huggingface.co/lllyasviel/misc/resolve/main/sdxl_lcm_lora.safetensors", MIN_LORA),
    (
        "models/loras/sdxl_lightning_4step_lora.safetensors",
        "https://huggingface.co/mashb1t/misc/resolve/main/sdxl_lightning_4step_lora.safetensors",
        MIN_LORA,
    ),
    (
        "models/loras/sdxl_hyper_sd_4step_lora.safetensors",
        "https://huggingface.co/mashb1t/misc/resolve/main/sdxl_hyper_sd_4step_lora.safetensors",
        MIN_LORA,
    ),
    (
        "models/controlnet/control-lora-canny-rank128.safetensors",
        "https://huggingface.co/lllyasviel/misc/resolve/main/control-lora-canny-rank128.safetensors",
        MIN_LORA,
    ),
    (
        "models/controlnet/fooocus_xl_cpds_128.safetensors",
        "https://huggingface.co/lllyasviel/misc/resolve/main/fooocus_xl_cpds_128.safetensors",
        MIN_LORA,
    ),
    (
        "models/clip_vision/clip_vision_vit_h.safetensors",
        "https://huggingface.co/lllyasviel/misc/resolve/main/clip_vision_vit_h.safetensors",
        MIN_SMALL,
    ),
    (
        "models/controlnet/fooocus_ip_negative.safetensors",
        "https://huggingface.co/lllyasviel/misc/resolve/main/fooocus_ip_negative.safetensors",
        MIN_SMALL,
    ),
    (
        "models/controlnet/ip-adapter-plus_sdxl_vit-h.bin",
        "https://huggingface.co/lllyasviel/misc/resolve/main/ip-adapter-plus_sdxl_vit-h.bin",
        MIN_SMALL,
    ),
    (
        "models/controlnet/ip-adapter-plus-face_sdxl_vit-h.bin",
        "https://huggingface.co/lllyasviel/misc/resolve/main/ip-adapter-plus-face_sdxl_vit-h.bin",
        MIN_SMALL,
    ),
    (
        "models/upscale_models/fooocus_upscaler_s409985e5.bin",
        "https://huggingface.co/lllyasviel/misc/resolve/main/fooocus_upscaler_s409985e5.bin",
        MIN_SMALL,
    ),
    (
        "models/safety_checker/stable-diffusion-safety-checker.bin",
        "https://huggingface.co/mashb1t/misc/resolve/main/stable-diffusion-safety-checker.bin",
        MIN_SMALL,
    ),
]


def collect_presets(only_focus: bool) -> tuple[dict, dict, dict]:
    ckpt, lora, vae = {}, {}, {}
    names = sorted(PRESETS_DIR.glob("*.json"))
    for p in names:
        if only_focus and p.name not in FOCUS_PRESETS:
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[warn] preset ignorado {p.name}: {e}")
            continue
        ckpt.update(data.get("checkpoint_downloads", {}))
        lora.update(data.get("lora_downloads", {}))
        vae.update(data.get("vae_downloads", {}))
    for fname, url in REED_HF_CANDIDATES:
        ckpt.setdefault(fname, url)
    return ckpt, lora, vae


def download_url(url: str, dest: Path, min_bytes: int) -> str:
    if "civitai.com" in url.lower():
        return "blocked_civitai"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_file() and dest.stat().st_size >= min_bytes:
        return "skipped"
    tmp = dest.with_suffix(dest.suffix + ".part")
    resume = tmp.stat().st_size if tmp.is_file() else 0
    headers = {"User-Agent": "Fooocus-local-download/1.0"}
    if resume:
        headers["Range"] = f"bytes={resume}-"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            mode = "ab" if resume and resp.status == 206 else "wb"
            if mode == "wb":
                resume = 0
            total = resp.headers.get("Content-Length")
            total = int(total) + resume if total and mode == "ab" else (int(total) if total else None)
            with open(tmp, mode) as f:
                while True:
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
    except urllib.error.HTTPError as e:
        if resume and e.code == 416:
            pass
        else:
            return f"http_error:{e.code}"
    except Exception as e:
        return f"error:{e}"
    if not tmp.is_file():
        return "missing_part"
    size = tmp.stat().st_size
    if size < min_bytes:
        try:
            tmp.unlink()
        except OSError:
            pass
        return f"too_small:{size}"
    if dest.is_file():
        dest.unlink()
    tmp.replace(dest)
    return "downloaded"


def main() -> int:
    only_focus = "--all-presets" not in sys.argv
    skip_aux = "--no-aux" in sys.argv
    ckpt_map, lora_map, vae_map = collect_presets(only_focus)

    stats = {"downloaded": [], "skipped": [], "failed": []}

    def run_item(label: str, dest: Path, url: str, min_b: int):
        if not url:
            stats["failed"].append((label, "no_url"))
            print(f"[fail] {label}: sem URL")
            return
        status = download_url(url, dest, min_b)
        if status == "skipped":
            stats["skipped"].append(label)
            print(f"[skip] {label} ({dest.stat().st_size/1e9:.2f} GB)")
        elif status == "downloaded":
            stats["downloaded"].append(label)
            print(f"[ok] {label} ({dest.stat().st_size/1e9:.2f} GB)")
        elif status == "blocked_civitai":
            stats["failed"].append((label, status))
            print(f"[fail] {label}: Civitai bloqueado")
        else:
            stats["failed"].append((label, status))
            print(f"[fail] {label}: {status}")

    print("=== Checkpoints ===")
    for fname, url in sorted(ckpt_map.items()):
        if not url.strip():
            stats["failed"].append((fname, "empty_url_in_preset"))
            print(f"[fail] {fname}: preset sem URL (ex.: REED — só Civitai)")
            continue
        run_item(fname, ROOT / "models/checkpoints" / fname, url, MIN_CHECKPOINT)

    print("=== Loras ===")
    for fname, url in sorted(lora_map.items()):
        run_item(fname, ROOT / "models/loras" / fname, url, MIN_LORA)

    print("=== VAE ===")
    for fname, url in sorted(vae_map.items()):
        run_item(fname, ROOT / "models/vae" / fname, url, MIN_VAE)

    print("=== Launch essentials ===")
    for rel, url, min_b in FOOOCUS_LAUNCH_ESSENTIALS:
        run_item(rel, ROOT / rel, url, min_b)

    if not skip_aux:
        print("=== Fooocus aux (controlnet, inpaint, ...) ===")
        for rel, url, min_b in FOOOCUS_AUX:
            run_item(rel, ROOT / rel, url, min_b)

    # REED default_model without download entry
    reed_preset = PRESETS_DIR / "reed_illustrious_v12.json"
    if reed_preset.is_file():
        reed = json.loads(reed_preset.read_text(encoding="utf-8"))
        dm = reed.get("default_model")
        p = ROOT / "models/checkpoints" / dm
        if dm and not p.is_file():
            stats["failed"].append((dm, "reed_no_hf_in_preset"))
            print(f"[fail] {dm}: não há URL HF no preset; baixe manualmente (Civitai) ou adicione REED_HF_CANDIDATES")

    total_bytes = sum(f.stat().st_size for f in ROOT.joinpath("models").rglob("*") if f.is_file())
    print("\n=== Resumo ===")
    print("Baixados:", len(stats["downloaded"]))
    for x in stats["downloaded"]:
        print("  +", x)
    print("Já existiam:", len(stats["skipped"]))
    print("Falharam:", len(stats["failed"]))
    for x, why in stats["failed"]:
        print(f"  ! {x}: {why}")
    print(f"Espaço total em models/: {total_bytes/1e9:.2f} GB")
    return 1 if stats["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
