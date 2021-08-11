import numpy as np
import matplotlib.pyplot as plt
from pH.pH_calculator import System

def bjerrum_plotter(reactant, start_pH=0, end_pH=14, show=True):
    """
    Args: 
        reactant (Acid, Base or Neutral) - a single reactant
        start_pH (int) - starting point for the numerical calculations
        end_pH (int) - ending point for the numerical calculation
        show (bool) - whether to do plt.show() immediately
            - default = `True`
        
    Returns:
        Bjerrum plot of reactant
        
    Example:
        >>>bjerrum_plotter_func(Acid(pKa=[2.148, 7.198, 12.375], charge=0, conc=1.e-3))
        **a bjerrum plot**
    """
    
    pH_list = np.linspace(start_pH, end_pH, 1000)

    alpha_list = []

    for pH in pH_list:
        alpha_list.append(reactant.alpha(pH))

    alpha_list = np.array(alpha_list)

    for i in range(len(alpha_list[0])):
        plt.plot(pH_list, alpha_list[:,i])
        
    if show:
        plt.show()

# Note - this function is pretty slow, but could be optimized quite a lot by adding guess_est as an argument to the system function
# just like it is done in the official github implementation `PHCALC`
def titration_curve_plotter(analyte_system_list, titrant_system_list, titrant_end_conc, titrant_start_conc=0., show=True):
    """
    Args: 
        analyte_system_list (list) - list of analytes
        titrant_system_list (list) - list of titrants
        titrant_end_conc (float) - the final concentration of the titrant
        titrant_start_conc (float) - the initial concentration of the titrant
        show (bool) - whether to do plt.show() immediately
        
    Returns:
        Titration curve of the described titration
    """
    
    titrant_concs = np.linspace(titrant_start_conc, titrant_end_conc, 1000)

    # pH-list
    phs = []

    for conc in titrant_concs:
        # create the titrant
        titrant_list = []
        for titrant in titrant_system_list:
            titrant.conc = conc
            titrant_list.append(titrant)

        # Define the system and solve for the pH
        s = System(analyte_system_list + titrant_list)
        s.pHsolve()
        phs.append(s.pH)
    plt.plot(titrant_concs, phs)
    if show:
        plt.show()
    
    
    