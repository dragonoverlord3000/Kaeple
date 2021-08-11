import numpy as np
from scipy.linalg import null_space

from global_vars import STATES_OF_MATTER
from utils.math_utils import normalize_coefficients, GCDOfMultipleNums
from utils.reaction_info_utils import (number_of_element, find_charge, is_reaction_solved, reaction_splitter, separate_states_of_matter,
                                       element_finder)
from utils.formatter_utils import (capitalizer, number_of_pluses_before_an_equal, remove_spaces, add_spaces)

def setup_chemical_composition_matrix(compound_list, element_list):
    """
    Args:
        compound_list (list) - list of all the compounds in the reaction - with correct capitalization
        element_list (list) - list of all the elements in the reaction - with correct capitalization
        
    Returns (np.array):
        chemical coefficient matrix of the reaction - as described in https://arxiv.org/ftp/arxiv/papers/1110/1110.4321.pdf
        
    Example:
        >>>setup_chemical_composition_matrix(["C6H12O6", "O2", "CO2", "H2O"], ["H", "C", "O"])
        array([[12.,  0.,  0.,  2.],
               [ 6.,  0.,  1.,  0.],
               [ 6.,  2.,  2.,  1.]])
        >>>compounds = ['Cr7N66H96C42O24', 'MnO4^-', 'H3O^+', 'Cr2O7^2-', 'Mn^2+', 'CO2', 'NO3^-', 'H2O']
        >>>elements = element_finder(c)
        >>>setup_chemical_composition_matrix(compounds, elements)
        array([[ 7.,  0.,  0.,  2.,  0.,  0.,  0.,  0.],
               [66.,  0.,  0.,  0.,  0.,  0.,  1.,  0.],
               [96.,  0.,  3.,  0.,  0.,  0.,  0.,  2.],
               [42.,  0.,  0.,  0.,  0.,  1.,  0.,  0.],
               [24.,  4.,  1.,  7.,  0.,  2.,  3.,  1.],
               [ 0.,  1.,  0.,  0.,  1.,  0.,  0.,  0.],
               [ 0., -1.,  1., -2.,  2.,  0., -1.,  0.]])
    """
    ChemicalCompositionMatrix = np.zeros([len(element_list), len(compound_list)])
    
    for i in range(len(compound_list)):
        for j in range(len(element_list)):
            ChemicalCompositionMatrix[j][i] = number_of_element(compound_list[i], element_list[j])
    
    # if charge is present insert it
    isChargePresent = False
    for compound in compound_list:
        if "^" in compound:
            isChargePresent = True
            break
    
    if isChargePresent:
        charge_vector = find_charge(compound_list)
        ChemicalCompositionMatrix = np.concatenate((ChemicalCompositionMatrix, [charge_vector]))   

    return ChemicalCompositionMatrix
        
        
# the function is much simpler than when it returned a matrix
def find_null_space_vector(compound_list, element_list):
    """
    Args:
        compound_list (list) - list of all the compounds in the reaction - with correct capitalization
        element_list (list) - list of all the elements in the reaction - with correct capitalization
        
    Returns (np.array):
        array describing the relation between the quantities of each compound in the balanced reaction
        
    Example:
        >>>compounds = ['Cr7N66H96C42O24', 'MnO4^-', 'H3O^+', 'Cr2O7^2-', 'Mn^2+', 'CO2', 'NO3^-', 'H2O']
        >>>elements = element_finder(c)
        >>>find_null_space_vector(compounds, elements)
        array([-0.00173861, -0.20446019, -0.48646225,  0.00608512,  0.20446019,
        0.0730215 ,  0.11474806,  0.81314651])
    """
    ChemicalCompositionMatrix = setup_chemical_composition_matrix(compound_list, element_list)
    
    return null_space(ChemicalCompositionMatrix).flatten()


