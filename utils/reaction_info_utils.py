from global_vars import STATES_OF_MATTER, END_PARENTHESES_TYPES, START_PARENTHESES_TYPES
from utils.formatter_utils import capitalizer

###### States of matter ######

# Checks whether there are states of matter in the reaction
def states_of_matter_in_reaction(compound_list):
    """
    Args: 
        compund_list (list) - list of compounds - can be capitalized or non-capitalized
    
    Returns (bool):
        True - if there are states of matter in any compound in the given compound list
        False - if there aren't states of matter in any compound in the given compound list
        
    Example:
        >>>states_of_matter_in_reaction(["h2o(g)", "C6H12O6(aq)", "CH3CH2(CHO)CH3(heptane)"])
        True
        >>>states_of_matter_in_reaction(["h2o", "C6H12O6", "CH3CH2(CHO)CH3"])
        False
    """
    
    for compound in compound_list:
        number_of_left = 0        
        number_of_right = 0
        
        first = True
        
        for char in reversed(compound):
            if first and (char != ")"):
                break
                
            elif first:
                first = False
                number_of_right += 1
                
            elif char.isupper():
                break
                
            elif char == ")":
                number_of_right += 1
                
            elif char == "(":
                number_of_left += 1
                
            if number_of_right == number_of_left:
                return True
            
    
    return False  


# Separates states of matter from compunds
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


###### Coefficients ######

def separate_coefficients(compound_list):
    """
    Args:
        compund_list (list) - list of compounds - can be capitalized or non-capitalized
        
    Returns (tuple):
        new_compound_list (list) - compund list without coefficients
        coefficient_list (list) - list of the coefficients
        
    Example:
        >>>separate_coefficients(["h2o", "23C6H12O6", "1032CH3CH2(CHO)CH3"])
        (['h2o', 'C6H12O6', 'CH3CH2(CHO)CH3'], ['1', '23', '1032'])
    """
    
    coefficient_list = []
    new_compound_list = []
    
    for compound in compound_list:
        current_num = ""
        if len(compound) > 0:
            for char in compound:
                if char.isnumeric():
                    current_num += char
                elif (char.isalpha() or char in START_PARENTHESES_TYPES) and (current_num == ""):
                    coefficient_list += ["1"]
                    break
                else:
                    coefficient_list += [current_num]
                    break
            
            if coefficient_list[-1] == "1":
                new_compound_list += [compound]
            else:
                new_compound_list += [compound[len(coefficient_list[-1]):]]
                
    return new_compound_list, coefficient_list


###### Elements in reaction ######

def element_finder(compound_list):
    """
    Args: 
        compound_list (list) - list of the compounds in the reaction with correct spacing and capitalization
    
    Returns (list):
        list of elements in the reaction
        
    Example:
        >>>element_finder(["H2O", "C6H12O6", "CH3CH2(CHO)CH3"])
        ['H', 'O', 'C']
    """
    
    list_of_elements = []
    for compound in compound_list:
        for i, character in enumerate(compound):
            
            # last character special case
            if (i + 1) == len(compound):
                if compound[i].isalpha():
                    if compound[i].islower():
                        continue
                    else:
                        list_of_elements += [character]
                        continue
                else:
                    continue
            
            # skip lowercase letters
            if compound[i].isalpha():
                if compound[i].islower():
                    continue
            
            # main loop
            
            # is it a letter
            if character.isalpha():
                # is the next character a letter
                if compound[i + 1].isalpha():
                    # is this character uppercase and the other one lower case
                    if compound[i].isupper() and compound[i+1].islower():
                        list_of_elements += [compound[i] + compound[i+1]]
                    else:
                        list_of_elements += [compound[i]]
                        
                else:
                    list_of_elements += [compound[i]]
                        
    # remove duplicates
    list_of_elements = list( dict.fromkeys(list_of_elements) )
    
    return list_of_elements

