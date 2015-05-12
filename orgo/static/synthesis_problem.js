function synthesisProblemMain(parameters) {
    $("#target").html(parameters.targetMoleculeSvg);
    $("#target").attr("data-smiles", parameters.targetMoleculeSmiles);

    var reactants;

    parameters.startingMoleculeSvgs.forEach(function(svg, i, arr) {
        var smiles = parameters.startingMoleculeSmileses[i];
        addMolecule(svg, smiles);
    });


    // obsolete code, here for your reference only

    // $(".draggableMolecule").draggable({
    //     //revert: 'invalid',
    //     helper: 'clone',
    //     cursor: 'pointer',
    // });
    
    // $("#inProgressReaction").droppable({
    //     drop: function(event, ui) {
    //         // TODO: Update the reactants list accordingly
    //         // and update the gui
    //         // ui.draggable
    //         $(this).append(clearer() + ui.draggable.html());
    //     },
    // });

    // OBSOLETE CODE, here for your reference only



    // Set up the reaction toolkit
    $("#toolkit").autocomplete({
        minLength: 0,
        source: function(request, response) {
            var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
            /* Search by description or label: */
            response($.grep(parameters.dropdownList, function(value) {
                return matcher.test(value.label) || 
                    matcher.test(value.desc) || matcher.test(removeTags(value.desc));
            }));
        },
        focus: function( event, ui ) {
            $( "#toolkit" ).val( ui.item.label );
            return false;
        },
        select: function( event, ui ) {
            $( "#toolkit" ).val( ui.item.label );
            $("#inProgressReaction").html(b(ui.item.desc)
                                          + clearer()
                                          + "<small>Click on input molecules to select them. Then, click here to apply the reaction.</small>");
            var reaction = ui.item.label;
            $("#inProgressReaction").unbind("click");
            $("#inProgressReaction").click(function() {
                var input_smileses = $.map($('.selectedMolecule').toArray(),
                                           function(element, index) { return $(element).attr('data-smiles'); });
                $.ajax(
                    '/run_reaction/',
                    {
                        'data': {
                            'input_smileses': input_smileses,
                            'answer': $('#target').attr('data-smiles'),
                            'reaction': reaction,
                        },
                        'error': function(jqXHR, textStatus, errorThrown) {
                            alert("An error occurred: "+errorThrown + textStatus);
                        },
                        'success': function(data, textStatus, jqXHR) {
                            data = JSON.parse(data);
                            $("#inProgressReaction").html(""); //Note: old text is b(ui.item.desc)
                            $(".molecule").each(function(index) { unselectMolecule($(this)); });
                            if (!data.reactionHappened) {
                                $("#inProgressReaction").html("<h31>No reaction!</h3>");
                            } else {
                                var svg = data.svg;
                                var smiles = data.smiles;
                                addMolecule(svg, smiles);

                                // Check for victory
                                if (data.isAnswer) {
                                    alert("Victory!");
                                }
                            }
                        }
                        
                    }
                ); 
            });
            reactants = [];
            return false;
        }
    }).autocomplete( "instance" )._renderItem = function( ul, item ) {
        return $( "<li>" )
            .append( "<a>" + item.label + "<br>" + item.desc + "</a>" )
            .appendTo( ul );
    };
}



// Helper functions

function removeTags(reactionDescription) {
    // Get rid of <sub>, </sub>, etc.
    return reactionDescription.replace(/\<sub\>/g, "").replace(/\<\/sub\>/g, "");
}


function clearer() {
    return "<br class=\"clearer\" />";
}

function b(thing) {
    return "<b>" + thing + "</b>";
}

function addMolecule(svg, smiles) {
    $("#workspace").append(molecule(svg, smiles));
    $(".molecule").unbind("click");
    $(".molecule").click(function() {
        isToggled = $(this).attr("data-toggled");
        if (isToggled === "false") {
            selectMolecule($(this));
        } else {
            unselectMolecule($(this));
        }            
    });
}

function molecule(svg, smiles) {
    return "<div class=\"molecule\" data-smiles=\""+smiles+"\" data-toggled=\"false\">"+svg+"</div>";
}

function unselectMolecule($this) {
    $this.attr("data-toggled", "false");
    $this.removeClass("selectedMolecule");
    $this.css("background-color", "");
}

function selectMolecule($this) {
    $this.attr("data-toggled", "true");
    $this.addClass("selectedMolecule");
    $this.css("background-color", "cornsilk");
}
