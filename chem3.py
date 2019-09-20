weight = float(input("Enter Mass Spectrometer Weight: "))
ligand_weight = float(input("Enter Weight of Ligand: "))
charge_input = input("Enter Charge ('n' or 'p') : ")
accuracy_range = float(input("Enger Accuracy Range (e.g. an input of 1 will return combinations that have + 1 or - 1 weight of the mass spectrometer weight): "))


## Basic Weights
# Ligand weight usually 847.23
Ligand = [ligand_weight, "Ligand", -2]
Copper = [63.54, "Copper", 2]

OAc = [3758, "OAc", 2]
MeOH = [3707, "MeOH", 2]

## atomic mass of 1st column
Hydrogen = [1.008, "Hydrogen", 1]
Lithium = [6.941, "Lithium", 1]
Sodium = [22.98977, "Sodium", 1]
Potassium = [39.0983, "Potassium", 1]



## atomic mass of 2nd column
Magnesium = [24.305, "Magnesium", 2]
Calcium = [40.078, "Calcium", 2]


## atomic mass of halogens
Fluorine = [18.998, "Fluorine", -1]
Chlorine = [35.45, "Chlorine", -1]
Bromine = [79.904, "Bromine", -1]
Iodine = [126.90, "Iodine", -1]

out_order = dict()

for aa in range(1, 6):
    # Prints how complete
    Percentage = (17 * (aa - 1))
    Percentage_final = "{}% complete"
    print(Percentage_final.format(Percentage))
    # Different types of adjusted weight
    adjusted_weight = weight * aa
    for a in range(6):
        difference_a = adjusted_weight - a * OAc[0]
        if difference_a < -1:
            break
        for b in range(6):
            difference_b = difference_a - b * MeOH[0]
            if difference_b < -1:
                break
            # 1st column elements
            for c in range(6):
                difference_c = difference_b - c * Ligand[0]
                if difference_c < -1:
                    break
                for d in range(6):
                    difference_d = difference_c - d * Copper[0]
                    if difference_d < -1:
                        break
                    for e in range(6):
                        #Checks to make sure there's at least 1 ligand or at least 1 copper
                        if (c == 0) and (d == 0):
                            break
                        difference_e = difference_d - e * Iodine[0]
                        if difference_e < -1:
                            break
                        for f in range(6):
                            difference_f = difference_e - f * Bromine[0]
                            if difference_f < -1:
                                break
                            for g in range(6):
                                difference_g = difference_f - g * Calcium[0]
                                if difference_g < -1:
                                    break
                                for h in range(6):
                                    difference_h = difference_g - h * Potassium[0]
                                    if difference_h < -1:
                                        break
                                    for i in range(6):
                                        difference_i = difference_h - i * Chlorine[0]
                                        if difference_i < -1:
                                            break
                                        for j in range(6):
                                            difference_j = difference_i - j * Magnesium[0]
                                            if difference_j < -1:
                                                break
                                            for k in range(6):
                                                difference_k = difference_j - k * Sodium[0]
                                                if difference_k < -1:
                                                    break
                                                for l in range(6):
                                                    difference_l = difference_k - l * Fluorine[0]
                                                    if difference_l < -1:
                                                        break
                                                    for m in range(6):
                                                        difference_m = difference_l - m * Lithium[0]
                                                        if difference_m < -1:
                                                            break
                                                        for n in range(6):
                                                            difference_n = difference_m - n * Hydrogen[0]

                                                            # overall charge with all components
                                                            overall_charge = a * OAc[2] + b * MeOH[2] + c * Ligand[2] + d * Copper[2] + e * Iodine[2] + f * Bromine[2] + g * Calcium[2] + h * Potassium[2] + i * Chlorine[2] + j * Magnesium[2] + k * Sodium[2] + l * Fluorine[2] + m * Lithium[2] + n * Hydrogen[2]

                                                            if charge_input == "n":
                                                                testing_charge = -1 * aa
                                                            else:
                                                                testing_charge = aa

                                                            if (abs(difference_n) < accuracy_range) and (
                                                                    testing_charge == overall_charge):
                                                                # Adds a plus sign if positive
                                                                overall_charge_present = ""
                                                                if overall_charge > 0:
                                                                    overall_charge_present = "+" + str(
                                                                        overall_charge)
                                                                else:
                                                                    overall_charge_present = str(overall_charge)
                                                                name = "{} charge: {} {}, {} {}, {} {}, {} {}, {} {}, {} {}, {} {}, {} {}, {} {}, {} {}, {} {}, {} {}, {} {}, {} {}"
                                                                name = name.format(overall_charge_present, c, Ligand[1], d, Copper[1], a , OAc[1], b, MeOH[1], e, Iodine[1], f, Bromine[1], g, Calcium[1], h, Potassium[1], i, Chlorine[1], j, Magnesium[1], k, Sodium[1], l, Fluorine[1], m, Lithium[1], n, Hydrogen[1])
                                                                out_order[name] = difference_n
# Finishes percentage count down
print("100% complete\n")

#Prints how many combinations were made
how_many = len(out_order)
top_message = "{} combinations found\n\nIn order list of combinations:"
print(top_message.format(how_many))


# Creates a list of tuples in order
listofTuples = sorted(out_order.items() ,  key=lambda x: abs(x[1]))

in_order =[]
# Iterate over the sorted sequence
for elem in listofTuples :
    stringboi = "{}         difference = {}"
    stringboi = stringboi.format(elem[0] , elem[1])
    in_order.append(stringboi)
# if len(in_order) > 100:
#     for elem in range(100):
#         print(in_order[elem])
# else:
for elem in range(len(in_order)):
    print(in_order[elem])
