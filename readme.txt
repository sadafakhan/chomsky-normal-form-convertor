Sadaf Khan, HW2, LING571, 10/20/2021. 

This is one of the longer projects I've done in a while, and I had the hardest time debugging. Unfortunately, I only learned best debugging practices as I graduated in the beginning of the pandemic, so I didn't have a lot of memory of what was taught. There were a lot of places for issues to occur in this program, and using print statements to get a look "inside" got really tedious. I will researching debugging methods this weekend as a result. 

Initially, when I created the function to cut down the unitary rules, I kept two lists: one, with the new non-unitary productions, and another list with all the unitary productions that were to get deleted. That way, if the program ran on the sample cfg, it would return a cfg that didn't have VP -> V or V -> sat | chased ; it would only have VP -> sat | chased. This caused issues, namely because the rule VP -> V NP was rendered unusable, as V didn't exist. However, in cases where the lexical rule's LHS (e.g. V) is not used anywhere else in the grammar (e.g. VP -> V NP doesn't exist, only VP -> V exists), shouldn't we delete rules like V -> chased | sat? They are technically unreachable after filtering out unitary rules. 

I couldn't figure out whether NLTK has a way of condensing a grammar, especially for disjunctions. This was also a hard part, since I couldn't as quickly compare my toy grammar results to the gold standard. 

An edge case I nearly forgot to handle was non-hybrid rules with more than one terminal on the RHS (such as VP -> "she" "flew" "away". I saw it on the Canvas discussion board and finagled it in using a variable, but it seems unlikely that an actual grammar would have these kinds of rules, as opposed to a single string i.e. "she flew away." What is the benefit of handling such an edge case? 

In terms of memory and time efficiency, I don't think my program's all that good. Some of this stems from the fact that seems to be impossible to edit or add production rules from within a loaded grammar. You have to load the productions into a new list, and then edit from there. Another issue is that the hybrid for loop is separate from the long + unitary for loops, as it can itself produce new long rules. However, I wonder if there was a way to correct every rule WITHIN the original grammar, first by correcting a non-hybrid status, and then unto that same edited rule checking for length. Something like: 

for rule in cfg.productions()
	if rule.is_hybrid(): 
		new_rules = de_hybridize(rule)

		#assume the first elem of the list a helper function returns is like an edit to the original rule, followed by additional rules
		rule = new_rules[0]
		for i in range [1,len(new_rules)]:
			cfg.productions().add(new_rules[i]) 

	if rule.is_long():
		new_rules = shorten(rule) 
		rule = new_rules[0]
		for i in range [1,len(new_rules)]:
			cfg.productions().add(new_rules[i])
	
	if rule.is_unitary(): 
		new_rules = deunitize(rule)[0]
		cfg.productions().remove(rule) 

	# rule is fine as is 
	else:
		pass
	

That way, a new grammar would not have to be created- the original grammar can simply be returned. Plus, the entire production rules list wouldn't have to be traversed numerous times. I guess the danger here is that by adding new rules to the end of cfg.productions(), which we are currently traversing, we run stack overflow risks? At least the memory would be better :-) 

Also, is there a way to simply return a cfg object as is, instead of writing the production rules to a text file? It feels somewhat hokey. I couldn't find anything in the NLTK documentation about it. 

While my code ran well on the sample grammars, it had issues with atis- many too-long rules were not filtered out, and I still don't know why. I ran out of time to bug check at this point and submit it as is. 
