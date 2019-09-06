# Projects
Projects worked on in 2018/2019

Introduction:
This project was created to help interpret data from a mass spectrometer. Users analyze unidentified particles using the mass spectrometer, and then the mass spectrometer outputs the ratio of mass of particle over charge and whether the particle is positively or negatively charged. Just from this single number, it is hard to determine what the structure of the particle is, so I made this program to determine the best combination of subunits of the particle that align with the out of the mass spectrometer. The possible subunit combinations were programmed based on the specific chemistry research project I was part of. 

Specifications of program:
User inputs weight found by mass spectrometer, the weight of the ligand, whether the charge was positive or negative (input ‘n’ or ‘p’), and the accuracy range (e.g. an input of 1 will return combinations that will be +1 or -1 of the inputted mass spectrometer weight).
The program tests every possible combination of 0-5 ligand, copper, OAc, MeOH, hydrogen, lithium, sodium, potassium, magnesium, calcium, fluorine, chlorine, bromine, iodine and compares each combination to the mass spectrometer weight. The program tests charges from -6 to +6 (based on whether n or p was inputted).
The program only shows combinations in which there is at least one copper or at least one ligand.
