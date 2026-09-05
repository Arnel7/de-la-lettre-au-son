Les quatre audios de l'ouverture (slide 03), dans l'ordre de passage.

1-fr-passe.wav     « bonjour et bienvenue a indabax benin »
                   bɔ̃ʒuʁ e bjɛ̃vəny a ɛ̃dabaks bɛnɛ̃          rien ne casse

2-fr-echoue.wav    « madame gbaguidi travaille a nyekonakpoe »
                   madam ɡbaɡidi tʁavaj a nikɔnakpo
                   attendu : ɲekɔnakpɔe
                   le « ny » devient « ni », la syllabe finale disparaît

3-fon-passe.wav    A PRODUIRE : phrase fongbé dans le domaine de mms-tts-fon
4-fon-echoue.wav   A PRODUIRE : phrase fongbé hors domaine
                   candidats : paire tonale minimale, nom propre, nombre

Les deux fichiers français sont produits par la MEME voix (Piper fr_FR-siwis-medium),
via la chaîne du notebook. Une seule variable change : la phrase.

Niveaux harmonisés, pic à -2,5 dB. Pour les deux fichiers manquants :
  ffmpeg -i entree.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 22050 sortie.wav
