SELECT
    src_tx.blockchain AS src_blockchain,
    src_tx.transaction_hash AS src_tx_hash,
    src_tx.from_address AS src_from_address,
    src_tx.to_address AS src_to_address,
    src_tx.fee AS src_fee,
    NULL AS src_fee_usd,
    src_tx.timestamp AS src_timestamp,
    dst_tx.blockchain AS dst_blockchain,
    dst_tx.transaction_hash AS dst_tx_hash,
    dst_tx.from_address AS dst_from_address,
    dst_tx.to_address AS dst_to_address,
    dst_tx.fee AS dst_fee,
    NULL AS dst_fee_usd,
    dst_tx.timestamp AS dst_timestamp,
    deposit.deposit_block_id AS deposit_id,
    deposit.owner AS depositor,
    fill.user AS recipient,
    fill.root_token AS src_contract_address,
    deposit.amount AS src_amount,
    deposit_state.data AS src_data
FROM polygon_new_deposit_block deposit
LEFT JOIN polygon_state_synced deposit_state ON deposit_state.transaction_hash = deposit.transaction_hash
LEFT JOIN polygon_blockchain_transactions src_tx ON deposit.transaction_hash = src_tx.transaction_hash
LEFT JOIN polygon_state_committed fill_state ON fill_state.state_id = deposit_state.state_id
LEFT JOIN polygon_token_deposited fill ON fill.transaction_hash = fill_state.transaction_hash
LEFT JOIN polygon_blockchain_transactions dst_tx ON dst_tx.transaction_hash = fill_state.transaction_hash
WHERE deposit_state.data LIKE '%' || SUBSTRING(deposit.token FROM 3) || '%'
AND deposit.amount = fill.amount
AND fill.deposit_count = deposit.deposit_block_id
AND deposit.token = fill.root_token;