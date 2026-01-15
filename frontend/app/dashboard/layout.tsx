import React from "react";
import type { Metadata } from "next";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/sidebarLogin";

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
      <SidebarProvider>
        <AppSidebar />
        <div className="px-4 w-full">
          <SidebarTrigger className="mt-4 mb-10"/>
          {children}
        </div>
      </SidebarProvider>
    </div>
  );
}