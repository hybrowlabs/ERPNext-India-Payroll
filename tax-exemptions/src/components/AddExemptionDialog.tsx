import React, {useEffect, useState} from "react";
import {useFrappeGetDocList} from "frappe-react-sdk";
import {Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger} from "@/components/ui/dialog.tsx";
import {Button} from "@/components/ui/button.tsx";
import {PlusCircle} from "lucide-react";
import {Label} from "@/components/ui/label.tsx";
import {Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select.tsx";
import {Input} from "@/components/ui/input.tsx";


export interface EmployeeTaxExemptionCategory {
    max_amount: number
    name: string
    is_active: boolean
}

export interface EmployeeTaxExemptionSubCategory {
    max_amount: number
    exemption_category: string
    name: string
    is_active: boolean
}

export interface EmployeeTaxExemptionDeclarationCategory {
    id: number;
    exemption_sub_category: string;
    exemption_category: string;
    max_amount: number;
    amount: number;
    proofUrl: string;
}

export interface AddExemptionDialogProps {
    onAdd: (newExemption: EmployeeTaxExemptionDeclarationCategory) => void;
}

export const AddExemptionDialog = ({onAdd}: AddExemptionDialogProps) => {
    const [isOpen, setIsOpen] = useState(false)
    const [newExemption, setNewExemption] = useState<EmployeeTaxExemptionDeclarationCategory>({
        id: 0,
        exemption_sub_category: '',
        exemption_category: '',
        max_amount: 0,
        amount: 0,
        proofUrl: ''
    });

    const {data: categories} = useFrappeGetDocList<EmployeeTaxExemptionCategory>('Employee Tax Exemption Category', {
        fields: ["*"]
    })
    const {data: subCategories} = useFrappeGetDocList<EmployeeTaxExemptionSubCategory>('Employee Tax Exemption Sub Category', {
        fields: ["*"]
    })

    useEffect(() => {
        if (!newExemption.exemption_sub_category)
            return
        const allowedSubCategories = subCategories?.filter(subCategory => subCategory.exemption_category === newExemption.exemption_category)?.map(subCategory => subCategory.name) ?? []
        if (!allowedSubCategories.includes(newExemption.exemption_sub_category)) {
            setNewExemption({
                ...newExemption,
                exemption_sub_category: ''
            })
        }
    }, [newExemption, subCategories])

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setNewExemption({...newExemption, [e.target.name]: e.target.value});
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!newExemption.exemption_category || !newExemption.exemption_sub_category || !newExemption.max_amount || !newExemption.amount)
            return
        onAdd(newExemption);
        setIsOpen(false)
        setNewExemption({
            id: 0,
            exemption_sub_category: '',
            exemption_category: '',
            max_amount: 0,
            amount: 0,
            proofUrl: ''
        })
    };

    return (
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
            <DialogTrigger asChild>
                <Button variant="outline" className='text-xs md:text-sm'>
                    <PlusCircle className="mr-2 h-4 w-4"/> Add New Exemption
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Add New Exemption</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <Label>Exemption Category</Label>
                        <Select
                            value={newExemption.exemption_category}
                            onValueChange={(value) => setNewExemption({...newExemption, exemption_category: value})}
                            required
                        >
                            <SelectTrigger className='mt-1'>
                                <SelectValue placeholder="Select Category"/>
                            </SelectTrigger>
                            <SelectContent>
                                <SelectGroup>
                                    {categories?.map(category => {
                                        return <SelectItem key={category.name} value={category.name}>
                                            {category.name}
                                        </SelectItem>
                                    })}
                                </SelectGroup>
                            </SelectContent>
                        </Select>
                    </div>
                    {newExemption.exemption_category &&
                        <div>
                            <Label htmlFor="category">Exemption Sub Category</Label>
                            <Select
                                value={newExemption.exemption_sub_category}
                                onValueChange={(value) => {
                                    setNewExemption({
                                        ...newExemption,
                                        exemption_sub_category: value,
                                        max_amount: subCategories?.find(subCategory => subCategory.name === value)?.max_amount || 0
                                    })
                                }}
                                required
                            >
                                <SelectTrigger className='mt-1'>
                                    <SelectValue placeholder="Select Sub Category"/>
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectGroup>
                                        {subCategories?.filter(subCategory => subCategory.exemption_category === newExemption.exemption_category)?.map(subCategory => {
                                            return <SelectItem key={subCategory.name}
                                                               value={subCategory.name}>{subCategory.name}</SelectItem>
                                        })}
                                    </SelectGroup>
                                </SelectContent>
                            </Select>
                        </div>
                    }
                    <div>
                        <Label htmlFor="maxAmount">Maximum Exempted Amount</Label>
                        <Input
                            className='mt-1'
                            id="maxAmount"
                            name="max_amount"
                            type="number"
                            value={Number(newExemption.max_amount) ? newExemption.max_amount.toString() : ''}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div>
                        <Label htmlFor="declaredAmount">Declared Amount</Label>
                        <Input
                            className='mt-1'
                            id="declaredAmount"
                            name="amount"
                            type="number"
                            value={newExemption.amount ? newExemption.amount.toString() : ''}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <Button type="submit">Add Exemption</Button>
                </form>
            </DialogContent>
        </Dialog>
    );
};
