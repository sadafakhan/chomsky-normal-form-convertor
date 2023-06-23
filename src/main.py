import nltk
from nltk.grammar import CFG, Nonterminal, Production
import sys

cfg = nltk.data.load(sys.argv[1])


# helper function that determines whether a production rule is a hybrid rule
def is_hybrid(rule):
    if len(rule.rhs()) > 1 and not rule.is_nonlexical():
        return True
    else:
        return False


# helper function that determines whether a production rule is too long
def is_long(rule):
    if len(rule.rhs()) > 2:
        return True
    # for the case that the rhs has exactly two terminals
    elif len(rule.rhs()) > 1 and not rule.is_nonlexical():
        return True
    else:
        return False


# helper function that determines whether a production rule is a unit production
def is_unit(rule):
    if len(rule.rhs()) == 1 & rule.is_nonlexical():
        return True
    else:
        return False


# integer that increments as we create new dummy terminals
dummy_counter = -1


# helper function that breaks up a hybrid production rule and splits it into intermediate rules that get returned
def split_hybrid(rule):
    split_rules = []
    end_rhs = []
    global dummy_counter

    for item in rule.rhs():
        if type(item) == str:
            # create a dummy NT that leads to the hybrid rule's terminal, and a new production with it
            dummy_counter += 1
            lhs = Nonterminal("_X" + str(dummy_counter) + "_")
            end_rhs.append(lhs)
            rhs = [item]
            new_dummy = Production(lhs, rhs)
            split_rules.append(new_dummy)
        else:
            # hold onto the original RHS terminals
            end_rhs.append(item)

    new_production = Production(rule.lhs(), end_rhs)
    split_rules.append(new_production)
    return split_rules


# helper function that takes long rule and cuts it down to binary rules
def cut_down(rule):
    cut = []
    lhs = rule.lhs()
    global dummy_counter

    # cut depending on whether RHS has >2 NTs or >1 T
    if rule.is_nonlexical():
        indexer = 2
    else:
        indexer = 1

    for i in range(0, len(rule.rhs()) - indexer):
        leftmost = rule.rhs()[i]
        dummy_counter += 1
        new_nt = Nonterminal("_X" + str(dummy_counter) + "_")
        new_production = Production(lhs, [leftmost, new_nt])
        lhs = new_nt
        cut.append(new_production)

    final_prod = Production(lhs, rule.rhs()[-indexer:])
    cut.append(final_prod)
    return cut


# recursive helper function that takes a grammar, and returns a list of productions without unit rules
def de_unitized(grammar):
    unit = []
    deunit = []

    # iterate through production rules, keeping track of unit rules in one list and non-unit rules in the other
    for p in grammar.productions():
        if is_unit(p):
            unit.append(p)
        else:
            deunit.append(p)

        # start "following" unit rules down, and add intermediate unitary rules to unit list to handle later
        while unit:
            rule = unit.pop(0)

            for p in grammar.productions(lhs=rule.rhs()[0]):
                new_rule = Production(rule.lhs(), p.rhs())
                if is_unit(new_rule):
                    unit.append(new_rule)

                #if the rule is not a unit,
                else:
                    deunit.append(new_rule)
    return deunit


not_cnf = cfg.productions()

# get rid of hybrid rules
for rule in not_cnf:
    if is_hybrid(rule):

        # add the split rules to the not_cnf, since they still need to be processed for length, and remove the hybrids
        for new_rule in split_hybrid(rule):
            not_cnf.append(new_rule)

        not_cnf.remove(rule)

# get rid of long rules
for rule in not_cnf:
    if is_long(rule):
        for new_rule in cut_down(rule):
            not_cnf.append(new_rule)
        not_cnf.remove(rule)

# create a new grammar for unit-production removal so that no untransformed rules are copied over
before_unit_cnf = CFG(Nonterminal('S'), not_cnf)

# create final CNF-compliant grammar
cnf = CFG(Nonterminal('S'), de_unitized(before_unit_cnf))
cnf_prod = cnf.productions()

# write to file
with open(sys.argv[2], 'w', encoding='utf8') as f:
    for line in cnf_prod:
        f.write(str(line) + "\n")
