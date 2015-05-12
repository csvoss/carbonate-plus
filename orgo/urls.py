import hashlib
import json
import random

from engine.renderSVG import render as smilesToSvg
from engine.reaction_functions import *
from engine.toMolecule import moleculify
from engine.toSmiles import smilesify
from engine.toCanonical import to_canonical

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.shortcuts import render

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'orgo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^run_reaction/', 'orgo.urls.run_reaction', name='run_reaction'),
#    url(r'^check_solution/', 'orgo.urls.check_solution', name='check_solution'),
    url(r'^render_molecule/', 'orgo.urls.render_molecule', name='render_molecule'),
    url(r'^(?P<random_seed>.[a-f0-9]*)/$', 'orgo.urls.synthesis_problem', name='synthesis_problem')
)

urlpatterns += staticfiles_urlpatterns()



## API
## Inputs:  - optional random seed
##          - optional problem-gen preferences (only permit some rxns?)
## Outputs: - rendered synthesis problem page
def synthesis_problem(request, random_seed):
    
    problem = SynthesisProblem(random_seed)

    objects = {
        'random_seed': random_seed,
        'next_random_seed': hexhash(random_seed + "salt"),
        'starting_svgs': json.dumps([smilesToSvg(i) for i in problem.starting_smiles]),
        'target_svg': json.dumps(smilesToSvg(problem.target_smiles)),
        'starting_smileses': json.dumps(problem.starting_smiles), #[ClientMolecule], aka list of SMILES
        'target_smiles': json.dumps(problem.target_smiles), #ClientMolecule, aka SMILES
        'dropdown_list': json.dumps(dropdown_list), #list of ClientReaction objects
    }
    return render(request, 'synthesis_problem.html', objects)

## API
## Inputs:  - Reaction identifier
##          - Signed? SMILES representations of each input molecule
## Outputs: - Signed? SMILES representation of the result
def run_reaction(request):
    answer = request.GET.get('answer', None)
    input_smileses = request.GET.getlist('input_smileses[]', [])
    reaction_name = request.GET.get('reaction', MIX)

    if type(input_smileses) is not list:
        input_smileses = [input_smileses]

    if reaction_name == MIX:        
        if len(input_smileses) <= 1:
            return HttpResponse(json.dumps({
                "reactionHappened": False,
            }))
        output_smiles = sorted(list(set(input_smileses)))
        output_smiles = '.'.join(output_smiles)
        return HttpResponse(json.dumps({
            "reactionHappened": True,
            "smiles": output_smiles,
            "svg": smilesToSvg(output_smiles),
            "isAnswer": check_solution(answer, output_smiles)
        }))

    else:
        input_molecule = moleculify(input_smileses)
        reaction_function = NAMES_TO_REACTIONS[reaction_name]
        output_molecule = reaction_function(input_molecule)
        if output_molecule == None:
            return HttpResponse(json.dumps({
                "reactionHappened": False,
            }))
        if type(output_molecule) is list:
            output_smiles = [smilesify(m, canonical=True) for m in output_molecule]
            output_smiles = sorted(list(set(output_smiles)))
        else:
            output_smiles = [output_molecule]
        if is_nr(output_smiles, input_smileses):
            return HttpResponse(json.dumps({
                "reactionHappened": False,
            }))
        output_smiles = '.'.join(output_smiles)
        return HttpResponse(json.dumps({
            "reactionHappened": True,
            "smiles": output_smiles,
            "svg": smilesToSvg(output_smiles),
            "isAnswer": check_solution(answer, output_smiles)
        }))


## API
## Inputs:  - SMILES representation of a molecule
## Outputs: - SVG representation of the molecule
def render_molecule(request):
    smiles = request.GET.get('molecule', '')
    return HttpResponse(smilesToSvg(smiles))



## Helper methods

def hexhash(string):
    return hashlib.sha224(string).hexdigest()

