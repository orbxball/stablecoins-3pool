# TODO: Add tests here that show the normal operation of this strategy
#       Suggestions to include:
#           - strategy loading and unloading (via Vault addStrategy/revokeStrategy)
#           - change in loading (from low to high and high to low)
#           - strategy operation at different loading levels (anticipated and "extreme")
from brownie import Wei, reverts
from useful_methods import genericStateOfVault, genericStateOfStrat
import brownie

def test_dai(Vault, StrategyDAI3pool, dai_vault, dai_whale, gov, dai):
    # deploy dai strategy
    dai_strategy = gov.deploy(StrategyDAI3pool, dai_vault)
    print(f'type of strategy: {type(dai_strategy)} @ {dai_strategy}')

    # activate the strategy from vault view
    dai_vault.addStrategy(dai_strategy, 2**64, 2**64, 1000, {'from': gov})
    print(f'credit of strategy: {dai_vault.creditAvailable(dai_strategy)}')

    # rm yvdai's guestlist
    dai_vault.setGuestList('0x0000000000000000000000000000000000000000', {'from': gov})
    print(f'yvdai guest list: {dai_vault.guestList()}')

    # approve dai vault to use dai
    dai.approve(dai_vault, 2**256-1, {'from': dai_whale})

    # start deposit
    print('\n=== deposit 100 dai ===')
    print(f'whale\'s dai balance before deposit: {dai.balanceOf(dai_whale)/1e18}')
    deposit_amount = Wei('100 ether')
    dai_vault.deposit(deposit_amount, {'from': dai_whale})
    print(f'whale\'s dai balance  after deposit: {dai.balanceOf(dai_whale)/1e18}')

    # start strategy
    print('\n=== harvest dai ===')
    dai_strategy.harvest({'from': gov})
    print('harvest done')

    print('\n=== dai status ===')
    genericStateOfStrat(dai_strategy, dai, dai_vault)
    genericStateOfVault(dai_vault, dai)

    # withdraw
    print('\n=== withdraw dai ===')
    print(f'whale\'s dai vault share: {dai_vault.balanceOf(dai_whale)/1e18}')
    dai_vault.withdraw(Wei('1 ether'), {'from': dai_whale})
    print(f'withdraw 1 share of dai done')
    print(f'whale\'s dai vault share: {dai_vault.balanceOf(dai_whale)/1e18}')
    
    # withdraw all
    print('\n=== withdraw all dai ===')
    print(f'whale\'s dai vault share: {dai_vault.balanceOf(dai_whale)/1e18}')
    dai_vault.withdraw({'from': dai_whale})
    print(f'withdraw all dai')
    print(f'whale\'s dai vault share: {dai_vault.balanceOf(dai_whale)/1e18}')

    # call tend
    print('\ncall tend')
    dai_strategy.tend()
    print('tend done')

