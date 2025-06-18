import argparse

from cli import Cli


def test_extract_data():
    args = argparse.Namespace(
        blockchains=[
            "ethereum",
            "base",
            "avalanche",
            "optimism",
            "arbitrum",
            "bnb",
            "polygon",
            "linea",
        ],
        bridge="mayan",
        start_ts=1741219200,  # 6th Mar 2025 00:00
        end_ts=1741262400,  # 6th Mar 2025 12:00
    )

    Cli.extract_data(args)

    from repository.database import DBSession
    from repository.mayan.repository import (
        MayanBlockchainTransactionRepository,
        MayanForwardedRepository,
        MayanOrderCreatedRepository,
        MayanOrderFulfilledRepository,
        MayanOrderUnlockedRepository,
        MayanSwapAndForwardedRepository,
    )

    mayan_swap_and_fwd = MayanSwapAndForwardedRepository(DBSession)
    events = mayan_swap_and_fwd.get_all()
    print(f"Number of events in MayanSwapAndForwarded: {len(events)}")
    assert len(events) == 5, "Expected 5 events in MayanSwapAndForwarded table after extraction."

    mayan_order_created = MayanOrderCreatedRepository(DBSession)
    events = mayan_order_created.get_all()
    print(f"Number of events in MayanOrderCreated: {len(events)}")
    assert len(events) == 2767, "Expected 2767 events in MayanOrderCreated table after extraction."

    mayan_order_fulfilled = MayanOrderFulfilledRepository(DBSession)
    events = mayan_order_fulfilled.get_all()
    print(f"Number of events in MayanOrderFulfilled: {len(events)}")
    assert len(events) == 1690, (
        "Expected 1690 events in MayanOrderFulfilled table after extraction."
    )  # noqa: E501

    mayan_order_unlocked = MayanOrderUnlockedRepository(DBSession)
    events = mayan_order_unlocked.get_all()
    print(f"Number of events in MayanOrderUnlocked: {len(events)}")
    assert len(events) == 2832, "Expected 2832 events in MayanOrderUnlocked table after extraction."

    mayan_forwarded = MayanForwardedRepository(DBSession)
    events = mayan_forwarded.get_all()
    print(f"Number of events in MayanForwarded: {len(events)}")
    assert len(events) == 4, "Expected 4 events in MayanForwarded table after extraction."

    mayan_blockchain_transaction = MayanBlockchainTransactionRepository(DBSession)
    transactions = mayan_blockchain_transaction.get_all()
    print(f"Number of transactions in MayanBlockchainTransaction: {len(transactions)}")
    assert len(transactions) == 4898, (
        "Expected 4898 transactions in MayanBlockchainTransaction table after extraction."
    )  # noqa: E501
