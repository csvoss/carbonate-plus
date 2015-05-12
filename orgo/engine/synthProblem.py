from reactions import *
from reaction_functions import *
import randomGenerator
import random
import molecularStructure as orgoStructure
import reactions as reactionsModule
import string
import renderSVG as serverRender
import copy
import itertools
try:
   import cPickle as pickle
except:
   import pickle



class ReactionStep:
    """
    ReactionStep class. Represents an individual step of a synthesis problem,
    as entered by a user.

    Attributes:
        parentMoleculeBox :: MoleculeBox. (to point from)
        otherMoleculeBox :: MoleculeBox. (also to point from, if multiple molecules were combined)
        productBox :: MoleculeBox. (to point to)
        reactionFunction :: [Molecule] -> [Molecule] -> [Molecule]
    """

    def __init__(self, parentMoleculeBox, reaction):
        """
        Initialize this ReactionStep.
        parentMoleculeBox :: MoleculeBox. (to point from)
        """
        self.reactantBox = parentMoleculeBox
        self.otherMoleculeBox = MoleculeBox([])
        self.productBox = None
        self.reaction = reaction
              
    def addMolecule(self, moleculeBox):
        """
        moleculeBox :: MoleculeBox
        Replace self.otherMoleculeBox with moleculeBox.
        Note: this overwrites the previous value of otherMoleculeBox!
        (TODO: Bad for scalability?...)
        """
        print "Added"
        self.otherMoleculeBox = moleculeBox
        
    def react(self, mode="generate"):
        """
        return :: True if a reaction occurred, False if no reaction.
        If True, it updates self.product to be a new MoleculeBox containing the products.

        mode :: str. -- either "generate" or "check".
            Generate returns true iff the reaction makes *new* products.
            Check returns true iff the reaction specified is a valid combination of reagents.
        """
        reaction = self.reaction
        try:
           products = reaction.function(self.reactantBox.molecules + self.otherMoleculeBox.molecules) #a function of two variables
        except ReactionTooCrazyError:
           #TODO: write some sort of return that alerts the frontend.
           return False

        if mode == "check":
            #check if the output list is non-empty
            #if so, reaction is successful
            if products != []:
                self.productBox = MoleculeBox(products)
            #if not, the old set of molecules remain intact
            else:
                self.productBox = MoleculeBox(self.reactantBox.molecules + self.otherMoleculeBox.molecules)
            return True
        elif mode == "generate":
            if len(products) > 4:
                #Too many molecules.  It takes too long to moleculeCompare them pairwise, so just 
                #return False now.
                return False
            #Return true if some new molecule was made during the course of the reaction
            for product in products:
                if any([not moleculeSame(product, reactant) for reactant in self.reactantBox.molecules]):
                    self.productBox = MoleculeBox(products)
                    return True
            return False
        else:
           raise StandardError("Invalid react mode in ReactionStep: "+mode)
                   
        
    def stringList(self):
        """
        return :: str. A string of the reagents contained in this reaction step, in proper HTML.
        """
        return self.reaction.reagentsHtml()
    
    def checkStep(self, target):
        """
        Used for checking if this step is the final, finishing step in a synthesis problem.
        target :: MoleculeBox.
        return :: (bool, MoleculeBox) -- two elements:
                   1. True if products of this reaction step are equal to target, else False
                   2. the products of this reaction step
        """
        if self.react(mode="check"):
            return (boxEqualityChecker(self.productBox, target), self.productBox)
        else:
            return (boxEqualityChecker(self.reactantBox, target), self.reactantBox)
        #The input was ill-formatted.
        return (False, self.productBox)

    def reactionStepHtml(self):
       html = self.stringList()
       return "<div class = \"reaction\" class = \"ui-widget-content\">"+(html)+"<img src=\"/orgo/static/arrow.png\"/></div>"


