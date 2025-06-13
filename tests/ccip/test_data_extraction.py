import argparse

from cli import Cli


def test_extract_data():
    args = argparse.Namespace(
        blockchains=[
            "ethereum",
            "arbitrum",
            "avalanche",
            "polygon",
            "optimism",
            "bnb",
            "base",
            "linea",
            "scroll",
        ],
        bridge="ccip",
        start_ts=1735689600,  # 1st Jan 2025 00:00
        end_ts=1735732800,  # 1st Jan 2025 12:00
    )

    Cli.extract_data(args)

    # now we can check if the data was extracted correctly
    # For example, we can check if the CCIPSendRequested table has been populated
    from repository.ccip.repository import (
        CCIPExecutionStateChangedRepository,
        CCIPSendRequestedRepository,
    )
    from repository.database import DBSession

    ccip_send_requested_repo = CCIPSendRequestedRepository(DBSession)
    events = ccip_send_requested_repo.get_all()
    print(f"Number of events in CCIPSendRequested: {len(events)}")
    assert len(events) == 61, "Expected 61 events in CCIPSendRequested table after extraction."

    ccip_execution_state_changed_repo = CCIPExecutionStateChangedRepository(DBSession)
    events = ccip_execution_state_changed_repo.get_all()
    print(f"Number of events in CCIPExecutionStateChanged: {len(events)}")
    assert len(events) == 163, (
        "Expected 163 events in CCIPExecutionStateChanged table after extraction."
    )

    args = argparse.Namespace(
        bridge="ccip",
    )
    Cli.generate_data(args)

    # Here we can check if the data was generated correctly
    from repository.ccip.repository import CCIPCrossChainTransactionsRepository
    from repository.database import DBSession

    ccip_cross_chain_transactions_repo = CCIPCrossChainTransactionsRepository(DBSession)
    transactions = ccip_cross_chain_transactions_repo.get_all()

    print(f"Number of transactions in CCIPCrossChainTransactions: {len(transactions)}")
    assert len(transactions) == 59, (
        "Expected 59 events in CCIPCrossChainTransactions table after extraction."
    )
