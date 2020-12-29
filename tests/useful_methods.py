import brownie
import requests

def genericStateOfStrat(strategy, currency, vault):
    decimals = currency.decimals()
    print(f'\n--- state of {strategy.name()} ---')

    print(f'Want: {currency.balanceOf(strategy) / 10**decimals}')
    print(f'Total assets estimate: {strategy.estimatedTotalAssets() / 10**decimals}')
    strState = vault.strategies(strategy)
    totalDebt = strState[5] / 10**decimals
    debtLimit = strState[2] / 10**decimals

    totalReturns = strState[6] / 10**decimals
    print(f'Total Strategy Debt: {totalDebt:.5f}')
    print(f'Strategy Debt Limit: {debtLimit:.5f}')
    print(f'Total Strategy Returns: {totalReturns:.5f}')
    print(f'Last Report: {strState[4]}')
    callCost = 1000000 * 30 * 1e9 # 1m gas at 30 gwei
    print(f'Harvest Trigger: {strategy.harvestTrigger(callCost)}')
    print(f'Tend Trigger: {strategy.tendTrigger(1000000 * 30 * 1e9)}')  
    print(f'Emergency Exit: {strategy.emergencyExit()}')


def genericStateOfVault(vault, currency):
    decimals = currency.decimals()
    print(f'\n--- state of {vault.name()} vault ---')
    balance = vault.totalAssets() / 10**decimals
    print(f'Total Assets: {balance:.5f}')
    balance = vault.totalDebt() / 10**decimals
    print(f'Loose balance in vault: {currency.balanceOf(vault) / 10**decimals}')
    print(f'Total Debt: {balance:.5f}')

