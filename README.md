# De la lettre au son

### Synthèse vocale, clonage, et ce qui manque à nos langues béninoises

**Atelier · IndabaX Bénin 2026 · Track principal B2 · Cotonou, 11 septembre**
**14 h 10 – 15 h 10 · salle PREFAB, 50 places**

---

## L'atelier en une phrase

Les participants assemblent un phonémiseur en français : là où toutes les ressources
existent et où chaque étape se vérifie : puis basculent sur le Fongbé et mesurent
eux-mêmes ce qui bloque.

Le blocage n'est ni le modèle, ni le code : **c'est le texte.**

## Ce que les participants emportent

1. Un phonémiseur qu'ils ont assemblé pièce par pièce
2. Une entrée de dictionnaire qu'ils ont réparée eux-mêmes
3. Leur propre voix, clonée, disant une phrase qu'ils n'ont jamais prononcée
4. Une mesure obtenue sur leur écran

## Le notebook

[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Arnel7/de-la-lettre-au-son/blob/main/notebook-indabax.ipynb)

[`notebook-indabax.ipynb`](notebook-indabax.ipynb) : Google Colab, processeur seul.
Environ 90 Mo de téléchargement par participant, dont 63 Mo pour la voix Piper.

Les cellules sont pré-écrites : on assemble, on ne code pas de zéro. Sept points sont à
compléter, aux étapes 1, 2, 3, 5 et 6. L'étape 4 n'en a pas : on y enregistre sa voix et
on écoute. Une cellule de secours reconstruit l'état de n'importe quelle étape, pour que
personne ne reste bloqué.

| étape | contenu | durée |
|---|---|--:|
| 1 | Voir un phonémiseur qui marche | 3 min |
| 2 | Nettoyer, puis découper | 4 min |
| 3 | Chercher dans le dictionnaire, et réparer une entrée | 5 min |
| 4 | La machine peut-elle fabriquer le texte ? | 6 min |
| 5 | Bascule Fongbé, et la mesure | 4 min |
| 6 | Écouter le résultat | 3 min |
| | | **25 min** |

## La démonstration centrale

Sur **« les poules du couvent couvent »**, gruut identifie correctement le nom et le
verbe, et prononce quand même les deux `kuvɑ̃`. Les deux prononciations sont pourtant
déjà dans le dictionnaire français.

```sql
UPDATE word_phonemes SET role = 'gruut:NOUN' WHERE word = 'couvent' AND pron_order = 0;
UPDATE word_phonemes SET role = 'gruut:VERB' WHERE word = 'couvent' AND pron_order = 1;
```

Deux lignes, et le verbe se prononce `kuv`.

Rien n'a été ajouté : `k u v` était déjà là. On a rempli **la case qui dit quand
l'utiliser**. Une entrée de dictionnaire n'est pas `mot → son`, c'est
`(mot, condition) → son`.

Vérifié sur le dictionnaire livré avec gruut 2.4.0 :

| | |
|---|--:|
| mots | 90 114 |
| mots à plusieurs prononciations | 1 870 |
| lignes portant la condition qui les départage | **0** |

## Les services distants

Trois appels du notebook passent par une infrastructure hébergée sur Modal, pour éviter
que trente personnes téléchargent plusieurs gigaoctets de modèles pendant la séance.

| service | modèle | usage |
|---|---|---|
| transcription | `Systran/faster-whisper-large-v3` | étape 4b : la machine écrit ce qu'elle entend |
| clonage | `Qwen/Qwen3-TTS-12Hz-1.7B-Base` | étape 4c : la voix du participant |
| transcription Fongbé | `chrisjay/fonxlsr` | étape 4d : et le ton, où est-il passé ? |

**Une clé est nécessaire.** Elle est donnée en séance, écrite au tableau, et la première
cellule de l'étape 4 commence par `CLE = ''`. Elle n'est pas dans le dépôt.

