# Clonage et transcription : services Modal

Deux services en ligne sur le workspace `arnellawson7`, app **`indabax-clonage`**.
Testés le 4 septembre 2026, tous les deux répondent.

    source   clonage/atelier_app.py
    deployer modal deploy clonage/atelier_app.py

L'app `qwen3-tts` existante n'est pas touchée : c'est une app séparée.

---

## Les deux URL

```
clonage        https://arnellawson7--indabax-clonage-atelier-cloner.modal.run
transcription  https://arnellawson7--indabax-clonage-transcription-transcrire.modal.run
```

La clé est dans `clonage/.cle`, hors dépôt.

---

## Transcrire

```bash
CLE=$(cut -d= -f2 clonage/.cle)

python - <<PY
import base64, requests
audio = base64.b64encode(open("audios/1-fr-passe.wav","rb").read()).decode()
r = requests.post(
    "https://arnellawson7--indabax-clonage-transcription-transcrire.modal.run",
    json={"cle": "$CLE", "audio_b64": audio, "langue": "fr"}, timeout=600)
print(r.json())
PY
```

`langue` accepte `"fr"`, un autre code, ou `null` pour la détection automatique.

**Réponse**

```json
{"texte": "Bonjour et bienvenue à Indabax Bénin.",
 "langue_detectee": "fr",
 "confiance_langue": 1.0}
```

Mesuré : **11 secondes**, conteneur déjà chaud.

---

## Cloner

```bash
python - <<PY
import base64, requests
audio = base64.b64encode(open("volontaire-1.wav","rb").read()).decode()
r = requests.post(
    "https://arnellawson7--indabax-clonage-atelier-cloner.modal.run",
    json={
        "cle": "$CLE",
        "audio_b64": audio,
        "transcription": "le texte exact qu'il a lu",
        "texte": "Bonjour, je suis à IndabaX Bénin.",
        "langue": "French",
    }, timeout=900)
open("clone-1.wav","wb").write(r.content)
PY
```

Réponse : un WAV brut, 24 kHz mono.
Mesuré : **44 secondes**, démarrage à froid compris.

`transcription` est **obligatoire**. C'est la transcription de l'extrait de référence,
pas le texte à prononcer. Sans elle, le modèle refuse.

---

## Le jour J

**1. La veille** : un appel de chaque, pour vérifier que les services répondent et que
les Volumes sont chauds.

**2. Bloc 2 (minute 14)** : chaque volontaire lit le même texte imprimé :

> Bonjour, je m'appelle …………, je suis à Cotonou pour IndabaX Bénin.
> J'accepte que ma voix serve pendant cet atelier.

La deuxième phrase enregistre le consentement et allonge l'extrait. Comme le texte est
connu, il se recopie tel quel dans `transcription` : pas besoin de Whisper.

**3. Pendant la pratique** : un appel de clonage par volontaire. Ils s'enchaînent sans
démarrage à froid tant qu'ils sont espacés de moins de dix minutes.

**4. Bloc 4 (minute 40)** : écoute.

---

## Protections

| | |
|---|---|
| clé partagée | `modal.Secret` nommé `indabax-cle` ; sans elle, `401` |
| plafond de dépense | `max_containers=2` par classe : jamais plus de deux GPU |
| quota | 200 appels au total, compteur dans un `modal.Dict` |
| conteneur chaud | `scaledown_window=600`, dix minutes après le dernier appel |

**Vérifié** : un appel sans clé renvoie `401 {"detail":"cle invalide"}`.

**Après l'atelier**, révoquer la clé :

```bash
modal secret delete indabax-cle
```

**Remettre le compteur à zéro** si le quota est atteint : supprimer la clé `appels`
du Dict `indabax-compteur` depuis le dashboard.

---

## Dans le notebook

L'étape 4 appelle le service de transcription. La cellule commence par `CLE = ''` :
**la clé n'est pas dans le notebook**, elle est écrite au tableau en séance. Le notebook
peut donc être publié sur GitHub sans exposer le compte.

---

## Repli

Le Space officiel `huggingface.co/spaces/Qwen/Qwen3-TTS` fait le même clonage dans le
navigateur, sans Modal ni clé.

---

## Ce qui a été corrigé pendant les tests

`faster-whisper` importe `requests`, absent de l'image au premier déploiement : les
conteneurs redémarraient en boucle avec `ModuleNotFoundError`. Le paquet est ajouté.

À surveiller si tu modifies l'image : l'erreur n'apparaît pas au déploiement, seulement
au premier appel, dans les logs (`modal app logs indabax-clonage`).
