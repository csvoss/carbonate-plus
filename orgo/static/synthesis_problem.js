function synthesisProblemMain(parameters) {
    $("span#share").click(function() {
        alert("This URL will show the same problem next time: /" + $("span#share").attr("data-url") + "/");
    });

    $("#target").html(parameters.targetMoleculeSvg);

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
    // $.ajax(
    //     '/render_molecule/',
    //     {
    //         'data': {
    //             'molecule': '',
    //         },
    //         'error': function(jqXHR, textStatus, errorThrown) {
    //             alert("An error occurred: "+errorThrown);
    //         },
    //         'success': function(data, textStatus, jqXHR) {
    //         }
         
    //     }
    // );



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
                                          + "Next, select two molecules to react. <button>Go</button>");
            
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
    $(".molecule").click(function() {
        isToggled = $(this).attr("data-toggled");
        if (isToggled === "false") {
            alert("Was not toggled!");
            $(this).attr("data-toggled", "true");
        } else {
            alert("Was toggled!");
            $(this).attr("data-toggled", "false");
        }            
    });
}


function molecule(svg, smiles) {
    return "<div class=\"molecule\" data-smiles=\""+smiles+"\" data-toggled=\"false\">"+svg+"</div>";
}
