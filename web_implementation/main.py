import gc
import sys

import Fog
import end_user
import miner
import blockchain
import random
import output
from math import ceil
import time
import modification
import new_consensus_module
import json
import shutil

data = None
expected_chain_length = None
trans_delay = None
user_informed = True
list_of_end_users = []
fogNodes = []
transactions_list = []
list_of_authorized_miners = []


def read_json():
    global data, expected_chain_length, trans_delay

    shutil.copyfile("static/data/Sim_parameters.json", "Sim_parameters.json")

    data = modification.read_file("Sim_parameters.json")

    expected_chain_length = ceil(
        (data["num_of_users_per_fog_node"] * data["NumOfTaskPerUser"] * data["NumOfFogNodes"]) / data[
            "numOfTXperBlock"])
    # Check if correct
    trans_delay = data["delay_between_fog_nodes"] if data["blockchainPlacement"] == 1 else data[
        "delay_between_end_users"]


def initiate_files():
    modification.initiate_files(data["Gossip_Activated"])
    new_consensus_module.prepare_necessary_files(data["consensusAlgorithm"])


def initiate_network():
    for count in range(data["NumOfFogNodes"]):
        fogNodes.append(Fog.Fog(count + 1))
        for p in range(data["num_of_users_per_fog_node"]):
            list_of_end_users.append(end_user.User(p + 1, count + 1))
    output.users_and_fogs_are_up()
    if data["blockchainFunction"] == 4:
        output.GDPR_warning()
        while True:
            print("If you don't want other attributes to be added to end_users, input: done\n")
            new_attribute = input("If you want other attributes to be added to end_users, input them next:\n")
            if new_attribute == 'done':
                break
            else:
                for user in list_of_end_users:
                    user.identity_added_attributes[new_attribute] = ''
                output.user_identity_addition_reminder(len(list_of_end_users))
    for user in list_of_end_users:
        user.create_tasks(data["NumOfTaskPerUser"], data["blockchainFunction"], list_of_end_users)
        user.send_tasks(fogNodes)
        print("End_user " + str(user.addressParent) + "." + str(
            user.addressSelf) + " had sent its tasks to the fog layer")


def initiate_miners():
    the_miners_list = []

    if data["blockchainPlacement"] == 1:
        for i in range(data["NumOfFogNodes"]):
            the_miners_list.append(miner.Miner(i + 1, trans_delay, data["Gossip_Activated"]))
    if data["blockchainPlacement"] == 2:
        for i in range(data["NumOfMiners"]):
            the_miners_list.append(miner.Miner(i + 1, trans_delay, data["Gossip_Activated"]))
    for entity in the_miners_list:
        modification.write_file("temporary/" + entity.address + "_local_chain.json", {})
        miner_wallets_log_py = modification.read_file("temporary/miner_wallets_log.json")
        miner_wallets_log_py[str(entity.address)] = data['miners_initial_wallet_value']
        modification.rewrite_file("temporary/miner_wallets_log.json", miner_wallets_log_py)
    print('Miners have been initiated..')
    connect_miners(the_miners_list)
    output.miners_are_up()
    return the_miners_list


def define_trans_delay(layer):
    transmission_delay = 0
    if layer == 1:
        transmission_delay = data["delay_between_fog_nodes"]
    if layer == 2:
        transmission_delay = data["delay_between_end_users"]
    return transmission_delay


def connect_miners(miners_list):
    print("Miners will be connected in a P2P fashion now. Hold on...")
    bridges = set()
    all_components = create_components(miners_list)
    for comp in all_components:
        bridge = random.choice(tuple(comp))
        bridges.add(bridge)
    bridging(bridges, miners_list)


def bridging(bridges, miners_list):
    while len(bridges) != 1:
        bridge = random.choice(tuple(bridges))
        other_bridge = random.choice(tuple(bridges))

        while bridge == other_bridge:
            other_bridge = random.choice(tuple(bridges))

        for entity in miners_list:
            if entity.address == bridge:
                entity.neighbours.add(other_bridge)
            if entity.address == other_bridge:
                entity.neighbours.add(bridge)
        bridges.remove(bridge)


def create_components(miners_list):
    all_components = set()
    for entity in miners_list:
        component = set()
        while len(entity.neighbours) < data["number_of_each_miner_neighbours"]:
            neighbour = random.choice(miners_list).address
            if neighbour != entity.address:
                entity.neighbours.add(neighbour)
                component.add(neighbour)
                for entity_2 in miners_list:
                    if entity_2.address == neighbour:
                        entity_2.neighbours.add(entity.address)
                        component.add(entity.address)
                        break
        if component:
            all_components.add(tuple(component))
    return all_components