def number_of_element(compound, element):
    """
    Args:
        compound (str) - capitalized compound
        element (str) - the element the search is with respect to
        
    Returns (int)
        The number of `element` in `compound`
        
    Example:
        >>>number_of_element("C6H12O6", "C")
        6
    """
    if not element in compound:
        return 0
    
    number_of = 0
    
    # for compounds with parentheses
    multiplier_list = [1]
    multiplier = 1
    number = ""
    
    # note that we're traversing the list backwards, since it makes working with parentheses easier
    
    # two letter element
    if len(element) == 2:
        for i, character in enumerate(reversed(compound)):
            
            # collect all the numbers
            if character.isnumeric():
                number += character
                continue
            
            # parentheses handling
            if (character in END_PARENTHESES_TYPES):
                if len(number) > 0:
                    t_num = ""
                    for num in reversed(number):
                        t_num += num
                    multiplier_list += [eval(t_num)]
                    number = ""
                    continue
                else:
                    multiplier_list += [1]
                    continue
            
            if (character in START_PARENTHESES_TYPES):
                multiplier_list.pop()
                continue
            
            # now to the element counting
            if (i + 1) < len(compound):
                if (compound[-(i+1)] == element[-1]) and (compound[-(i+2)] == element[0]):
                    if len(number) > 0:
                        # some stuff cause 'reversed' is weird
                        for m in multiplier_list:
                            multiplier = multiplier * m
                        t_num = ""
                        for num in reversed(number):
                            t_num += num
                        number_of += eval(t_num) * multiplier 
                        
                        number = ""
                        multiplier = 1
                    
                    else:
                        for m in multiplier_list:
                            multiplier = multiplier * m
                        number_of += 1 * multiplier 
                        multiplier = 1
                
                # not the element we're searcing for
                else:
                    number = ""
                    
                continue
            
            else:
                continue
            
    # single letter element
    if len(element) == 1:
        
        skip = False
        
        for i, character in enumerate(reversed(compound)):            
            
            if character.islower():
                skip = True
                number = ""
                continue
            
            elif skip:
                skip = False
                continue
            
            # collect all the numbers
            elif character.isnumeric():
                number += character
                continue
            
            # parentheses handling
            elif (character in END_PARENTHESES_TYPES):
                if len(number) > 0:
                    t_num = ""
                    for num in reversed(number):
                        t_num += num
                    multiplier_list += [eval(t_num)]
                    number = ""
                    continue
                else:
                    multiplier_list += [1]
                    continue
            
            elif (character in START_PARENTHESES_TYPES):
                multiplier_list.pop()
                continue
            
            # now to the element counting
            if (compound[-(i+1)] == element[-1]):
                if len(number) > 0:
                    # some stuff cause 'reversed' is weird
                    for m in multiplier_list:
                        multiplier = multiplier * m
                    t_num = ""
                    for num in reversed(number):
                        t_num += num
                    number_of += eval(t_num) * multiplier 
                        
                    number = ""
                    multiplier = 1
                    
                else:
                    for m in multiplier_list:
                        multiplier = multiplier * m
                    number_of += 1 * multiplier 
                    multiplier = 1
                
                continue
            # not the element we're searcing for
            else:
                number = ""
                continue
            
        
    return number_of

###### Charge ######
def find_charge(compound_list):
    chargeList = []
    
    for compound in compound_list:
        isChargePresent = "^" in compound
        
        if isChargePresent:
            index = compound.find("^")
            if (index + 1) < len(compound):
                if compound[index + 1] == "+":
                    chargeList.append(1)
                elif compound[index + 1] == "-":
                    chargeList.append(-1)
                else:
                    if (index + 2) < len(compound):
                        if compound[index + 2] == "+":
                            chargeList.append(int(compound[index + 1]))
                        elif compound[index +2] == "-":
                            chargeList.append(-int(compound[index + 1]))
        else:
            chargeList.append(0)
                
    return chargeList



###### Is the reaction solved ? ######

