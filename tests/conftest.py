import pytest
from brownie import config

@pytest.fixture
def andre(accounts):
    # Andre, giver of tokens, and maker of yield
    yield accounts[0]


@pytest.fixture
def gov(accounts):
    # yearn multis... I mean YFI governance. I swear!
    yield accounts.at('0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52', force=True)


@pytest.fixture
def rewards(gov):
    yield gov  # TODO: Add rewards contract


@pytest.fixture
def guardian(accounts):
    # YFI Whale, probably
    yield accounts[2]


@pytest.fixture
def vault(pm, gov, rewards, guardian, token):
    Vault = pm(config["dependencies"][0]).Vault
    vault = guardian.deploy(Vault, token, gov, rewards, "", "")
    yield vault


@pytest.fixture
def strategist(accounts):
    # You! Our new Strategist!
    yield accounts[3]


@pytest.fixture
def keeper(accounts):
    # This is our trusty bot!
    yield accounts.at('0x13dAda6157Fee283723c0254F43FF1FdADe4EEd6', force=True)


@pytest.fixture
def strategy(strategist, keeper, vault, Strategy):
    strategy = strategist.deploy(Strategy, vault)
    strategy.setKeeper(keeper)
    yield strategy


@pytest.fixture
def Vault(pm):
    yield pm(config["dependencies"][0]).Vault


@pytest.fixture
def dai(interface):
    yield interface.ERC20('0x6B175474E89094C44Da98b954EedeAC495271d0F')


@pytest.fixture
def dai_vault(Vault):
    yield Vault.at('0xBFa4D8AA6d8a379aBFe7793399D3DdaCC5bBECBB')


@pytest.fixture
def dai_whale(accounts):
    # binance7
    yield accounts.at('0xBE0eB53F46cd790Cd13851d5EFf43D12404d33E8', force=True)
