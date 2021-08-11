import matplotlib
import matplotlib.pyplot as plt

# for plotting text with latex formatting
def latex_plotter(text, fontsize=18, figsize=(14, 1)):
    # creates the plot
    plt.figure(figsize=figsize)
    plt.text(-0.15, 0.95, "$" + text + "$", fontsize = fontsize, ha="left", va="top")
    plt.axis("off")
    plt.show()


