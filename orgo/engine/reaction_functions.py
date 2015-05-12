"""
reaction_functions
Database-friendly reactions.
"""

import reactions as rxns
from toMolecule import moleculify as molec

REACTIONS = []
REAGENTS = []
NAME_TO_REACTION = {}

# class Reagent(object):
#     def __init__(self, html):
#         self.html = html
#         REAGENTS.append(self)

# class REAGENT(object):
#     NR = Reagent("No Reaction")
#     H2 = Reagent("H<sub>2</sub>")
#     PDC = Reagent("Pd|C")
#     ETOH = Reagent("EtOH")
#     HF = Reagent("HF")
#     HBR = Reagent("HBr")
#     HCL = Reagent("HCl")
#     HI = Reagent("HI")
#     CH2CL2 = Reagent("CH<sub>2</sub>Cl<sub>2</sub>")
#     F2 = Reagent("F<sub>2</sub>")
#     BR2 = Reagent("Br<sub>2</sub>")
#     CL2 = Reagent("Cl<sub>2</sub>")
#     I2 = Reagent("I<sub>2</sub>")
#     ROOR = Reagent("ROOR")
#     RCO3H = Reagent("RCO<sub>3</sub>H")
#     H2SO4 = Reagent("H<sub>2</sub>SO<sub>4</sub>")
#     H2O = Reagent("H<sub>2</sub>O")
#     HGSO4 = Reagent("HgSO<sub>4</sub> accels.")
#     BH3 = Reagent("BH<sub>3</sub>")
#     THF = Reagent("THF")
#     NAOH = Reagent("NaOH")
#     H2O2 = Reagent("H<sub>2</sub>O<sub>2</sub>")
#     OSO4 = Reagent("OsO<sub>4</sub>")
#     NMO = Reagent("NMO")
#     ACETONE = Reagent("Acetone")
#     O3 = Reagent("O<sub>3</sub>")
#     ME2S = Reagent("Me<sub>2</sub>S")
#     ZN = Reagent("Zn")
#     LINDLAR = Reagent("cat. Lindlar")
#     NA = Reagent("Na")
#     NH3 = Reagent("NH<sub>3 (L)</sub>")
#     NANH2 = Reagent("NaNH<sub>2</sub>")
#     EQV1 = Reagent("1 equiv.")
#     HEAT = Reagent("Heat")
#     LIGHT = Reagent("Light")
#     HEATORLIGHT = Reagent("Heat or Light")
#     KOCCH33 = Reagent("Tert-butoxide")
#     MAGIC = Reagent("Magic")

# class Reaction(object):
#     def __init__(self, function, name, reagents):
#         self.function = function
#         self.name = name
#         self.reagents = reagents
#         REACTIONS.append(self)
#         NAME_TO_REACTION[name] = self

#     def reagentsHtml(self):
#         html = ""
#         reagents = [reagent.html for reagent in self.reagents]
#         html = ', '.join(reagents)
#         return html

