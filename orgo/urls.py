import hashlib
import json

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

    input_molecule = moleculify(input_smileses)
    reaction_function = NAMES_TO_REACTIONS[reaction_name]

    output_molecule = reaction_function(input_molecule)

    if type(output_molecule) is list:
        output_smiles = [smilesify(m, canonical=True) for m in output_molecule]
        output_smiles = list(set(output_smiles))

    if type(output_smiles) is list:
        output_smiles = '.'.join(output_smiles)


    return HttpResponse(json.dumps({
        "smiles": output_smiles,
        "svg": smilesToSvg(output_smiles),
        "isAnswer": check_solution(answer, output_smiles)
    })) ## TODO

## API
## Inputs:  - Signed? SMILES representation of the answer
##          - Signed? SMILES representation of an intermediate
## Outputs: - True/False if right/not right yet
def check_solution(answer, newest):
    if answer is None or newest is None:
        return False
    else:
        return to_canonical(answer) == to_canonical(newest)

## API
## Inputs:  - SMILES representation of a molecule
## Outputs: - SVG representation of the molecule
def render_molecule(request):
    smiles = request.GET.get('molecule', '')
    return HttpResponse(smilesToSvg(smiles))







## Helper methods

def hexhash(string):
    return hashlib.sha224(string).hexdigest()


class SynthesisProblem(object):

    def __init__(self, random_seed):
        ##  major TODO here
        self.starting_smiles = ['CCCCC#CCCCC']
        self.target_smiles = 'CCCCC(=O)CCCCC'

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
    # dropdown_item("1-equiv Hydrobromination", "", hydrobrominate_it_once),
    # dropdown_item("1-equiv Hydroiodination", "", hydroiodinate_it_once),
    # dropdown_item("1-equiv Hydrochlorination", "", hydrochlorinate_it_once),
    # dropdown_item("Hydroiodination", "", hydroiodinate_it),
    # dropdown_item("1-equiv Bromination", "", brominate_it_once),
    # dropdown_item("1-equiv Iodination", "", iodinate_it_once),
    # dropdown_item("1-equiv Chlorination", "", chlorinate_it_once),
    # dropdown_item("Bromination", "", brominate_it),
    # dropdown_item("Iodination", "", iodinate_it),
    # dropdown_item("Chlorination", "", chlorinate_it),
    # dropdown_item("Epoxidation", "", epoxidate_it),
    # dropdown_item("Acid Hydration (Water)", "H<sub>2</sub>SO<sub>4</sub>, H<sub>2</sub>O", acidhydrate_it),
    # dropdown_item("Acid Hydration (Water) (HgSO<sub>4</sub> accels.)", "H<sub>2</sub>SO<sub>4</sub>, H<sub>2</sub>O, HgSO<sub>4</sub> accels.", acidhydrate_it_hgso4),
    # dropdown_item("Acid Hydration (Ethanol)", "H<sub>2</sub>SO<sub>4</sub>, EtOH", acidhydrate_it_ethanol),
    # dropdown_item("Acid Hydration (Ethanol) (HgSO<sub>4</sub> accels.)", "H<sub>2</sub>SO<sub>4</sub>, EtOH, HgSO<sub>4</sub> accels.", acidhydrate_it_hgso4_ethanol),
    # dropdown_item("", "", acidhydrate_it_auto),
    # dropdown_item("", "", acidhydrate_it_hgso4_auto),
    # dropdown_item("", "", bromohydrate_it_water),
    # dropdown_item("", "", bromohydrate_it_ethanol),
    # dropdown_item("", "", bromohydrate_it_auto),
    # dropdown_item("", "", iodohydrate_it_water),
    # dropdown_item("", "", iodohydrate_it_ethanol),
    # dropdown_item("", "", iodohydrate_it_auto),
    # dropdown_item("", "", chlorohydrate_it_water),
    # dropdown_item("", "", chlorohydrate_it_ethanol),
    # dropdown_item("", "", chlorohydrate_it_auto),
    # dropdown_item("", "", hydroborate_oxidate_it),
    # dropdown_item("", "", hydroborate_oxidate_it_1),
    # dropdown_item("", "", hydroborate_oxidate_it_2),
    # dropdown_item("", "", dihydroxylate_it),
    # dropdown_item("", "", ozonolyse_it),
    # dropdown_item("", "", sodium_ammonia_it),
    # dropdown_item("", "", lindlar_it),
    # dropdown_item("", "", alkyne_deprotonate_it),
    # dropdown_item("", "", tert_butoxide_it),
    # dropdown_item("", "", acetylide_add_it),
]

dropdown_list = sorted(dropdown_list)
