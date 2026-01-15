import React from "react";
import type { Metadata } from "next";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/sidebarLogin";
import { WalletProvider } from "@/components/walletProvider";
import WalletInput from "@/components/walletInput";

export const metadata: Metadata = {
  title: "PRPay Dashboard",
  description: "Dashboard page for PRPay application",
};

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="w-full">
      <WalletProvider>
        <SidebarProvider>
          <AppSidebar />
          <div className="px-4 w-full">
            <div className="flex flex-row gap-2 mt-4 mb-10 items-center">
              <SidebarTrigger/>
              <WalletInput />
            </div>
            {children}
          </div>
        </SidebarProvider>
      </WalletProvider>
    </div>
  );
}