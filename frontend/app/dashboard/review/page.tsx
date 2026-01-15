import ReviewPR from "@/components/events/reviewPr";
import ReviewPRProps from "@/components/events/types";
import { createClient } from "@/lib/supabase/server";
import CollapsibleSection from "./collapsible-section";

async function fetchPRs(githubId: string, status: string): Promise<ReviewPRProps[]> {
    const params = new URLSearchParams({ user_id: githubId, status });
    const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}getPRs?${params}`, {
        cache: "no-store"
    });
    return res.json();
}

export default async function ReviewPage(){
    const supabase = await createClient();
    const { data: { user } } = await supabase.auth.getUser()

    const githubId = user?.user_metadata?.provider_id

    const [requestedPRs, ineligiblePRs] = await Promise.all([
        fetchPRs(githubId, "requested"),
        fetchPRs(githubId, "ineligible")
    ]);

    return (
        <div className="flex flex-col gap-4">
            <CollapsibleSection title="Current" defaultOpen={true}>
                {requestedPRs.length === 0 ? (
                    <p className="text-muted-foreground text-sm py-2">No pending reviews</p>
                ) : (
                    requestedPRs.map((pr) => (
                        <ReviewPR
                            key={pr.pr_id}
                            pr_id={pr.pr_id}
                            pr_title={pr.pr_title}
                            pr_created_at={pr.pr_created_at}
                            pr_url={pr.pr_url}
                            payout={pr.payout}
                            status="requested"
                        />
                    ))
                )}
            </CollapsibleSection>

            <CollapsibleSection title="Cancelled" defaultOpen={false}>
                {ineligiblePRs.length === 0 ? (
                    <p className="text-muted-foreground text-sm py-2">No cancelled reviews</p>
                ) : (
                    ineligiblePRs.map((pr) => (
                        <ReviewPR
                            key={pr.pr_id}
                            pr_id={pr.pr_id}
                            pr_title={pr.pr_title}
                            pr_created_at={pr.pr_created_at}
                            pr_url={pr.pr_url}
                            payout={pr.payout}
                            status="ineligible"
                        />
                    ))
                )}
            </CollapsibleSection>
        </div>
    )
}
