# Fooocus no Docker — Guia de Configuração

Este guia descreve como executar o Fooocus com Docker Compose no Windows, com modelos persistentes no host, download automático dos presets na primeira execução, e integração dos modelos SDXL do [Automatic1111 WebUI](D:/Apps/stable-diffusion-webui).

Documentação upstream (inglês): [docker.md](docker.md)

---

## Requisitos

| Componente | Detalhe |
|---|---|
| **Docker Desktop** | Com backend WSL2 (Windows) |
| **GPU NVIDIA** (recomendado) | Drivers atualizados + [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) |
| **Espaço em disco** | ~15–30 GB para modelos preset + os seus SDXL do WebUI |
| **WebUI** (opcional) | `D:\Apps\stable-diffusion-webui` — checkpoints e LoRAs SDXL montados automaticamente |

---

## Estrutura de ficheiros

```
Fooocus/
├── docker-compose.yml          # Compose principal (GPU)
├── docker-compose.cpu.yml      # Override sem GPU
├── docker/
│   └── config.txt              # Config Docker: paths Linux + default_model SDXL
├── Dockerfile
├── entrypoint.sh
├── DOCKER-SETUP.md             # Este ficheiro
└── models/                     # Bind mount → /content/data/models
    ├── checkpoints/
    │   ├── juggernautXL_v8Rundiffusion.safetensors
    │   └── webui-sdxl/         # Sobrescrito pelo mount do WebUI (ver abaixo)
    ├── loras/
    ├── vae/
    ├── controlnet/
    ├── inpaint/
    └── ...
```

### Paths dentro do container

| Path no container | Origem |
|---|---|
| `/content/app` | Código da aplicação (imagem) |
| `/content/data` | Dados persistentes (modelos, config) |
| `/content/data/models` | Bind: `d:/Apps/Fooocus/models` |
| `/content/data/models/checkpoints/webui-sdxl` | Bind: WebUI `Stable-diffusion` (ro) |
| `/content/data/models/loras/webui-sdxl-loras` | Bind: WebUI `Lora` (ro) |
| `/content/data/outputs` | Bind: `d:/Apps/Fooocus/outputs` |
| `/content/app/outputs` | Symlink → `/content/data/outputs` |

---

## Passo a passo

### 1. Validar a configuração

```powershell
cd D:\Apps\Fooocus
docker compose config
```

Deve imprimir o YAML mesclado sem erros.

### 2. Construir a imagem (recomendado na primeira vez)

Usa o `Dockerfile` local (CUDA 12.4, PyTorch 2.1, pins fastapi/starlette/pydantic):

```powershell
docker compose build
```

Alternativa sem build — só puxar imagem upstream (pode não ter os pins de dependências locais):

```powershell
docker compose pull
```

### 3. Subir o container

**Com GPU NVIDIA:**

```powershell
docker compose up
```

**Em segundo plano:**

```powershell
docker compose up -d
docker compose logs -f
```

**Sem GPU (CPU, muito lento):**

```powershell
docker compose -f docker-compose.yml -f docker-compose.cpu.yml up
```

Ou comente o bloco `deploy.resources.reservations.devices` em `docker-compose.yml`.

### 4. Abrir a interface

Quando aparecer no log:

```
Use the app with http://0.0.0.0:7865/
```

Abra no browser: **http://localhost:7865**

---

## Modelo SDXL padrão

Configurado em `docker/config.txt` e via variável de ambiente:

| Chave | Valor |
|---|---|
| `default_model` | `[SDXL] RealVis XL v5 - Fotorrealismo.safetensors` |
| `previous_default_models` | Juggernaut XL Ragnarok, juggernautXL_v8Rundiffusion |

Se o RealVis não existir, o Fooocus tenta os fallbacks antes de descarregar novos modelos.

Para mudar para Juggernaut como padrão, edite `docker/config.txt`:

```json
"default_model": "[SDXL] Juggernaut XL Ragnarok - Fotorrealismo.safetensors"
```

Ou defina no `docker-compose.yml`:

```yaml
- default_model=[SDXL] Juggernaut XL Ragnarok - Fotorrealismo.safetensors
```

---

## O que é descarregado automaticamente vs. o que vem do WebUI

### Download automático (primeira execução)

