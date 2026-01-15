"use client"

import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { ChevronDown } from "lucide-react"
import { useState } from "react"

interface CollapsibleSectionProps {
    title: string
    defaultOpen?: boolean
    children: React.ReactNode
}

export default function CollapsibleSection({ title, defaultOpen = true, children }: CollapsibleSectionProps) {
    const [isOpen, setIsOpen] = useState(defaultOpen)

    return (
        <Collapsible open={isOpen} onOpenChange={setIsOpen}>
            <CollapsibleTrigger className="flex items-center gap-2 w-full py-2 hover:cursor-pointer">
                <ChevronDown
                    className={`h-4 w-4 transition-transform ${isOpen ? "" : "-rotate-90"}`}
                />
                <span className="font-semibold text-lg">{title}</span>
            </CollapsibleTrigger>
            <CollapsibleContent className="flex flex-col gap-2">
                {children}
            </CollapsibleContent>
        </Collapsible>
    )
}
