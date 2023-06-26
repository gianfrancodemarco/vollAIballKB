assert((narrative(X, Text) :- format(atom(Text), "Player ~w performed.", ['pinco']))).
assert((narrative(X, Text) :- format(atom(Text), "Player ~w performed.", [X]))). 
assert((write_narrative_to_file(File, X) :- open(File, write, Stream), findall(Text, narrative(X, Text), Texts), write_list_to_stream(Stream, Texts), close(Stream))).
assert(write_list_to_stream(_, [])).
assert((write_list_to_stream(Stream, [Item|Items]) :-write(Stream, Item), nl(Stream), write_list_to_stream(Stream, Items))).