import { Card, CardAction, CardDescription, CardHeader, CardTitle } from "../ui/card";
import ClaimButton from "../claimButton";

export default function ClaimPR(){
    return (
        <Card className="w-full bg-green-300/20">
            <CardHeader>
                <CardTitle>PR Title</CardTitle>
                <CardDescription>PR Date</CardDescription>
                <CardAction>
                    <ClaimButton />
                </CardAction>
            </CardHeader>
        </Card>
    )
}