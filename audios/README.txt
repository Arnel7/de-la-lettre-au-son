Les quatre audios de l'ouverture (slide 03), dans l'ordre de passage.

1-fr-passe.wav     « bonjour et bienvenue a indabax benin »
                   bɔ̃ʒuʁ e bjɛ̃vəny a ɛ̃dabaks bɛnɛ̃          rien ne casse

2-fr-echoue.wav    « les poules du couvent couvent »
                   le pul dy kuvɑ̃ kuvɑ̃
                   attendu : le pul dy kuvɑ̃ kuv
                   le verbe se prononce comme le nom : gruut sort deux fois
                   la meme chose. C'est la panne reparee en seance, slide 07.

3-fon-passe.wav    « E ɖɔ nu mi »   sans ton, comme tout le monde l'ecrit
                   21 symboles recus, rien n'est jete. Le modele dit du
                   fongbe correct : la synthese vocale fongbe existe.

4-fon-echoue.wav   « É ɖɔ̀ nú mì »  les tons ecrits : « Il m'a dit »
                   21 symboles aussi. L'accent grave de ɔ̀ est jete.
                   Ecrire les tons ne change pas le resultat : mesure a
                   bruit fixe, l'ecart est celui de deux tirages du modele.

                   La question a poser apres l'audio 4 n'est PAS
                   « entendez-vous une difference ? » mais
                   « lequel des six sens venez-vous d'entendre ? ».
                   Personne ne peut repondre : c'est la demonstration.

Les deux fichiers fongbé sont produits par facebook/mms-tts-fon, 16 kHz a la
source, reechantillonnes en 22050 Hz. UNE SEULE VARIABLE CHANGE : les tons.

Les deux fichiers français sont produits par la MEME voix (Piper fr_FR-siwis-medium),
via la chaîne du notebook. Une seule variable change : la phrase.

Niveaux harmonisés, pic à -2,5 dB. Pour les deux fichiers manquants :
  ffmpeg -i entree.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 22050 sortie.wav
