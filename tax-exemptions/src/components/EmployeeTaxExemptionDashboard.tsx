import React, {useEffect, useState} from 'react';
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {Input} from "@/components/ui/input";
import {Progress} from "@/components/ui/progress";
import {HelpCircle, Send, Trash2, Upload} from "lucide-react";
import {Alert, AlertDescription} from "@/components/ui/alert";
import {Label} from "@/components/ui/label";
import {Tooltip, TooltipContent, TooltipProvider, TooltipTrigger,} from "@/components/ui/tooltip";
import {useFrappeFileUpload, useFrappeGetDoc, useFrappeGetDocList, useFrappeUpdateDoc} from "frappe-react-sdk";
import {AddExemptionDialog, EmployeeTaxExemptionDeclarationCategory} from "@/components/AddExemptionDialog.tsx";
import {NotEmployee} from "@/components/NotEmployee.tsx";

interface Employee {
    name: string
}

interface EmployeeTaxExemptionDeclaration {
    name: string
    employee: string
    declarations: EmployeeTaxExemptionDeclarationCategory[]
}

export const EmployeeTaxExemptionDashboard = () => {
    const [declarationCategories, setDeclarationCategories] = useState<EmployeeTaxExemptionDeclarationCategory[]>([]);
    const [totalSavings, setTotalSavings] = useState(0); // Example value

    const {upload: uploadFile} = useFrappeFileUpload()
    const {data: employees} = useFrappeGetDocList<Employee>('Employee', {
        fields: ["*"],
        filters: window.frappe?.session?.user ? [['user_id', '=', window.frappe?.session?.user]] : []
    })
    const {data: taxDeclarations} = useFrappeGetDocList<EmployeeTaxExemptionDeclaration>('Employee Tax Exemption Declaration', {
        filters: [['employee', '=', employees?.[0]?.name || '']]
    })
    const {
        data: taxDeclaration,
        mutate: refetchTaxDeclaration
    } = useFrappeGetDoc<EmployeeTaxExemptionDeclaration>('Employee Tax Exemption Declaration', taxDeclarations?.[0]?.name)

    const {updateDoc} = useFrappeUpdateDoc<EmployeeTaxExemptionDeclaration>()

    useEffect(() => {
        setTotalSavings(declarationCategories.map(exemption => Math.min(exemption.amount, exemption.max_amount)).reduce((a, b) => a + b, 0))
    }, [declarationCategories])

    useEffect(() => {
        setDeclarationCategories(taxDeclaration?.declarations?.map((d, i) => {
            return {
                ...d,
                id: i
            }
        }) || [])
    }, [taxDeclaration]);

    const handleAddExemption = (newExemption: EmployeeTaxExemptionDeclarationCategory) => {
        setDeclarationCategories([...declarationCategories, {
            ...newExemption,
            id: Math.max(...declarationCategories.map(exemption => exemption.id), 0) + 1
        }]);
    };

    const handleSubmit = async () => {
        if (!taxDeclaration)
            return
        const response = await updateDoc('Employee Tax Exemption Declaration', taxDeclaration.name, {
            ...taxDeclaration,
            declarations: declarationCategories
        })
        await refetchTaxDeclaration()
        console.log(response)
    };

    // const handleEdit = (name: number) => {
    //     console.log(`Editing exemption with name: ${name}`);
    //     // Implement edit logic here
    // };

    const handleDelete = (id: number) => {
        setDeclarationCategories(declarationCategories.filter(exemption => exemption.id !== id));
    };

    const handleAmountChange = (id: number, amount: string) => {
        setDeclarationCategories(declarationCategories.map(exemption =>
            exemption.id === id ? {...exemption, amount: parseInt(amount) || 0} : exemption
        ));
    };

    const handleProofUpload = async (id: number, event: React.ChangeEvent<HTMLInputElement>) => {
        const files = event.target.files
        const firstFile = files?.item(0)
        if (!firstFile)
            return
        const uploadedFile = await uploadFile(firstFile, {})
        setDeclarationCategories(declarationCategories.map(exemption =>
            exemption.id === id ? {...exemption, proofUrl: uploadedFile.file_url} : exemption
        ));
    };

    if (!employees?.length)
        return <NotEmployee/>

    return (
        <div className="md:p-4 max-w-4xl mx-auto">
            <h1 className="text-2xl font-bold mb-6">Tax Exemption Declaration</h1>

            <div className="flex justify-between items-center mb-6">
                <AddExemptionDialog onAdd={handleAddExemption}/>
                <Button onClick={handleSubmit} className="bg-green-600 hover:bg-green-700 text-xs md:text-sm">
                    <Send className="mr-2 h-4 w-4"/> Submit Declarations
                </Button>
            </div>

            <Alert className="mb-6">
                <AlertDescription>
                    Your estimated tax savings: ₹{totalSavings.toLocaleString()}
                    <TooltipProvider>
                        <Tooltip>
                            <TooltipTrigger asChild>
                                <HelpCircle className="inline-block ml-2 h-4 w-4 cursor-help"/>
                            </TooltipTrigger>
                            <TooltipContent>
                                <p>This is an estimate based on your current declarations.</p>
                            </TooltipContent>
                        </Tooltip>
                    </TooltipProvider>
                </AlertDescription>
            </Alert>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {declarationCategories.map((exemption) => (
                    <Card key={exemption.id}>
                        <CardHeader className='pb-1'>
                            <CardTitle className="text-lg">{exemption.exemption_sub_category}</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-sm text-muted-foreground mb-6">
                                Category: {exemption.exemption_category}
                            </p>
                            <div className="flex justify-between items-center mb-2">
                                <span className="text-sm font-medium">Maximum Exempted:</span>
                                <span>₹{exemption.max_amount.toLocaleString()}</span>
                            </div>
                            <div className="flex items-center mb-2">
                                <span className="text-sm font-medium mr-2">Declared Amount:</span>
                                <Input
                                    type="number"
                                    value={exemption.amount}
                                    onChange={(e) => handleAmountChange(exemption.id, e.target.value)}
                                    className="max-w-[120px]"
                                />
                            </div>
                            <Progress
                                value={(Math.min(exemption.amount, exemption.max_amount) / exemption.max_amount) * 100}
                                className="mb-2"
                            />
                            <div className="flex items-center justify-between mb-2">
                                <Label htmlFor={`proof-upload-${exemption.id}`} className="cursor-pointer">
                                    <div className="flex items-center">
                                        <Upload className="h-4 w-4 mr-2"/>
                                        <span className="text-sm">Upload Proof</span>
                                    </div>
                                </Label>
                                <Input
                                    id={`proof-upload-${exemption.id}`}
                                    type="file"
                                    className="hidden"
                                    onChange={(e) => handleProofUpload(exemption.id, e)}
                                />
                                {exemption.proofUrl ? (
                                    <span className="text-green-600 text-sm">✓ Proof Submitted</span>
                                ) : (
                                    <span className="text-red-600 text-sm">Proof Required</span>
                                )}
                            </div>
                            <div className="flex justify-end space-x-2">
                                {/*<Button variant="outline" size="sm" onClick={() => handleEdit(exemption.id)}>*/}
                                {/*    <Edit2 className="h-4 w-4"/>*/}
                                {/*</Button>*/}
                                <Button variant="outline" size="sm" onClick={() => handleDelete(exemption.id)}>
                                    <Trash2 className="h-4 w-4"/>
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
};
