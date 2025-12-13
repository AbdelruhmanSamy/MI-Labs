from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

import itertools

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula



    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        def all_diff(val1, val2) -> bool:
            return val1 != val2
        
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).
        
        # appending all equation strings and inserting into set of chars in order to get
        # the unique letters to evaluate the problem variables 
        full_string = LHS0 + LHS1 + RHS
        letters = sorted(set(full_string))
        
        # adding n_cols carry vars to be used to formulate column equation
        # note: carry-count = n_cols + 1, where the last carry is used just 
        # to generalize the column equation
        n_cols = len(RHS)
        carries = [f'c{i}' for i in range(n_cols + 1)]
        
        # evaluating problem variables: the combination of letters and carries
        problem.variables = letters  + carries
        
        # initializing problem domains
        problem.domains = dict()
        
        # initializing domains for all letters: {0 - 9}
        for ch in letters:
            problem.domains[ch] = set(range(10))
        
        # first character in each string cannot be 0
        problem.domains[LHS0[0]] -= {0}
        problem.domains[LHS1[0]] -= {0}
        problem.domains[RHS[0]] -= {0}
        
        # carries can have only values of {0, 1}
        for c in carries:
            problem.domains[c] = {0 , 1}

        # except for those of the first and the after-last column are always 0
        problem.domains['c0'] = {0}
        problem.domains[f'c{n_cols}'] = {0}
        
        # initializing constraints
        problem.constraints = []
        
        max_lhs_len = max(len(LHS0), len(LHS1))
        
        # if the RHS_size is greater than the max len of the 2 LHS strings,
        # then the domain of the last-column-carry must be 1 or the RHS[0]
        # will be =0 which is impossible,
        # accordingly, RHS[0] must be equal to the last-col-carry = 1 
        if n_cols > max_lhs_len:
            problem.domains[f'c{n_cols - 1}'] = {1}
            problem.domains[RHS[0]] = {1}
            
        # A. AllDiff Constraints
        # generating a binary constraint for every unique pair of letters
        for pair in itertools.combinations(letters, 2):
            problem.constraints.append(BinaryConstraint(pair, all_diff))
        
        

        
        # B. Column Constraints (N-ary)
        
        # reversing strings to start columns from the rightmost 
        l1_rev = LHS0[: : -1]
        l2_rev = LHS1[: : -1]
        res_rev = RHS[: : -1]
        
        # We iterate through the columns and link: L1 + L2 + Cin = Res + 10*Cout
        for i in range(n_cols):
            # 1. Identify valid variables
            # We pad with None if one word is shorter than the others, 
            l1_var = l1_rev[i] if i < len(l1_rev) else None
            l2_var = l2_rev[i] if i < len(l2_rev) else None
            r_var = res_rev[i]
            cin_var = f'c{i}'
            cout_var = f'c{i+1}'

            # 2. Create Aux Variables
            # initializing  auxilary variables used to combine the LHS and the RHS,
            # as we are working with max binary constraints
            aux_in_name = f'aux_{i}_in'
            aux_out_name = f'aux_{i}_out'
            problem.variables.extend([aux_in_name, aux_out_name])

            # 3. Generate Domains
            # getting domains for each variable
            # if the variable is NONE, then the domain is a set containing a zero value
            d1 = problem.domains[l1_var] if l1_var else {0}
            d2 = problem.domains[l2_var] if l2_var else {0}
            d_cin = problem.domains[cin_var]
            
            # The domain is a set of tuples, e.g., {(2, 3, 0), (2, 3, 1), ...}
            problem.domains[aux_in_name] = set(itertools.product(d1, d2, d_cin))
            
            # Domain for aux_out: (0-9, 0-1)
            d_r = problem.domains[r_var]
            d_cout = problem.domains[cout_var]
            
            # same as for the LHS
            problem.domains[aux_out_name] = set(itertools.product(d_r, d_cout))
            
            # Helper Factory: Creates a function that handles swapped arguments
            # idx is the index in the tuple (0 for l1, 1 for l2, 2 for cin)
            def make_link_check(idx):
                def check(val_a, val_b):
                    # One value is an int (real), one is a tuple (aux)
                    # We detect which is which dynamically
                    if isinstance(val_a, tuple):
                        aux, real = val_a, val_b
                    else:
                        real, aux = val_a, val_b
                    return real == aux[idx]
                return check

            # The Math Constraint (Aux_in vs Aux_out)
            # We must also handle swapping here! (Length 3 tuple vs Length 2 tuple)
            def check_math(v1, v2):
                if len(v1) == 3:
                    val_in, val_out = v1, v2
                else:
                    val_in, val_out = v2, v1
                return (val_in[0] + val_in[1] + val_in[2]) == (val_out[0] + 10 * val_out[1])

            problem.constraints.append(BinaryConstraint((aux_in_name, aux_out_name), check_math))

            # Linking Aux vars back to real vars
            # We must ensure that if Aux_in says L1 is 5, the actual variable L1 is also 5.
            
            # Link L1
            if l1_var:
                # val_l1 is int, val_aux is tuple (l1, l2, cin)
                problem.constraints.append(BinaryConstraint(
                    (l1_var, aux_in_name), 
                    make_link_check(0)
                ))

            # Link L2
            if l2_var:
                problem.constraints.append(BinaryConstraint(
                    (l2_var, aux_in_name), 
                    make_link_check(1)
                
                ))

            # Link Cin
            problem.constraints.append(BinaryConstraint(
                (cin_var, aux_in_name), 
                    make_link_check(2)
            
            ))

            # Link R
            problem.constraints.append(BinaryConstraint(
                (r_var, aux_out_name), 
                    make_link_check(0)
            
            ))

            # Link Cout
            problem.constraints.append(BinaryConstraint(
                (cout_var, aux_out_name), 
                    make_link_check(1)
            
            ))
                
        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())