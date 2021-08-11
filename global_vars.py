# Most common states of matter
STATES_OF_MATTER = ["(s)", "(l)", "(g)", "(aq)"]

PTABLENAME = ["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K",
              "Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr",
              "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe",
              "Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf",
              "Ta","W","Re","Os","Ir","Pt","Au","Hg","Ti","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th",
              "Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs",
              "Mt","Ds","Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og"]

PTABLENAMEUPPER = [element.upper() for element in PTABLENAME]
PTABLENAMELOWER = [element.lower() for element in PTABLENAME]


# modified -> removed "Cn", "Nh", "Po", "No", "Cf" and "Co"
MODIFIEDPTABLENAME = ["H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl",
                      "Ar","K", "Ca","Sc","Ti","V","Cr","Mn","Fe","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr",
                      "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe",
                      "Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf",
                      "Ta","W","Re","Os","Ir","Pt","Au","Hg","Ti","Pb","Bi","At","Rn","Fr","Ra","Ac","Th",
                      "Pa","U","Np","Pu","Am","Cm","Bk","Es","Fm","Md","Lr","Rf","Db","Sg","Bh","Hs",
                      "Mt","Ds","Rg","Fl","Mc","Lv","Ts","Og"]

MODIFIEDPTABLENAMELOWER = [element.lower() for element in MODIFIEDPTABLENAME]

LIST_OF_EQUILIBRIUM_CONSTANTS_FORMATTED = ["K_c", "K_F", "K_p", "k_o", "K_K", "K_s", "K_b", "K_w", "K_H"]
LIST_OF_EQUILIBRIUM_CONSTANTS_LOWER_NOT_FORMATTED = ["kc", "kf", "kp", "ko", "kk", "ka", "kb", "kw", "kh"]

START_PARENTHESES_TYPES = ["(", "[", "{"]
END_PARENTHESES_TYPES = [")", "]", "}"]
