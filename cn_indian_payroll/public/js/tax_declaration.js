const DECLARATION_FORM = {
  "display": "form",
  "components": [
    {
      "label": "Table",
      "cellAlignment": "left",
      "bordered": true,
      "key": "table",
      "conditional": {
        "eq": "0"
      },
      "type": "table",
      "numRows": 8,
      "numCols": 6,
      "input": false,
      "tableView": false,
      "rows": [
        [
          {
            "components": [
              {
                "html": "<p>Sl No.</p>",
                "label": "Sl No",
                "refreshOnChange": false,
                "key": "slNo",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Invested Description</p>",
                "label": "Investment Description",
                "refreshOnChange": false,
                "key": "investmentDescription",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Maximum Limit</p>",
                "label": "Maximum Limit",
                "refreshOnChange": false,
                "key": "maximumLimit",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Section</p>",
                "label": "Section",
                "refreshOnChange": false,
                "key": "section",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Narration</p>",
                "label": "Narration",
                "refreshOnChange": false,
                "key": "narration",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Amount</p>",
                "label": "Amount",
                "refreshOnChange": false,
                "key": "amount2",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          }
        ],
        [
          {
            "components": [
              {
                "html": "<p>1</p>",
                "label": "One",
                "refreshOnChange": false,
                "key": "one",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Mediclaim Self, Spouse & Children (Below 60 years)</p>",
                "label": "Mediclaim Self, Spouse & Children (Below 60 years)",
                "refreshOnChange": false,
                "key": "mediclaimPremium1",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>25000</p>",
                "label": "25000",
                "refreshOnChange": false,
                "key": "m_value",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>80-D</p>",
                "label": "80D",
                "refreshOnChange": false,
                "key": "D",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Mediclaim</p>",
                "label": "Mediclaim Premium",
                "refreshOnChange": false,
                "key": "mediclaimPremium",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "label": "mp_amount1",
                "applyMaskOn": "change",
                "hideLabel": true,
                "mask": false,
                "tableView": false,
                "delimiter": false,
                "requireDecimal": false,
                "inputFormat": "plain",
                "truncateMultipleSpaces": false,
                "calculateValue": "if (data.amount>25000){\n  value = 0;\n} ",
                "validateWhenHidden": false,

                "validateWhenHidden": false,
                "key": "amount",
                "type": "number",
                "input": true,
                "defaultValue": 0,
                
              }
            ]
          }
        ],
        [
          {
            "components": []
          },
          {
            "components": [
              {
                "html": "<p>&nbsp;Mediclaim Self (Senior Citizen - 60 years & above)</p>",
                "label": " Mediclaim Self (Senior Citizen - 60 years & above)",
                "refreshOnChange": false,
                "key": "aDeductionUS80DPaidForParents",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">50000</span></p>",
                "label": "50000",
                "refreshOnChange": false,
                "key": "m1_value",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">80-D</span></p>",
                "label": "80-D",
                "refreshOnChange": false,
                "key": "D1",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Mediclaim</p>",
                "label": "Mediclaim2",
                "refreshOnChange": false,
                "key": "mediclaim2",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "label": "mp_amount2",
                "applyMaskOn": "change",
                "hideLabel": true,
                "mask": false,
                "tableView": false,
                "defaultValue": 0,
                "delimiter": false,
                "requireDecimal": false,
                "inputFormat": "plain",
                "truncateMultipleSpaces": false,
                "calculateValue": "if (data.amount3>50000){\n  value = 0;\n} ",
                "validateWhenHidden": false,
                "validateWhenHidden": false,
                "key": "amount3",
                "type": "number",
                "input": true
              }
            ]
          }
        ],
        [
          {
            "components": []
          },
          {
            "components": [
              {
                "html": "<p>Parents (Below 60 years)</p>",
                "label": "Parents (Below 60 years)",
                "refreshOnChange": false,
                "key": "mediclaimPolicyForSelfSpouseChildren",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>25000</p>",
                "label": "p_amount",
                "refreshOnChange": false,
                "key": "pAmount",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>80-D</p>",
                "label": "80d3",
                "refreshOnChange": false,
                "key": "D3",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Mediclaim</p>",
                "label": "Mediclaim4",
                "refreshOnChange": false,
                "key": "mediclaim4",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "label": "mp_amount3",
                "applyMaskOn": "change",
                "hideLabel": true,
                "mask": false,
                "tableView": false,
                "defaultValue": 0,
                "delimiter": false,
                "requireDecimal": false,
                "inputFormat": "plain",
                "truncateMultipleSpaces": false,
                "calculateValue": "if (data.mpAmount3>25000){\n  value = 0;\n} ",
                "validateWhenHidden": false,
                
                "validateWhenHidden": false,
                "key": "mpAmount3",
                "type": "number",
                "input": true
              }
            ]
          }
        ],
        [
          {
            "components": []
          },
          {
            "components": [
              {
                "html": "<p>Parents (Senior Citizen - 60 years & above)</p>",
                "label": "Parents (Senior Citizen - 60 years & above)",
                "refreshOnChange": false,
                "key": "mediclaimPolicyForParentsForSeniorCitizen",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>50000</p>",
                "label": "max_amount_4",
                "refreshOnChange": false,
                "key": "maxAmount4",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>80-D</p>",
                "label": "80d_4",
                "refreshOnChange": false,
                "key": "D4",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Mediclaim</p>",
                "label": "Mediclaim4",
                "refreshOnChange": false,
                "key": "mediclaim5",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "label": "mp_amount4",
                "applyMaskOn": "change",
                "hideLabel": true,
                "mask": false,
                "tableView": false,
                "defaultValue": 0,
                "delimiter": false,
                "requireDecimal": false,
                "inputFormat": "plain",
                "truncateMultipleSpaces": false,
                "validateWhenHidden": false,
                "key": "mpAmount4",
                "type": "number",
                "input": true,
                "calculateValue": "if (data.mpAmount4>50000){\n  value = 0;\n} ",
                "validateWhenHidden": false,
              }
            ]
          }
        ],
        [
          {
            "components": []
          },
          {
            "components": [
              {
                "html": "<p>Preventive Health Check-up for Parents</p>",
                "label": "Preventive Health Check-up for Parents",
                "refreshOnChange": false,
                "key": "preventiveHealthCheckUpForParents",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>5000</p>",
                "label": "5000A",
                "refreshOnChange": false,
                "key": "A",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>80-D</p>",
                "label": "80dA",
                "refreshOnChange": false,
                "key": "DA",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": []
          },
          {
            "components": [
              {
                "label": "mp_amount_5",
                "applyMaskOn": "change",
                "hideLabel": true,
                "mask": false,
                "tableView": false,
                "defaultValue": 0,
                "delimiter": false,
                "requireDecimal": false,
                "inputFormat": "plain",
                "truncateMultipleSpaces": false,
                "validateWhenHidden": false,
                "key": "mp5",
                "type": "number",
                "input": true,
                "calculateValue": "if (data.mp5>5000){\n  value = 0;\n} ",
                "validateWhenHidden": false,
              }
            ]
          }
        ],
        [
          {
            "components": []
          },
          {
            "components": [
              {
                "html": "<p>Preventive Health Check-up</p>",
                "label": "Preventive Health Check-up",
                "refreshOnChange": false,
                "key": "preventiveHealthCheckUp",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>5000</p>",
                "label": "5000B",
                "refreshOnChange": false,
                "key": "B",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>80-D</p>",
                "label": "80db",
                "refreshOnChange": false,
                "key": "Db",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": []
          },
          {
            "components": [
              {
                "label": "mp_amount_6",
                "applyMaskOn": "change",
                "hideLabel": true,
                "mask": false,
                "tableView": false,
                "defaultValue": 0,
                "delimiter": false,
                "requireDecimal": false,
                "inputFormat": "plain",
                "truncateMultipleSpaces": false,
                "validateWhenHidden": false,
                "key": "mpAmount6",
                "type": "number",
                "input": true,
                "calculateValue": "if (data.mpAmount6>5000){\n  value = 0;\n} ",
                "validateWhenHidden": false,
              }
            ]
          }
        ],
        [
          {
            "components": [
              {
                "html": "<p>2</p>",
                "label": "Two",
                "refreshOnChange": false,
                "key": "two",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Interest Paid On Housing Loan</p>",
                "label": "Interest Paid On Housing Loan",
                "refreshOnChange": false,
                "key": "interestPaidOnHousingLoan1",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">200000</span></p>",
                "label": "200000",
                "refreshOnChange": false,
                "key": "hl_value",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Section 24(b)</p>",
                "label": "Section 24(b)",
                "refreshOnChange": false,
                "key": "hl_section",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "html": "<p>Interest Paid On Housing Loan</p>",
                "label": "nterest Paid On Housing Loan",
                "refreshOnChange": false,
                "key": "nterestPaidOnHousingLoan",
                "type": "content",
                "input": false,
                "tableView": false
              }
            ]
          },
          {
            "components": [
              {
                "label": "hl_amount",
                "applyMaskOn": "change",
                "hideLabel": true,
                "mask": false,
                "tableView": false,
                "defaultValue": 0,
                "delimiter": false,
                "requireDecimal": false,
                "inputFormat": "plain",
                "truncateMultipleSpaces": false,
                "validateWhenHidden": false,
                "key": "hlAmount",
                "type": "number",
                "input": true,
                "calculateValue": "if (data.hlAmount>200000){\n  value = 0;\n} ",
                "validateWhenHidden": false,
              }
            ]
          }
        ]
      ]
    },
    {
      "label": "Table2",
      "cellAlignment": "left",
      "bordered": true,
      "key": "table2",
      "type": "table",
      "numRows": 1,
      "input": false,
      "tableView": false,
      "rows": [
        [
          {
            "components": [
              {
                "html": "<p>Lender</p>",
                "label": "Lender",
                "refreshOnChange": false,
                "key": "lender",
                "type": "content",
                "input": false,
                "tableView": false
              },
              {
                "label": "Table",
                "cellAlignment": "left",
                "bordered": true,
                "key": "table1",
                "type": "table",
                "numCols": 4,
                "input": false,
                "tableView": false,
                "rows": [
                  [
                    {
                      "components": [
                        {
                          "html": "<p>Name</p>",
                          "label": "Name",
                          "refreshOnChange": false,
                          "key": "name",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "Name Value",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "tableView": true,
                          "validateWhenHidden": false,
                          "key": "nameValue",
                          "type": "textfield",
                          "input": true
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Address Title1</p>",
                          "label": "Address Title1",
                          "refreshOnChange": false,
                          "key": "addressTitle1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "Address_one_value",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "tableView": true,
                          "validateWhenHidden": false,
                          "key": "addressoneValue",
                          "type": "textfield",
                          "input": true
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>PAN</p>",
                          "label": "PAN",
                          "refreshOnChange": false,
                          "key": "pan",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "Pan value",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "tableView": true,
                          "validateWhenHidden": false,
                          "key": "panValue",
                          "type": "textfield",
                          "input": true
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Address Title2</p>",
                          "label": "Address Title2",
                          "refreshOnChange": false,
                          "key": "addressTitle2",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "address_two_value",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "tableView": true,
                          "validateWhenHidden": false,
                          "key": "addresstwoValue",
                          "type": "textfield",
                          "input": true
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>Type</p>",
                          "label": "Type",
                          "refreshOnChange": false,
                          "key": "type",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "Type Value",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "tableView": true,
                          "validateWhenHidden": false,
                          "key": "typeValue",
                          "type": "textfield",
                          "input": true
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Address Title3</p>",
                          "label": "Address Title3",
                          "refreshOnChange": false,
                          "key": "addressTitle3",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "address_three_value",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "tableView": true,
                          "validateWhenHidden": false,
                          "key": "addressThreeValue",
                          "type": "textfield",
                          "input": true
                        }
                      ]
                    }
                  ]
                ]
              },
              {
                "label": "Table",
                "cellAlignment": "left",
                "bordered": true,
                "key": "table3",
                "type": "table",
                "numRows": 1,
                "numCols": 2,
                "input": false,
                "tableView": false,
                "rows": [
                  [
                    {
                      "components": [
                        {
                          "html": "<p>3</p>",
                          "label": "three",
                          "refreshOnChange": false,
                          "key": "three",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Investment Under Section 80 C &nbsp; Overall Limit Of Rs. 1.5 Lakh</p>",
                          "label": "Investment Under Section 80 C",
                          "refreshOnChange": false,
                          "key": "investmentUnderSection80C",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    }
                  ]
                ]
              },
              {
                "label": "Table",
                "cellAlignment": "left",
                "bordered": true,
                "key": "table4",
                "type": "table",
                "numRows": 13,
                "numCols": 6,
                "input": false,
                "tableView": false,
                "rows": [
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Investments In PF(Auto)</p>",
                          "label": "Investments In PF(Auto)\t",
                          "refreshOnChange": false,
                          "key": "investmentsInPf",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "150000",
                          "refreshOnChange": false,
                          "key": "max_amount1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">80-C</span></p>",
                          "label": "80-C",
                          "refreshOnChange": false,
                          "key": "C",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "label": "pf_value",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "pfValue",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0,
                          "disabled": true,
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">(A) Pension Scheme Investments &amp; ULIP</span></p>",
                          "label": "(A) Pension Scheme Investments & ULIP",
                          "refreshOnChange": false,
                          "key": "aPensionSchemeInvestmentsUlip",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "150000",
                          "refreshOnChange": false,
                          "key": "max_amount2",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80-CCC&nbsp;</p>",
                          "label": "80-CCC\t",
                          "refreshOnChange": false,
                          "key": "Ccc",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Pension Scheme Investments &amp; ULIP</p>",
                          "label": "Pension Scheme Investments & ULIP",
                          "refreshOnChange": false,
                          "key": "pensionSchemeInvestmentsUlip1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "a_value_1",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "aValue2",
                          "type": "number",
                          "input": true
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">(B) Housing Loan Principal Repayment</span></p>",
                          "label": "(B) Housing Loan Principal Repayment",
                          "refreshOnChange": false,
                          "key": "bHousingLoanPrincipalRepayment",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "150000",
                          "refreshOnChange": false,
                          "key": "max_amount3",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">80-C</span></p>",
                          "label": "80-C",
                          "refreshOnChange": false,
                          "key": "80-C_3",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Housing Loan Principal Repayment</p>",
                          "label": "Housing Loan Principal Repayment",
                          "refreshOnChange": false,
                          "key": "housingLoanPrincipalRepayment",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "b_value_1",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "bValue1",
                          "type": "number",
                          "input": true
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">(C) PPF - Public Provident Fund</span></p>",
                          "label": "(C) PPF - Public Provident Fund",
                          "refreshOnChange": false,
                          "key": "cPpfPublicProvidentFund",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "150000",
                          "refreshOnChange": false,
                          "key": "max_value4",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80-C</p>",
                          "label": "80-C\t",
                          "refreshOnChange": false,
                          "key": "80-C_4",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>PPF</p>",
                          "label": "PPF",
                          "refreshOnChange": false,
                          "key": "ppf",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "c_value_1",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          
                          "validateWhenHidden": false,
                          "key": "amount4",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p>(D) Home Loan Account Of National Housing Bank&nbsp;</p>",
                          "label": "(D) Home Loan Account Of National Housing Bank\t",
                          "refreshOnChange": false,
                          "key": "dHomeLoanAccountOfNationalHousingBank",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "max_value5",
                          "refreshOnChange": false,
                          "key": "maxValue5",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80-C</p>",
                          "label": "80-C",
                          "refreshOnChange": false,
                          "key": "C1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Home Loan Account Of National Housing Bank</p>",
                          "label": "Home Loan Account Of National Housing Bank",
                          "refreshOnChange": false,
                          "key": "homeLoanAccountOfNationalHousingBank",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "d_value1",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          
                          "validateWhenHidden": false,
                          "key": "dValue1",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">(E) LIC- Life Insurance Premium Directly Paid By Employee</span></p>",
                          "label": "(E) LIC- Life Insurance Premium Directly Paid By Employee",
                          "refreshOnChange": false,
                          "key": "eLicLifeInsurancePremiumDirectlyPaidByEmployee",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "max_value6",
                          "refreshOnChange": false,
                          "key": "maxValue6",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80-C</p>",
                          "label": "80-C",
                          "refreshOnChange": false,
                          "key": "80-C_6",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>LIC</p>",
                          "label": "LIC",
                          "refreshOnChange": false,
                          "key": "lic",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "e_value_1",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          
                          "validateWhenHidden": false,
                          "key": "eValue1",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p>(F) NSC - National Saving Certificate&nbsp;</p>",
                          "label": "(F) NSC - National Saving Certificate\t",
                          "refreshOnChange": false,
                          "key": "fNscNationalSavingCertificate",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "max_value7",
                          "refreshOnChange": false,
                          "key": "maxValue7",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80-C</p>",
                          "label": "80-C",
                          "refreshOnChange": false,
                          "key": "80-C_7",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>NSC</p>",
                          "label": "NSC",
                          "refreshOnChange": false,
                          "key": "nsc",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "f_value1",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "fValue1",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p>(G) Mutual Funds - Notified Under Clause 23D Of Section 10&nbsp;</p>",
                          "label": "(G) Mutual Funds - Notified Under Clause 23D Of Section 10\t",
                          "refreshOnChange": false,
                          "key": "gMutualFundsNotifiedUnderClause23DOfSection10",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "max_value8",
                          "refreshOnChange": false,
                          "key": "maxValue8",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80-C</p>",
                          "label": "80-C",
                          "refreshOnChange": false,
                          "key": "80-C_8",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Mutual Funds</p>",
                          "label": "Mutual Funds",
                          "refreshOnChange": false,
                          "key": "mutualFunds",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "g_value1",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "gValue1",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p>(H) ELSS - Equity Link Saving Scheme Of Mutual Funds&nbsp;</p>",
                          "label": "(H) ELSS - Equity Link Saving Scheme Of Mutual Funds\t",
                          "refreshOnChange": false,
                          "key": "hElssEquityLinkSavingSchemeOfMutualFunds",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "max_value9",
                          "refreshOnChange": false,
                          "key": "maxValue9",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80-C</p>",
                          "label": "80-C",
                          "refreshOnChange": false,
                          "key": "80-C_9",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>ELSS - Equity Link Saving Scheme Of Mutual Funds</p>",
                          "label": "ELSS - Equity Link Saving Scheme Of Mutual Funds",
                          "refreshOnChange": false,
                          "key": "elssEquityLinkSavingSchemeOfMutualFunds",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "h_value1",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "hValue1",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p>(I) Tuition Fees For Full Time Education&nbsp;</p>",
                          "label": "(I) Tuition Fees For Full Time Education\t",
                          "refreshOnChange": false,
                          "key": "iTuitionFeesForFullTimeEducation",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "max_value10",
                          "refreshOnChange": false,
                          "key": "maxValue10",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80-C</p>",
                          "label": "80-C",
                          "refreshOnChange": false,
                          "key": "80-C_9",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Tuition Fees For Full Time Education</p>",
                          "label": "Tuition Fees For Full Time Education",
                          "refreshOnChange": false,
                          "key": "tuitionFeesForFullTimeEducation",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "i_value1",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "iValue1",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p>(J) Fixed Deposits In Banks (Period As Per Income Tax Guidelines)&nbsp;</p>",
                          "label": "(J) Fixed Deposits In Banks (Period As Per Income Tax Guidelines)\t",
                          "refreshOnChange": false,
                          "key": "jFixedDepositsInBanksPeriodAsPerIncomeTaxGuidelines",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "max_value11",
                          "refreshOnChange": false,
                          "key": "maxValue11",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80-C</p>",
                          "label": "80-C",
                          "refreshOnChange": false,
                          "key": "80-C_10",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Fixed Deposits In Banks</p>",
                          "label": "Fixed Deposits In Banks",
                          "refreshOnChange": false,
                          "key": "fixedDepositsInBanks",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "j_value1",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "jValue1",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p>(K) 5 Years Term Deposit An Account Under Post Office Term Deposit Rules&nbsp;</p>",
                          "label": "(K) 5 Years Term Deposit An Account Under Post Office Term Deposit Rules\t",
                          "refreshOnChange": false,
                          "key": "k5YearsTermDepositAnAccountUnderPostOfficeTermDepositRules",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "max_value12",
                          "refreshOnChange": false,
                          "key": "maxValue12",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80-C</p>",
                          "label": "80-C",
                          "refreshOnChange": false,
                          "key": "80-C_11",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>5 Years Term Deposit An Account Under Post Office</p>",
                          "label": "5 Years Term Deposit An Account Under Post Office",
                          "refreshOnChange": false,
                          "key": "YearsTermDepositAnAccountUnderPostOffice",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "k_value1",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "kValue1",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p>(L) Others&nbsp;</p>",
                          "label": "(L) Others\t",
                          "refreshOnChange": false,
                          "key": "lOthers",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80-C</p>",
                          "label": "80-C",
                          "refreshOnChange": false,
                          "key": "80-C_12",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Others</p>",
                          "label": "Others",
                          "refreshOnChange": false,
                          "key": "others",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "label": "l_value1",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "kValue2",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ]
                ]
              },
              {
                "label": "total_value",
                "cellAlignment": "center",
                "bordered": true,
                "key": "totalValue",
                "type": "table",
                "numRows": 1,
                "numCols": 2,
                "input": false,
                "tableView": false,
                "rows": [
                  [
                    {
                      "components": [
                        {
                          "html": "<p>Total 80-C</p>",
                          "label": "Total 80-C",
                          "refreshOnChange": false,
                          "key": "total80C1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "Total_80c",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "total80C",
                          "type": "number",
                          "input": true
                        }
                      ]
                    }
                  ]
                ]
              },
              {
                "label": "Table",
                "cellAlignment": "left",
                "bordered": true,
                "key": "table5",
                "type": "table",
                "numRows": 8,
                "numCols": 6,
                "input": false,
                "tableView": false,
                "rows": [
                  [
                    {
                      "components": [
                        {
                          "html": "<p>4</p>",
                          "label": "four",
                          "refreshOnChange": false,
                          "key": "four",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">(Medical treatment / insurance of handicapped dependant)</span></p>",
                          "label": "(Medical treatment / insurance of handicapped dependant)",
                          "refreshOnChange": false,
                          "key": "medicalTreatmentInsuranceOfHandicappedDependant",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">75000</span></p>",
                          "label": "seventyfivethousand",
                          "refreshOnChange": false,
                          "key": "seventyfivethousand",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">80-DD</span></p>",
                          "label": "80-DD",
                          "refreshOnChange": false,
                          "key": "Dd",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80DD</p>",
                          "label": "Deduction U/S 80DD",
                          "refreshOnChange": false,
                          "key": "deductionUS80Dd",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "four_Number",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "fourValue",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0,
                          "calculateValue": "if (data.fourValue>75000){\n  value = 0;\n} ",
                          "validateWhenHidden": false,
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>5</p>",
                          "label": "five",
                          "refreshOnChange": false,
                          "key": "five",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">Medical treatment (specified diseases only)</span></p>",
                          "label": "Medical treatment (specified diseases only)",
                          "refreshOnChange": false,
                          "key": "medicalTreatmentSpecifiedDiseasesOnly",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">40000</span></p>",
                          "label": "fourty_thousand",
                          "refreshOnChange": false,
                          "key": "fourtyThousand",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">80-DDB</span></p>",
                          "label": "80-DDB",
                          "refreshOnChange": false,
                          "key": "Ddb",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80-DDB</p>",
                          "label": "Deduction U/S 80-DDB",
                          "refreshOnChange": false,
                          "key": "deductionUS80Ddb",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "five_Number",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "fiveNumber",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0,
                          "calculateValue": "if (data.fiveNumber>40000){\n  value = 0;\n} ",
                          "validateWhenHidden": false,
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>6</p>",
                          "label": "six",
                          "refreshOnChange": false,
                          "key": "six",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">Interest repayment of Loan for higher education</span></p>",
                          "label": "Interest repayment of Loan for higher education",
                          "refreshOnChange": false,
                          "key": "interestRepaymentOfLoanForHigherEducation",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">80-E</span></p>",
                          "label": "80-E",
                          "refreshOnChange": false,
                          "key": "E",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80-E</p>",
                          "label": "Deduction U/S 80-E",
                          "refreshOnChange": false,
                          "key": "deductionUS80E",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "six_Number",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "sixNumber",
                          "type": "number",
                          "input": true
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>7</p>",
                          "label": "seven",
                          "refreshOnChange": false,
                          "key": "seven",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">Deduction for Physically Disabled</span></p>",
                          "label": "Deduction for Physically Disabled",
                          "refreshOnChange": false,
                          "key": "deductionForPhysicallyDisabled",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">75000</span></p>",
                          "label": "seventyfive_thousand1",
                          "refreshOnChange": false,
                          "key": "seventyfiveThousand1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80-U</p>",
                          "label": "80-U\t",
                          "refreshOnChange": false,
                          "key": "U",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80-U</p>",
                          "label": "Deduction U/S 80-U",
                          "refreshOnChange": false,
                          "key": "deductionUS80U",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "seven_Number",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "sevenNumber",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0,
                          "calculateValue": "if (data.sevenNumber>75000){\n  value = 0;\n} ",
                          "validateWhenHidden": false,
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>8</p>",
                          "label": "eight",
                          "refreshOnChange": false,
                          "key": "eight",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">Donation U/S 80G</span></p>",
                          "label": "Donation U/S 80G",
                          "refreshOnChange": false,
                          "key": "donationUS80G",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">80-G</span></p>",
                          "label": "80-G",
                          "refreshOnChange": false,
                          "key": "G",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80G</p>",
                          "label": "Deduction U/S 80G",
                          "refreshOnChange": false,
                          "key": "deductionUS80G",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "eight_Number",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "eightNumber",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>9</p>",
                          "label": "nine",
                          "refreshOnChange": false,
                          "key": "nine",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">NPS Deduction U/S 80CCD(2)</span></p>",
                          "label": "Deduction U/S 80CCD(2)",
                          "refreshOnChange": false,
                          "key": "deductionUS80Ccd2",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">80-CCD(2)</span></p>",
                          "label": "80-CCD(2)",
                          "refreshOnChange": false,
                          "key": "Ccd2",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80CCD(2)</p>",
                          "label": "Deduction U/S 80CCD(2)",
                          "refreshOnChange": false,
                          "key": "deductionUS80Ccd3",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "nine_Number",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "nineNumber",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0,
                          "disabled":true
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>10</p>",
                          "label": "ten",
                          "refreshOnChange": false,
                          "key": "ten",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">First HSG Loan Interest Ded.(80EE)</span></p>",
                          "label": "First HSG Loan Interest Ded.(80EE)",
                          "refreshOnChange": false,
                          "key": "firstHsgLoanInterestDed80Ee",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">50000</span></p>",
                          "label": "fifty_thousand1",
                          "refreshOnChange": false,
                          "key": "fiftyThousand1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">80-EE</span></p>",
                          "label": "80-EE",
                          "refreshOnChange": false,
                          "key": "Ee",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>First HSG Loan Interest Ded.(80EE)</p>",
                          "label": "First HSG Loan Interest Ded.(80EE)",
                          "refreshOnChange": false,
                          "key": "firstHsgLoanInterestDed80Ee1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "ten_Number",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "tenNumber",
                          "type": "number",
                          "input": true,
                          "calculateValue": "if (data.tenNumber>50000){\n  value = 0;\n} ",
                          "validateWhenHidden": false,
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>11</p>",
                          "label": "eleven",
                          "refreshOnChange": false,
                          "key": "eleven",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">Contribution in National Pension Scheme</span></p>",
                          "label": "Contribution in National Pension Scheme",
                          "refreshOnChange": false,
                          "key": "contributionInNationalPensionScheme",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">50000</span></p>",
                          "label": "fifty_thousand2",
                          "refreshOnChange": false,
                          "key": "fiftyThousand2",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80CCD(1B)</p>",
                          "label": "80CCD(1B)",
                          "refreshOnChange": false,
                          "key": "Ccd1B",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80CCD(1B)</p>",
                          "label": "Deduction U/S 80CCD(1B)",
                          "refreshOnChange": false,
                          "key": "deductionUS80Ccd1B",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "eleven_Number",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "elevenNumber",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0,
                          "calculateValue": "if (data.elevenNumber>50000){\n  value = 0;\n} ",
                          "validateWhenHidden": false,
                        }
                      ]
                    }
                  ]
                ]
              },
              {
                "label": "Table",
                "cellAlignment": "left",
                "bordered": true,
                "key": "table6",
                "type": "table",
                "numRows": 2,
                "input": false,
                "tableView": false,
                "rows": [
                  [
                    {
                      "components": [
                        {
                          "html": "<p>12</p>",
                          "label": "twelve",
                          "refreshOnChange": false,
                          "key": "twelve",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Report Your Additional Income Here to be Taken Into Consideration While Calculating TDS&nbsp;</p>",
                          "label": "Report Your Additional Income Here to be Taken Into Consideration While Calculating TDS\t",
                          "refreshOnChange": false,
                          "key": "reportYourAdditionalIncomeHereToBeTakenIntoConsiderationWhileCalculatingTds",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "twelveNumber",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "twelveNumber",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>13</p>",
                          "label": "thirteen",
                          "refreshOnChange": false,
                          "key": "thirteen",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Report TDS on above Income&nbsp;</p>",
                          "label": "Report TDS on above Income\t",
                          "refreshOnChange": false,
                          "key": "reportTdsOnAboveIncome",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "thirteenNumber",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "thirteenNumber",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ]
                ]
              },
              {
                "label": "Table",
                "cellAlignment": "left",
                "bordered": true,
                "key": "table7",
                "type": "table",
                "numRows": 13,
                "numCols": 6,
                "input": false,
                "tableView": false,
                "rows": [
                  [
                    {
                      "components": [
                        {
                          "html": "<p>14</p>",
                          "label": "fourteen",
                          "refreshOnChange": false,
                          "key": "fourteen",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Tax Incentive for Affordable Housing for Ded U/S 80EEA&nbsp;</p>",
                          "label": "Tax Incentive for Affordable Housing for Ded U/S 80EEA\t",
                          "refreshOnChange": false,
                          "key": "taxIncentiveForAffordableHousingForDedUS80Eea",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "onelakh_fiftythousand1",
                          "refreshOnChange": false,
                          "key": "onelakhFiftythousand1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80EEA&nbsp;</p>",
                          "label": "80EEA",
                          "refreshOnChange": false,
                          "key": "Eea",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80EEA</p>",
                          "label": "Deduction U/S 80EEA",
                          "refreshOnChange": false,
                          "key": "deductionUS80Eea",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "fourteenNumber",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "twelveNumber1",
                          "type": "number",
                          "input": true,
                          "calculateValue": "if (data.twelveNumber1>150000){\n  value = 0;\n} ",
                          "validateWhenHidden": false,
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>15</p>",
                          "label": "fifteen",
                          "refreshOnChange": false,
                          "key": "fifteen",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Tax Incentives for Electric Vehicles for Ded U/S 80EEB&nbsp;</p>",
                          "label": "Tax Incentives for Electric Vehicles for Ded U/S 80EEB\t",
                          "refreshOnChange": false,
                          "key": "taxIncentivesForElectricVehiclesForDedUS80Eeb",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>150000</p>",
                          "label": "one_lakh_fiftythousand2",
                          "refreshOnChange": false,
                          "key": "oneLakhFiftythousand2",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80EEB</p>",
                          "label": "80EEB",
                          "refreshOnChange": false,
                          "key": "Eeb",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80EEB</p>",
                          "label": "Deduction U/S 80EEB",
                          "refreshOnChange": false,
                          "key": "deductionUS80Eeb",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "fifteenNumber",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "fifteenNumber",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0,
                          "calculateValue": "if (data.fifteenNumber>150000){\n  value = 0;\n} ",
                          "validateWhenHidden": false,
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>16</p>",
                          "label": "sixteen",
                          "refreshOnChange": false,
                          "key": "sixteen",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Donations/contribution made to a political party or an electoral trust&nbsp;</p>",
                          "label": "Donations/contribution made to a political party or an electoral trust\t",
                          "refreshOnChange": false,
                          "key": "donationsContributionMadeToAPoliticalPartyOrAnElectoralTrust",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": []
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80GGC</p>",
                          "label": "80GGC",
                          "refreshOnChange": false,
                          "key": "Ggc",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80GGC</p>",
                          "label": "Deduction U/S 80GGC",
                          "refreshOnChange": false,
                          "key": "deductionUS80Ggc",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "sixteenNumber",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "sixteenNumber",
                          "type": "number",
                          "input": true,
                          "defaultValue": 0
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>17</p>",
                          "label": "seventeen",
                          "refreshOnChange": false,
                          "key": "seventeen",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Interest on deposits in saving account for Ded U/S 80TTA&nbsp;</p>",
                          "label": "Interest on deposits in saving account for Ded U/S 80TTA\t",
                          "refreshOnChange": false,
                          "key": "interestOnDepositsInSavingAccountForDedUS80Tta",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">10000</span></p>",
                          "label": "ten_thousand",
                          "refreshOnChange": false,
                          "key": "tenThousand",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80TTA</p>",
                          "label": "80TTA",
                          "refreshOnChange": false,
                          "key": "Tta",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80TTA</p>",
                          "label": "Deduction U/S 80TTA",
                          "refreshOnChange": false,
                          "key": "deductionUS80Tta",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "seventeenNumber",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "seventeenNumber",
                          "type": "number",
                          "input": true,
                          "calculateValue": "if (data.seventeenNumber>10000){\n  value = 0;\n} ",
                          "validateWhenHidden": false,
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>18</p>",
                          "label": "eighteen",
                          "refreshOnChange": false,
                          "key": "eighteen",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Interest on deposits in saving account for Ded U/S 80TTB&nbsp;</p>",
                          "label": "Interest on deposits in saving account for Ded U/S 80TTB\t",
                          "refreshOnChange": false,
                          "key": "interestOnDepositsInSavingAccountForDedUS80Ttb",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>50000</p>",
                          "label": "fifty_thousand",
                          "refreshOnChange": false,
                          "key": "fiftyThousand",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80TTB</p>",
                          "label": "80TTB",
                          "refreshOnChange": false,
                          "key": "Ttb",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80TTB</p>",
                          "label": "Deduction U/S 80TTB",
                          "refreshOnChange": false,
                          "key": "deductionUS80Ttb",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "eighteenNumber",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "eighteenNumber",
                          "type": "number",
                          "input": true,
                          "calculateValue": "if (data.eighteenNumber>50000){\n  value = 0;\n} ",
                          "validateWhenHidden": false,
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>19</p>",
                          "label": "nineteen",
                          "refreshOnChange": false,
                          "key": "nineteen",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>P.T. Paid by employee&nbsp;</p>",
                          "label": "P.T. Paid by employee\t",
                          "refreshOnChange": false,
                          "key": "pTPaidByEmployee",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>2500</p>",
                          "label": "twothousand_fivehundred",
                          "refreshOnChange": false,
                          "key": "twothousandFivehundred",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>16 (iii)&nbsp;</p>",
                          "label": "16 (iii)\t",
                          "refreshOnChange": false,
                          "key": "Iii",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>P.T. Paid by employee</p>",
                          "label": "P.T. Paid by employee",
                          "refreshOnChange": false,
                          "key": "pTPaidByEmployee1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "nineteenNumber",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "nineteenNumber",
                          "type": "number",
                          "input": true,
                          "disabled":true,
                          "calculateValue": "if (data.nineteenNumber>2500){\n  value = 0;\n} ",
                          "validateWhenHidden": false,
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>20</p>",
                          "label": "twenty",
                          "refreshOnChange": false,
                          "key": "twenty",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80GG&nbsp;</p>",
                          "label": "Deduction U/S 80GG\t",
                          "refreshOnChange": false,
                          "key": "deductionUS80Gg",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>60000</p>",
                          "label": "six_thousand",
                          "refreshOnChange": false,
                          "key": "sixThousand",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80GG</p>",
                          "label": "80GG",
                          "refreshOnChange": false,
                          "key": "Gg",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Deduction U/S 80GG</p>",
                          "label": "Deduction U/S 80GG",
                          "refreshOnChange": false,
                          "key": "deductionUS80Gg1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "twentyNumber",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "twentyNumber",
                          "type": "number",
                          "input": true,
                          "calculateValue": "if (data.twentyNumber>60000){\n  value = 0;\n} ",
                          "validateWhenHidden": false,
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>21</p>",
                          "label": "twenty_one",
                          "refreshOnChange": false,
                          "key": "twentyOne",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Rajiv Gandhi Equity Saving Scheme 80CCG&nbsp;</p>",
                          "label": "Rajiv Gandhi Equity Saving Scheme 80CCG\t",
                          "refreshOnChange": false,
                          "key": "rajivGandhiEquitySavingScheme80Ccg",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>25000</p>",
                          "label": "twenty_five_thousand3",
                          "refreshOnChange": false,
                          "key": "twentyFiveThousand3",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>80CCG</p>",
                          "label": "80CCG",
                          "refreshOnChange": false,
                          "key": "Ccg",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Rajiv Gandhi Equity Saving Scheme 80CCG</p>",
                          "label": "Rajiv Gandhi Equity Saving Scheme 80CCG",
                          "refreshOnChange": false,
                          "key": "rajivGandhiEquitySavingScheme80Ccg1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "twentyoneNumber",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "twentyoneNumber",
                          "type": "number",
                          "input": true,
                          "calculateValue": "if (data.twentyoneNumber>25000){\n  value = 0;\n} ",
                          "validateWhenHidden": false,
                        }
                      ]
                    }
                  ],
                  [
                    {
                      "components": [
                        {
                          "html": "<p>22</p>",
                          "label": "twentytwenty",
                          "refreshOnChange": false,
                          "key": "twentytwenty",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Uniform</p>",
                          "label": "Uniform",
                          "refreshOnChange": false,
                          "key": "uniform",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>15000</p>",
                          "label": "fifteen_thousand_uniform",
                          "refreshOnChange": false,
                          "key": "fifteenThousandUniform",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>10(14)</p>",
                          "label": "10(14)",
                          "refreshOnChange": false,
                          "key": "ten_fourteen",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                        "html": "<p>Less : Allowances Exempted U/s 10</p>",
                          "label": "Less : Allowances Exempted U/s 10",
                          "refreshOnChange": false,
                          "key": "u4",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "twenty_four",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "twentyFour",
                          "type": "number",
                          "input": true
                        }
                      ]
                    },

                  ],

                  [
                    {
                      "components": [
                        {
                          "html": "<p>23</p>",
                          "label": "twentythree",
                          "refreshOnChange": false,
                          "key": "twentythree",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Education Allowance</p>",
                          "label": "Education Allowance",
                          "refreshOnChange": false,
                          "key": "education",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>10(14)</p>",
                          "label": "10(14)",
                          "refreshOnChange": false,
                          "key": "ten_fourteen_1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                        "html": "<p>Less : Allowances Exempted U/s 10</p>",
                          "label": "Less : Allowances Exempted U/s 10",
                          "refreshOnChange": false,
                          "key": "u3",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "twenty_five",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "thirteen",
                          "type": "number",
                          "input": true
                        }
                      ]
                    },

                  ],


                  [
                    {
                      "components": [
                        {
                          "html": "<p>24</p>",
                          "label": "twentyfour",
                          "refreshOnChange": false,
                          "key": "twentyfour",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Hostel Allowance</p>",
                          "label": "Hostel Allowance",
                          "refreshOnChange": false,
                          "key": "hostel",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>10(14)</p>",
                          "label": "10(14)",
                          "refreshOnChange": false,
                          "key": "ten_fourteen_2",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                        "html": "<p>Less : Allowances Exempted U/s 10</p>",
                          "label": "Less : Allowances Exempted U/s 10",
                          "refreshOnChange": false,
                          "key": "u2",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "twenty_six",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "twentysix",
                          "type": "number",
                          "input": true
                        }
                      ]
                    },

                  ],



                  
                  [
                    {
                      "components": [
                        {
                          "html": "<p>25</p>",
                          "label": "twentyfive",
                          "refreshOnChange": false,
                          "key": "twentyfive",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>Gratuity</p>",
                          "label": "Gratuity",
                          "refreshOnChange": false,
                          "key": "gratuity",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>10(14)</p>",
                          "label": "10(14)",
                          "refreshOnChange": false,
                          "key": "ten_fourteen_3",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                        "html": "<p>Less : Allowances Exempted U/s 10</p>",
                          "label": "Less : Allowances Exempted U/s 10",
                          "refreshOnChange": false,
                          "key": "u1",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }

                        

                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "twenty_seven",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "twentyseven",
                          "type": "number",
                          "input": true
                        }
                      ]
                    },

                  ],


                  [
                    {
                      "components": [
                        {
                          "html": "<p>26</p>",
                          "label": "twentysix",
                          "refreshOnChange": false,
                          "key": "twentysix",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>LTA  U/s 10 (5)</p>",
                          "label": "LTA  U/s 10 (5)",
                          "refreshOnChange": false,
                          "key": "lta",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        
                      ]
                    },
                    {
                      "components": [
                        {
                          "html": "<p>10(14)</p>",
                          "label": "10(14)",
                          "refreshOnChange": false,
                          "key": "ten_fourteen_4",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }
                      ]
                    },
                    {
                      "components": [
                        {
                        "html": "<p>Less : Allowances Exempted U/s 10</p>",
                          "label": "Less : Allowances Exempted U/s 10",
                          "refreshOnChange": false,
                          "key": "u2",
                          "type": "content",
                          "input": false,
                          "tableView": false
                        }

                        

                      ]
                    },
                    {
                      "components": [
                        {
                          "label": "twenty_eight",
                          "applyMaskOn": "change",
                          "hideLabel": true,
                          "mask": false,
                          "tableView": false,
                          "defaultValue": 0,
                          "delimiter": false,
                          "requireDecimal": false,
                          "inputFormat": "plain",
                          "truncateMultipleSpaces": false,
                          "validateWhenHidden": false,
                          "key": "twentyeight",
                          "type": "number",
                          "input": true
                        }
                      ]
                    },

                  ],




                  

                 
                ]
              }
            ]
          }
        ]
      ],
      "numCols": 1
    },
    
  ]
}




var array

frappe.ui.form.on('Employee Tax Exemption Declaration', {

  refresh:function(frm)
  {


    tds_projection_html(frm)



      if(frm.doc.custom_tax_regime=="Old Regime")
      {
      frm.set_df_property("custom_declaration_form","hidden",0)
      const wrapper = frm.fields_dict.custom_declaration_form.$wrapper;
      const formContainer = document.createElement("div");
      wrapper.html('');
      wrapper.append(formContainer);

      // Create Form.io form
      Formio.createForm(formContainer, DECLARATION_FORM, { baseUrl: window?.location?.origin || '' })
          .then((form) => {
              window.cur_formioInstance = form;

              // Pre-fill the form with saved data (if available)
              const savedData = frm.doc.custom_declaration_form_data
                  ? JSON.parse(frm.doc.custom_declaration_form_data)
                  : {};

              const defaultData = { pfValue: 0, aValue2: 0, bValue1: 0,amount4:0,dValue1:0,eValue1:0,fValue1:0,gValue1:0,hValue1:0,iValue1:0,jValue1:0,kValue1:0,kValue2:0,...savedData };

              form.submission = { data: defaultData };

              let isUpdating = false; 

              form.on('change', ({ data }) => {
                  if (isUpdating) return; 
                  isUpdating = true;


                  const a = parseFloat(data.pfValue || 0);
                  
                  const b = parseFloat(data.aValue2 || 0);
                  const c = parseFloat(data.bValue1 || 0);
                  const d=parseFloat(data.amount4 || 0);

                  const e=parseFloat(data.dValue1 || 0);

                  const f=parseFloat(data.eValue1 || 0);
                  const g=parseFloat(data.fValue1 || 0);
                  const h=parseFloat(data.gValue1 || 0);
                  const i=parseFloat(data.hValue1 || 0);
                  const j=parseFloat(data.iValue1 || 0);
                  const k=parseFloat(data.jValue1 || 0);
                  const l=parseFloat(data.kValue1 || 0);
                  const m=parseFloat(data.kValue2 || 0);
                  

                  total=a+b+c+d+e+f+g+h+i+j+k+l+m


                  data.total80C = total;

                  form.submission.data = data;

                  console.log(data,"999999999999999999")

                  frm.set_value("custom_declaration_form_data", JSON.stringify(data));

                  isUpdating = false; // Allow further updates
              });
          })
          .catch((err) => {
              console.error("Error creating Form.io form:", err);
          });

        }

      if(frm.doc.custom_tax_regime=="New Regime")
      {
        frm.set_df_property("custom_declaration_form","hidden",1)
      }


      if(frm.doc.docstatus==1)
          {
              frm.add_custom_button("Choose Regime",function()
              {

                let d = new frappe.ui.Dialog({
                  title: 'Enter details',
                  fields: [
                     
                      {
                          label: 'Select Regime',
                          fieldname: 'select_regime',
                          fieldtype: 'Select',
                          options:['Old Regime','New Regime'],
                          reqd:1,
                          default:frm.doc.custom_tax_regime,
                          description: `Your current tax regime is ${frm.doc.custom_tax_regime}`


                      },
  
                     
  
  
                  ],
                  size: 'small', // small, large, extra-large 
                  primary_action_label: 'Submit',
                  primary_action(values) {
                      console.log(values);
  
                      frappe.call({
                        "method":"cn_indian_payroll.cn_indian_payroll.overrides.declaration.choose_regime",
                        args:{
    
                            doc_id: frm.doc.name,
                            employee:frm.doc.employee,
                            company:frm.doc.company,
                            payroll_period:frm.doc.payroll_period,
                            regime:values.select_regime
                            
    
                        },
                        callback :function(res)
                        {
                            frm.reload_doc();
                           
    
                        }
    
                    })
  
  
  
                      d.hide();
                  }
              });
              
              d.show();

    
                  
                  
              })
              frm.change_custom_button_type('Choose Regime', null, 'primary');


              
          }
      
  },



  custom_declaration_form_data(frm)
  {
    
    if(frm.doc.custom_declaration_form_data)
    {
      frm.set_value("custom_status","Pending")
      frm.set_value("workflow_state","Pending")
    }
  },


  monthly_house_rent:function(frm)
  {
    if(frm.doc.monthly_house_rent)
    {
      frm.set_value("custom_check",0)
    }
  }

  

 

  
 
});




function tds_projection_html(frm) {
  if (frm.doc.docstatus == 1) {

      let section10_component = []; // Ensure it's an array
      let section10_amount = []; // Ensure it's an array

      let section80c_component=[]
      let section80c_amount=[]

      let section80d_component=[]
      let section80d_amount=[]

      let other_component=[]
      let other_amount=[]


      let total_array = [];
      let total_value = [];
      let from_amount = [];
      let to_amount = [];
      let percentage = [];
      let difference = [];




      let total_sum_old=0

      frappe.call({
          method: "cn_indian_payroll.cn_indian_payroll.overrides.accrual_bonus.get_doc_data",
          args: {
              doc_name: frm.doc.name,
              employee: frm.doc.employee,
              company: frm.doc.company,
              payroll_period: frm.doc.payroll_period
          },
          callback: function (res) {
              if (res.message) {
                  const from_month = res.message.from_month;
                  const to_month = res.message.to_month;
                  const oldValue = Math.round(res.message.current_old_value);
                  const newValue = Math.round(res.message.current_new_value);
                  const old_future_amount = Math.round(res.message.future_old_value);
                  const new_future_amount = Math.round(res.message.future_new_value);

                  const num_months=res.message.num_months
                  const salary_slip_count=res.message.salary_slip_count



                  const old_std=res.message.old_standard
                  const new_std=res.message.new_standard

                  const pt_value=Math.round(res.message.pt)
                  const nps_value=Math.round(res.message.nps)


                  const per_comp = res.message.perquisite_component || []; 
                  const per_values = res.message.perquisite_amount || [];

                  const total_per_sum = per_values.reduce((total, value) => total + value, 0);

                  const maxLength = Math.max(per_comp.length, per_values.length);

                  let perquisiteRows = "";
                  for (let i = 0; i < maxLength; i++) {
                      let component = per_comp[i] || "-";  
                      let oldPer = per_values[i] || "-";
                      let newPer = per_values[i] || "-";
                      perquisiteRows += `<tr><td>${component}</td><td>${"₹" + oldPer}</td><td>${"₹" + newPer}</td></tr>`;
                  }

                  // Check if declarations exist
                  if (frm.doc.declarations) {
                      $.each(frm.doc.declarations, function (i, v) {
                          if (v.exemption_category == "Section 10(14)") {
                              section10_component.push(v.exemption_sub_category);
                              section10_amount.push(v.amount);
                          }

                          if(v.exemption_category == "Section 80C")
                          {
                            section80c_component.push(v.exemption_sub_category)
                            section80c_amount.push(v.amount)

                          }

                          if(v.exemption_category == "Section 80D" || v.exemption_category == "Section 80DD" || v.exemption_category == "Section 80E" || v.exemption_category == "Section 80EE"||v.exemption_category == "Section 80U")
                            {
                              section80d_component.push(v.exemption_sub_category)
                              

                              if(v.amount<=v.max_amount)
                                {
                                  
                                  section80d_amount.push(v.amount)
                                }
                                else
                                {
                                  section80d_amount.push(v.max_amount)
  
                                }
  
                            }

                          


                              const validCategories = [
                                
                                "Section 80DDB",
                                "Section 80-G",
                                "Section 80CCD(1B)",
                                "Section 80EEA",
                                "Section 80EEB",
                                "Section 80GGC",
                                "Section 80TTA",
                                "Section 80TTB",
                                "Section 80GG",
                                "Section 80CCG",
                                "Section 24(b)",
                            ];
                            
                            if (validCategories.includes(v.exemption_category)) {
                              other_component.push(v.exemption_sub_category)
                              

                              if(v.amount<=v.max_amount)
                                {
                                  
                                  other_amount.push(v.amount)
                                }
                                else
                                {
                                  other_amount.push(v.amount)
  
                                }
                            }
                      });
                  }


                  const total_section10_sum = section10_amount.reduce((total, value) => total + value, 0);
                  const total_section80C_sum = Math.min(section80c_amount.reduce((total, value) => total + value, 0), 150000);
                  const total_section80d_sum = section80d_amount.reduce((total, value) => total + value, 0);
                  const total_other_sum = other_amount.reduce((total, value) => total + value, 0);


                  const section10_maxLength = Math.max(section10_component.length, section10_amount.length);
                  const section80_maxLength = Math.max(section80c_component.length, section80c_amount.length);
                  const section80D_maxLength = Math.max(section80d_component.length, section80d_amount.length);
                  const other_maxLength = Math.max(other_component.length, other_amount.length);


                  const annual_hra_exemption=Math.max(frm.doc.annual_hra_exemption)

                  


                  // Create rows for section 10 details
                  let Section10Rows = "";
                  for (let i = 0; i < section10_maxLength; i++) {
                      let Section10component = section10_component[i] || "-";  // If index out of bounds, insert "-"
                      let oldSection10 = section10_amount[i] || "0";
                      let newSection10 = 0;  // Assuming new value is 0 for now
                      Section10Rows += `<tr><td>${Section10component}</td><td>${"₹" + oldSection10}</td><td>${"₹" + newSection10}</td></tr>`;
                  }


                  let Section80Rows = "";
                  for (let i = 0; i < section80_maxLength; i++) {
                      let Section80component = section80c_component[i] || "-";  // If index out of bounds, insert "-"
                      let oldSection80c = section80c_amount[i] || "0";
                      let newSection80c = 0;  // Assuming new value is 0 for now
                      Section80Rows += `<tr><td>${Section80component}</td><td>${"₹" + oldSection80c}</td><td>${"₹" + newSection80c}</td></tr>`;
                  }

                  let Section80DRows = "";
                  for (let i = 0; i < section80D_maxLength; i++) {
                      let Section80Dcomponent = section80d_component[i] || "-";  // If index out of bounds, insert "-"
                      let oldSection80D = section80d_amount[i] || "0";
                      let newSection80D = 0;  // Assuming new value is 0 for now
                      Section80DRows += `<tr><td>${Section80Dcomponent}</td><td>${"₹" + oldSection80D}</td><td>${"₹" + newSection80D}</td></tr>`;
                  }

                  let OtherRows = "";
                  for (let i = 0; i < other_maxLength; i++) {
                      let Othercomponent = other_component[i] || "-";  // If index out of bounds, insert "-"
                      let oldSectionOther = other_amount[i] || "0";
                      let newSectionOther = 0;  // Assuming new value is 0 for now
                      OtherRows += `<tr><td>${Othercomponent}</td><td>${"₹" + oldSectionOther}</td><td>${"₹" + newSectionOther}</td></tr>`;
                  }



                  
                  

                  let annual_old_taxable_income=(oldValue+old_future_amount+total_per_sum)-(total_section10_sum+old_std+pt_value+total_section80C_sum+total_section80d_sum+total_other_sum+nps_value+annual_hra_exemption)
                  let annual_new_taxable_income=(newValue+new_future_amount+total_per_sum)-(nps_value+new_std)


                  console.log(annual_old_taxable_income,"11111")
                  console.log(annual_new_taxable_income,"222222")


                  function getPerComp1() {
                    return new Promise((resolve, reject) => {
                        frappe.call({
                            method: "cn_indian_payroll.cn_indian_payroll.overrides.accrual_bonus.slab_calculation",
                            args: {
                                employee: frm.doc.employee,
                                company: frm.doc.company,
                                payroll_period: frm.doc.payroll_period,
                                old_annual_slab: annual_old_taxable_income,
                                new_annual_slab: annual_new_taxable_income
                            },
                            callback: function (response) {
                                if (response.message) {
                                    let old_from_amount = response.message.from_amount || [];
                                    let old_to_amount = response.message.to_amount || [];
                                    let old_percentage_amount = response.message.percentage || [];
                                    let old_value_amount = response.message.total_value || [];
                                    let total_sum=response.message.total_sum
                                    let rebate=response.message.rebate
                                    let max_amount=response.message.max_amount
                                    let old_rebate_value=response.message.old_rebate_value


                                    let  old_surcharge_m=response.message.old_surcharge_m                              
                                    let old_education_cess=response.message.old_education_cess
                                    let new_from_amount = response.message.from_amount_new || [];
                                    let new_to_amount = response.message.to_amount_new || [];
                                    let new_percentage_amount = response.message.percentage_new || [];
                                    let new_value_amount = response.message.total_value_new || [];
                                    let total_sum_new=response.message.total_sum_new
                                    let newrebate=response.message.rebate_new
                                    let newmax_amount=response.message.max_amount_new
                                    let new_rebate_value=response.message.new_rebate_value
                                    let  new_surcharge_m=response.message.new_surcharge_m                              
                                    let new_education_cess=response.message.new_education_cess


                                    let salary_slip_sum=Math.round(response.message.salary_slip_sum)
                                    
                                    

                                    
                                    resolve({ 
                                      old_from_amount,
                                       old_to_amount, 
                                       old_percentage_amount, 
                                       old_value_amount,
                                       new_from_amount ,
                                       new_to_amount,
                                       new_percentage_amount,
                                       new_value_amount,
                                       total_sum,
                                       total_sum_new,
                                       rebate,
                                       max_amount,
                                       newrebate,
                                       newmax_amount,
                                       old_rebate_value,
                                       new_rebate_value,
                                       old_surcharge_m,
                                        old_education_cess,
                                        new_surcharge_m,
                                        new_education_cess,
                                        salary_slip_sum,
                                        num_months,
                                        salary_slip_count,
                                        from_month,
                                        to_month,
                                        


                                      });
                                } else {
                                    console.error("Error: No response received from Python method.");
                                    reject("No response received");
                                }
                            }
                        });
                    });
                }
                
                async function processPerComp1() {
                  try {
                      let { old_from_amount, old_to_amount, old_percentage_amount, old_value_amount,new_from_amount ,
                        new_to_amount,
                        new_percentage_amount,
                        new_value_amount,total_sum,total_sum_new,
                        rebate,
                        max_amount,
                        newrebate,
                        newmax_amount,
                        old_rebate_value,
                        new_rebate_value,
                        old_surcharge_m,
                        old_education_cess,
                        new_surcharge_m,
                        new_education_cess,
                        salary_slip_sum,
                        num_months,
                        salary_slip_count,
                        from_month,
                        to_month,
                        
                      } = await getPerComp1();
                     
                      let OtherRows1 = "";
                      for (let i = 0; i < old_from_amount.length; i++) {
                          let fromcomponent = old_from_amount[i]|| 0;  
                          let tocomponent = old_to_amount[i] || 0; 
                          let percentage =old_percentage_amount[i] || 0; 
                          let final_amount = old_value_amount[i] || 0;


                          
                          OtherRows1 += `<tr><td>${fromcomponent}</td><td>${"₹" + tocomponent}</td><td>${"₹" + percentage}</td><td>${"₹" + final_amount}</td></tr>`;
                          console.log(OtherRows1,"OtherRows1OtherRows1")
                      
                        }

                      let OtherRows2 = "";
                      for (let i = 0; i < new_from_amount.length; i++) {
                          let newfromcomponent = new_from_amount[i]|| 0;  
                          let newtocomponent = new_to_amount[i] || 0; 
                          let newpercentage =new_percentage_amount[i] || 0; 
                          let newfinal_amount = new_value_amount[i] || 0;


                          
                          OtherRows2 += `<tr><td>${newfromcomponent}</td><td>${"₹" + newtocomponent}</td><td>${"₹" + newpercentage}</td><td>${"₹" + newfinal_amount}</td></tr>`;
                      }
              
                      // Define the table HTML with dropdowns and expandable rows
                  const table_html = `
                  <table class="table table-bordered">
                      <thead>
                          <tr>
                              <th>Title</th>
                              <th>Old Regime</th>
                              <th>New Regime</th>
                          </tr>
                      </thead>
                      <tbody>
                          <tr>
                              <td>Current Taxable Earnings(${from_month}-${to_month})</td>
                              <td>₹ ${oldValue}</td>
                              <td>₹ ${newValue}</td>
                          </tr>
                          <tr>
                              <td>Future Taxable Earnings</td>
                              <td>₹ ${old_future_amount}</td>
                              <td>₹ ${new_future_amount}</td>
                          </tr>
                          <tr>
                              <td>
                                  Total Perquisite
                                  <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                      <i class="fa fa-caret-down"></i>
                                  </button>
                                  <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                      <table class="table table-sm table-bordered">
                                          <thead>
                                              <tr>
                                                  <th>Perquisite Component</th>
                                                  <th>Old Regime</th>
                                                  <th>New Regime</th>
                                              </tr>
                                          </thead>
                                          <tbody>${perquisiteRows}</tbody>
                                      </table>
                                  </div>
                              </td>
                              <td>₹ ${total_per_sum}</td>
                              <td>₹ ${total_per_sum}</td>
                          </tr>



                           <tr>
                              <td>Total Taxable Income</td>
                              <td>₹ ${oldValue+old_future_amount+total_per_sum}</td>
                              <td>₹ ${newValue+new_future_amount+total_per_sum}</td>
                          </tr>





                          <tr>
                              <td>
                                  Less : Allowances Exempted U/s 10
                                  <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                      <i class="fa fa-caret-down"></i>
                                  </button>
                                  <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                      <table class="table table-sm table-bordered">
                                          <thead>
                                              <tr>
                                                  <th>Title</th>
                                                  <th>Old Regime</th>
                                                  <th>New Regime</th>
                                              </tr>
                                          </thead>
                                          <tbody>${Section10Rows}</tbody>
                                      </table>
                                  </div>
                              </td>
                              <td>₹ ${total_section10_sum}</td>
                              <td>₹ 0</td>
                          </tr>

                          <tr>
                                <td>Less: Allowances Exempted U/s 16
                                    <button class="btn btn-secondary btn-sm incomeTaxDropdown">
                                        <i class="fa fa-caret-down"></i>
                                    </button>
                                    <div class="incomeTaxDetails" style="display: none;">
                                        <table class="table table-sm table-bordered">
                                            <thead>
                                                <tr>
                                                    <th>Option</th>
                                                    <th>Old Regime</th>
                                                    <th>New Regime</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    <td>Standard Deduction</td>
                                                    <td>₹ ${old_std}</td>
                                                    <td>₹ ${new_std}</td>
                                                </tr>
                                                <tr>
                                                    <td>Tax on Employment</td>
                                                    <td>₹ ${pt_value}</td>
                                                    <td>₹ 0</td>
                                                </tr>

                                                 
                                            </tbody>
                                        </table>
                                    </div>
                                </td>
                                <td>₹ ${old_std+pt_value}</td>
                                <td>₹ ${new_std}</td>
                            </tr>


                            <tr>
                              <td>
                                  Less: Deduction under Sec 80C (Max Rs.1,50,000/-)
                                  <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                      <i class="fa fa-caret-down"></i>
                                  </button>
                                  <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                      <table class="table table-sm table-bordered">
                                          <thead>
                                              <tr>
                                                  <th>Title</th>
                                                  <th>Old Regime</th>
                                                  <th>New Regime</th>
                                              </tr>
                                          </thead>
                                          <tbody>${Section80Rows}</tbody>
                                      </table>
                                  </div>
                              </td>
                              <td>₹ ${total_section80C_sum}</td>
                              <td>₹ 0</td>
                          </tr>

                          <tr>
                              <td>
                                  Less: Deductions Under Chapter VI- A(80D,80DD,80E,80EE,80U)
                                  <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                      <i class="fa fa-caret-down"></i>
                                  </button>
                                  <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                      <table class="table table-sm table-bordered">
                                          <thead>
                                              <tr>
                                                  <th>Title</th>
                                                  <th>Old Regime</th>
                                                  <th>New Regime</th>
                                              </tr>
                                          </thead>
                                          <tbody>${Section80DRows}</tbody>
                                      </table>
                                  </div>
                              </td>
                              <td>₹ ${total_section80d_sum}</td>
                              <td>₹ 0</td>
                          </tr>

                          <tr>
                              <td>NPS</td>
                              <td>₹ ${nps_value}</td>
                              <td>₹ ${nps_value}</td>
                          </tr>


                          <tr>
                              <td>
                                 Other
                                  <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                      <i class="fa fa-caret-down"></i>
                                  </button>
                                  <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                      <table class="table table-sm table-bordered">
                                          <thead>
                                              <tr>
                                                  <th>Title</th>
                                                  <th>Old Regime</th>
                                                  <th>New Regime</th>
                                              </tr>
                                          </thead>
                                          <tbody>${OtherRows}</tbody>
                                      </table>
                                  </div>
                              </td>
                              <td>₹ ${total_other_sum}</td>
                              <td>₹ 0</td>
                          </tr>

                          <tr>
                              <td>HRA Exemption</td>
                              <td>₹ ${annual_hra_exemption}</td>
                              <td>₹ 0</td>
                          </tr>






                          <tr>
                              <td>Total Exemption/Deductions</td>
                              <td>₹ ${total_section10_sum+old_std+pt_value+total_section80C_sum+total_section80d_sum+total_other_sum+nps_value+annual_hra_exemption}</td>
                              <td>₹ ${nps_value+new_std}</td>
                          </tr>
                          <tr>
                              <td>Annual Taxable Income</td>
                              <td>₹ ${(oldValue+old_future_amount+total_per_sum)-(total_section10_sum+old_std+pt_value+total_section80C_sum+total_section80d_sum+total_other_sum+nps_value+annual_hra_exemption)}</td>
                              <td>₹ ${(newValue+new_future_amount+total_per_sum)-(nps_value+new_std)}</td>
                          </tr>



                          <tr>
                              <td>
                                  Tax Slab
                                  <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                      <i class="fa fa-caret-down"></i>
                                  </button>
                                  <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                      <table class="table table-sm table-bordered">
                                          <thead>
                                              <tr>
                                                  <th>From Amount</th>
                                                  <th>To Amount</th>
                                                  <th>Percentage</th>
                                                  <th>Amount</th>
                                              </tr>
                                          </thead>
                                          Old Regime Slab
                                          <tbody>${OtherRows1}</tbody>
                                      </table>

                                      <table class="table table-sm table-bordered">
                                          <thead>
                                              <tr>
                                                  <th>From Amount</th>
                                                  <th>To Amount</th>
                                                  <th>Percentage</th>
                                                  <th>Amount</th>
                                              </tr>
                                          </thead>
                                          New Regime Slab
                                          <tbody>${OtherRows2}</tbody>
                                      </table>


                                  </div>
                              </td>
                              <td>₹ ${total_sum}</td>
                              <td>₹ ${total_sum_new}</td>
                          </tr>


                          

                          <tr>
                              <td>
                                 Rebate
                                  <button class="btn btn-secondary btn-sm incomeTaxDropdown" style="margin-left: 10px;">
                                      <i class="fa fa-caret-down"></i>
                                  </button>
                                  <div class="incomeTaxDetails" style="display: none; margin-top: 10px;">
                                      <table class="table table-sm table-bordered">
                                          <thead>
                                              <tr>
                                                  <th>Regime</th>
                                                  <th>Annual Taxable Lessthan</th>
                                                  <th>Max Amount</th>
                                                  
                                                  
                                              </tr>
                                          </thead>
                                          <tbody>
                  
                                          <tr>
                                                  <th>Old Regime</th>
                                                  <th>₹ ${rebate}</th>
                                                  <th>₹ ${max_amount}</th>
                                                  
                                          </tr>
                                          <tr>
                                                  <th>New Regime</th>
                                                  <th>₹ ${newrebate}</th>
                                                  <th>₹ ${newmax_amount}</th>
                                                  
                                          </tr>
                                          </tbody>
                                      </table>
                                  </div>
                              </td>
                              <td>₹ ${Math.round(old_rebate_value)}
                                       </td>
                              <td>₹ ${Math.round(new_rebate_value)}</td>
                          </tr>


                          <tr>
                              <td>Total Tax on Income</td>
                              <td>₹ ${Math.round(total_sum-old_rebate_value)}</td>
                              <td>₹ ${Math.round(total_sum_new-new_rebate_value)}</td>
                          </tr>

                          <tr>
                              <td>Surcharge</td>
                              <td>₹ ${Math.round(old_surcharge_m)}</td>
                              <td>₹ ${Math.round(new_surcharge_m)}</td>

                              
                                    
                          </tr>

                          <tr>
                              <td>Education Cess</td>
                              <td>₹ ${Math.round(old_education_cess)}</td>
                              <td>₹ ${Math.round(new_education_cess)}</td>
                          </tr>


                          

                          <tr>
                              <td>Tax Payable</td>
                              <td>₹ ${Math.round(old_education_cess+old_surcharge_m+(total_sum-old_rebate_value))}</td>
                              <td>₹ ${Math.round(new_education_cess+new_surcharge_m+(total_sum_new-new_rebate_value))}</td>
                          </tr>

                          <tr>
                              <td>Tax Paid</td>
                              <td>₹ ${Math.round(salary_slip_sum)}</td>
                              <td>₹ ${Math.round(salary_slip_sum)}</td>
                          </tr>

                          <tr>
                              <td>Current Tax</td>
                              <td>₹ ${Math.round((total_sum-old_rebate_value)/num_months)}</td>
                              <td>₹ ${Math.round((total_sum_new-new_rebate_value)/num_months)}</td>
                          </tr>


                          <tr>
                              <td>Total Tax Deducted at source</td>
                              <td>₹ ${Math.round(((total_sum-old_rebate_value)/num_months)+(salary_slip_sum))}</td>
                              <td>₹ ${Math.round(((total_sum_new-new_rebate_value)/num_months)+(salary_slip_sum))}</td>
                          </tr>

                          <tr>
                              <td>Tax Payable / Refundable (14 - 15(A))</td>
                              <td>₹ ${Math.round((old_education_cess+old_surcharge_m+(total_sum-old_rebate_value))-(((total_sum-old_rebate_value)/num_months)+(salary_slip_sum)))}</td>
                              <td>₹ ${Math.round((new_education_cess+new_surcharge_m+(total_sum_new-new_rebate_value))-(((total_sum_new-new_rebate_value)/num_months)+(salary_slip_sum)))}</td>
                              
                          </tr>

                          <tr>
                              <td>TDS For Future Month</td>
                              <td>₹ ${Math.round(((old_education_cess+old_surcharge_m+(total_sum-old_rebate_value))-(((total_sum-old_rebate_value)/num_months)+(salary_slip_sum)))/(num_months-salary_slip_count))}</td>
                              <td>₹ ${Math.round(((new_education_cess+new_surcharge_m+(total_sum_new-new_rebate_value))-(((total_sum_new-new_rebate_value)/num_months)+(salary_slip_sum)))/(num_months-salary_slip_count))}</td>
                          </tr>



                      </tbody>
                  </table>
              `;
              
                      // Set the value of the HTML field
                      frm.set_df_property('custom_employee_tax_projection', 'options', table_html);
              
                      // Add event listeners for dropdown buttons
                      setTimeout(() => {
                          document.querySelectorAll('.incomeTaxDropdown').forEach((button, index) => {
                              button.addEventListener('click', function () {
                                  const detailsDiv = document.querySelectorAll('.incomeTaxDetails')[index];
                                  detailsDiv.style.display = (detailsDiv.style.display === 'none') ? 'block' : 'none';
                              });
                          });
                      }, 100);
              
                  } catch (error) {
                      console.error("Error fetching per_comp1:", error);
                  }
              }
              
              // Call the function to fetch and process the data
              processPerComp1();
              }
          }
      });

  }
}