###### The Reaction Balancer ######
def balance_reaction(reaction, reaction_solution=1):
    """
    Args:
        reaction (str) - unformatted or custom formatted reaction
        reaction_solution - the environment the reaction is taking place in
            1. neutral
            2. alkaline
            3. acidic
            
    Returns (str):
        Formatted and balanced reaction
        
    Example:
        >>>balance_reaction("cr7n66h96c42o24+mno4^-=>cr2o7^2-+mn^2++co2+no3^-", 3)
        '10Cr7N66H96C42O24 + 1176MnO4^- + 2798H^+ => 35Cr2O7^2- + 1176Mn^2+ + 420CO2 + 660NO3^- + 1879H2O'
    """
    
    reaction = remove_spaces(reaction)
    reaction = add_spaces(reaction)
    
    # Is reaction already solved
    if is_reaction_solved(reaction):
        # return the formatted reaction then. NOTE: all this should probably be it's own function
        
        compound_list = [compound for compound in reaction_splitter(reaction)]
        states_of_matter_list = ["" for _ in compound_list]
        states_of_matter_in_reaction = False
        
        if any([(state_of_matter in reaction) for state_of_matter in STATES_OF_MATTER]):
            compound_list = [compound for compound in reaction_splitter(reaction)]
            compound_list, states_of_matter_list = separate_states_of_matter(compound_list)
            states_of_matter_in_reaction = True
        
        new_compound_list = []
        for i, compound in enumerate(compound_list):
            new_compound_list += [capitalizer(compound_list[i]) + states_of_matter_list[i]]
            
        compound_list = new_compound_list
        
        new_reaction = ""
        
        number_of_pluses_reactants = number_of_pluses_before_an_equal(reaction)
        
        # if there are only pluses
        if len(compound_list) <= number_of_pluses_reactants:
            for i, compound in enumerate(compound_list):
                if (i + 1) == len(compound_list):
                    new_reaction += compound
                else:
                    new_reaction += compound + " + "
                    
        else:
            in_products = False
            
            for i, compound in enumerate(compound_list):
                if (not in_products) and (number_of_pluses_reactants > 0):
                    new_reaction += compound + " + "
                    number_of_pluses_reactants -= 1
                elif (not in_products) and (number_of_pluses_reactants == 0):
                    new_reaction += compound + " => "
                    in_products = True
                elif in_products:
                    if (i + 1) < len(compound_list):
                        new_reaction += compound + " + "
                    else:
                        new_reaction += compound
        
        
        return new_reaction
    
    
    # lower case compound list
    compound_list = [compound for compound in reaction_splitter(reaction)]
    states_of_matter_list = ["" for _ in compound_list]
    states_of_matter_in_reaction = False
    
    # are the states of matter indicated
    if any([(state_of_matter in reaction) for state_of_matter in STATES_OF_MATTER]):
        compound_list, states_of_matter_list = separate_states_of_matter(compound_list)
        states_of_matter_in_reaction = True    
    
    compound_list = [capitalizer(compound) for compound in compound_list]
        
    # acidic
    if reaction_solution == 3:
        if "H^+" not in compound_list:
            compound_list.append("H^+")
        if "H2O" not in compound_list:
            compound_list.append("H2O")
        
        # I just add "", since the user can add (aq) and (l) if they want to by adding H2O and H^+ themselves
        states_of_matter_list += ["", ""]

    # alkaline
    elif reaction_solution == 2:
        if "OH^-" not in compound_list:
            compound_list.append("OH^-")
        if "H2O" not in compound_list:
            compound_list.append("H2O")
        
        # I just add "", since the user can add (aq) and (l) if they want to by adding H2O and H^+ themselves
        states_of_matter_list += ["", ""]
            
    
    element_list = element_finder(compound_list)    
    null_space_vector = find_null_space_vector(compound_list, element_list)
        
    absolute_null_space_vector = [abs(value) for value in null_space_vector]
    # an error is thrown here if the null space vector is empty - this might for example be caused by an unsolvable reaction
    min_abs = min(absolute_null_space_vector)
    if min_abs == 0:
          return "Dividing by zero error at the - SolveReaction - function"

    reaction_coefficients = np.array(null_space_vector)/min_abs
    
    # normalize coefficients
    reaction_coefficients = normalize_coefficients(reaction_coefficients)
    reaction_coefficients = [round(value) for value in reaction_coefficients]    
    reaction_coefficients = np.array(reaction_coefficients)/GCDOfMultipleNums([abs(value) for value in reaction_coefficients])
    reaction_coefficients = np.array([round(value) for value in reaction_coefficients])
    
    # make sure reactants are positive and products negative
    if reaction_coefficients[0] < 0:
        reaction_coefficients = reaction_coefficients * (-1)

   
    # insert coefficients to the molecule list and turn the molecule list back into a reaction
    reactant_list = []
    product_list = []
    for i in range(len(reaction_coefficients)):
        if reaction_coefficients[i] > 0:
            if reaction_coefficients[i] == 1:
                reactant_list += [str(compound_list[i]) + str(states_of_matter_list[i])]
                continue
            reactant_list += [str(abs(reaction_coefficients[i])) + str(compound_list[i]) + str(states_of_matter_list[i])]
        
        else:
            if reaction_coefficients[i] == (-1):
                product_list += [str(compound_list[i]) + str(states_of_matter_list[i])]
                continue
                
            product_list += [str(abs(reaction_coefficients[i])) + str(compound_list[i]) + str(states_of_matter_list[i])]
    
    # the output reaction
    stochiometric_reaction = ""
    for i, reactant in enumerate(reactant_list):
        
        stochiometric_reaction += reactant
        
        if (i + 1) == len(reactant_list):
            stochiometric_reaction += " => "
        else:
            stochiometric_reaction += " + "
    
    for i, product in enumerate(product_list):
        
        stochiometric_reaction += product
        
        if (i + 1) == len(product_list):
            continue
        else:
            stochiometric_reaction += " + "
    
    return stochiometric_reaction

