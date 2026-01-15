import { GitBranch } from "lucide-react";
import { Button } from "../ui/button";
import { Card, CardAction, CardDescription, CardHeader, CardTitle } from "../ui/card";

export default function ReviewPR(){
    return (
        <Card className="w-full bg-sky-300/20">
            <CardHeader>
                <CardTitle>PR Title</CardTitle>
                <CardDescription>PR Description</CardDescription>
                <CardAction>
                    <Button variant="outline">
                        <GitBranch />
                        View on GitHub
                    </Button>
                </CardAction>
            </CardHeader>
        </Card>
    )
}