'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useAccount } from 'wagmi';

interface Wallet {
  address: string;
  balance?: number;
  // Add other wallet properties as needed
}

interface WalletContextType {
  wallet: Wallet | null;
  setWallet: (wallet: Wallet | null) => void;
  connectWallet: (address: string) => void;
  disconnectWallet: () => void;
}

const WalletContext = createContext<WalletContextType | undefined>(undefined);

export function WalletProvider({ children }: { children: ReactNode }) {
  const [wallet, setWallet] = useState<Wallet | null>(null);
  const { address, isConnected } = useAccount();

  // Sync Wagmi account state with wallet context
  useEffect(() => {
    if (isConnected && address) {
      setWallet({ address });
    } else {
      setWallet(null);
    }
  }, [address, isConnected]);

  const connectWallet = (walletAddress: string) => {
    setWallet({ address: walletAddress });
  };

  const disconnectWallet = () => {
    setWallet(null);
  };

  return (
    <WalletContext.Provider
      value={{ wallet, setWallet, connectWallet, disconnectWallet }}
    >
      {children}
    </WalletContext.Provider>
  );
}

export function useWallet() {
  const context = useContext(WalletContext);
  if (context === undefined) {
    throw new Error('useWallet must be used within a WalletProvider');
  }
  return context;
}