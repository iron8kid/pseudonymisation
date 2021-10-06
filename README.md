# pseudonymisation
Pseudonymisation de données sensibles

# Contexte du projet

Dans le cadre du projet ASESID (Analyse Sémantique Et Syntaxique Informatisée du Discours libre), le CHU de Brest enregistre depuis quelques années des entretiens de bilan psychiatrique de personnes non hospitalisées. Ces entretiens sont transcrits et servent à des études linguistiques dans le but de détecter des signaux faibles qui permettraient de prédire une potentielle pathologie psychiatrique.

Or, il existe une réglementation européenne (alinéas i et j de l’article 9.2 du RGPD) concernant les données personnelles qui est très stricte sur la protection de ces données et rend impossible leur traitement sans une étape de protection préalable. Si les données qui seront traitées dans ce projet seront des données de santé, il faut noter que la pseudonymisation ne se limite aucunement au domaine de la santé.

 

 

# Descriptif succinct du projet

Longtemps cette protection a consisté à « anonymiser » les données, dans le sens du masquage des entités nommées (noms de personnes, de lieux ou d’organismes) ou du remplacement de celles-ci par des codes informatiques : à la place de «mon père enseigne au Lycée naval à Brest» on écrivait «mon père enseigne au ▇​​▇▇▇ à ▇​​▇▇▇» ou «mon père enseigne au XXX031 à XXX007». Cette façon d’anonymiser n’est pas optimale pour les traitements linguistiques puisqu’elle produit des phrases incomplètes, que ce soit syntaxiquement ou sémantiquement. L’Union européenne préconise aujourd’hui une autre méthode de protection des données : la pseudonymisation (voir le texte de la RGPD, https://www.cnil.fr/fr/reglement-europeen-protection-donnees, sections 28 et 29).

La pseudonymisation présente notamment deux challenges : garantir une cohérence sémantique entre les entités nommées et les entités qui les remplacent ; garantir que les entités nommées ne peuvent être retrouvées par un mécanisme d’inférence ou de croisement sur les entités qui les remplacent.

 1. Cohérence sémantique : en pseudonymisant on peut donc écrire « mon père enseigne au Lycée Debussy à Reims », en vérifiant qu’un tel lycée n’existe pas dans cette ville. La difficulté de la pseudonymisation est que le texte doit rester sémantiquement cohérent : on ne peut pas remplacer « lors de notre voyage au Canada on a visité Vancouver » par « lors de notre voyage au Maroc on a visité Tokyo », il faut détecter la relation sémantique entre « Canada » et « Vancouver » et remplacer les deux entités nommées par des entités ayant la même relation (par exemple : « lors de notre voyage au Maroc on a visité Casablanca »).

 2. Inférence et/ou croisement : la pseudonymisation doit garantir que les entités nommées ne peuvent être retrouvées par un mécanisme d’inférence ou de croisement sur les entités qui les remplacent. Par exemple, « la capitale du pays aux 365 fromages » n’est techniquement pas une entité nommée, mais la valeur «Paris» peut être obtenue à l’aide de deux inférences (« pays aux 365 fromages » -> « France », capitale(« France ») -> « Paris »).

Dans ce projet, après avoir consulté la RGPD et le Code de la Santé Publique on détectera d’abord manuellement les infractions à ces deux réglementations dans les entretiens de bilan psychiatrique qui seront fournis, avant de considérer par quelles méthodes du traitement automatique de la langue et de l’ingénierie des connaissances cette détection peut être faite automatiquement, ou semi-automatiquement. 

Ensuite on se posera la question : par quoi remplacer les informations sensibles ? Pour cela, on créera des graphes sémantiques qui modélisent les relations entre elles. En se servant de bases de connaissances comme DBPedia, on procédera à l’insertion de pseudo-informations cohérentes au niveau du graphe sémantique.

La pseudonymisation est un domaine en plein essor et ne se limite aucunement au domaine de la santé (par exemple afin de mettre à disposition en données ouvertes les décisions de justice comme préconisé par la Loi pour une République Numérique ; ou encore dans le domaine bancaire lorsque des traitements sur les données clients sont externalisés) , après tout elle est préconisée par l’Union européenne pour la protection de toutes les données. Ayant travaillé dans ce domaine peut constituer un avantage non-négligeable pour une embauche dans une entreprise européenne.

 La «partenaire industriel» est Christophe LEMEY, psychiatre au CHU de Brest.

# Livrables identifiés

Rapport d’étude de la faisabilité d’un outil pouvant répondre au problème posé. Prototypage. Rapport de tests sur données réelles.

Code source et documentation associée.

Selon l’avancée des travaux et des résultats obtenus, une publication scientifique ou un article de médiation pourront être envisagés.

# Données d'entrée fournies par les encadrants

Cahier des charges des livrables attendus

Quelques références :

https://tel.archives-ouvertes.fr/tel-01783967/document

https://www.cnil.fr/fr/identifier-les-donnees-personnelles

https://guides.etalab.gouv.fr/pseudonymisation/en-pratique/
