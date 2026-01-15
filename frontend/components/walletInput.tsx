'use client';
import { WalletMinimalIcon } from "lucide-react"
import { InputGroup, InputGroupInput, InputGroupAddon } from "./ui/input-group"
import { useWallet } from "./walletProvider";

export default function WalletInput() {
    const { connectWallet, disconnectWallet } = useWallet();
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const address = e.target.value;
        if (address) {
            connectWallet(address);
        } else {
            disconnectWallet();
        }
    }
    return (
        <InputGroup className="max-w-100">
            <InputGroupInput type="email" placeholder="Enter your Wallet Address" onChange={handleInputChange}/>
            <InputGroupAddon>
                <WalletMinimalIcon />
            </InputGroupAddon>
        </InputGroup>
    )
}