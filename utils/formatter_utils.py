from global_vars import MODIFIEDPTABLENAMELOWER

###### Automatic Capitalization ######
def capitalizer_helper_func(alphabetic_piece):
    alphabetic_piece_length = len(alphabetic_piece)
    new_alphabetic_piece = ""
    skip = False
    
    for i in range(alphabetic_piece_length):
        if skip:
            skip = False
            continue
        
        if (i + 1) < alphabetic_piece_length:
            
            if alphabetic_piece[i:i+2] in MODIFIEDPTABLENAMELOWER:
                skip = True
                new_alphabetic_piece += alphabetic_piece[i].upper() + alphabetic_piece[i+1]
                continue
            
            else:
                new_alphabetic_piece += alphabetic_piece[i].upper()
                continue
        
        # last character
        else:
            # only character
            if (i == 0) or alphabetic_piece[i-1].islower():
                new_alphabetic_piece += alphabetic_piece[i].upper()
            else:
                new_alphabetic_piece += alphabetic_piece[i]
    
    return new_alphabetic_piece

def capitalizer(compound):
    """
    Args:
        molecule
    
    Returns (str):
        p
    
    Example:
        >>>capitalizer("na^+ + cl^- => nacl") # a reaction
        'Na^+ + Cl^- => NaCl'
        >>>capitalizer("mgcl2") # single compound
        'MgCl2'
    """
    
    # don't edit if the user already capitalized a letter in the molecule
    if any(c.isupper() for c in compound):
        return compound
    
    # electron special case
    if (compound == "e^-"):
        return compound
    
    # constants
    molecule_length = len(compound)
    alphabetic_piece = ""
    new_compound = ""
    
    # find non-numeric values
    for i in range(molecule_length):
        # non-alphabetic characters
        if (not compound[i].isalpha()):
            
            # use capitalizer function
            if len(alphabetic_piece) > 0:
                new_compound += capitalizer_helper_func(alphabetic_piece)
                alphabetic_piece = ""
            new_compound += compound[i]
            continue
        
        # is alphabetic
        elif compound[i].isalpha():
            alphabetic_piece += compound[i]
            continue
    
    # if the last character is an alphabetic one
    if len(alphabetic_piece) > 0:
        new_compound += capitalizer_helper_func(alphabetic_piece)
    
    return new_compound


###### Latex formatting ######
def format_sub_sup_reaction(reaction):
    """
    Args:
        reaction (str) - reaction with correct capitalization
    
    Returns (str):
        reaction with `_{}` to indicate subscript and `^{}` to indicate superscript
    
    Example:
        >>>format_sub_sup_reaction("[Cr(N2H4CO)6]4[Cr(CN)6]3(S)+MnO4^-(AQ)+H2O=Cr2O7^2-(AQ)+CO2(G)+NO3^-(AQ)+Mn^2+(AQ)+H^+")
        '[Cr(N_{2}H_{4}CO)_{6}]_{4}[Cr(CN)_{6}]_{3}(S)+MnO_{4}^{-}(AQ)+H_{2}O=Cr_{2}O_{7}^{2-}(AQ)+CO_{2}(G)+NO_{3}^{-}(AQ)+Mn^{2+}(AQ)+H^{+}'
    """
    
    new_reaction = ""
    in_charge = False
    in_element_num = False
    
    number_of_left = 0
    number_of_right = 0
    
    
    is_coefficient = True

    for char in reaction:
        if char == "^":
            in_charge = True
            if in_element_num:
                new_reaction += "}"
                in_element_num = False
                number_of_right += 1
            new_reaction += (char + "{")
            number_of_left += 1
        elif not in_charge:

            if char == " ":
                is_coefficient = True
            if char.isalpha():
                is_coefficient = False

            # not in charge - handle subscripts
            if char.isnumeric() and (not in_element_num) and (not is_coefficient):
                new_reaction += "_{"
                in_element_num = True
                number_of_left += 1
            elif (not char.isnumeric()) and in_element_num:
                new_reaction += "}"
                in_element_num = False
                number_of_right += 1
            new_reaction += char


        elif in_charge:
            if (char == "+") or (char == "-"):
                new_reaction += (char + "}")
                number_of_right += 1
                in_charge = False
            else:
                new_reaction += char
                    
    
    while number_of_left > number_of_right:
        new_reaction += "}"
        number_of_right += 1
    
    return new_reaction

###### Spacing ######
# Formatting spaces in the reaction
def letter_space_num_conditional(last_character, current_character, next_character):
    return (last_character.isalpha() and current_character == " " and next_character.isdigit())