def boxEqualityChecker(first, second):
    """
    first :: MoleculeBox
    second :: MoleculeBox
    Checks if two molecule boxes contain the same molecules.
    return :: bool. True if equal.

    Called by checkIfEqualsTarget in MoleculeBoxModel in models.
    Called by checkStep in ReactionStep in synthProblem (above).
    """
    assert isinstance(first, MoleculeBox)
    assert isinstance(second, MoleculeBox)
    #Does each product correspond to exactly one target?
    if len(first.molecules) != len(second.molecules):
        return False
    for output in first.molecules:
        OK = False
        for target in second.molecules:
            if moleculeSame(output, target):
                OK = True
                second.molecules.remove(target)
                break
            #If by this point, we haven't found a match, return False.
        if not OK:
            return False
    #Reached the end of molecule list - must have perfect match.
    return True
    

class MoleculeBox:
    """
    Represents a draggable box in the UI containing molecules.
    Attributes:
        self.molecules :: [Molecule].
    """
    def __init__(self, molecules_list):
        """
        Initialize this MoleculeBox.
        molecules_list :: [Molecule].
        """
        self.molecules = molecules_list

    def stringList(self):
        """
        return :: a string of SMILES of the molecules contained in this box, separated by '.'
        """
        outp = ""
        for mol in self.molecules:
            outp += smilesify(mol) + "."
        return serverRender.render(outp)
 
# def parseReagentsString(inpstring):
#     """
#     inpstring :: str. User-generated text, such as "H2 cat Pd|C"
#     return :: {reagent (int) : bool}. For example, {H2:True, PDC:True, ETOH:False, ...}
#     """
#     string = inpstring.lower()
#     outp = {}
    
#     if (string == ""):
#         for reagent in list(REAGENTS):
#             outp[reagent] = False
#         return outp
        
#     for reagent in list(REAGENTS):
#         outp[reagent] = False
#         for spelling in REAGENTS[reagent][1]:
#             if spelling.lower() in string:
#                 outp[reagent] = True

#     #no longer hacky
#     #Check all valid reagent strings for whether they are substrings of OTHER valid reagent strings.
#     #If so, check the count on the substring.
#     #Make sure you don't count substrings if you're counting things they're part of.
#     #We will precompute and load the precise set of things we need to check.
    
#     #Every now and then, set recompute to True.
#     recompute = True
#     structure = []
#     filename = "SubstringCheckerData.pickle"
    
#     if recompute:
#         def getOtherReagentStringsContaining(reagentID, substring):
#             retval = []
#             for key in REAGENTS:
#                 if not key==reagentID:
#                     validStrings = REAGENTS[key][1]
#                     for validString in validStrings:
#                         validStringLower = validString.lower()
#                         if substring in validStringLower:
#                             retval += [validStringLower]
#             return retval
        
#         structure = []
#         for key in REAGENTS:
#             validStrings = REAGENTS[key][1]
#             for validString in validStrings:
#                 validStringLower = validString.lower()
#                 get = getOtherReagentStringsContaining(key, validStringLower)
#                 if not (get == []):
#                     structure += [(key, validStringLower, get)]
                    
                    
#         ##write 'structure' down somewhere
#         toWrite = pickle.dumps(structure)
#         f = open(filename, 'w')
#         f.write(toWrite)
#         f.close()
                    
#     else:
#         ##read 'structure' from somewhere
#         f = open(filename, 'r')
#         toLoad = f.read()
#         structure = pickle.loads(toLoad)
#         f.close()
    
#     for value in structure:
#         val = value[0]
#         sub = value[1]
#         bigList = value[2]
        
#         if (string.count(sub) != 0):
#             if sum([string.count(big.lower()) for big in bigList]) >= sum([string.count(x.lower()) for x in REAGENTS[val][1]]):
#                 outp[val] = False
#     return outp
    
def makeStartingMaterial(mode, count=1):
    """
    Generate random starting materials.
    Used to be based on classes of reactions selected; currently is not.
    mode :: [str].
    count :: int. Number of starting molecules to make. Default 1.
    return :: [MoleculeBox].
    """
    molecules = []
    ## if ('10A Alkenes: halide addition' in mode) or ('10B Alkenes: other' in mode) or ('11 Alkynes' in mode):
    for i in xrange(count):
        forceTerminalAlkyne = random.random() < 0.4
        molecules.append(randomGenerator.random_molecule())
    molecules = removeDuplicates(molecules)
    if debug:
        print "Starting material: " + str(smilesify(molecules))
    return [MoleculeBox([molecule]) for molecule in molecules]