# class REACTION(object):
#     ##MAGIC = Reaction(lambda x: molec("[AuH8]"), "Magic", [REAGENT.MAGIC])
#     HYDROGENATION = Reaction(lambda x: rxns.hydrogenate(x), "Hydrogenation", [REAGENT.H2, REAGENT.PDC, REAGENT.ETOH])
#     RADICALBROMINATION = Reaction(lambda x: rxns.radicalhydrohalogenate(x, "Br"), "Free-radical Bromination", [REAGENT.HBR, REAGENT.ROOR, REAGENT.HEATORLIGHT])
#     BROMINATE1EQ = Reaction(lambda x: rxns.hydrohalogenate1eq(x, "Br"),"Halogenation: Br (1 equiv.)",[REAGENT.HBR, REAGENT.CH2CL2, REAGENT.EQV1])    
#     FLUORINATE1EQ = Reaction(lambda x: rxns.hydrohalogenate1eq(x, "F"),"Halogenation: F (1 equiv.)",[REAGENT.HF, REAGENT.CH2CL2, REAGENT.EQV1])
#     IODINATE1EQ = Reaction(lambda x: rxns.hydrohalogenate1eq(x, "I"),"Halogenation: I (1 equiv.)",[REAGENT.HI, REAGENT.CH2CL2, REAGENT.EQV1])
    # TEMPNAME = Reaction(lambda x: rxns.hydrohalogenate1eq(x, "Cl"),,[REAGENT.HCL, REAGENT.CH2CL2, REAGENT.EQV1])
    # TEMPNAME = Reaction(lambda x: rxns.hydrohalogenate(x, "Br"),,[REAGENT.HBR, REAGENT.CH2CL2])
    # TEMPNAME = Reaction(lambda x: rxns.hydrohalogenate(x, "F"),,[REAGENT.HF, REAGENT.CH2CL2])
    # TEMPNAME = Reaction(lambda x: rxns.hydrohalogenate(x, "I"),,[REAGENT.HI, REAGENT.CH2CL2])
    # TEMPNAME = Reaction(lambda x: rxns.hydrohalogenate(x, "Cl"),,[REAGENT.HCL, REAGENT.CH2CL2])
    # TEMPNAME = Reaction(lambda x: rxns.halogenate1eq(x, "Br"),,[REAGENT.BR2, REAGENT.CH2CL2, REAGENT.EQV1])
    # TEMPNAME = Reaction(lambda x: rxns.halogenate1eq(x, "F"),,[REAGENT.F2, REAGENT.CH2CL2, REAGENT.EQV1])
    # TEMPNAME = Reaction(lambda x: rxns.halogenate1eq(x, "I"),,[REAGENT.I2, REAGENT.CH2CL2, REAGENT.EQV1])
    # TEMPNAME = Reaction(lambda x: rxns.halogenate1eq(x, "Cl"),,[REAGENT.CL2, REAGENT.CH2CL2, REAGENT.EQV1])
    # TEMPNAME = Reaction(lambda x: rxns.halogenate(x, "Br"),,[REAGENT.BR2, REAGENT.CH2CL2])
    # TEMPNAME = Reaction(lambda x: rxns.halogenate(x, "F"),,[REAGENT.F2, REAGENT.CH2CL2])
    # TEMPNAME = Reaction(lambda x: rxns.halogenate(x, "I"),,[REAGENT.I2, REAGENT.CH2CL2])
    # TEMPNAME = Reaction(lambda x: rxns.halogenate(x, "Cl"),,[REAGENT.CL2, REAGENT.CH2CL2])
    # TEMPNAME = Reaction(lambda x: rxns.epoxidate(x),,[REAGENT.RCO3H, REAGENT.CH2CL2])
    # TEMPNAME = Reaction(lambda x: rxns.acidhydrate(x, WATER, True),,[REAGENT.H2SO4, REAGENT.H2O, REAGENT.HGSO4])
    # TEMPNAME = Reaction(lambda x: rxns.acidhydrate(x, ethanol, True),,[REAGENT.H2SO4, REAGENT.ETOH, REAGENT.HGSO4])
    # TEMPNAME = Reaction(lambda x: rxns.acidhydrate(x, x, True),,[REAGENT.H2SO4, REAGENT.HGSO4])
    # TEMPNAME = Reaction(lambda x: rxns.acidhydrate(x, WATER),,[REAGENT.H2SO4, REAGENT.H2O])
    # TEMPNAME = Reaction(lambda x: rxns.acidhydrate(x, ethanol),,[REAGENT.H2SO4, REAGENT.ETOH])
    # TEMPNAME = Reaction)lambda x: rxns.acidhydrate(x, x),,[REAGENT.H2SO4])
    # TEMPNAME = Reaction(lambda x: rxns.halohydrate(x, WATER, "Br"),,[REAGENT.BR2, REAGENT.H2O])
    # TEMPNAME = Reaction(lambda x: rxns.halohydrate(x, ethanol, "Br"),,[REAGENT.BR2, REAGENT.ETOH])
    # TEMPNAME = Reaction(lambda x: rxns.halohydrate(x, x, "Br"),,[REAGENT.BR2])
    # TEMPNAME = Reaction(lambda x: rxns.halohydrate(x, WATER, "I"),,[REAGENT.I2, REAGENT.H2O])
    # TEMPNAME = Reaction(lambda x: rxns.halohydrate(x, ethanol, "I"),,[REAGENT.I2, REAGENT.ETOH])
    # TEMPNAME = Reaction(lambda x: rxns.halohydrate(x, x, "I"),,[REAGENT.I2])
    # TEMPNAME = Reaction(lambda x: rxns.halohydrate(x, WATER, "F"),,[REAGENT.F2, REAGENT.H2O])
    # TEMPNAME = Reaction(lambda x: rxns.halohydrate(x, ethanol, "F"),,[REAGENT.F2, REAGENT.ETOH])
    # TEMPNAME = Reaction(lambda x: rxns.halohydrate(x, x, "F"),,[REAGENT.F2])
    # TEMPNAME = Reaction(lambda x: rxns.halohydrate(x, WATER, "Cl"),,[REAGENT.CL2, REAGENT.H2O])
    # TEMPNAME = Reaction(lambda x: rxns.halohydrate(x, ethanol, "Cl"),,[REAGENT.CL2, REAGENT.ETOH])
    # TEMPNAME = Reaction(lambda x: rxns.halohydrate(x, x, "Cl"),,[REAGENT.CL2])
    # TEMPNAME = Reaction(lambda x: rxns.hydroborate(x),,[REAGENT.BH3, REAGENT.THF, REAGENT.NAOH, REAGENT.H2O2])
    # TEMPNAME = Reaction(lambda x: rxns.hydroborate1(x),,[REAGENT.BH3, REAGENT.THF])
    # TEMPNAME = Reaction(lambda x: rxns.hydroborate2(x),,[REAGENT.NAOH, REAGENT.H2O2])
    # TEMPNAME = Reaction(lambda x: rxns.dihydroxylate(x),,[REAGENT.OSO4, REAGENT.NMO, ACETONE, H2O])
    # TEMPNAME = Reaction(lambda x: rxns.ozonolyse(x),,[REAGENT.O3, REAGENT.CH2CL2, ME2S,ZN])
    # TEMPNAME = Reaction(lambda x: rxns.sodiumAmmonia(x),,[REAGENT.NA, REAGENT.NH3])
    # TEMPNAME = Reaction(lambda x: rxns.lindlar(x),,[REAGENT.LINDLAR, REAGENT.H2])
    # TEMPNAME = Reaction(lambda x: rxns.alkyneDeprotonate(x),,[REAGENT.NANH2, REAGENT.NH3])
    # TEMPNAME = Reaction(lambda x: rxns.tertButoxide(x),,[REAGENT.KOCCH33])


