"""
Crypto payment service for handling native ETH payments on Base Sepolia testnet.
"""
import logging
from decimal import Decimal
from typing import Optional

from web3 import Web3
from web3.exceptions import Web3Exception

from config import get_settings

logger = logging.getLogger(__name__)


class CryptoPaymentService:
    """Service for handling native ETH payments on Base Sepolia testnet."""

    def __init__(self):
        """Initialize the Web3 connection and wallet."""
        settings = get_settings()

        # Validate configuration
        if not settings.WALLET_PRIVATE_KEY:
            raise ValueError("WALLET_PRIVATE_KEY not configured in environment")
        if not settings.BASE_SEPOLIA_RPC_URL:
            raise ValueError("BASE_SEPOLIA_RPC_URL not configured in environment")

        # Initialize Web3 with Base Sepolia RPC
        self.w3 = Web3(Web3.HTTPProvider(settings.BASE_SEPOLIA_RPC_URL))

        # Check connection
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Base Sepolia RPC endpoint")

        # Load wallet from private key
        self.account = self.w3.eth.account.from_key(settings.WALLET_PRIVATE_KEY)
        self.wallet_address = self.account.address

        logger.info(f"CryptoPaymentService initialized with wallet: {self.wallet_address}")

    def validate_address(self, address: str) -> bool:
        """
        Validate an Ethereum address.

        Args:
            address: The Ethereum address to validate

        Returns:
            True if valid, False otherwise
        """
        return Web3.is_address(address)

    def send_eth_payment(
        self,
        recipient_address: str,
        amount_eth: float
    ) -> dict:
        """
        Send native ETH payment to a recipient on Base Sepolia.

        Args:
            recipient_address: The recipient's Ethereum address
            amount_eth: The amount in ETH units

        Returns:
            Dictionary containing:
                - success (bool): Whether the transaction succeeded
                - transaction_hash (str): The transaction hash if successful
                - error (str): Error message if failed
        """
        try:
            # Validate recipient address
            if not self.validate_address(recipient_address):
                return {
                    "success": False,
                    "transaction_hash": None,
                    "error": f"Invalid recipient address: {recipient_address}"
                }

            recipient_address = Web3.to_checksum_address(recipient_address)

            # Convert ETH amount to Wei
            amount_wei = self.w3.to_wei(amount_eth, 'ether')

            logger.info(f"Preparing to send {amount_eth} ETH ({amount_wei} Wei) to {recipient_address}")

            # Get current nonce
            nonce = self.w3.eth.get_transaction_count(self.wallet_address)

            # Build transaction
            transaction = {
                'from': self.wallet_address,
                'to': recipient_address,
                'value': amount_wei,
                'nonce': nonce,
                'gas': 21000,  # Standard gas limit for ETH transfer
                'gasPrice': self.w3.eth.gas_price,
                'chainId': 84532  # Base Sepolia chain ID
            }

            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                private_key=get_settings().WALLET_PRIVATE_KEY
            )

            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            tx_hash_hex = tx_hash.hex()

            logger.info(f"Transaction sent: {tx_hash_hex}")

            # Wait for transaction receipt
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

            if tx_receipt.status == 1:
                logger.info(f"Transaction successful: {tx_hash_hex}")
                return {
                    "success": True,
                    "transaction_hash": tx_hash_hex,
                    "error": None
                }
            else:
                logger.error(f"Transaction failed: {tx_hash_hex}")
                return {
                    "success": False,
                    "transaction_hash": tx_hash_hex,
                    "error": "Transaction reverted"
                }

        except Web3Exception as e:
            error_msg = f"Web3 error: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "transaction_hash": None,
                "error": error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "transaction_hash": None,
                "error": error_msg
            }

    def get_wallet_balance(self) -> Optional[Decimal]:
        """
        Get the ETH balance of the payment wallet.

        Returns:
            Balance in ETH units, or None if error
        """
        try:
            balance_wei = self.w3.eth.get_balance(self.wallet_address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return Decimal(str(balance_eth))
        except Exception as e:
            logger.error(f"Failed to get wallet balance: {e}")
            return None


# Singleton instance
_payment_service: Optional[CryptoPaymentService] = None


def get_payment_service() -> CryptoPaymentService:
    """
    Get or create the payment service singleton.

    Returns:
        CryptoPaymentService instance
    """
    global _payment_service
    if _payment_service is None:
        _payment_service = CryptoPaymentService()
    return _payment_service