# Separates the compounds in the reaction
def reaction_splitter(reaction):
    """
    Args:
        reaction (str) - reaction with correct spacing and correct reaction arrow `=>`
    
    Returns (list):
        List of compounds in the reaction
        
    Example:
        >>>reaction_splitter("c6h12o6 + 6o2 => 6h2o + 6co2")
        ['c6h12o6', '6o2', '6h2o', '6co2']
    """
    reaction = reaction.replace(" => ", " + ")
    compounds = reaction.split(" + ")
    return [compound.strip() for compound in compounds]

# Checks if the reaction has already been solved
def is_reaction_solved(reaction):
    """
    Args:
        reaction (str) - correct spacing and reaction arrow, `=>`, is required
        
    Returns:
        True - reaction has already been solved
        False - the reaction is not solved
    
    Example:
        >>>is_reaction_solved("c6h12o6 + 6o2 = 6h2o + 6co2")
        True
        >>>is_reaction_solved("na^+ + cl^- => nacl")
        True
    """
    
    # make sure we have an arrow to separate after
    if "= " in reaction:
        reaction = reaction.replace("=", " => ")
    elif not "=" in reaction:
        
        """
        There is no arrow in the reaction, so it cannot be split into reactants and products
        One possible solution could be to add the arrow in stead of every plus sign in turn
        and then run this function with the newly placed reaction arrow again.
        
        This solution could even serve as a 'find where the reaction arrow should be' function
        """
        # For now we just return False
        return False
        
    
    reactants = reaction.split(" => ")[0]
    products = reaction.split(" => ")[1]
    
    # reactants
    compound_list_reactants = [compound for compound in reaction_splitter(reactants)]
    
    # products
    compound_list_products = [compound for compound in reaction_splitter(products)]
    
        
    # are the states of matter indicated
    if any([(state_of_matter in reaction) for state_of_matter in STATES_OF_MATTER]):
        compound_list_reactants, _ = separate_states_of_matter(compound_list_reactants)
        
    # are the states of matter indicated
    if any([(state_of_matter in reaction) for state_of_matter in STATES_OF_MATTER]):
        compound_list_products, _ = separate_states_of_matter(compound_list_products)        

    
    compound_list_reactants = [capitalizer(compound) for compound in compound_list_reactants]
    compound_list_products = [capitalizer(compound) for compound in compound_list_products]
    
    element_list = element_finder(compound_list_reactants + compound_list_products)

    
    compound_list_reactants, coefficients_reactants = separate_coefficients(compound_list_reactants)
    compound_list_products, coefficients_products = separate_coefficients(compound_list_products)
        
    coefficients_reactants = [eval(value) for value in coefficients_reactants]
    coefficients_products = [eval(value) for value in coefficients_products]
    
    
    
    # reactants
    number_of_list_reactants_temporary = []
    number_of_list_reactants_total = []
    for element in element_list:
        for i, compound in enumerate(compound_list_reactants):
            number_of_list_reactants_temporary += [number_of_element(compound, element) * coefficients_reactants[i]]
        number_of_list_reactants_total += [sum([value for value in number_of_list_reactants_temporary])]
        number_of_list_reactants_temporary = []
    
    # products
    number_of_list_products_temporary = []
    number_of_list_products_total = []
    for element in element_list:
        for i, compound in enumerate(compound_list_products):
            number_of_list_products_temporary += [number_of_element(compound, element) * coefficients_products[i]]
        number_of_list_products_total += [sum([value for value in number_of_list_products_temporary])]
        number_of_list_products_temporary = []
   
    # does it match
    if len(number_of_list_reactants_total) == len(number_of_list_products_total):
        for i in range(len(number_of_list_reactants_total)):
            if number_of_list_reactants_total[i] != number_of_list_products_total[i]:
                return False
    else:
        return False
    
    if "^" in reaction:
        total_charge_reactants = sum(find_charge(compound_list_reactants))
        total_charge_products = sum(find_charge(compound_list_products))
        if total_charge_reactants != total_charge_products:
            return False
        
    return True













