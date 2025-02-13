from logic import *

# Define the symbols for characters
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Constraints: Each character is either a knight or a knave, but not both
base_constraints = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave))
)

# Puzzle 0: A says "I am both a knight and a knave."
knowledge0 = And(
    base_constraints,
    Implication(AKnight, And(AKnight, AKnave)),  # If A is a knight, the statement is true
    Implication(AKnave, Not(And(AKnight, AKnave)))  # If A is a knave, the statement is false
)

# Puzzle 1: 
# A says "We are both knaves."
knowledge1 = And(
    base_constraints,
    Implication(AKnight, And(AKnave, BKnave)),  # If A is a knight, the statement must be true
    Implication(AKnave, Not(And(AKnave, BKnave)))  # If A is a knave, the statement must be false
)

# Puzzle 2:
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    base_constraints,
    Implication(AKnight, Biconditional(AKnight, BKnight)),  # If A is a knight, A and B must be the same
    Implication(AKnave, Not(Biconditional(AKnight, BKnight))),  # If A is a knave, they must be different
    Implication(BKnight, Not(Biconditional(AKnight, BKnight)))  # B's statement should be true if B is a knight
)

# Puzzle 3:
# A says either "I am a knight." or "I am a knave."
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    base_constraints,
    # A says either "I am a knight" or "I am a knave"
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    # B says "A said 'I am a knave'" -> if B is knight, A must be knave
    Implication(BKnight, AKnave),
    # B says "C is a knave"
    Implication(BKnight, CKnave),
    # C says "A is a knight"
    Implication(CKnight, AKnight)
)



def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