# (lambda x: acetylideAdd(x, x))

mix_it = lambda x: x
    
hydrobrominate_it_once = lambda x: rxns.hydrohalogenate1eq(x, "Br")
hydroiodinate_it_once = lambda x: rxns.hydrohalogenate1eq(x, "I")
hydrochlorinate_it_once = lambda x: rxns.hydrohalogenate1eq(x, "Cl")
hydrobrominate_it = lambda x: rxns.hydrohalogenate(x, "Br")
hydroiodinate_it = lambda x: rxns.hydrohalogenate(x, "I")
hydrochlorinate_it = lambda x: rxns.hydrohalogenate(x, "Cl")
brominate_it_once = lambda x: rxns.halogenate1eq(x, "Br")
iodinate_it_once = lambda x: rxns.halogenate1eq(x, "I")
chlorinate_it_once = lambda x: rxns.halogenate1eq(x, "Cl")
brominate_it = lambda x: rxns.halogenate(x, "Br")
iodinate_it = lambda x: rxns.halogenate(x, "I")
chlorinate_it = lambda x: rxns.halogenate(x, "Cl")

epoxidate_it = rxns.epoxidate

acidhydrate_it = lambda x: rxns.acidhydrate(x, molec("O"), False)
acidhydrate_it_hgso4 = lambda x: rxns.acidhydrate(x, molec("O"), True)
acidhydrate_it_ethanol = lambda x: rxns.acidhydrate(x, molec("CCO"), False)
acidhydrate_it_hgso4_ethanol = lambda x: rxns.acidhydrate(x, molec("CCO"), True)
acidhydrate_it_auto = lambda x: rxns.acidhydrate(x, x, False)
acidhydrate_it_hgso4_auto = lambda x: rxns.acidhydrate(x, x, True)

bromohydrate_it_water = lambda x: rxns.halohydrate(x, molec("O"), "Br")
bromohydrate_it_ethanol = lambda x: rxns.halohydrate(x, molec("CCO"), "Br")
bromohydrate_it_auto = lambda x: rxns.halohydrate(x, x, "Br")
iodohydrate_it_water = lambda x: rxns.halohydrate(x, molec("O"), "I")
iodohydrate_it_ethanol = lambda x: rxns.halohydrate(x, molec("CCO"), "I")
iodohydrate_it_auto = lambda x: rxns.halohydrate(x, x, "I")
chlorohydrate_it_water = lambda x: rxns.halohydrate(x, molec("O"), "Cl")
chlorohydrate_it_ethanol = lambda x: rxns.halohydrate(x, molec("CCO"), "Cl")
chlorohydrate_it_auto = lambda x: rxns.halohydrate(x, x, "Cl")

hydroborate_oxidate_it = rxns.hydroborate
hydroborate_oxidate_it_1 = rxns.hydroborate1
hydroborate_oxidate_it_2 = rxns.hydroborate2

dihydroxylate_it = rxns.dihydroxylate
ozonolyse_it = rxns.ozonolyse
sodium_ammonia_it = rxns.sodiumAmmonia
lindlar_it = rxns.lindlar
alkyne_deprotonate_it = rxns.alkyneDeprotonate
tert_butoxide_it = rxns.tertButoxide
acetylide_add_it = lambda x: rxns.acetylideAdd(x, x)
