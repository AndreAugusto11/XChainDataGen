class PayloadDecoder:
    @staticmethod
    def decode(payload_hex: str, decimals: int) -> dict:
        """
        Decode a Wormhole BridgeStructs.Transfer payload and reconstruct the original token amount.

        Args:
            payload_hex (str): Hex string of the payload (with or without '0x').
            decimals (int): Number of token decimals (e.g., 18 for ERC20).

        Returns:
            dict: Decoded normalized fields and reconstructed original amount.
        """
        # Remove '0x' prefix if present
        if payload_hex.startswith("0x"):
            payload_hex = payload_hex[2:]
        payload = bytes.fromhex(payload_hex)

        # Check length
        # expected_len = 133
        # if len(payload) != expected_len:
        # raise ValueError(f"Invalid payload length: {len(payload)} bytes
        # (expected {expected_len})")

        offset = 0
        # payloadID
        payload_id = payload[offset]
        offset += 1
        # normalized amount
        amt_bytes = payload[offset : offset + 32]
        normalized_amount = int.from_bytes(amt_bytes, "big")
        offset += 32
        # tokenAddress
        token_address = "0x" + payload[offset : offset + 32].hex()
        offset += 32
        # tokenChain
        token_chain = int.from_bytes(payload[offset : offset + 2], "big")
        offset += 2
        # recipient
        recipient = "0x" + payload[offset : offset + 32].hex()
        offset += 32
        # toChain
        to_chain = int.from_bytes(payload[offset : offset + 2], "big")
        offset += 2
        # fee
        fee = int.from_bytes(payload[offset : offset + 32], "big")

        # Reconstruct original amount:
        # normalizeAmount = raw_amount / 10**(decimals - 8)
        # => raw_amount = normalized_amount * 10**(decimals - 8)
        shift = max(decimals - 8, 0)
        original_amount = normalized_amount * (10**shift)

        return {
            "payloadID": payload_id,
            "normalizedAmount": normalized_amount,
            "originalAmount": original_amount,
            "tokenAddress": token_address,
            "tokenChain": token_chain,
            "to": recipient,
            "toChain": to_chain,
            "fee": fee,
        }