def is_nr(output_smiles, input_smiles = []):
    ## Return True if we don't need to add another molecule box for this.
    ## Not to be used for the "mixing" reaction.
    if type(output_smiles) is not list:
        output_smiles = [output_smiles]
    if type(input_smiles) is not list:
        input_smiles = [input_smiles]

    if output_smiles == '' or output_smiles == [] or output_smiles == [''] or output_smiles is None:
        print "WAS no reaction."
        return True
    
    input_smiles = sorted(list(set([to_canonical(s) for s in input_smiles])))
    output_smiles = sorted(list(set([to_canonical(s) for s in output_smiles])))

    if input_smiles == output_smiles:
        return True

    return False

## Inputs:  - SMILES representation of the answer
##          - SMILES representation of an intermediate
## Outputs: - True/False if right/not right yet
def check_solution(answer, newest):
    if answer is None or newest is None:
        return False
    else:
        return to_canonical(answer) == to_canonical(newest)



MAKE_RANDOM_PROBLEM = True

ALKENES = [
    'CCC=CCC',
    'C1CC=CCC1',
    'C=C',
    'C=CCCO',
    'C=CCCBr',
    'CC=C(C)CC',
]

ALKYNES = [
    'CC#CC(C)C',
    'CC#CCC',
]

class SynthesisProblem(object):

    def __init__(self, random_seed):
        if MAKE_RANDOM_PROBLEM:
            random.seed(random_seed)
            self.starting_smiles = [random.choice(ALKENES)]
            reaction = random.choice(NAMES_TO_REACTIONS.values())
            self.target_smiles = smilesify(reaction(moleculify(self.starting_smiles)))
            count = 0
            while is_nr(self.target_smiles, self.starting_smiles):
                if count > 100:
                    raise StandardError("Could not gen problem. Try again.")
                reaction = random.choice(NAMES_TO_REACTIONS.values())
                self.target_smiles = smilesify(reaction(moleculify(self.starting_smiles)))
                count += 1
        else:
            self.starting_smiles = ['CCC=CCC']
            self.target_smiles = 'CCC=O'


NAMES_TO_REACTIONS = {}

def dropdown_item(label, desc, function):
    NAMES_TO_REACTIONS[label] = function
    return {
        "label": label,
        "desc": desc,
    }


MIX = "Mix together"