## THIS CODE IS TERRIBLE
## IT'S SO TERRIBLE
## NOT ENOUGH TYPES
## ...actually, it's mostly Felix's
## but I have my fair share of the blame in other files
## namely, I liked list comprehensions way too much
## like, look at this data structure

def randomSynthesisProblemMake(mode, steps = 20, maxLength = 30, count = 2):
    """
    Generate a synthesis problem.
    TODO: finish docstrings in this file
    """
    steps, fused = randomSynthesisProblemStart(mode, steps, maxLength, count)
    if fused:
        return steps
    productsNeeded = []  #Tracks all of the molecules we need.
    productsNeeded += steps[-1].reactantBox.molecules
    steps[-1].keep = True  #Add this new attribute to track which reactions are necessary.
    keepers = 0
    #If we found at least one more keeper in the last cycle, keep going.
    while sum([hasattr(step, "keep") for step in steps]) > keepers:
        keepers = sum([hasattr(step, "keep") for step in steps])
        for step in steps:
            for molecule in step.productBox.molecules:
                if molecule in productsNeeded:
                    step.keep = True
                    productsNeeded += (step.reactantBox.molecules + step.otherMoleculeBox.molecules)
    steps2 = copy.copy(steps)
    for step in steps:
        if not(hasattr(step, "keep")):
            steps2.remove(step)
    return steps2
    
def randomSynthesisProblemStart(mode, steps = 20, maxLength = 30, count = 2):
    fused = False
    reactions = []
    #Mode controls the reagents that are legal, as well as the distribution of starting materials.

    molBoxes = makeStartingMaterial(mode, count)
     
    #Try to react a bunch of times.
    for attemptNo in xrange(steps):
        #Tests for prematurely ending the generation process.
        if sum([len(molBox.molecules) for molBox in molBoxes]) > 4:
            if debug:
                print "Too many molecules!"
            return randomSynthesisProblemStart(mode, steps, maxLength, 1)
        for molBox in molBoxes:
            for molecule in molBox.molecules:
                if len(molecule.atoms) > maxLength:
                    if debug:
                        print "Molecule too large!"
                    return randomSynthesisProblemStart(mode, steps, maxLength, 1)
        newMolBoxes = []
        
        #Go through each molecule, and attempt a random reaction.
        for molBox in molBoxes:
            #There's a small chance of skipping. - Maybe delete, idk?
            if random.random() < .2:
                newMolBoxes.append(molBox)
                continue
            #Otherwise, come up with a random reaction, and try it out.
            reaction = pickReaction()
            currentStep = ReactionStep(molBox, reaction)
            if currentStep.react() and len(currentStep.productBox.molecules)+len(molBox.molecules)<5:
                #A good reaction.
                newMolBoxes.append(currentStep.productBox)
                reactions.append(currentStep)
                if debug:
                    print "Result of successful reaction: " +str(smilesify(currentStep.productBox.molecules))
 
            else:
                #Not a good reaction - that's OK, keep going
                newMolBoxes.append(molBox)
                
        molBoxes = []
        if len(newMolBoxes) == 1:
            #No point in trying to fuse molecules if you only have one molecule to begin with.
            molBoxes = newMolBoxes
            continue
         
        #Now, try to fuse molecules?
        reaction = pickAddReaction()
        for i in xrange(len(newMolBoxes)):
            for j in xrange(i+1,len(newMolBoxes)):
                #Loop through all pairs of molecules.
                molBox1 = newMolBoxes[i]
                molBox2 = newMolBoxes[j]
                cc1 = molBox1.molecules[0].countElement('C')
                cc2 = molBox2.molecules[0].countElement('C')
                currentStep = ReactionStep(molBox1, reaction)
                currentStep.addMolecule(molBox2)
                if currentStep.react():
                    #OK, we have a reaction.  But, did we get fusion?
                    if any([product.countElement('C') == cc1 + cc2 for product in currentStep.productBox.molecules]): ## TODO: this is the WRONG check
                        #Success!
                        reactions.append(currentStep)
                        newMolBoxes.remove(molBox1)
                        newMolBoxes.remove(molBox2)
                        molBoxes = newMolBoxes + [currentStep.productBox]
                        fused = True
                        if debug:
                            print "Result: " +str(smilesify(currentStep.productBox.molecules))
                            print molBoxes
        if len(molBoxes) == 0:
            #Didn't fuse any molecules.  Oh well.
            molBoxes = newMolBoxes
    if len(reactions) == 0:
 
        return randomSynthesisProblemStart(mode, steps, maxLength, 1)
    return reactions, fused
                         
 
