import argparse

from cli import Cli


def test_extract_data():
    args = argparse.Namespace(
        blockchains=["ethereum", "arbitrum", "avalanche", "polygon", "optimism", "base"],
        bridge="cctp",
        start_ts=1735689600,  # 1st Dec 2024 00:00
        end_ts=1735776000,  # 2nd Jan 2024 00:00
    )

    Cli.extract_data(args)

    from repository.cctp.repository import CCTPDepositForBurnRepository
    from repository.database import DBSession

    cctp_send_requested_repo = CCTPDepositForBurnRepository(DBSession)

    events = cctp_send_requested_repo.get_all()

    print(f"Number of events in CCTPDepositForBurn: {len(events)}")
    assert len(events) == 2675, "Expected 2675 events in CCTPDepositForBurn table after extraction."

    args = argparse.Namespace(
        bridge="cctp",
    )
    Cli.generate_data(args)

    # Here we can check if the data was generated correctly
    from repository.cctp.repository import CctpCrossChainTransactionsRepository
    from repository.database import DBSession

    cctp_cross_chain_transactions_repo = CctpCrossChainTransactionsRepository(DBSession)
    transactions = cctp_cross_chain_transactions_repo.get_all()

    print(f"Number of transactions in CCTPCrossChainTransactions: {len(transactions)}")
    assert len(transactions) == 2619, (
        "Expected 2619 events in CCTPCrossChainTransactions table after extraction."
    )
