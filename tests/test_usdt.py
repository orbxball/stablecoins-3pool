# TODO: Add tests here that show the normal operation of this strategy
#       Suggestions to include:
#           - strategy loading and unloading (via Vault addStrategy/revokeStrategy)
#           - change in loading (from low to high and high to low)
#           - strategy operation at different loading levels (anticipated and "extreme")
from brownie import Wei, reverts
from useful_methods import genericStateOfVault, genericStateOfStrat
import brownie

def test_usdt(Vault, StrategyUSDT3pool, usdt_whale, gov, usdt):
    # deploy usdt vault
    usdt_vault = gov.deploy(Vault, usdt, gov, gov, '', '')
    print(f'type of vault: {type(usdt_vault)} @ {usdt_vault}')

    # deploy usdt strategy
    usdt_strategy = gov.deploy(StrategyUSDT3pool, usdt_vault)
    print(f'type of strategy: {type(usdt_strategy)} @ {usdt_strategy}')

    # activate the strategy from vault view
    usdt_vault.addStrategy(usdt_strategy, 2**64, 2**64, 1000, {'from': gov})
    print(f'credit of strategy: {usdt_vault.creditAvailable(usdt_strategy)}')

    # rm yvusdt's guestlist
    usdt_vault.setGuestList('0x0000000000000000000000000000000000000000', {'from': gov})
    print(f'yvusdt guest list: {usdt_vault.guestList()}')

    # approve usdt vault to use usdt
    usdt.approve(usdt_vault, 2**256-1, {'from': usdt_whale})

    # start deposit
    print('\n=== deposit 100 usdt ===')
    print(f'whale\'s usdt balance before deposit: {usdt.balanceOf(usdt_whale)/1e6}')
    deposit_amount = Wei('100 ether')/1e12
    usdt_vault.deposit(deposit_amount, {'from': usdt_whale})
    print(f'whale\'s usdt balance  after deposit: {usdt.balanceOf(usdt_whale)/1e6}')

    # start strategy
    print('\n=== harvest usdt ===')
    usdt_strategy.harvest({'from': gov})
    print('harvest done')

    print('\n=== usdt status ===')
    genericStateOfStrat(usdt_strategy, usdt, usdt_vault)
    genericStateOfVault(usdt_vault, usdt)

    # withdraw
    print('\n=== withdraw usdt ===')
    print(f'whale\'s usdt vault share: {usdt_vault.balanceOf(usdt_whale)/1e6}')
    usdt_vault.withdraw(Wei('1 ether')/1e12, {'from': usdt_whale})
    print(f'withdraw 1 share of usdt done')
    print(f'whale\'s usdt vault share: {usdt_vault.balanceOf(usdt_whale)/1e6}')
    
    # withdraw all
    print('\n=== withdraw all usdt ===')
    print(f'whale\'s usdt vault share: {usdt_vault.balanceOf(usdt_whale)/1e6}')
    usdt_vault.withdraw({'from': usdt_whale})
    print(f'withdraw all usdt')
    print(f'whale\'s usdt vault share: {usdt_vault.balanceOf(usdt_whale)/1e6}')

    # call tend
    print('\ncall tend')
    usdt_strategy.tend()
    print('tend done')
