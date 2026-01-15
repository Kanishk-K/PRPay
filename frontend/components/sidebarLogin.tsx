import { CircleCheckBig, Coins, Inbox, ShieldUser, WalletMinimalIcon } from "lucide-react"

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

// Menu items.
const items = [
  {
    title: "Inbox",
    url: "/dashboard/review",
    icon: Inbox,
  },
  {
    title: "Rewards",
    url: "/dashboard/claim",
    icon: Coins,
  },
  {
    title: "Claimed",
    url: "/dashboard/completed",
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
              <a href="/dashboard/admin">
                <ShieldUser />
                <span>Team Overview</span>
              </a>
            </SidebarMenuButton>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarFooter>
    </Sidebar>
  )
}