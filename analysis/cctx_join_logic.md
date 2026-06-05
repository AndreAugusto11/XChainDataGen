# CCTX Join Logic

| bridge | source_events | destination_events | join_keys | additional_conditions |
| --- | --- | --- | --- | --- |
| CCTP | DepositForBurn | MessageReceived | nonce + chain pair | amount, burn_token, depositor, recipient equal |
| CCIP | CCIPSendRequested | ExecutionStateChanged | message_id + sequence_number | input_token IS NOT NULL |
| Stargate Taxi (v2) | OFTSent | OFTReceived | guid | Chain direction check |
| Stargate Taxi (v1) | OFTSendToChain | OFTReceiveFromChain | packet.nonce (via packet relay) | amount equal, chain check |
| Stargate Pool (v1) | Swap | SwapRemote | packet.nonce | amount_sd, protocol_fee, eq_fee equal |
| Stargate Bus | BusRode + OFTSent | BusDriven + OFTReceived | ticket_id in [start, start+n); guid; passenger | Amount with 10^12 decimal tolerance; ROW_NUMBER for intra-tx ordering |
| Across | V3FundsDeposited | FilledV3Relay | deposit_id | output_amount equal, chain checks |
| deBridge | CreatedOrder | FulfilledOrder | order_id (EVM src); maker_order_nonce (Solana src) | Chain filter |
| Mayan | InitOrder / OrderCreated | OrderFulfilled / FulfillOrder | order_hash (via .key on dst) | Auction subquery joined separately on order_hash |
| Omnibridge | UserRequestForSignature / TokensBridgingInitiated | RelayedMessage / TokensBridged | src_tx_hash + recipient + value / message_id | Value equality |
| Polygon PoS | StateSynced (via deposit) | StateCommitted / TokenDeposited | state_id | amount, deposit_count, token equal |
| Ronin | TokenDeposited / MainchainWithdrew | TokenDeposited / TokenWithdrew | deposit_id / withdrawal_id | depositor, recipient, input_token, output_token equal |