#def [moleculeboxes] = getStartingMoleculeBoxes(reactionSteps) in synthProblem
#Helper method used by a constructor in models.
def getStartingMoleculeBoxes(reactionSteps):
    products = list(set([reactionStep.productBox for reactionStep in reactionSteps]))
    allMolecules = list(set([step.reactantBox for step in reactionSteps]) | set([step.otherMoleculeBox for step in reactionSteps if (step.otherMoleculeBox.molecules != [])]))
    startingMoleculeBoxes = [molecule for molecule in allMolecules if (molecule not in products)]
    startingMoleculeBoxes = list(set(startingMoleculeBoxes)) #this should remove duplicates
    return startingMoleculeBoxes

def moleculeBoxHtml(moleculeBox):
    html = "<div class = \"molecule\" class=\"ui-widget-content\"  >"
    html += serverRender.render(moleculeBox.stringList())
    html += "</div>"
    return html   
 
def reactionStepHtml(reactionStep):
    return reactionStep.reactionStepHtml()

def generateNameReagentProblem(mode="AlkeneAlkyne"):
    #Endless loop, for now.  Maybe have some sort of give-up condition?
    while True:
        reactantBox = makeStartingMaterial(mode)[0]  #makeStartingMaterial returns a list of molBoxes
        #Try up to 10 times to make a reaction.
        for attemptNo in xrange(10):
            reaction = pickReaction()
            currentStep = ReactionStep(reactantBox, reaction)
            for reagent in reagents:
                currentStep.hasReagents[reagent[0]] = True
            if currentStep.react() and len(currentStep.productBox.molecules)<3:
                #A good reaction.
                #Decode labels to find the reaction label.
                for label in labels:
                    if not(label in nonLabelKeywords):
                        currentStep.catagory = label
                return currentStep
                if debug:
                    print "Result of successful reaction: " +str(smilesify(currentStep.productBox.molecules))
            else:
                #Try again.
                pass     

def pickReaction():
    return random.choice(REACTIONS)
 
def pickAddReaction():
    return Reaction(lambda x: lambda o: acetylideAdd(alkyneDeprotonate(x+o), x+o), [CH2CL2]) 

def parseReaction(data):
    data = data.rstrip(", ")
    return NAME_TO_REACTION[data]

def nopReaction():
    return Reaction((lambda x: x), "No Reaction", [REAGENT.NR])


#This gigantic terrible tuple is for determining which reaction should take place.

#First item of each tuple in this list:
    #a set of necessary reagents. Things listed together have an "or" relationship.
            #E.g. (("O3",),("CH2CL2",),("ME2S", "ZN")) means ozone AND ch2cl2 AND (me2s OR zn)
#Second item of each tuple in this list:
    #a function of two variables, which takes in a list of molecules (x) and another list of molecules (o) and returns them reacted
#These are listed roughly by precedence: earlier-listed reactions which qualify take precedence over later-listed ones.
# REACTIONS = (


# SYNTHONLY = [
# (((NANH2,), (NH3,)), (lambda x: lambda o: acetylideAdd(alkyneDeprotonate(x+o), x+o)),('11 Alkynes','add')),
# (((NANH2,), (NH3,)), (lambda x: lambda o: acetylideAdd(x+o, alkyneDeprotonate(x+o))),('11 Alkynes','add'))
# ]



def makeReactionAutocomplete():
    return NAME_TO_REACTION.keys()

typeToReaction = {
   'test1': ['test2']
}
   
