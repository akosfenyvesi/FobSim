import json_data from '../data/Sim_parameters.json' assert {type: 'json'};

let blockchainPlacement = json_data["blockchainPlacement"];
let NumOfFogNodes = json_data["NumOfFogNodes"];
let num_of_users_per_fog_node = json_data["num_of_users_per_fog_node"]
let NumOfMiners = json_data["NumOfMiners"];
let number_of_each_miner_neighbours = json_data["number_of_each_miner_neighbours"]


let nodes = new vis.DataSet([]);
var edges = new vis.DataSet([]);

let nodesId = 1;

// add fog nodes to the nodes list
for (let i = 0; i < NumOfFogNodes; i++) {
    nodes.add({id: nodesId, label: "Fog node " + (i + 1), color: "#54BAB9", level: 1});
    nodesId++;
}

// add end users to the nodes list
for (let i = 0; i < NumOfFogNodes; ++i) {
    for (let j = 0; j < num_of_users_per_fog_node; ++j) {
        nodes.add({
            id: nodesId,
            label: "End user " + (nodesId - NumOfFogNodes),
            color: "#E9DAC1",
            level: 2
        });
        edges.add({from: nodesId, to: i+1});
        nodesId++;
    }
}

// check where the miners are located
if (blockchainPlacement === 1) { // fog

} else if (blockchainPlacement === 2) { // end-user layer

}

for (let i = 0; i < NumOfMiners; i++) {

}

// create a network
let container = document.getElementById('mynetwork');

// provide the data in the vis format
let data = {
    nodes: nodes,
    edges: edges
};
let options = {
    layout: {
        hierarchical: {
            direction: "UD",
        },
    },
    physics: false,
};

let network = new vis.Network(container, data, options);