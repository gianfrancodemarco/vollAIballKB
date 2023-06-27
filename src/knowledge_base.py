from pyswip import Prolog

# This sould be done using consult, but it seems to be working...
knowledge_base = Prolog()
knowledge_base.dynamic("scored/1")
knowledge_base.assertz("""narrative(score, Text) :- format(atom(Text), "Total score: ~w : ~w.", [score(1), score(0)])""")
knowledge_base.assertz("""narrative(scored, Text) :- scored(Player), format(atom(Text), "~w scored.", [Player])""")
knowledge_base.assertz("""all_narratives(Narratives) :- findall(Text, narrative(_, Text), Narratives)""")
