import argparse

from cli import Cli


def test_extract_data():
    args = argparse.Namespace(
        blockchains=["ethereum", "ronin"],
        bridge="ronin",
        start_ts=1735689600,  # 1st Jan 2025
        end_ts=1735776000,  # 2nd Jan 2025
    )

    Cli.extract_data(args)

    from repository.database import DBSession
    from repository.ronin.repository import (
        RoninDepositRequestedRepository,
        RoninWithdrawalRequestedRepository,
    )

    ronin_deposit_requested = RoninDepositRequestedRepository(DBSession)

    events = ronin_deposit_requested.get_all()

    print(f"Number of events in RoninDepositRequested: {len(events)}")
    assert len(events) == 30, "Expected 30 events in RoninDepositRequested table after extraction."

    ronin_withdrawal_requested = RoninWithdrawalRequestedRepository(DBSession)

    events = ronin_withdrawal_requested.get_all()

    print(f"Number of events in RoninWithdrawalRequested: {len(events)}")
    assert len(events) == 49, (
        "Expected 49 events in RoninWithdrawalRequested table after extraction."
    )

    args = argparse.Namespace(
        bridge="ronin",
    )
    Cli.generate_data(args)

    # Here we can check if the data was generated correctly
    from repository.database import DBSession
    from repository.ronin.repository import RoninCrossChainTransactionRepository

    ronin_cross_chain_transactions_repo = RoninCrossChainTransactionRepository(DBSession)
    transactions = ronin_cross_chain_transactions_repo.get_all()

    print(f"Number of transactions in RoninCrossChainTransactions: {len(transactions)}")
    assert len(transactions) == 70, (
        "Expected 70 events in RoninCrossChainTransactions table after extraction."
    )
