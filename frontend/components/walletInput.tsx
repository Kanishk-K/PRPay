'use client';
import { ConnectButton } from '@rainbow-me/rainbowkit';

export default function WalletInput() {
    return (
        <ConnectButton.Custom>
            {({
                account,
                chain,
                openAccountModal,
                openChainModal,
                openConnectModal,
                mounted,
            }) => {
                const ready = mounted;
                const connected = ready && account && chain;

                return (
                    <div
                        {...(!ready && {
                            'aria-hidden': true,
                            'style': {
                                opacity: 0,
                                pointerEvents: 'none',
                                userSelect: 'none',
                            },
                        })}
                    >
                        {(() => {
                            if (!connected) {
                                return (
                                    <button
                                        onClick={openConnectModal}
                                        type="button"
                                        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
                                    >
                                        Connect Wallet
                                    </button>
                                );
                            }

                            if (chain.unsupported) {
                                return (
                                    <button
                                        onClick={openChainModal}
                                        type="button"
                                        className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors"
                                    >
                                        Wrong network
                                    </button>
                                );
                            }

                            return (
                                <div className="flex items-center gap-2">
                                    <button
                                        onClick={openChainModal}
                                        type="button"
                                        className="flex items-center gap-2 px-3 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
                                    >
                                        {chain.hasIcon && (
                                            <div
                                                style={{
                                                    background: chain.iconBackground,
                                                    width: 20,
                                                    height: 20,
                                                    borderRadius: 999,
                                                    overflow: 'hidden',
                                                }}
                                            >
                                                {chain.iconUrl && (
                                                    <img
                                                        alt={chain.name ?? 'Chain icon'}
                                                        src={chain.iconUrl}
                                                        style={{ width: 20, height: 20 }}
                                                    />
                                                )}
                                            </div>
                                        )}
                                    </button>

                                    <button
                                        onClick={openAccountModal}
                                        type="button"
                                        className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg font-mono text-sm transition-colors whitespace-nowrap"
                                    >
                                        {account.address}
                                    </button>
                                </div>
                            );
                        })()}
                    </div>
                );
            }}
        </ConnectButton.Custom>
    );
}