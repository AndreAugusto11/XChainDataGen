import argparse

from cli import Cli


def test_extract_data():
    args = argparse.Namespace(
        blockchains=["ethereum", "gnosis"],
        bridge="omnibridge",
        start_ts=1735689600,  # 1st Jan 2025
        end_ts=1735776000,  # 2nd Jan 2025
    )

    Cli.extract_data(args)

    from repository.database import DBSession
    from repository.omnibridge.repository import (
        OmnibridgeAffirmationCompletedRepository,
        OmnibridgeRelayedMessageRepository,
        OmnibridgeTokensBridgedRepository,
        OmnibridgeTokensBridgingInitiatedRepository,
        OmnibridgeUserRequestForAffirmationRepository,
        OmnibridgeUserRequestForSignatureRepository,
    )

    omnibridge_user_req_for_sign = OmnibridgeUserRequestForSignatureRepository(DBSession)
    events = omnibridge_user_req_for_sign.get_all()
    print(f"Number of events in OmnibridgeUserRequestForSignature: {len(events)}")
    assert len(events) == 51, (
        "Expected 51 events in OmnibridgeUserRequestForSignature table after extraction."
    )

    omnibridge_relayed_message = OmnibridgeRelayedMessageRepository(DBSession)
    events = omnibridge_relayed_message.get_all()
    print(f"Number of events in OmnibridgeRelayedMessage: {len(events)}")
    assert len(events) == 13, (
        "Expected 13 events in OmnibridgeRelayedMessage table after extraction."
    )

    omnibridge_user_req_for_aff = OmnibridgeUserRequestForAffirmationRepository(DBSession)
    events = omnibridge_user_req_for_aff.get_all()
    print(f"Number of events in OmnibridgeUserRequestForAffirmation: {len(events)}")
    assert len(events) == 53, (
        "Expected 53 events in OmnibridgeUserRequestForAffirmation table after extraction."
    )

    omnibridge_affirmation_completed = OmnibridgeAffirmationCompletedRepository(DBSession)
    events = omnibridge_affirmation_completed.get_all()
    print(f"Number of events in OmnibridgeAffirmationCompleted: {len(events)}")
    assert len(events) == 12, (
        "Expected 12 events in OmnibridgeAffirmationCompleted table after extraction."
    )

    omnibridge_tokens_bridged = OmnibridgeTokensBridgedRepository(DBSession)
    events = omnibridge_tokens_bridged.get_all()
    print(f"Number of events in OmnibridgeTokensBridged: {len(events)}")
    assert len(events) == 75, (
        "Expected 75 events in OmnibridgeTokensBridged table after extraction."
    )

    omnibridge_tokens_bridging_initiated = OmnibridgeTokensBridgingInitiatedRepository(DBSession)
    events = omnibridge_tokens_bridging_initiated.get_all()
    print(f"Number of events in OmnibridgeTokensBridgingInitiated: {len(events)}")
    assert len(events) == 79, (
        "Expected 79 events in OmnibridgeTokensBridgingInitiated table after extraction."
    )

    args = argparse.Namespace(
        bridge="omnibridge",
    )
    Cli.generate_data(args)

    # Here we can check if the data was generated correctly
    from repository.database import DBSession
    from repository.omnibridge.repository import (
        OmnibridgeCrossChainTransactionsRepository,
        OmnibridgeOperatorTransactionsRepository,
    )

    omnibridge_cross_chain_transactions_repo = OmnibridgeCrossChainTransactionsRepository(DBSession)
    transactions = omnibridge_cross_chain_transactions_repo.get_all()

    print(f"Number of transactions in OmnibridgeCrossChainTransactions: {len(transactions)}")
    assert len(transactions) == 97, (
        "Expected 97 events in OmnibridgeCrossChainTransactions table after extraction."
    )

    omnibridge_operator_transactions_repo = OmnibridgeOperatorTransactionsRepository(DBSession)
    operator_transactions = omnibridge_operator_transactions_repo.get_all()
    print(f"Number of transactions in OmnibridgeOperatorTransactions: {len(operator_transactions)}")
    assert len(operator_transactions) == 156, (
        "Expected 156 events in OmnibridgeOperatorTransactions table after extraction."
    )
