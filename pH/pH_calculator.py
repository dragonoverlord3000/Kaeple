#### NOTE: This method and a lot of the code is inspired by: https://github.com/rnelsonchem/pHcalc ####
import numpy as np
import scipy.optimize as spo


class Acid():
    """
    Args: 
        Ka (list) - list of Ka values for the acid
        pKa (list) - list of pKa values for the acid
        charge (int) - the charge of the acid in the form it's added
        conc (float) - the initial concentration of the acid
    """
    def __init__(self, Ka=None, pKa=None, charge=None, conc=None, Kw=10.**(-14.)):
        if Ka == None:
            Ka = 10.**((-1.) * np.array([pKa], dtype=float))
        
        Ka = np.array([Ka], dtype=float).flatten()
        Ka.sort() # smallest first
        self.Ka = np.array(Ka, dtype=float)[::-1] # largest first
        self.conc = np.array(conc, dtype=float)
        self.charge = np.arange(charge, charge - len(self.Ka) - 1, -1, dtype=float)
        
    def alpha(self, pH):
        """
        Args: 
            pH (float) - the pH at which the 'DOD' is calculated
        """
        pH = np.array([pH], dtype=float)
        h3o = 10.**((-1.) * pH)
        n = len(self.Ka)
        
        l = np.array([h3o**(n - m) * np.prod(self.Ka[:m]) for m in range(n + 1)])

        return (l / l.sum()).flatten()
    
    def __repr__(self):
        return f"Acid: \n\tKa={self.Ka} \n\tcharge={self.charge} \n\tinitial concentration={self.conc}"


class Base():
    """
    Args: 
        Kb (list) - list of Kb values for the acid
        pKb (list) - list of pKb values for the acid
        charge (int) - the charge of the acid in the form it's added
        conc (float) - the initial concentration of the acid
    """
    def __init__(self, Kb=None, pKb=None, charge=None, conc=None, Kw=10.**(-14.)):
        if Kb == None:
            Kb = 10.**((-1.) * np.array([pKb], dtype=float))
        
        Kb = np.array([Kb], dtype=float).flatten()
        Kb.sort() # smallest first
        self.Kb = np.array(Kb, dtype=float)[::-1] # largest first
        self.Kw = np.array(Kw, dtype=float)
        self.conc = np.array(conc, dtype=float)
        self.charge = np.arange(charge, charge + len(self.Kb) + 1, 1, dtype=float)
        
    def alpha(self, pH):
        """
        Input: pH - single value
        """
        pH = np.array([pH], dtype=float)
        oh = 10.**(np.log10(self.Kw) + pH)
        n = len(self.Kb)
        
        l = np.array([oh**(n - m) * np.prod(self.Kb[:m]) for m in range(n + 1)])

        return (l / l.sum()).flatten()

    
    def __repr__(self):
        return f"Base: \n\tKb={self.Kb} \n\tcharge={self.charge} \n\tinitial concentration={self.conc}"
    
    
class NonReactive():
    """
    Ions which do not have any inherent reactivity with water, like K^+ and I^-,
    but which contribute to the charge balance.
    """
    
    def __init__(self, charge, conc):
        self.charge = np.array(charge, dtype=float)
        self.conc = np.array(conc, dtype=float)
        
    def alpha(self, pH):
        """
        The model just assumes that the actual concentration of the ions are known
        or that all nonreactive ions dissociate fully which is ofc a bit naive, 
        but it should be pretty easy to add an option to provide a K_o of the salt
        """
        
        return np.array(1, dtype=float)
    
    
class System():
    """
    A list of species (Acid, NonReactive or Base instances) representing the system.
    """
    
    def __init__(self, species, Kw=10.**(-14)):
        """
        Args:
            Kw (float) - waters ion product constant
            species - the species that determine the system
        """
        self.species = species
        self.Kw = Kw
        
    def charge_balance(self, pH):
        """
        Args: 
            pH (float) - single value
        
        Returns (float): 
            absolute value of the charge balance difference
        """
        
        pH = np.array([pH], dtype=float)
        
        h3o = 10.**(-pH)
        oh = self.Kw/h3o
        diff = (h3o - oh)
        
        for s in self.species:
            diff += (s.conc * s.charge * s.alpha(pH)).sum()
            
        return np.abs(diff)
    
    def pHsolve(self, guess=7, mehtod="Nelder-Mead", tol=1e-5):
        
        self.pHsolution = spo.minimize(self.charge_balance, guess, method='Nelder-Mead', tol=1e-5)
                
        if len(self.pHsolution.x) == 1:
            self.pH = self.pHsolution.x[0]
            return self.pH
    
    def __repr__(self):
        representation_str = ""
        for s in self.species:
            representation_str += str(s) + "\n\n"
        return representation_str.strip()


