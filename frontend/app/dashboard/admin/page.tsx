import { Card, CardContent, CardHeader, CardDescription, CardTitle } from "@/components/ui/card";
import { Pagination, PaginationContent, PaginationItem, PaginationPrevious, PaginationNext, PaginationLink } from "@/components/ui/pagination";
import { Table, TableCaption, TableHeader, TableRow, TableHead, TableBody, TableCell} from "@/components/ui/table";

export default function AdminDashboardPage() {
    return (
        <div className="flex flex-wrap gap-4">
            <Card className="lg:w-1/2">
            <CardContent>
                <Table>
                <TableCaption>A list of recent claimable and paid out PRs.</TableCaption>
                <TableHeader>
                    <TableRow>
                    <TableHead className="w-25">Date</TableHead>
                    <TableHead>Name</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead className="text-right">Payout</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <TableRow>
                    <TableCell className="font-medium">INV001</TableCell>
                    <TableCell>Paid</TableCell>
                    <TableCell>Credit Card</TableCell>
                    <TableCell className="text-right">$250.00</TableCell>
                    </TableRow>
                </TableBody>
                </Table>
            </CardContent>
                <Pagination>
                <PaginationContent>
                    <PaginationItem className="cursor-pointer">
                        <PaginationPrevious/>
                    </PaginationItem>
                    <PaginationItem>
                        <PaginationLink className="opacity-40">
                            1
                        </PaginationLink>
                    </PaginationItem>
                    <PaginationItem className="cursor-pointer">
                        <PaginationNext/>
                    </PaginationItem>
                </PaginationContent>
                </Pagination>
            </Card>
        </div>
    )
}