Chaque cellule concernée a un repli : si le service ne répond pas, un résultat
pré-enregistré s'affiche avec un message explicite, et la séance continue.

Le modèle Fongbé peut aussi tourner en local : le code est donné en fin d'étape 4, avec
son coût : 1,26 Go.

## Pour exécuter le notebook sans la clé

Les étapes 1, 2, 3, 5 et 6 ne dépendent d'aucun service et fonctionnent seules. Seule
l'étape 4 bascule sur ses replis.

## Ce qui manque au Fongbé

Cinq des six pièces d'un phonémiseur existent, dans
[`fongbe_g2p`](https://github.com/Arnel7/fongbe-g2p) : digraphes `gb`, `kp`, `ny`,
nasalisation contextuelle, quatre tons, sortie IPA, licence MIT.

La sixième est le dictionnaire, et il n'existe pas dans un format lisible par une
machine.

L'étape 5 le montre sur une phrase tirée de *Lire et compter en fongbé pour ceux qui
savent lire le français*, page 15 :

```
E ɖɔ nu mi        ->  e˧ ɖ ɔ˧ n u˧ m i˧      une seule sortie

É ɖɔ̀ nú mì   Il m'a dit          È ɖɔ̀ nú mì   On m'a dit
É ɖɔ̀ nú mi   Il vous a dit       È ɖɔ̀ nú mi   On vous a dit
É ɖɔ̀ nú mǐ   Il nous a dit       È ɖɔ̀ nú mǐ   On nous a dit
```

Six sens, six sorties distinctes quand les tons sont écrits. Une seule quand ils ne le
sont pas, et **100 % des voyelles en ton moyen**.

Il manque donc deux ressources distinctes, et aucune des deux n'est du code :

1. **un dictionnaire de prononciation** lisible par une machine, la sixième pièce ;
2. **du texte fongbé tonné**, validé par des linguistes.

La première donne les prononciations. La seconde est ce qui permettrait d'entraîner la
restauration des tons, que l'écriture courante n'écrit pas.

## Contenu du dépôt

| | |
|---|---|
| `notebook-indabax.ipynb` | le notebook de l'atelier |
| `deck-indabax.pptx` | les diapositives, 16 slides |
| `deck-indabax.pdf` | les mêmes, pour lecture directe |
| `requirements.txt` | dépendances, pour exécution hors Colab |
| `audios/` | les extraits de l'ouverture, normalisés au même niveau |
| `clonage/` | le service Modal et sa documentation |
| `LICENSE` | MIT |

Le script qui génère les diapositives n'est pas publié : il dépend du gabarit officiel
d'IndabaX, qui ne se redistribue pas.

## Licence

Ce dépôt est publié sous licence MIT. Vous pouvez l'utiliser, le modifier et le
redistribuer, y compris pour un usage commercial.

## Dépendances et licences

| | licence |
|---|---|
| [gruut](https://github.com/rhasspy/gruut) 2.4.0 | MIT |
| [piper-tts](https://github.com/OHF-Voice/piper1-gpl) | GPL-3.0 |
| voix `fr_FR-siwis-medium` | MIT |
| [fongbe_g2p](https://github.com/Arnel7/fongbe-g2p) | MIT |
| [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) | Apache-2.0 |
| `facebook/mms-tts-fon` | CC-BY-NC 4.0 : écoute seule, à titre d'illustration |

Aucune API payante pour les participants, aucun compte requis en dehors de Google Colab.
L'infrastructure de clonage tourne sur le compte de l'intervenant.

## Données et consentement

Les enregistrements de volontaires réalisés pendant la session le sont avec accord oral
enregistré, servent uniquement pendant la séance, et sont supprimés ensuite.

Les extraits enregistrés par les participants dans le notebook restent dans leur propre
session Colab et ne sont conservés nulle part.

## Sources

G. Guillet, *Principes de l'écriture et de la lecture de la langue Fon.*
*Lire et compter en fongbé pour ceux qui savent lire le français*, p. 15.
