import numpy as np

#Data
volumes = np.array([0.37, 0.60, 0.83, 1.05]) #ml
mass = np.array([1.075, 1.675, 2.229, 2.795]) #g

#Density 
density = np.round((mass/volumes), decimals=2)

medium_density = np.mean(density)

round_density = np.round(medium_density, decimals = 2)

#Print
print(f"Densitys:{density} \n"
      f"Medium density: {round_density} g/ml")