def remove_spaces_letter_num(reaction):
    formatted_reaction = ""
    last_character = ""
    for i, character in enumerate(reaction):
        if character != " ":
            formatted_reaction += character
        elif letter_space_num_conditional(reaction[i-1], reaction[i], reaction[i + 1]):
            continue
        else:
            formatted_reaction += character
            
    return formatted_reaction

def remove_spaces(reaction):
    """
    Args:
        reaction (str) - reaction of any formatting
        
    Returns (str):
        reaction with no unnecessary spacings
    
    Example:
        >>>remove_spaces("Na^+ +   Cl^- =>  NaCl  ")
        'Na^+ + Cl^- => NaCl'
    """
    formatted_reaction = ""
    last_character = ""
    for character in reaction:
        if character == " " and last_character == " ":
            continue
        else:
            last_character = character
            formatted_reaction += character
    
    if len(formatted_reaction) > 0:
        if formatted_reaction[-1] == " ":
              formatted_reaction = formatted_reaction[:-1]

    formatted_reaction = remove_spaces_letter_num(formatted_reaction)
            
    return formatted_reaction

def add_spaces(reaction):
    """
    Args:
        reaction (str) - reaction of any formatting
        
    Returns (str):
        reaction with no added spacings
    
    Example:
        >>>add_spaces("[Cr(N2H4CO)6]4[Cr(CN)6]3(S)+MnO4^-(AQ)+H2O=Cr2O7^2-(AQ)+CO2(G)+NO3^-(AQ)+Mn^2+(AQ)+H^+")
        '[Cr(N2H4CO)6]4[Cr(CN)6]3(S) + MnO4^-(AQ) + H2O => Cr2O7^2-(AQ) + CO2(G) + NO3^-(AQ) + Mn^2+(AQ) + H^+'
    """
    
    new_reaction = ""
    
    for i in range(len(reaction)):        
        if i > 0 and (i + 1) < len(reaction):
            
            # if not A^x+ and no spaces
            if (i > 1) and reaction[i] == "+" and (not reaction[i-2] == "^") and (not reaction[i-1].isspace()) and (not reaction[i-1] == "^"):
                new_reaction += " +"
                
                if not reaction[i+1].isspace():
                    new_reaction += " "
                continue
            
            # if A^++ or A^-+
            if (i > 1) and reaction[i] == "+" and (reaction[i-1] == "+" or reaction[i-1] == "-"):
                new_reaction += " +"
                if not reaction[i+1].isspace():
                    new_reaction += " "
                continue
            
            # if + and then not a space make sure the next characters aren't the states of matter and then add a space
            if reaction[i] == "+" and (not reaction[i+1].isspace()):
                if reaction[i+1] == "(":
                    new_reaction += reaction[i]
                    continue
                else:
                    new_reaction += reaction[i] + " "
                    continue
                    
        
        # second to last character
        if (i + 1) < len(reaction):
            if reaction[i] == "=" and (not reaction[i+1] == ">"):
                new_reaction += "=>"
                continue
            
            
            # This is based on the assumption that no charge will have more than 1 digit
            elif reaction[i] == "+":
                if i > 1:
                    if (not reaction[i-2] == "^") and (not reaction[i-1] == "^"):
                        new_reaction += " + "
                        continue
                elif i > 0:
                    if (not reaction[i-1] == "^"):
                        new_reaction += " + "
                        continue          
        
        # last character
        else:
            if reaction[i] == "=":
                new_reaction += "=>"
                continue
            elif reaction[i] == "+":
                if i > 1:
                    if (not reaction[i-2] == "^") and (not reaction[i-1] == "^"):
                        new_reaction += " + "
                        continue
                elif i > 0:
                    if (not reaction[i-1] == "^"):
                        new_reaction += " + "
                        continue   
                
        
        # add the character at each loop unless continue has been used
        new_reaction += reaction[i]
    
    new_reaction = new_reaction.replace("=>", " => ")
    
    # having to call RemoveSpaces each time each time AddSpaces is used is probably not optimal
    return remove_spaces(new_reaction)




###### Full formatter ######

# Specialized reaction splitter
def formatter_reaction_splitter(reaction):
    reaction = reaction.replace("=>", " + ")
    molecules = reaction.split(" +")
    return [molecule.strip() for molecule in molecules]

