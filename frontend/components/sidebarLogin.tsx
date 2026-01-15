import { CircleCheckBig, Coins, Inbox } from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import WalletBar from "./walletBar";

// Menu items.
const items = [
  {
    title: "Inbox",
    url: "#",
    icon: Inbox,
  },
  {
    title: "Rewards",
    url: "#",
    icon: Coins,
  },
  {
    title: "Claimed",
    url: "#",
    icon: CircleCheckBig,
  }
]

export function AppSidebar() {
  return (
    <Sidebar collapsible="icon">
    <SidebarContent>
        <SidebarGroup>
        <SidebarGroupContent>
            <SidebarMenu>
            {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                <SidebarMenuButton asChild>
                    <a href={item.url}>
                    <item.icon />
                    <span>{item.title}</span>
                    </a>
                </SidebarMenuButton>
                </SidebarMenuItem>
            ))}
            </SidebarMenu>
        </SidebarGroupContent>
        </SidebarGroup>
    </SidebarContent>
    <SidebarFooter>
      <SidebarMenu>
        <SidebarMenuItem>
            <SidebarMenuButton asChild>
                <WalletBar />
            </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarFooter>
    </Sidebar>
  )
}