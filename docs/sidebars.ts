import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebars: SidebarsConfig = {
  mainSidebar: [
    {
      type: "doc",
      id: "index",
      label: "Introduction",
    },
    {
      type: "doc",
      id: "installation",
      label: "Installation",
    },
    {
      type: "doc",
      id: "configuration",
      label: "Initial Configuration",
    },
    {
      type: "category",
      label: "Payroll",
      collapsed: false,
      items: [
        "payroll/processing",
        "payroll/salary-structure",
        "payroll/lop-attendance",
        "payroll/loans",
        "payroll/full-and-final",
      ],
    },
    {
      type: "category",
      label: "Compliance",
      collapsed: false,
      items: [
        "compliance/epf",
        "compliance/esic",
        "compliance/professional-tax",
        "compliance/tds",
        "compliance/tax-declaration",
        "compliance/form-16",
      ],
    },
    {
      type: "category",
      label: "Reports",
      collapsed: true,
      items: [
        "reports/overview",
        "reports/epf-challan",
        "reports/salary-book",
        "reports/bank-mandate",
        "reports/tds-register",
        "reports/monthly-mis",
      ],
    },
    {
      type: "category",
      label: "Reference",
      collapsed: true,
      items: [
        "reference/architecture",
        "reference/custom-fields",
        "reference/api",
      ],
    },
  ],
};

export default sidebars;
