# Equillibrium constant formatter
from utils.reaction_info_utils import (reaction_splitter, separate_states_of_matter, 
                                       separate_coefficients)


def equillibrium_constant(reaction, specified_constant="INFER"):
    """
    Args:
        reaction (str) - formatted reaction **with states of matter**
        specified_constant (str) - the symbol to use for the equillibrium constant
            - if `specified_constant='INFER'`, then the symbol to use is inferred from the states of matter in the reaction
        
        
    Returns: latex formatted equilibrium fraction
    """
    
    infered_constant = "K"

    reactant_list = reaction.split(" => ")[0]
    product_list = reaction.split(" => ")[1]
    
    reactant_list = reaction_splitter(reactant_list)
    product_list = reaction_splitter(product_list)
    # the 'separate_states_of_matter' function is definitly one of the functions that should change based on the above
    reactant_list, states_of_matter_list_reactants = separate_states_of_matter(reactant_list)
    product_list, states_of_matter_list_products = separate_states_of_matter(product_list)
    # the code assumes the states of matter is split correctly        
    reactant_list, reactant_coefficients = separate_coefficients(reactant_list)
    product_list, product_coefficients = separate_coefficients(product_list)
    
    
    # the standard fraction
    fraction = ""
    non_traditional_states_in_reactants = True
    non_traditional_states_in_products = True
    
    if all([(state == "(g)" or state == "(l)" or state == "(aq)" or state == "(s)" or state == "") for state in (states_of_matter_list_reactants)]):
        non_traditional_states_in_reactants = False
        
    if all([(state == "(g)" or state == "(l)" or state == "(aq)" or state == "(s)" or state == "") for state in (states_of_matter_list_products)]):
        non_traditional_states_in_products = False
    
    non_traditional_states_in_reaction = (non_traditional_states_in_reactants or non_traditional_states_in_products)
    
    # the code that actually makes the fraction
    if all([(state == "(l)" or state == "(s)" or state == "") for state in states_of_matter_list_reactants]) and (not non_traditional_states_in_reactants):
        if all((state == "(aq)" or state == "") for state in states_of_matter_list_products):
            if "(s)" in states_of_matter_list_reactants and (len(reactant_list) == 1):
                infered_constant = "K_o"
        
        # all interisting states are on the product side
        for i, state in enumerate(states_of_matter_list_products):
            if (state != "(l)") and (state != "(s)") and (product_coefficients[i] != 0):
                if state == "(g)":
                    if product_coefficients[i] == "1":
                        fraction += r"p(" + product_list[i] + ")"
                    else:
                        fraction += r"p(" + product_list[i] + ")" + "^{" + product_coefficients[i] + "}"
                
                elif state == "(aq)" and (not non_traditional_states_in_reaction):
                    if product_coefficients[i] == "1":
                        fraction += fr"[{product_list[i]}]"
                    else:
                        fraction += fr"[{product_list[i]}]" + r"^{" + product_coefficients[i] + "}"
                        
                else:
                    # e.g. [I_2(oktan-1-ol)]
                    pass
    
    elif all([(state == "(l)" or state == "(s)" or state == "") for state in states_of_matter_list_products]) and (not non_traditional_states_in_products):
        # all interisting states are on the reactant side
        fraction += r"\frac{1}{"
        
        if all((state == "(aq)" or state == "") for state in states_of_matter_list_reactants):
            infered_constant = r"\frac{1}{K_o}"
        # all interisting states are on the product side
        for i, state in enumerate(states_of_matter_list_reactants):
            if (state != "(l)") and (state != "(s)") and (reactant_coefficients[i] != 0):
                if state == "(g)":
                    if reactant_coefficients[i] == "1":
                        fraction += r"p(" + reactant_list[i] + ")"
                    else:
                        fraction += r"p(" + reactant_list[i] + ")" + r"^{" + reactant_coefficients[i] + "}"
                
                elif state == "(aq)" and (not non_traditional_states_in_reaction):
                    if reactant_coefficients[i] == "1":
                        fraction += fr"[{reactant_list[i]}]"
                    else:
                        fraction += fr"[{reactant_list[i]}]" + r"^{" + reactant_coefficients[i] + "}"
                        
                else:
                    
                    # e.g. [I_2(oktan-1-ol)] and [I_2(aq)]
                    pass
        
        fraction += "}"
    
    else:
        # Note the loops below are just a slightly modified copy paste of the two if statements above
        fraction += r"\frac{"
        
        # first the products in the numerator
        for i, state in enumerate(states_of_matter_list_products):
            if (state != "(l)") and (state != "(s)") and (state != "") and (product_coefficients[i] != 0):
                if state == "(g)":
                    if product_coefficients[i] == "1":
                        fraction += r"p(" + product_list[i] + ")"
                    else:
                        fraction += r"p(" + product_list[i] + ")" + "^{" + product_coefficients[i] + "}"
                
                elif state == "(aq)" and (not non_traditional_states_in_reaction):
                    if product_coefficients[i] == "1":
                        fraction += fr"[{product_list[i]}]"
                    else:
                        fraction += fr"[{product_list[i]}]" + r"^{" + product_coefficients[i] + "}"
                        
                else:
                    # e.g. [I_2(oktan-1-ol)] and [I_2(aq)]
                    if product_coefficients[i] == "1":
                        fraction += fr"[{product_list[i]}{state}]"
                    else:
                        fraction += fr"[{product_list[i]}{state}]" + r"^{" + product_coefficients[i] + "}"
        
        # then the reactants in the denominator
        fraction += "}{"
        
        for i, state in enumerate(states_of_matter_list_reactants):
            if (state != "(l)") and (state != "(s)") and (state != "") and (reactant_coefficients[i] != 0):
                if state == "(g)":
                    if reactant_coefficients[i] == "1":
                        fraction += r"p(" + reactant_list[i] + ")"
                    else:
                        fraction += r"p(" + reactant_list[i] + ")" + "^{" + reactant_coefficients[i] + "}"
                
                elif state == "(aq)" and (not non_traditional_states_in_reaction):
                    if reactant_coefficients[i] == "1":
                        fraction += fr"[{reactant_list[i]}]"
                    else:
                        fraction += fr"[{reactant_list[i]}]" + r"^{" + reactant_coefficients[i] + "}"
                        
                else:
                    # e.g. [I_2(oktan-1-ol)] and [I_2(aq)]
                    if reactant_coefficients[i] == "1":
                        fraction += fr"[{reactant_list[i]}{state}]"
                    else:
                        fraction += fr"[{reactant_list[i]}{state}]" + r"^{" + reactant_coefficients[i] + "}"
                    
                    
        
        fraction += "}"
        
        
    # infer the constant - if possible and not already done
    if infered_constant == "K":
        # if both (g) and (aq) is in the reaction, then K does not equal K_c and K does not equal K_p
        if ("(g)" in reaction) and ("(aq)" in reaction):
            if (len(reactant_list) == 1) and (len(product_list) == 1) and (reactant_list[0] == product_list[0]):
                if (states_of_matter_list_reactants[0] == "(g)") and (states_of_matter_list_products[0] == "(aq)"):
                    infered_constant = "K_H"
                    right_bracket_index = fraction.index("]")
                    fraction = fraction[:right_bracket_index] + "(aq)" + fraction[right_bracket_index:]
                    
                else:
                    infered_constant = r"\frac{1}{K_H}"
                    right_bracket_index = fraction.index("]")
                    fraction = fraction[:right_bracket_index] + "(aq)" + fraction[right_bracket_index:]            
        
        # if all states that matter are gaseous 
        elif all([(state == "(g)" or state == "(s)" or state == "(l)" or state == "") for state in (states_of_matter_list_reactants + states_of_matter_list_products)]):
            if "(g)" in reaction:
                infered_constant = "K_p"
            
        # if all states that matter are aqueous 
        elif all([(state == "(aq)" or state == "(s)" or state == "(l)" or state == "") for state in (states_of_matter_list_reactants + states_of_matter_list_products)]):
            # this might be K_c, but could also be K_a, K_b, K_w or maybe K_K
            
            #  K_a, K_b
            if ("H_{3}O^{+}" in reaction or "OH^{-}" in reaction):
                # K_w
                if all([(reactant == "H_{2}O") for reactant in reactant_list]):
                    if all([(product == "H_{3}O^{+}" or product == "OH^{-}" for product in product_list)]):
                        infered_constant = "K_w"
                # K_a
                elif ("H_{3}O^{+}" in product_list or "H^{+}" in product_list):
                    infered_constant = "K_a"
                
                # K_b
                elif ("OH^{-}" in product_list or "H_{3}O^{+}" in reactant_list):
                    infered_constant = "K_b"
                
                # K_c
                else:
                    infered_constant = "K_c"
                        
        else:
            # K_F
            if (len(reactant_list) == 1) and (len(product_list) == 1) and (reactant_list[0] == product_list[0]):
                if (states_of_matter_list_reactants[0] != "") and (states_of_matter_list_products != ""):
                    infered_constant = "K_F"
    
        
    if specified_constant == "INFER":
        fraction = infered_constant + " = " + fraction
    else:
        fraction = specified_constant + " = " + fraction
        
    if len(fraction) == 0:
        raise Exception("Error, please specify states of matter for your reaction")
    
    return fraction





