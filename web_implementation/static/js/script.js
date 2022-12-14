import json_data from '../data/Sim_parameters.json' assert {type: 'json'};

let blockchainFunction, blockchainPlacement, consensusAlgorithm;
let numFogNodes, numUsers, numTasks, numMiners, numNeighbours, numTxBlock, puzzleDiff, poetBlockTime, maxPayment,
    intialWalletValue, miningAward, fogNodeDelay, endUserDelay, assymKeyLength, dposDelegates, gossipActivated,
    automaticAuthorization, parrallelMining;

$(document).ready(function () {
    initForm();
    fillForm();

    let current_fs, next_fs, previous_fs;
    let opacity;

    $(".next").click(function () {
        disableInputs();

        current_fs = $(this).parent();
        next_fs = $(this).parent().next();

        next_fs.show();

        current_fs.animate({opacity: 0}, {
            step: function (now) {
                opacity = 1 - now;

                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                next_fs.css({'opacity': opacity});
            }, duration: 600
        });
    });

    $(".previous").click(function () {
        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();

        previous_fs.show();

        $(":input").prop("disabled", false);

        current_fs.animate({opacity: 0}, {
            step: function (now) {
                opacity = 1 - now;

                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                previous_fs.css({'opacity': opacity});
            }, duration: 600
        });
    });

    $(".start").click(function () {
        console.log("Clicked start");
        // TODO: start simulation

        (function () {
            'use strict'

            var forms = document.querySelectorAll('.needs-validation')

            Array.prototype.slice.call(forms)
                .forEach(function (form) {
                    form.addEventListener('submit', function (event) {
                        if (!form.checkValidity()) {
                            event.preventDefault()
                            event.stopPropagation()
                        }

                        form.classList.add('was-validated')
                    }, false)
                })
        })()
    });
});

function initForm() {
    // add ai assisted mining
    blockchainFunction = $('#selectFunction');
    blockchainPlacement = $('#selectPlacement');
    consensusAlgorithm = $('#selectConsensus');

    numFogNodes = $('#NumOfFogNodes');
    numUsers = $('#num_of_users_per_fog_node');
    numTasks = $('#NumOfTaskPerUser');
    numMiners = $('#NumOfMiners');
    numNeighbours = $('#number_of_each_miner_neighbours');
    numTxBlock = $('#numOfTXperBlock');
    puzzleDiff = $('#puzzle_difficulty');
    poetBlockTime = $('#poet_block_time');
    maxPayment = $('#Max_enduser_payment');
    intialWalletValue = $('#miners_initial_wallet_value');
    miningAward = $('#mining_award');
    fogNodeDelay = $('#delay_between_fog_nodes');
    endUserDelay = $('#delay_between_end_users');
    assymKeyLength = $('#Asymmetric_key_length');
    dposDelegates = $('#Num_of_DPoS_delegates');
    gossipActivated = $('#Gossip_Activated');
    automaticAuthorization = $('#Automatic_PoA_miners_authorization');
    parrallelMining = $('#Parallel_PoW_mining');
}

function fillForm() {
    numFogNodes.val(json_data['NumOfFogNodes'] >= 1 ? json_data['NumOfFogNodes'] : 1);
    numUsers.val(json_data['num_of_users_per_fog_node'] >= 1 ? json_data['num_of_users_per_fog_node'] : 1);
    numTasks.val(json_data['NumOfTaskPerUser'] >= 1 ? json_data['NumOfTaskPerUser'] : 1);
    let numOfMinersMax = blockchainPlacement.val() === "1" ? numFogNodes.val() : 1500;
    numMiners.val(2 <= json_data['NumOfMiners'] && json_data['NumOfMiners'] <= numOfMinersMax ? json_data['NumOfMiners'] : 2);
    numNeighbours.val(1 <= json_data['number_of_each_miner_neighbours'] && json_data['number_of_each_miner_neighbours'] < numMiners.val() ? json_data['number_of_each_miner_neighbours'] : 1);
    numTxBlock.val(json_data['numOfTXperBlock'] >= 1 ? json_data['numOfTXperBlock'] : 1);
    puzzleDiff.val(1 <= json_data['puzzle_difficulty'] && json_data['puzzle_difficulty'] <= 64 ? json_data['puzzle_difficulty'] : 1);
    poetBlockTime.val(json_data['poet_block_time'] >= 1 ? json_data['poet_block_time'] : 1);
    maxPayment.val(json_data['Max_enduser_payment'] >= 1 ? json_data['Max_enduser_payment'] : 1);
    intialWalletValue.val(json_data['miners_initial_wallet_value'] >= 0 ? json_data['NumOfTaskPerUser'] : 0);
    miningAward.val(json_data['mining_award'] >= 0 ? json_data['mining_award'] : 0);
    fogNodeDelay.val(json_data['delay_between_fog_nodes'] >= 0 ? json_data['delay_between_fog_nodes'] : 0);
    endUserDelay.val(json_data['delay_between_end_users'] >= 0 ? json_data['delay_between_end_users'] : 0);
    assymKeyLength.val(json_data['Asymmetric_key_length'] >= 1 ? json_data['Asymmetric_key_length'] : 1);
    dposDelegates.val(1 <= json_data['Num_of_DPoS_delegates'] && json_data['Num_of_DPoS_delegates'] <= numMiners.val() ? json_data['Num_of_DPoS_delegates'] : 1);
    gossipActivated.prop('checked', json_data['Gossip_Activated']);
    automaticAuthorization.prop('checked', json_data['Automatic_PoA_miners_authorization?']);
    parrallelMining.prop('checked', json_data['Parallel_PoW_mining']);
}

function disableInputs() {
    switch (blockchainPlacement.val()) {
        case "1":

            break;
        case "2":

            break;
    }

    switch (consensusAlgorithm.val()) {
        case "1":
            poetBlockTime.prop('disabled', true);
            dposDelegates.prop('disabled', true);
            automaticAuthorization.prop('disabled', true);
            break;
        case "2":

            break;
        case "3":

            break
        case "4":

            break;
        case "5":

            break
        case "6":

            break;
    }
}