dropdown_list = [
    dropdown_item("Hydrobromination", "HBr in CH<sub>2</sub>Cl<sub>2</sub>", hydrobrominate_it),
    dropdown_item("Hydrochlorination", "HCl in CH<sub>2</sub>Cl<sub>2</sub>", hydrochlorinate_it),
    dropdown_item(MIX, "(no reagents)", mix_it),
    dropdown_item("1-equiv Hydrobromination", "HBr (1 equiv) in CH<sub>2</sub>Cl<sub>2</sub>", hydrobrominate_it_once),
    dropdown_item("1-equiv Hydroiodination", "HI (1 equiv) in CH<sub>2</sub>Cl<sub>2</sub>", hydroiodinate_it_once),
    dropdown_item("1-equiv Hydrochlorination", "HCl (1 equiv) in CH<sub>2</sub>Cl<sub>2</sub>", hydrochlorinate_it_once),
    dropdown_item("Hydroiodination", "HI in CH<sub>2</sub>Cl<sub>2</sub>", hydroiodinate_it),
    dropdown_item("1-equiv Bromination", "Br<sub>2</sub> (1 equiv) in CH<sub>2</sub>Cl<sub>2</sub>", brominate_it_once),
    dropdown_item("1-equiv Iodination", "I<sub>2</sub> (1 equiv) in CH<sub>2</sub>Cl<sub>2</sub>", iodinate_it_once),
    dropdown_item("1-equiv Chlorination", "Cl<sub>2</sub> (1 equiv) in CH<sub>2</sub>Cl<sub>2</sub>", chlorinate_it_once),
    dropdown_item("Bromination", "Br<sub>2</sub> in CH<sub>2</sub>Cl<sub>2</sub>", brominate_it),
    dropdown_item("Iodination", "I<sub>2</sub> in CH<sub>2</sub>Cl<sub>2</sub>", iodinate_it),
    dropdown_item("Chlorination", "Cl<sub>2</sub> in CH<sub>2</sub>Cl<sub>2</sub>", chlorinate_it),
    dropdown_item("Epoxidation", "mCPBA or PhCO<sub>3</sub>H in CH<sub>2</sub>Cl<sub>2</sub>", epoxidate_it),
    dropdown_item("Acid Hydration (Water)", "H<sub>2</sub>SO<sub>4</sub>, H<sub>2</sub>O", acidhydrate_it),
    dropdown_item("Acid Hydration (Water) (HgSO4 accels.)", "H<sub>2</sub>SO<sub>4</sub>, H<sub>2</sub>O, HgSO<sub>4</sub> accels.", acidhydrate_it_hgso4),
    dropdown_item("Acid Hydration (Ethanol)", "H<sub>2</sub>SO<sub>4</sub>, EtOH", acidhydrate_it_ethanol),
    dropdown_item("Acid Hydration (Ethanol) (HgSO4 accels.)", "H<sub>2</sub>SO<sub>4</sub>, EtOH, HgSO<sub>4</sub> accels.", acidhydrate_it_hgso4_ethanol),
    dropdown_item("Acid Hydration (ROH)", "H<sub>2</sub>SO<sub>4</sub>", acidhydrate_it_auto),
    dropdown_item("Acid Hydration (ROH) (HgSO4 accels.)", "H<sub>2</sub>SO<sub>4</sub>, HgSO<sub>4</sub> accels.", acidhydrate_it_hgso4_auto),
    dropdown_item("Bromohydration (H2O)", "Br<sub>2</sub> in H<sub>2</sub>O", bromohydrate_it_water),
    dropdown_item("Bromohydration (EtOH)", "Br<sub>2</sub> in EtOH", bromohydrate_it_ethanol),
    dropdown_item("Bromohydration (ROH)", "Br<sub>2</sub> in ROH", bromohydrate_it_auto),
    dropdown_item("Iodohydration (H2O)", "I<sub>2</sub> in H<sub>2</sub>O", iodohydrate_it_water),
    dropdown_item("Iodohydration (EtOH)", "I<sub>2</sub> in EtOH", iodohydrate_it_ethanol),
    dropdown_item("Iodohydration (ROH)", "I<sub>2</sub> in ROH", iodohydrate_it_auto),
    dropdown_item("Chlorohydration (H2O)", "Cl<sub>2</sub> in H<sub>2</sub>O", chlorohydrate_it_water),
    dropdown_item("Chlorohydration (EtOH)", "Cl<sub>2</sub> in EtOH", chlorohydrate_it_ethanol),
    dropdown_item("Chlorohydration (ROH)", "Cl<sub>2</sub> in ROH", chlorohydrate_it_auto),
    dropdown_item("Hydroboration-Oxidation", "BH<sub>3</sub> in THF; then NaOH, H<sub>2</sub>O<sub>2</sub>", hydroborate_oxidate_it),
    dropdown_item("Hydroboration", "BH<sub>3</sub> in THF", hydroborate_oxidate_it_1),
    dropdown_item("Oxidation", "NaOH, H<sub>2</sub>O<sub>2</sub>", hydroborate_oxidate_it_2),
    dropdown_item("Dihydroxylation", "cat. OsO<sub>4</sub> in NMO or acetone", dihydroxylate_it),
    dropdown_item("Ozonolysis", "O<sub>3</sub> in CH<sub>2</sub>Cl<sub>2</sub>, then Me<sub>2</sub>S or Zn", ozonolyse_it),
    dropdown_item("Sodium-Ammonia Reduction", "Na in NH<sub>3(l)</sub>", sodium_ammonia_it),
    dropdown_item("Lindlar Reduction", "H<sub>2</sub> cat. Lindlar", lindlar_it),
    dropdown_item("Acetylide Formation", "NaNH<sub>2</sub> in NH<sub>3</sub>", alkyne_deprotonate_it),
    dropdown_item("Tert-butoxide Elimination", "KOC(CH<sub>3</sub>)<sub>3</sub> (aka KOtBu)", tert_butoxide_it),
    dropdown_item("Acetylide Addition", "(no reagents)", acetylide_add_it),
    dropdown_item("Hydrogenation", "H<sub>2</sub> cat. Pd/C in EtOH", hydrogenate_it),
    dropdown_item("Free-radical Hydrobromination", "HBr cat. ROOR (peroxide), with heat or light", radical_hydrobrominate_it),
]

dropdown_list = sorted(dropdown_list)

