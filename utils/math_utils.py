import numpy as np

def gcd(a,b):
    """
    Args:
        a (int) - first number
        b (int) - second number
    
    Returns (int):
        The gcd of a and b
        
    Example:
        >>> a = 2025
        >>> b = 450
        >>> gcd(a,b)
        225
    """
    # make sure b > a
    if a > b:
        t = a
        a = b
        b = t    
    
    # if b is congruent to 0 mod a, then a is the gcd
    if (b % a) == 0:
        return a
    
    # if not, then take 1 step using euclids algorithm
    else:
        return gcd(a,b%a)
    
# Uses the 'gcd' function to find gcd of multiple numbers
def GCDOfMultipleNums(num_list):
    """
    Args:
        num_list (list) - list of the numbers who's gcd is to be found
        
    Returns (int):
        the gcd of all the numbers in num_list
        
    Example:
        >>> num_list = [1000, 100, 10]
        >>> GCDOfMultipleNums(num_list)
        10
    """
    gcd_list = []
    for i in range(len(num_list) - 1):
        for j in range(len(num_list) - i):
            gcd_list += [gcd(num_list[i], num_list[i+j])]
    
    return min(gcd_list)


# Note: there is definitly a better way to do this - this is just a horrible solution - ...         but it works
# Make the coefficient integer valued
def normalize_coefficients(coefficients):
    """
    Args:
        coefficients (list or np.array) - list of coefficients from the `find_null_space_vector` function
        
    Returns (np.array):
        numpy array of integerized coefficients
        
    Example:
        >>>compounds = ['Cr7N66H96C42O24', 'MnO4^-', 'H3O^+', 'Cr2O7^2-', 'Mn^2+', 'CO2', 'NO3^-', 'H2O']
        >>>elements = element_finder(c)
        >>>nv = find_null_space_vector(compounds, elements); nv
        array([-0.00173861, -0.20446019, -0.48646225,  0.00608512,  0.20446019,
        0.0730215 ,  0.11474806,  0.81314651])
        >>>normalize_coefficients(nv / min([abs(v) for v in nv])) # the `/min` part is important
        array([  -10., -1176., -2798.,    35.,  1176.,   420.,   660.,  4677.])
        """
    
    string_coefficients = [str(coef) for coef in coefficients]
    new_coefficients = np.array([coef for coef in coefficients])
    string_decimals = [string_coef.split(".")[1] for string_coef in string_coefficients]
    repeat = False
    
    for i, coef in enumerate(string_coefficients):
        if not ((coef.index(".") + 1) > len(coef)):
            if coef[coef.index(".") + 1] != "0" and coef[coef.index(".") + 1] != "9":
                new_coefficients = new_coefficients * 10
                repeat = True
                break
        
    if repeat:
        new_coefficients = normalize_coefficients(new_coefficients)
        
    # repeated 0 case
    for i, decimals in enumerate(string_decimals):
        if decimals != "":
            if 0 < len(decimals):
                if decimals[0] == "0":
                    
                    if 1 < len(decimals):
                        if decimals[1] == "0":
                        
                            if 2 < len(decimals):
                                if decimals[2] == "0":
                                    
                                    new_coefficients[i] = float(round(new_coefficients[i]))
                            
                                # there are more than 3 decimals: 00x????
                                else:
                                    new_coefficients = new_coefficients * 1000
                                    repeat = True
                                    break
                        
                        # there are 2 decimals: 0x
                        else:
                            new_coefficients = new_coefficients * 100
                            repeat = True
                            break
    
    if repeat:
        new_coefficients = normalize_coefficients(new_coefficients)
    
    # repeated 9 case
    for i, decimals in enumerate(string_decimals):
        if decimals != "":
            if 0 < len(decimals):
                if decimals[0] == "9":
                    
                    if 1 < len(decimals):
                        if decimals[1] == "9":
                        
                            if 2 < len(decimals):
                                if decimals[2] == "9":
                                    
                                    # there are three nines in a row 999????
                                    new_coefficients[i] = float(round(new_coefficients[i]))
                            
                                # there are more than 3 decimals: 99x????
                                else:
                                    new_coefficients = new_coefficients * 1000
                                    repeat = True
                                    break
                        
                        # there are 2 decimals: 9x
                        else:
                            new_coefficients = new_coefficients * 100
                            repeat = True
                            break 
                    
                    # there is a single 9's decimal
                    else:
                        new_coefficients = new_coefficients * 10
                        repeat = True
                        break
         
    if repeat:
        new_coefficients = normalize_coefficients(new_coefficients)
    
    
    
    return np.array([coef for coef in new_coefficients])

