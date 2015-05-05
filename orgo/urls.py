import hashlib
import json

from engine.renderSVG import render as smilesToSvg

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
    url(r'^check_solution/', 'orgo.urls.check_solution', name='check_solution'),
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
    return ""

## API
## Inputs:  - Signed? SMILES representation of the answer
##          - Signed? SMILES representation of an intermediate
## Outputs: - True/False if right/not right yet
def check_solution(request):
    return ""

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
        self.starting_smiles = ['CC=C', 'CCBr', 'C1CC(-Cl)CC1']
        self.target_smiles = 'C1CCC1CCCC3CC3Br'


def dropdown_item(label, desc, numInputs):
    return {
        "label": label,
        "desc": desc,
        "numInputs": numInputs
    }


dropdown_list = [
    dropdown_item("Hydrobromination", "HBr in CH<sub>2</sub>Cl<sub>2</sub>", 1),
    dropdown_item("Hydrochlorination", "HCl in CH<sub>2</sub>Cl<sub>2</sub>", 1),
]
