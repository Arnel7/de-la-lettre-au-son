"""Endpoint HTTP protege, pour appeler le clonage depuis Colab.

App separee : ne touche pas a `qwen3-tts`, qui reste tel quel.
Reutilise le meme Volume, donc les poids sont deja en cache.

    modal deploy clonage/atelier_app.py
"""

import io

import modal

MODELE = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
CACHE = "/cache"
LIMITE = 800          # nombre total d'appels autorises

cache = modal.Volume.from_name("qwen3-tts-cache", create_if_missing=True)
compteur = modal.Dict.from_name("indabax-compteur", create_if_missing=True)

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg", "sox", "libsox-fmt-all")
    .pip_install("torch", "qwen-tts==0.1.1", "soundfile", "numpy",
                 "hf_transfer", "fastapi[standard]")
    .env({"HF_HOME": CACHE, "HF_HUB_ENABLE_HF_TRANSFER": "1"})
)

app = modal.App("indabax-clonage", image=image)


@app.cls(
    gpu="L4",
    volumes={CACHE: cache},
    secrets=[modal.Secret.from_name("indabax-cle")],
    max_containers=6,        # plafonne la depense : jamais plus de 6 GPU
    scaledown_window=600,
    timeout=300,
)
class Atelier:
    @modal.enter()
    def charger(self):
        import torch
        from qwen_tts import Qwen3TTSModel

        self.modele = Qwen3TTSModel.from_pretrained(
            MODELE, device_map="cuda:0", dtype=torch.bfloat16,
            attn_implementation="sdpa",
        )

    @modal.fastapi_endpoint(method="POST")
    def cloner(self, corps: dict):
        import base64
        import os

        import soundfile as sf
        from fastapi import HTTPException, Response

        if corps.get("cle") != os.environ["CLE"]:
            raise HTTPException(401, "cle invalide")

        appels = compteur.get("appels", 0)
        if appels >= LIMITE:
            raise HTTPException(429, f"quota atteint ({LIMITE} appels)")
        compteur["appels"] = appels + 1

        with open("/tmp/ref.wav", "wb") as f:
            f.write(base64.b64decode(corps["audio_b64"]))

        wavs, sr = self.modele.generate_voice_clone(
            text=corps["texte"],
            language=corps.get("langue", "French"),
            ref_audio="/tmp/ref.wav",
            ref_text=corps["transcription"],
        )

        sortie = io.BytesIO()
        sf.write(sortie, wavs[0], sr, format="WAV")
        return Response(content=sortie.getvalue(), media_type="audio/wav")


# ── Transcription ─────────────────────────────────────────────────────────────
# ctranslate2 exige libcublas et libcudnn au runtime : on part d'une image CUDA,
# pas de debian_slim. Le Volume est celui de kappela-whisper, deja rempli.

MODELE_WHISPER = "large-v3"
DOSSIER_MODELES = "/models"
volume_whisper = modal.Volume.from_name("kappela-whisper-model", create_if_missing=True)

image_whisper = (
    modal.Image.from_registry(
        "nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04", add_python="3.11"
    )
    .apt_install("ffmpeg")
    .pip_install("faster-whisper==1.0.3", "huggingface_hub", "hf_transfer",
                 "requests", "fastapi[standard]")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
)


@app.cls(
    image=image_whisper,
    gpu="L4",
    volumes={DOSSIER_MODELES: volume_whisper},
    secrets=[modal.Secret.from_name("indabax-cle")],
    max_containers=6,
    scaledown_window=600,
    timeout=300,
)
class Transcription:
    @modal.enter()
    def charger(self):
        from faster_whisper import WhisperModel

        self.modele = WhisperModel(
            MODELE_WHISPER, device="cuda", compute_type="float16",
            download_root=DOSSIER_MODELES,
        )
        volume_whisper.commit()

    @modal.fastapi_endpoint(method="POST")
    def transcrire(self, corps: dict):
        import base64
        import io
        import os

        from fastapi import HTTPException

        if corps.get("cle") != os.environ["CLE"]:
            raise HTTPException(401, "cle invalide")

        appels = compteur.get("appels", 0)
        if appels >= LIMITE:
            raise HTTPException(429, f"quota atteint ({LIMITE} appels)")
        compteur["appels"] = appels + 1

        audio = base64.b64decode(corps["audio_b64"])
        langue = corps.get("langue", "fr")      # None = detection automatique

        segments, info = self.modele.transcribe(
            io.BytesIO(audio), language=langue, vad_filter=True, beam_size=5,
        )
        texte = " ".join(s.text.strip() for s in segments).strip()

        return {
            "texte": texte,
            "langue_detectee": info.language,
            "confiance_langue": round(info.language_probability, 3),
        }


# ── Transcription Fongbe ──────────────────────────────────────────────────────
# wav2vec2-large-xlsr affine sur le Fon. Son vocabulaire de sortie CONTIENT des
# marques de ton : a a e e i i o o u u, accents aigu et grave, breves.
# La question de l'atelier est donc : les ecrit-il vraiment ?

MODELE_FON = "chrisjay/fonxlsr"

image_fon = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg")
    .pip_install("torch", "transformers", "soundfile", "librosa",
                 "hf_transfer", "fastapi[standard]")
    .env({"HF_HOME": CACHE, "HF_HUB_ENABLE_HF_TRANSFER": "1"})
)


@app.cls(
    image=image_fon,
    gpu="L4",
    volumes={CACHE: cache},
    secrets=[modal.Secret.from_name("indabax-cle")],
    max_containers=6,
    scaledown_window=600,
    timeout=300,
)
class Fongbe:
    @modal.enter()
    def charger(self):
        from transformers import AutoProcessor, Wav2Vec2ForCTC

        self.proc = AutoProcessor.from_pretrained(MODELE_FON)
        self.modele = Wav2Vec2ForCTC.from_pretrained(MODELE_FON).to("cuda")
        cache.commit()

    @modal.fastapi_endpoint(method="POST")
    def transcrire_fongbe(self, corps: dict):
        import base64
        import io
        import os

        import librosa
        import torch
        from fastapi import HTTPException

        if corps.get("cle") != os.environ["CLE"]:
            raise HTTPException(401, "cle invalide")

        appels = compteur.get("appels", 0)
        if appels >= LIMITE:
            raise HTTPException(429, f"quota atteint ({LIMITE} appels)")
        compteur["appels"] = appels + 1

        audio = base64.b64decode(corps["audio_b64"])
        signal, _ = librosa.load(io.BytesIO(audio), sr=16000, mono=True)

        entree = self.proc(signal, sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            logits = self.modele(entree.input_values.to("cuda")).logits
        texte = self.proc.batch_decode(torch.argmax(logits, dim=-1))[0]

        tons = [c for c in texte if c in "́̀̆áàéèíìóòúù"]
        return {"texte": texte, "marques_de_ton": len(tons), "modele": MODELE_FON}