Na primeira execução, o Fooocus descarrega para `d:\Apps\Fooocus\models\` (via bind mount):

| Categoria | Ficheiros | URL base |
|---|---|---|
| **Checkpoint preset** | `juggernautXL_v8Rundiffusion.safetensors` | [huggingface.co/lllyasviel/fav_models](https://huggingface.co/lllyasviel/fav_models) |
| **LoRA preset** | `sd_xl_offset_example-lora_1.0.safetensors` | [huggingface.co/stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| **VAE approx** | `xlvaeapp.pth`, `vaeapp_sd15.pth`, `xl-to-v1_interposer-v4.0.safetensors` | [huggingface.co/lllyasviel/misc](https://huggingface.co/lllyasviel/misc) |
| **Prompt expansion** | `pytorch_model.bin` (fooocus_expansion) | huggingface.co/lllyasviel/misc |
| **Inpaint** | `fooocus_inpaint_head.pth`, patches v1/v2.5/v2.6 | huggingface.co/lllyasviel/fooocus_inpaint |
| **LoRA utilitários** | `sdxl_lcm_lora`, `sdxl_lightning_4step_lora`, `sdxl_hyper_sd_4step_lora` | huggingface.co |
| **ControlNet** | `control-lora-canny-rank128`, `fooocus_xl_cpds_128` | huggingface.co/lllyasviel/misc |
| **IP-Adapter / CLIP** | `clip_vision_vit_h`, `fooocus_ip_negative`, IP adapters SDXL | huggingface.co/lllyasviel/misc |
| **Upscaler** | `fooocus_upscaler_s409985e5.bin` | huggingface.co/lllyasviel/misc |
| **Safety checker** | `stable-diffusion-safety-checker.bin` | huggingface.co/lllyasviel/misc |
| **SAM** | `sam_vit_b/l/h` (conforme uso) | huggingface.co/lllyasviel/misc |

Para forçar download mesmo com modelos locais: `--always-download-new-model` em `CMDARGS`.

Para saltar downloads preset: `--disable-preset-download` em `CMDARGS`.

### Modelos do WebUI (montados, não copiados)

Estas pastas do Automatic1111 são montadas **read-only** no container:

| Host (Windows) | Container |
|---|---|
| `D:\Apps\stable-diffusion-webui\models\Stable-diffusion` | `/content/data/models/checkpoints/webui-sdxl` |
| `D:\Apps\stable-diffusion-webui\models\Lora` | `/content/data/models/loras/webui-sdxl-loras` |

**Vantagem:** novos checkpoints/LoRAs adicionados ao WebUI aparecem no Fooocus após reiniciar o container (ou refresh da lista de modelos).

**Nota:** a pasta inclui modelos SD 1.5 e SDXL; o Fooocus lista todos os `.safetensors` encontrados. O `default_model` aponta só para SDXL.

Os hardlinks existentes em `Fooocus\models\checkpoints\webui-sdxl` no host Windows são substituídos pelo bind mount directo ao WebUI dentro do container Linux (mais fiável que hardlinks cross-filesystem).

### Modelos já presentes localmente

Ficheiros em `d:\Apps\Fooocus\models\` (ex.: `juggernautXL_v8Rundiffusion.safetensors`, LoRAs locais) são reutilizados — o download só ocorre se o ficheiro não existir.

---

## Volumes e persistência

| Volume bind | Conteúdo |
|---|---|
| `d:/Apps/Fooocus/models` | Todos os modelos (checkpoints, loras, vae, controlnet, inpaint, clip_vision, etc.) |
| `d:/Apps/Fooocus/outputs` | Imagens geradas |
| `./docker/config.txt` | Configuração Docker (read-only) |

Não é usado volume Docker anónimo `fooocus-data` — tudo fica visível no host em `D:\Apps\Fooocus\`.

---

## GPU — resolução de problemas

### Erro: `could not select device driver "nvidia"`

1. Instale [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
2. add restart Docker Desktop
3. Teste: `docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi`

### Fallback CPU

```powershell
docker compose -f docker-compose.yml -f docker-compose.cpu.yml up
```

---

## Comandos úteis

```powershell
# Validar YAML
docker compose config

# Rebuild sem cache (após git pull)
docker compose build --no-cache

# Parar
docker compose down

# Ver logs
docker compose logs -f

# Shell no container
docker compose exec app bash
```

---

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `CMDARGS` | Argumentos para `launch.py` (ex.: `--listen --disable-preset-download`) |
| `HF_MIRROR` | Espelho Hugging Face |
| `default_model` | Sobrescreve modelo padrão |
| `path_*` | Paths simples (arrays em docker/config.txt) |

---

## Referências

- Imagem upstream: [ghcr.io/lllyasviel/fooocus](https://github.com/lllyasviel/Fooocus/pkgs/container/fooocus)
- Interface: http://localhost:7865
- Hugging Face: https://huggingface.co/lllyasviel
