from pyswip import Prolog

# This sould be done using consult, but it seems to be working...
knowledge_base = Prolog()

knowledge_base.dynamic("team/1")
knowledge_base.dynamic("player/1")
knowledge_base.dynamic("playsinteam/2")
knowledge_base.dynamic("hitbluegoal/3")
knowledge_base.dynamic("hitredgoal/3")
knowledge_base.dynamic("hitoutofbounds/3")
knowledge_base.dynamic("hitwall/3")
knowledge_base.dynamic("doubletouch/3")
knowledge_base.dynamic("narrative/1")
knowledge_base.dynamic("touchplayerataction/4")

# Setup information
knowledge_base.assertz("""narrative(Text) :- team(X), format(atom(Text), "Team: ~w.", [X])""")
knowledge_base.assertz("""narrative(Text) :- playsinteam(X, Y), format(atom(Text), "Player ~w in team ~w.", [X, Y])""")

# Score goals and own goals
knowledge_base.assertz("""narrative(Text) :- hitbluegoal(X, Y, _), playsinteam(X, blue), format(atom(Text), "Player ~w scored! (point ~w)", [X, Y])""")
knowledge_base.assertz("""narrative(Text) :- hitbluegoal(X, Y, _), playsinteam(X, red), format(atom(Text), "Player ~w made a own-goal -.-' (point ~w)", [X, Y])""")

knowledge_base.assertz("""narrative(Text) :- hitredgoal(X, Y, _), playsinteam(X, red), format(atom(Text), "Player ~w scored! (point ~w)", [X, Y])""")
knowledge_base.assertz("""narrative(Text) :- hitredgoal(X, Y, _), playsinteam(X, blue), format(atom(Text), "Player ~w made a own-goal -.-' (point ~w)", [X, Y])""")

# Special cases that score a point
knowledge_base.assertz("""narrative(Text) :- hitoutofbounds(X, Y, _), format(atom(Text), "Player ~w sent the ball flying in space! (point ~w)", [X, Y])""")
knowledge_base.assertz("""narrative(Text) :- hitwall(X, Y, _), format(atom(Text), "Player ~w tried to break the wall! (point ~w)", [X, Y])""")
knowledge_base.assertz("""narrative(Text) :- doubletouch(X, Y, _), format(atom(Text), "Player ~w wants the ball all for himself :O (point ~w)", [X, Y])""")

# Compute current score
knowledge_base.assertz("""narrative(Text) :- 
    playsinteam(X1, blue), aggregate_all(count, hitbluegoal(X1, _, _), BlueGoals), 
    playsinteam(X2, red), aggregate_all(count, hitbluegoal(X2, _, _), RedOwnGoals), 
    playsinteam(X3, red), aggregate_all(count, hitoutofbounds(X3, _, _), RedOutOfBounds),
    playsinteam(X4, red), aggregate_all(count, doubletouch(X4, _, _), RedDoubleTouches),

    playsinteam(X5, red), aggregate_all(count, hitredgoal(X5, _, _), RedGoals), 
    playsinteam(X6, blue), aggregate_all(count, hitredgoal(X6, _, _), BlueOwnGoals),
    playsinteam(X7, blue), aggregate_all(count, hitoutofbounds(X7, _, _), BlueOutOfBounds),
    playsinteam(X8, blue), aggregate_all(count, doubletouch(X8, _, _), BlueDoubleTouches),

    plus(BlueGoals, RedOwnGoals, BlueScorePartial1),
    plus(BlueScorePartial1, RedOutOfBounds, BlueScorePartial2),
    plus(BlueScorePartial2, RedDoubleTouches, BlueScore),

    plus(RedGoals, BlueOwnGoals, RedScorePartial1),
    plus(RedScorePartial1, BlueOutOfBounds, RedScorePartial2),
    plus(RedScorePartial2, BlueDoubleTouches, RedScore),

    format(atom(Text), "Red ~w - ~w Blue", [RedScore, BlueScore])"""
)

# Nice actions
knowledge_base.assertz("""ace(X1, Y) :- hitredgoal(X1, Y, _), playsinteam(X1, red), touchplayerataction(X1, Y, _, _), playsinteam(X2, blue), \+touchplayerataction(X2, Y, _, _)""")
knowledge_base.assertz("""ace(X1, Y) :- hitbluegoal(X1, Y, _), playsinteam(X1, blue), touchplayerataction(X1, Y, _, _), playsinteam(X2, red), \+touchplayerataction(X2, Y, _, _)""")
knowledge_base.assertz("""narrative(Text) :- ace(X, Y), format(atom(Text), "Ace for player ~w (point ~w)", [X, Y])""")

knowledge_base.assertz("""greataction(Y) :- 
    player(X1),
    \+doubletouch(X1, _, _),
    touchplayerataction(_, Y, _, _),
    aggregate_all(count, touchplayerataction(_, Y, _, _), DribblesInAction),
    DribblesInAction > 2""")
knowledge_base.assertz("""narrative(Text) :- greataction(Y), format(atom(Text), "Great action! (point ~w)", [Y])""")

knowledge_base.assertz("""all_narratives(Narratives) :- findall(Text, narrative(Text), Narratives)""")