def give_miners_authorization(the_miners_list, the_type_of_consensus):
    if the_type_of_consensus == 1:
        wanted = data["aiAssistedMining?"]
        float_portion = data["aiAssistedMinersPercentage"] / 100
        if wanted:
            num_of_miners_requested_to_use_AI = ceil(float_portion * len(the_miners_list))
            num_of_miners_instructed_to_use_AI = 0
            while num_of_miners_instructed_to_use_AI < num_of_miners_requested_to_use_AI:
                random_miner = random.choice(the_miners_list)
                if not random_miner.adversary:
                    random_miner.adversary = True
                    num_of_miners_instructed_to_use_AI += 1
            print(str(num_of_miners_instructed_to_use_AI) + ' miners were successfully instructed to use AI.')
        return wanted
    if the_type_of_consensus == 3:
        # automated approach:
        if data["Automatic_PoA_miners_authorization?"]:
            for i in range(len(the_miners_list)):
                the_miners_list[i].isAuthorized = True
                list_of_authorized_miners.append(the_miners_list[i])
        else:
            # user input approach:
            output.authorization_trigger(data["blockchainPlacement"], data["NumOfFogNodes"], data["NumOfMiners"])
            while True:
                authorized_miner = input()
                if authorized_miner == "done":
                    break
                else:
                    for node in the_miners_list:
                        if node.address == "Miner_" + authorized_miner:
                            node.isAuthorized = True
                            list_of_authorized_miners.append(node)
    return None


def initiate_genesis_block(AI_wanted):
    genesis_transactions = ["genesis_block"]
    for i in range(len(miner_list)):
        genesis_transactions.append(miner_list[i].address)
    genesis_block = new_consensus_module.generate_new_block(genesis_transactions, 'The Network', 0,
                                                            data["consensusAlgorithm"], AI_wanted, False)
    output.block_info(genesis_block, data["consensusAlgorithm"])
    for elem in miner_list:
        elem.receive_new_block(genesis_block, data["consensusAlgorithm"], miner_list, data["blockchainFunction"],
                               expected_chain_length)
    output.genesis_block_generation()


def send_tasks_to_BC():
    global user_informed
    for node in fogNodes:
        node.send_tasks_to_BC(user_informed)
        if not user_informed:
            user_informed = True


def store_fog_data():
    for node in fogNodes:
        log = open('temporary/Fog_node_' + str(node.address) + '.txt', 'w')
        log.write(str(node.local_storage))


def inform_miners_of_users_wallets():
    if data["blockchainFunction"] == 3:
        user_wallets = {}
        for user in list_of_end_users:
            wallet_info = {'parent': user.addressParent,
                           'self': user.addressSelf,
                           'wallet_value': user.wallet}
            user_wallets[str(user.addressParent) + '.' + str(user.addressSelf)] = wallet_info
        for i in range(len(miner_list)):
            modification.rewrite_file(str("temporary/" + miner_list[i].address + "_users_wallets.json"), user_wallets)


def run_simulations():
    global miner_list, expected_chain_length
    read_json()
    initiate_files()
    initiate_network()
    miner_list = initiate_miners()
    AI_assisted_mining_wanted = give_miners_authorization(miner_list, data["consensusAlgorithm"])
    inform_miners_of_users_wallets()
    blockchain.stake(miner_list, data["consensusAlgorithm"])
    initiate_genesis_block(AI_assisted_mining_wanted)
    send_tasks_to_BC()
    time_start = time.time()
    if data["blockchainFunction"] == 2:
        expected_chain_length = ceil(
            (data["num_of_users_per_fog_node"] * data["NumOfTaskPerUser"] * data["NumOfFogNodes"]))
    new_consensus_module.miners_trigger(miner_list, data["consensusAlgorithm"], expected_chain_length,
                                        data["Parallel_PoW_mining?"],
                                        data["numOfTXperBlock"], data["blockchainFunction"], data['poet_block_time'],
                                        data['Asymmetric_key_length'],
                                        data['Num_of_DPoS_delegates'], AI_assisted_mining_wanted)

    blockchain.award_winning_miners(len(miner_list), miner_list)
    blockchain.fork_analysis(miner_list)
    output.finish()
    store_fog_data()
    elapsed_time = time.time() - time_start
    print("elapsed time = " + str(elapsed_time) + " seconds")


if __name__ == '__main__':
    pass
