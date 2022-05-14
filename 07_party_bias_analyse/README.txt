### party_bias.py

Le rice index des groupes d'âge est calculé sans prendre en conte les parties ou des autres facteurs (regardez 06_commision_age_analyse).
Néonmoins, les différentes parties n'ont pas des même distributions de l'âge. Par example, les Vertes est une partie beaucoup plus jeune que les autres.
Alors, les groupes d'âge ne sont pas indépendant des parties. Il faut analyser le bias qui est introduit par les parties dans l'analyse du rice index
des différente groupe d'âge. Le programme party_bias.py essaye d'estimer ce bias par comparer le rice index des groupes d'âge qui était utiliser dans
les analyses précédants (regardez 06_commision_age_analyse) avec un rice index de référance. Ce rice index de référance prend en compte que 
les parties ne sont pas réprésentées du même façon dans chaque groupe d'âge. Alors, on calcule un poid pour chaque vote qui est lié à la quantité des personnes 
d'une partie dans une groupe d'âge. Si une partie a peu personnes dans une groupe d'âge, ce poid est plus grand que 1 et va "emplifier" les votes des 
personnes de cette partie. En contraire, si une partie a plus personnes que la moyenne dans une groupe d'âge, le poid est moins grand que 1 et va 
"diminuer" l'influence des votes. On prend aussi en compte la taille des différentes parties (pultiplier le poid par la taille d'une partie
diviser par la taille totale du parlament). A la fin, ça donne un rice index de référance qui simule un parlament ou toutes les parties ont la même
quantité de personnes dans chaque groupe d'âge.

Le rice index de référance peut être comparer avec celui du vrai parlament (ou les parties ne sont pas équilibrées dans les groupes d'âge). Si l'erreur
entre les deux est petit, ça veut dire que le bias des parties sur l'analyse du rice index des groupes d'âge n'est pas important. Si l'erreur est grand,
ça veut dire que la distribution de l'âge des différentes parties introduit un bias dans l'analyse du rice index (si on cosidere seulement l'influence des
groupes d'âge et on ignore l'influence des parties, ce qu'on a fait dans 06_commision_age_analyse).

Dans la figure party_bias.png on voit les résultats. La figure montre que le bias n'est pas négligable pour les groupes d'âge 49-60 et 60-80. L'ordre du 
rice index et exactement inverser si on fait le calcule de référance (avec le parlament pondéré ou toutes les parties sont réprésentées du même façon dans 
chaque groupe d'âge). Mais la tendance que les jeunes (28-48) on un rice index moins élévé reste la même. Pour l'analyse du rice index des différentes 
groupes d'âge (sans prendre en compte l'influence des parties) ça veut dire le suivant: Si on compare les groupes d'âges 49-60 et 60-80, il faut faire prendre
conscience qu'il y a un bias des parties assez fort. Ce bias n'est pas visible si on represente seulement le rice index en fonction des groupes d'âge. Néonmoins,
ces analyses sont comme même intéressantes parce que la distribution des groupes d'âge pour chaque partie est un attribut intrinsique du parlament. Et très
probablement ce effet ne va pas changer beaucoup dans le futur. Si on compare les groupes 49-60 et 60-80 avec la groupe 28-48, on peut supposer que le bias des 
parties n'a pas un influence important. Ce point souligne le résultat que les jeunes sont significativement moins cohérants que les plus âgés.

Note, que l'analyse avec le rice index de référance est seulement fait pour tous les votes et n'est pas fais pour toutes les commissions séparémentes parce 
que le nombre des votes dans quelque commission est assez bas. ça fait le calcule du rice index de référance beaucoup moins valable parce que la pondération
des votes fait seulement du sense si on a des grandes données qui peut donner des moyennes significatives. Note aussi, que l'erreur sur la figure party_bias.png
n'est pas forcément la différance entre le rice index de référance ("Mean weighted votes") moins le rice index non-pondéré ("Mean unweighted votes") parce que 
l'erreur est calculé pour chaque vote et le "Mean error" c'est la moyenne de tous les erreurs.