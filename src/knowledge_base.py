from pyswip import Prolog

# This sould be done using consult, but it seems to be working...
knowledge_base = Prolog()

knowledge_base.dynamic("team/1")
knowledge_base.dynamic("player/2")
knowledge_base.dynamic("playsinteam/2")
knowledge_base.dynamic("hitbluegoal/3")
knowledge_base.dynamic("hitredgoal/3")

# Setup information
knowledge_base.assertz("""narrative(Text) :- team(X), format(atom(Text), "Team: ~w.", [X])""")
knowledge_base.assertz("""narrative(Text) :- playsinteam(X, Y), format(atom(Text), "Player ~w in team ~w.", [X, Y])""")

# Score goals and own goals
knowledge_base.assertz("""narrative(Text) :- hitbluegoal(X, Y, _), playsinteam(X, blue), format(atom(Text), "Player ~w scored the point number ~w", [X, Y])""")
knowledge_base.assertz("""narrative(Text) :- hitbluegoal(X, Y, _), playsinteam(X, red), format(atom(Text), "Player ~w made a own-goal for the point number ~w", [X, Y])""")

knowledge_base.assertz("""narrative(Text) :- hitredgoal(X, Y, _), playsinteam(X, red), format(atom(Text), "Player ~w scored the point number ~w", [X, Y])""")
knowledge_base.assertz("""narrative(Text) :- hitredgoal(X, Y, _), playsinteam(X, blue), format(atom(Text), "Player ~w made a own-goal for the point number ~w", [X, Y])""")

knowledge_base.assertz("""narrative(Text) :- format(atom(Text), "Total score: ~w : ~w.", [score(1), score(0)])""")
#knowledge_base.assertz("""narrative(Text) :- scored(Player), format(atom(Text), "~w scored.", [Player])""")
knowledge_base.assertz("""all_narratives(Narratives) :- findall(Text, narrative(Text), Narratives)""")