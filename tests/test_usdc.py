# TODO: Add tests here that show the normal operation of this strategy
#       Suggestions to include:
#           - strategy loading and unloading (via Vault addStrategy/revokeStrategy)
#           - change in loading (from low to high and high to low)
#           - strategy operation at different loading levels (anticipated and "extreme")
from brownie import Wei, reverts
from useful_methods import genericStateOfVault, genericStateOfStrat
import brownie

def test_usdc(Vault, StrategyUSDC3pool, usdc_whale, gov, usdc):
    # deploy usdc vault
    usdc_vault = gov.deploy(Vault, usdc, gov, gov, '', '')
    print(f'type of vault: {type(usdc_vault)} @ {usdc_vault}')

    # deploy usdc strategy
    usdc_strategy = gov.deploy(StrategyUSDC3pool, usdc_vault)
    print(f'type of strategy: {type(usdc_strategy)} @ {usdc_strategy}')

    # activate the strategy from vault view
    usdc_vault.addStrategy(usdc_strategy, 2**64, 2**64, 1000, {'from': gov})
    print(f'credit of strategy: {usdc_vault.creditAvailable(usdc_strategy)}')

    # rm yvusdc's guestlist
    usdc_vault.setGuestList('0x0000000000000000000000000000000000000000', {'from': gov})
    print(f'yvusdc guest list: {usdc_vault.guestList()}')

    # approve usdc vault to use usdc
    usdc.approve(usdc_vault, 2**256-1, {'from': usdc_whale})

    # start deposit
    print('\n=== deposit 100 usdc ===')
    print(f'whale\'s usdc balance before deposit: {usdc.balanceOf(usdc_whale)/1e6}')
    deposit_amount = Wei('100 ether')/1e12
    usdc_vault.deposit(deposit_amount, {'from': usdc_whale})
    print(f'whale\'s usdc balance  after deposit: {usdc.balanceOf(usdc_whale)/1e6}')

    # start strategy
    print('\n=== harvest usdc ===')
    usdc_strategy.harvest({'from': gov})
    print('harvest done')

    print('\n=== usdc status ===')
    genericStateOfStrat(usdc_strategy, usdc, usdc_vault)
    genericStateOfVault(usdc_vault, usdc)

    # withdraw
    print('\n=== withdraw usdc ===')
    print(f'whale\'s usdc vault share: {usdc_vault.balanceOf(usdc_whale)/1e6}')
    usdc_vault.withdraw(Wei('1 ether')/1e12, {'from': usdc_whale})
    print(f'withdraw 1 share of usdc done')
    print(f'whale\'s usdc vault share: {usdc_vault.balanceOf(usdc_whale)/1e6}')
    
    # withdraw all
    print('\n=== withdraw all usdc ===')
    print(f'whale\'s usdc vault share: {usdc_vault.balanceOf(usdc_whale)/1e6}')
    usdc_vault.withdraw({'from': usdc_whale})
    print(f'withdraw all usdc')
    print(f'whale\'s usdc vault share: {usdc_vault.balanceOf(usdc_whale)/1e6}')

    # call tend
    print('\ncall tend')
    usdc_strategy.tend()
    print('tend done')