# General helper function for the `format_full_reaction` function
def number_of_pluses_before_an_equal(reaction):
    """
    Args:
        reaction (str) - reaction with correctly formatted spacing
        
    Returns (int):
        number_of - the number of pluses before the arrow `=>`
        
    Example:
        >>>number_of_pluses_before_an_equal("C6H12O6 + 6O2=> 6CO2 + 6H2O")
        1
    """
    number_of = 0
    # so we don't have to worry about (i - 1) < 0
    reac = reaction.strip()
    for i in range(1, len(reaction)):
        if reaction[i] == "=":
            return number_of
        
        if i > 0:
            #  and reaction[i+1] == " " is omitted because of formatting reasons
            if reaction[i] == "+" and reaction[i-1] == " ":
                number_of += 1
                
    return number_of

# Separates states of matter from compunds - note that this function is an exact copy of the one in `reaction_info_utils.py`
def separate_states_of_matter(compound_list):
    """
    Args: 
        compund_list (list) - list of compounds - can be capitalized or non-capitalized
    
    Returns (tuple):
        new_compound_list (list) - compund list without states of matter
        states_of_matter_list (list) - list of the states of matter
            
    Example:
        >>>separate_states_of_matter(["h2o(g)", "C6H12O6(aq)", "CH3CH2(CHO)CH3(heptane)"])
        (['h2o', 'C6H12O6', 'CH3CH2(CHO)CH3'], ['(g)', '(aq)', '(heptane)'])
    """
    
    # Make sure there are no arrows in the reaction
    t_list = []
    for compound in compound_list:
        t = compound.replace("=>", "")
        t_list += [t.strip()]
    
    compound_list = t_list
    

    new_compound_list = []
    states_of_matter_list = []
    
    # Essentially just reverses the compound string and checks for **normal parentheses** i.e. `(` and `)`
    for compound in compound_list:
        number_of_left = 0        
        number_of_right = 0
        
        first = True
        
        number_of_char = 0
        
        for char in reversed(compound):
            if first and (char != ")"):
                break
            elif first:
                first = False
                number_of_right += 1
                number_of_char += 1
                
            elif number_of_right == number_of_left:
                break
                
            elif char == ")":
                number_of_right += 1
                number_of_char += 1
                
            elif char == "(":
                number_of_left += 1
                number_of_char += 1
                
            else:
                number_of_char += 1
        
        if number_of_char > 0:
            new_compound_list += [compound[:-number_of_char]]
            states_of_matter_list += [compound[-number_of_char:]]
        else:
            new_compound_list += [compound]
            states_of_matter_list += [""]
            
    
    return new_compound_list, states_of_matter_list

# format full reaction
def format_full_reaction(reaction):
    """
    Args:
        reaction (str) - unformatted reaction
        
    Returns (str):
        Latex formatted reaction - with 
        
    Example:
        >>>format_full_reaction("cr7n66h96c42o24+mno4^-+h2o=>cr2o7^2-+mn^2++co2+no3^-+h3o^+")
        'Cr_{7}N_{66}H_{96}C_{42}O_{24} + MnO_{4}^{-} + H_{2}O => Cr_{2}O_{7}^{2-} + Mn^{2+} + CO_{2} + NO_{3}^{-} + H_{3}O^{+}'
    """
    # would probably be optimal if this formatter and the formatter used in the actual
    # solver were the same, since possible errors would be more transparent for the user
    
    new_reaction = add_spaces(remove_spaces(reaction))

    n_pluses = number_of_pluses_before_an_equal(new_reaction)
    new_reac_compound_list = formatter_reaction_splitter(new_reaction)
    new_reac_compound_list_wo_states, states_of_matter_list = separate_states_of_matter(new_reac_compound_list)
        
    formatted_reaction = ""
    
    for i, compound in enumerate(new_reac_compound_list_wo_states):
        if n_pluses == 0 and "=>" in new_reaction and i > 0:
            formatted_reaction += " => "
            n_pluses -= 1
        elif i > 0 and n_pluses > 0:
            formatted_reaction += " + "
            n_pluses -= 1
        elif n_pluses < 0:
            formatted_reaction += " + "
        
        formatted_reaction += capitalizer(format_sub_sup_reaction(compound)) 
        formatted_reaction += states_of_matter_list[i]
        
    return formatted_reaction
    
###### Latex arrow ######
def place_arrow(reaction):
    if "=" in reaction:
        if (not ">" in reaction) and reaction[-1] != "=":
            arrow_index = reaction.index("=")
            reaction = reaction[:arrow_index] + r" \longrightarrow " + reaction[arrow_index + 2:]

        elif (not ">" in reaction) and reaction[-1] == "=":
            reaction = reaction[:-1] + r" \longrightarrow " 

        elif "=>" in reaction:
            arrow_index = reaction.index("=>")
            reaction = reaction[:arrow_index] + r" \longrightarrow " + reaction[arrow_index + 3:]
    
    return reaction




