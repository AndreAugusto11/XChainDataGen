import argparse

from cli import Cli


def test_extract_data():
    args = argparse.Namespace(
        blockchains=["ethereum", "arbitrum", "bnb", "base"],
        bridge="debridge",
        start_ts=1733011200,  # 1st Dec 2024 00:00
        end_ts=1733014800,  # 1st Dec 2024 01:00
    )

    Cli.extract_data(args)

    from repository.database import DBSession
    from repository.debridge.repository import (
        DeBridgeClaimedUnlockRepository,
        DeBridgeCreatedOrderRepository,
        DeBridgeFulfilledOrderRepository,
    )

    debridge_created_order_repo = DeBridgeCreatedOrderRepository(DBSession)
    events = debridge_created_order_repo.get_all()
    print(f"Number of events in DeBridgeCreatedOrder: {len(events)}")
    assert len(events) == 72, "Expected 72 events in DeBridgeCreatedOrder table after extraction."
    debridge_fulfilled_order_repo = DeBridgeFulfilledOrderRepository(DBSession)
    events = debridge_fulfilled_order_repo.get_all()
    print(f"Number of events in DeBridgeFulfilledOrder: {len(events)}")
    assert len(events) == 71, "Expected 71 events in DeBridgeFulfilledOrder table after extraction."
    debridge_claimed_unlock_repo = DeBridgeClaimedUnlockRepository(DBSession)
    events = debridge_claimed_unlock_repo.get_all()
    print(f"Number of events in DeBridgeClaimedUnlock: {len(events)}")
    assert len(events) == 108, (
        "Expected 108 events in DeBridgeClaimedUnlock table after extraction."
    )

    args = argparse.Namespace(
        bridge="debridge",
    )
    Cli.generate_data(args)

    # Here we can check if the data was generated correctly
    from repository.database import DBSession
    from repository.debridge.repository import DeBridgeCrossChainTransactionsRepository

    debridge_cross_chain_transactions_repo = DeBridgeCrossChainTransactionsRepository(DBSession)
    events = debridge_cross_chain_transactions_repo.get_all()
    print(f"Number of events in DeBridgeCrossChainTransactions: {len(events)}")
    assert len(events) == 71, (
        "Expected 71 events in DeBridgeCrossChainTransactions table after extraction."
    )
