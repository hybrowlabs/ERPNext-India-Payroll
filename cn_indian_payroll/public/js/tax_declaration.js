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
                  "html": "<p>Mediclaim Policy for Parents</p>",
                  "label": "Mediclaim Premium",
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
                  "html": "<p>50000</p>",
                  "label": "50000",
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
                  "calculateValue": "if (data.amount>50000){\n  value = 0;\n} ",
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
                  "html": "<p>&nbsp;Mediclaim Policy for Self, Spouse, Children for Senior Citizen</p>",
                  "label": " Mediclaim Policy for Self, Spouse, Children for Senior Citizen",
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
                  "html": "<p><span style=\"background-color:rgb(255,255,255);color:rgb(93,93,93);\">25000</span></p>",
                  "label": "25000",
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
                  "calculateValue": "if (data.amount3>25000){\n  value = 0;\n} ",
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
                  "html": "<p>Mediclaim Policy for Self, Spouse, Children</p>",
                  "label": "Mediclaim Policy for Self, Spouse, Children",
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
                  "html": "<p>50000</p>",
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
                  "calculateValue": "if (data.mpAmount3>50000){\n  value = 0;\n} ",
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
                  "html": "<p>Mediclaim Policy for Parents for Senior Citizen</p>",
                  "label": "Mediclaim Policy for Parents for Senior Citizen",
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
                  "html": "<p>25000</p>",
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
                  "calculateValue": "if (data.mpAmount4>25000){\n  value = 0;\n} ",
                  "validateWhenHidden": false,
                  "key": "mpAmount4",
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
                  "calculateValue": "if (data.mp5>5000){\n  value = 0;\n} ",
                  "validateWhenHidden": false,
                  "key": "mp5",
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
                  "calculateValue": "if (data.mpAmount6>5000){\n  value = 0;\n} ",
                  "validateWhenHidden": false,
                  "key": "mpAmount6",
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
                  "html": "<p>Section 80EE</p>",
                  "label": "Section 80EE",
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
                  "calculateValue": "if (data.hlAmount>200000){\n  value = 0;\n} ",
                  "validateWhenHidden": false,
                  "key": "hlAmount",
                  "type": "number",
                  "input": true
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
                            "calculateValue": "if (data.pfValue>200000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.aValue2>150000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.bValue1>150000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.amount4>150000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.dValue1>150000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.eValue1>150000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.fValue1>150000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.gValue1>150000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.hValue1>150000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.iValue1>150000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.jValue1>150000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.kValue1>150000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.kValue2>150000){\n  value = 0;\n} ",
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
                            "calculateValue": "if (data.fourValue>75000){\n  value = 0;\n} ",
                            "validateWhenHidden": false,
                            "key": "fourValue",
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
                            "calculateValue": "if (data.fiveNumber>40000){\n  value = 0;\n} ",
                            "validateWhenHidden": false,
                            "key": "fiveNumber",
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
                            "calculateValue": "if (data.sevenNumber>75000){\n  value = 0;\n} ",
                            "validateWhenHidden": false,
                            "key": "sevenNumber",
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
                            "calculateValue": "if (data.tenNumber>50000){\n  value = 0;\n} ",
                            "validateWhenHidden": false,
                            "key": "tenNumber",
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
                            "calculateValue": "if (data.elevenNumber>50000){\n  value = 0;\n} ",
                            "validateWhenHidden": false,
                            "key": "elevenNumber",
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
                  "numRows": 9,
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
                            "calculateValue": "if (data.twelveNumber1>150000){\n  value = 0;\n} ",
                            "validateWhenHidden": false,
                            "key": "twelveNumber1",
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
                            "calculateValue": "if (data.fifteenNumber>150000){\n  value = 0;\n} ",
                            "validateWhenHidden": false,
                            "key": "fifteenNumber",
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
                            "calculateValue": "if (data.seventeenNumber>10000){\n  value = 0;\n} ",
                            "validateWhenHidden": false,
                            "key": "seventeenNumber",
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
                            "calculateValue": "if (data.eighteenNumber>50000){\n  value = 0;\n} ",
                            "validateWhenHidden": false,
                            "key": "eighteenNumber",
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
                            "calculateValue": "if (data.nineteenNumber>2500){\n  value = 0;\n} ",
                            "validateWhenHidden": false,
                            "key": "nineteenNumber",
                            "type": "number",
                            "input": true,
                            "disabled":true
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
                            "calculateValue": "if (data.twentyNumber>60000){\n  value = 0;\n} ",
                            "validateWhenHidden": false,
                            "key": "twentyNumber",
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
                            "calculateValue": "if (data.twentyoneNumber>25000){\n  value = 0;\n} ",
                            "validateWhenHidden": false,
                            "key": "twentyoneNumber",
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
                        "components": []
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
                      }
                    ]
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
       



        if(frm.doc.custom_tax_regime=="New Regime")
            {
                frm.set_df_property('declarations',  'read_only',  1);
            }



            // if(frm.doc.docstatus==1)
            // {
            //     frm.add_custom_button("Edit Declaration",function()
            //     {
                    
            //         // edit_declaration(frm)

            //         edit(frm)
                    
            //     })
            //     frm.change_custom_button_type('Edit Declaration', null, 'primary');
            // }



            //sum of all 80C



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

         



//--------------------------------------------------------------------------------------------------




        
        // const wrapper = frm.fields_dict.custom_declaration_form.$wrapper;
        // const formContainer = document.createElement("div");
        // wrapper.html('');
        // wrapper.append(formContainer);

        // // Create Form.io form
        // Formio.createForm(formContainer, DECLARATION_FORM, { baseUrl: window?.location?.origin || '' })
        //     .then((form) => {
        //         window.cur_formioInstance = form;

        //         // Pre-fill the form with saved data (if available)
        //         const savedData = frm.doc.custom_declaration_form_data
        //             ? JSON.parse(frm.doc.custom_declaration_form_data)
        //             : {};

        //         // Apply default value if no saved data exists
        //         const defaultData = { number: 0, ...savedData };

        //         if (Object.keys(defaultData).length) {
        //             form.submission = { data: defaultData };
        //         }


        //         form.on('change', ({ data }) => {
                    
        //             frm.set_value("custom_declaration_form_data", JSON.stringify(data));
        //         });
        //     })
        //     .catch((err) => {
        //         console.error("Error creating Form.io form:", err);
        //     });


            //GRAVISH CODE

        
            // const wrapper=frm.fields_dict.custom_declaration_form.$wrapper;
            // const form=document.createElement("div")
            // wrapper.html('')
            // wrapper.append(form)

            // const f = Formio.createForm(form, DECLARATION_FORM, { baseUrl: window?.location?.origin || '' })
            // .then((form) => {
            //     window.cur_formioInstance = form
            //     // form.submission = { data: JSON.parse(frm.doc.custom_operation_form_data || '{}') }
            //     form.on('change', ({ data }) => {
            //         frm.set_value("custom_declaration_form_data", JSON.stringify(data))
            //     })
            // })

            // console.log(frm.doc.custom_declaration_form_data,"11111")


            
    },



    custom_declaration_form_data(frm)
    {
      
      if(frm.doc.custom_declaration_form_data)
      {
        frm.set_value("custom_status","Pending")
        frm.set_value("workflow_state","Pending")
      }
    },


    

   

    // before_save: function (frm) {

    //     if (window.cur_formioInstance) {
    //         const data = window.cur_formioInstance.submission.data;
    //         frm.set_value("custom_declaration_form_data", JSON.stringify(data));

    //     }
    // }

    
   
});






// function change_regime(frm) {


//   let d = new frappe.ui.Dialog({
//       title: 'Enter details',
//       fields: [
//           {
//               label: 'Select Regime',
//               fieldname: 'select_regime',
//               fieldtype: 'Select',
//               options: ['Old Regime', 'New Regime'],
//               reqd: 1,
//               default: frm.doc.custom_tax_regime,
//               description: `Your current tax regime is ${frm.doc.custom_tax_regime}`

//           }
//       ],
//       size: 'small', // small, large, extra-large 
//       primary_action_label: 'Submit',
//       primary_action(values) {
//           // console.log(values);

//           if (values.select_regime == "New Regime") {
//               frappe.call({
//                   method: "frappe.client.get_list",
//                   args: {
//                       doctype: "Salary Slip",
//                       filters: { employee: frm.doc.employee, docstatus: 1, custom_payroll_period: frm.doc.payroll_period },
//                       fields: ["*"]
//                   },
//                   callback: function (kes) {
//                       if (kes.message.length == 0) {
//                           frappe.call({
//                               method: "frappe.client.get_list",
//                               args: {
//                                   doctype: "Salary Structure Assignment",
//                                   filters: { employee: frm.doc.employee, docstatus: 1 },
//                                   fields: ["*"],
//                                   limit: 1,
//                                   order_by: "from_date desc"
//                               },
//                               callback: function (res) {
//                                   if (res.message) {
//                                       // console.log(res.message);

//                                       frappe.call({
//                                           method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
//                                           args: {
//                                               source_name: res.message[0].salary_structure,
//                                               employee: frm.doc.employee,
//                                               print_format: 'Salary Slip Standard for CTC',
//                                               docstatus: 1,
//                                               for_preview: 1
//                                           },
//                                           callback: function (response) {
//                                               if (response.message.earnings) {
//                                                   $.each(response.message.earnings, function (i, v) {
//                                                       frappe.call({
//                                                           method: "frappe.client.get",
//                                                           args: {
//                                                               doctype: "Salary Component",
//                                                               filters: { name: v.salary_component },
//                                                               fields: ["*"]
//                                                           },
//                                                           callback: function (mes) {
//                                                               if (mes.message && mes.message.component_type == "NPS") {

//                                                                 // console.log(res.message[0].from_date)

                                                                


//                                                                 frappe.call({
//                                                                   method: "frappe.client.get",
//                                                                   args: {
//                                                                       doctype: "Payroll Period",
//                                                                       filters: { name:frm.doc.payroll_period },
//                                                                       fields: ["*"]
//                                                                   },
//                                                                   callback: function (zes) {
//                                                                       if (zes.message) {

//                                                                         end_date=zes.message.end_date

//                                                                         var from_date

//                                                                         if (zes.message.start_date<=res.message[0].from_date)
//                                                                         {
//                                                                           from_date=zes.message.start_date

//                                                                         }

//                                                                         else{
//                                                                           from_date=res.message[0].from_date

//                                                                         }

                                                                         

                                                                        



//                                                                         const startDate = new Date(from_date);
//                                                                         const endDate = new Date(end_date);

//                                                                         // Calculate the difference in months
//                                                                         function getMonthsBetween(startDate, endDate) {
//                                                                             const startYear = startDate.getFullYear();
//                                                                             const startMonth = startDate.getMonth(); // 0-based
//                                                                             const endYear = endDate.getFullYear();
//                                                                             const endMonth = endDate.getMonth(); // 0-based

//                                                                             // Total months calculation
//                                                                             return (endYear - startYear) * 12 + (endMonth - startMonth) + 1; // +1 to include the start month
//                                                                         }

//                                                                         // const monthsBetween = getMonthsBetween(startDate, endDate);

//                                                                         const monthsBetween = getMonthsBetween(new Date(from_date), end_date);
//                                                                         // const nineNumber = Math.round(monthsBetween * v.amount);
//                                                                         const nineNumber = 500

//                                                                                 // Set JSON with only nineNumber
//                                                                                 try {
//                                                                                     let newJsonData = { nineNumber };
//                                                                                     frm.set_value("custom_declaration_form_data", JSON.stringify(newJsonData));
//                                                                                     frm.save('Update');
//                                                                                 } catch (error) {
//                                                                                     console.error("Failed to update custom_declaration_form_data JSON", error);
//                                                                                 }




//                                                                   // try {
//                                                                   //     let jsonData = JSON.parse(frm.doc.custom_declaration_form_data);

//                                                                   //     jsonData.nineNumber = Math.round(monthsBetween*v.amount);

//                                                                   //     // console.log(v.amount)

//                                                                   //     // console.log(monthsBetween*v.amount)

//                                                                   //     frm.set_value("custom_declaration_form_data", JSON.stringify(jsonData));

//                                                                   //     frm.save('Update');
//                                                                   // } catch (error) {
//                                                                   //     console.error("Failed to parse custom_declaration_form_data JSON", error);
//                                                                   // }

//                                                                 }
//                                                               }
//                                                             })
//                                                               }
//                                                           }
//                                                       });
//                                                   });
//                                               }
//                                           }
//                                       });
//                                   }
//                               }
//                           });
//                       }

//                       else{


//                       //   frappe.call({
//                       //     method: "frappe.client.get_list",
//                       //     args: {
//                       //         doctype: "Salary Structure Assignment",
//                       //         filters: { employee: frm.doc.employee, docstatus: 1 },
//                       //         fields: ["*"],
//                       //         limit: 1,
//                       //         order_by: "from_date desc"
//                       //     },
//                       //     callback: function (res) {
//                       //         if (res.message) {
//                       //             console.log(res.message);

//                       //             frappe.call({
//                       //                 method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
//                       //                 args: {
//                       //                     source_name: res.message[0].salary_structure,
//                       //                     employee: frm.doc.employee,
//                       //                     print_format: 'Salary Slip Standard for CTC',
//                       //                     docstatus: 1,
//                       //                     for_preview: 1
//                       //                 },
//                       //                 callback: function (response) {
//                       //                     if (response.message.earnings) {
//                       //                         $.each(response.message.earnings, function (i, v) {
//                       //                             frappe.call({
//                       //                                 method: "frappe.client.get",
//                       //                                 args: {
//                       //                                     doctype: "Salary Component",
//                       //                                     filters: { name: v.salary_component },
//                       //                                     fields: ["*"]
//                       //                                 },
//                       //                                 callback: function (mes) {
//                       //                                     if (mes.message && mes.message.component_type == "NPS") {

//                       //                                       console.log(res.message[0].from_date)

                                                            


//                       //                                       frappe.call({
//                       //                                         method: "frappe.client.get",
//                       //                                         args: {
//                       //                                             doctype: "Payroll Period",
//                       //                                             filters: { name:frm.doc.payroll_period },
//                       //                                             fields: ["*"]
//                       //                                         },
//                       //                                         callback: function (zes) {
//                       //                                             if (zes.message) {

//                       //                                               end_date=zes.message.end_date

//                       //                                               from_date=res.message[0].from_date

//                       //                                               const startDate = new Date(from_date);
//                       //                                               const endDate = new Date(end_date);

//                       //                                               // Calculate the difference in months
//                       //                                               function getMonthsBetween(startDate, endDate) {
//                       //                                                   const startYear = startDate.getFullYear();
//                       //                                                   const startMonth = startDate.getMonth(); // 0-based
//                       //                                                   const endYear = endDate.getFullYear();
//                       //                                                   const endMonth = endDate.getMonth(); // 0-based

//                       //                                                   // Total months calculation
//                       //                                                   return (endYear - startYear) * 12 + (endMonth - startMonth) + 1; // +1 to include the start month
//                       //                                               }

//                       //                                               const monthsBetween = getMonthsBetween(startDate, endDate);




//                       //                                         try {
//                       //                                             // Parse the custom_declaration_form_data JSON
//                       //                                             let jsonData = JSON.parse(frm.doc.custom_declaration_form_data);

//                       //                                             // Update the nineNumber field
//                       //                                             jsonData.nineNumber = Math.round(monthsBetween*v.amount);

//                       //                                             console.log(v.amount)

//                       //                                             console.log(monthsBetween*v.amount)

//                       //                                             // Update the field on the form
//                       //                                             frm.set_value("custom_declaration_form_data", JSON.stringify(jsonData));

//                       //                                             // Save the form to persist changes
//                       //                                             frm.save('Update');
//                       //                                         } catch (error) {
//                       //                                             console.error("Failed to parse custom_declaration_form_data JSON", error);
//                       //                                         }

//                       //                                       }
//                       //                                     }
//                       //                                   })
//                       //                                     }
//                       //                                 }
//                       //                             });
//                       //                         });
//                       //                     }
//                       //                 }
//                       //             });
//                       //         }
//                       //     }
//                       // });



//                       }
//                   }
//               });
//           }

//           else{

//           }

//           d.hide();
//       }
//   });

//   d.show();
// }



function change_regime(frm) {
  let d = new frappe.ui.Dialog({
      title: 'Enter details',
      fields: [
          {
              label: 'Select Regime',
              fieldname: 'select_regime',
              fieldtype: 'Select',
              options: ['Old Regime', 'New Regime'],
              reqd: 1,
              default: frm.doc.custom_tax_regime,
              description: `Your current tax regime is ${frm.doc.custom_tax_regime}`
          }
      ],
      size: 'small',
      primary_action_label: 'Submit',
      primary_action(values) {
          if (values.select_regime === "New Regime") {


            frappe.call({
              method: "frappe.client.get_list",
              args: {
                  doctype: "Income Tax Slab",
                  filters: { docstatus: 1, custom_select_regime:values.select_regime,company:frm.doc.company},
                  fields: ["*"]
              },
              callback: function (tes) {
                  if (tes.message) {

                    var new_tax_regime=tes.message[0].name






              frappe.call({
                  method: "frappe.client.get_list",
                  args: {
                      doctype: "Salary Slip",
                      filters: { employee: frm.doc.employee, docstatus: ["in", [0, 1]], custom_payroll_period: frm.doc.payroll_period },
                      fields: ["*"]
                  },
                  callback: function (kes) {
                      if (kes.message.length === 0) {
                          frappe.call({
                              method: "frappe.client.get_list",
                              args: {
                                  doctype: "Salary Structure Assignment",
                                  filters: { employee: frm.doc.employee, docstatus: 1 },
                                  fields: ["*"],
                                  limit: 1,
                                  order_by: "from_date desc"
                              },
                              callback: function (res) {
                                  if (res.message) {
                                      frappe.call({
                                          method: "hrms.payroll.doctype.salary_structure.salary_structure.make_salary_slip",
                                          args: {
                                              source_name: res.message[0].salary_structure,
                                              employee: frm.doc.employee,
                                              print_format: 'Salary Slip Standard for CTC',
                                              docstatus: 1,
                                              for_preview: 1
                                          },
                                          callback: function (response) {
                                              if (response.message.earnings) {
                                                  $.each(response.message.earnings, function (i, v) {
                                                      frappe.call({
                                                          method: "frappe.client.get",
                                                          args: {
                                                              doctype: "Salary Component",
                                                              filters: { name: v.salary_component },
                                                              fields: ["*"]
                                                          },
                                                          callback: function (mes) {
                                                              if (mes.message && mes.message.component_type === "NPS") {
                                                                  frappe.call({
                                                                      method: "frappe.client.get",
                                                                      args: {
                                                                          doctype: "Payroll Period",
                                                                          filters: { name: frm.doc.payroll_period },
                                                                          fields: ["*"]
                                                                      },
                                                                      callback: function (zes) {
                                                                          if (zes.message) {
                                                                              let from_date = Math.max(new Date(zes.message.start_date), new Date(res.message[0].from_date));
                                                                              const end_date = new Date(zes.message.end_date);

                                                                              // Calculate months between two dates
                                                                              function getMonthsBetween(startDate, endDate) {
                                                                                  const startYear = startDate.getFullYear();
                                                                                  const startMonth = startDate.getMonth();
                                                                                  const endYear = endDate.getFullYear();
                                                                                  const endMonth = endDate.getMonth();
                                                                                  return (endYear - startYear) * 12 + (endMonth - startMonth) + 1;
                                                                              }

                                                                              const monthsBetween = getMonthsBetween(new Date(from_date), end_date);
                                                                              const nineNumber = Math.round(monthsBetween * v.amount);

                                                                              // Set JSON with only nineNumber
                                                                              try {
                                                                                  let newJsonData = { nineNumber };
                                                                                  frm.set_value("custom_declaration_form_data", JSON.stringify(newJsonData));

                                                                                  frm.set_value("custom_income_tax",new_tax_regime)
                                                                                  frm.save('Update');
                                                                              } catch (error) {
                                                                                  console.error("Failed to update custom_declaration_form_data JSON", error);
                                                                              }


                                                                              



                                                                          }
                                                                      }
                                                                  });
                                                              }
                                                          }
                                                      });
                                                  });
                                              }
                                          }
                                      });
                                  }
                              }
                          });
                      }

                      else
                      {

                        var count=kes.message.length


                        $.each(kes.message,function(i,k)
                          {

                            frappe.call({
                              method: "frappe.client.get",
                              args: {
                                  doctype: "Salary Slip",
                                  filters: {name:k.name},
                                  fields: ["*"]
                              },
                              callback: function (salary_response) {

                                if(salary_response.message)
                                {
                                  console.log(salary_response.message)

                                }
    
    
                              }
                            })

                          })

                        





                      }
                  }
              });

            }
          }
        })
          }
          d.hide();
      }
  });

  d.show();
}








function edit_declaration(frm) {
    if (frm.doc.employee) {
        var sub_category = [];

        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Employee Tax Exemption Sub Category",
                filters: {
                    "is_active": 1,
                    "name": ["not in", ["Employee Provident Fund (Auto)", "NPS Contribution by Employer", "Tax on employment (Professional Tax)"]]
                },
                fields: ["*"],
                limit_page_length: 999999999999
            },
            callback: function(subcategory_response) {
                if (subcategory_response.message && subcategory_response.message.length > 0) {
                    subcategory_response.message.forEach(function(v) {
                        sub_category.push(v.name);
                    });
                }

                if (frm.doc.custom_tax_regime === "Old Regime") {
                    let component_array = [];

                    let d = new frappe.ui.Dialog({
                        title: 'Enter details',
                        fields: [
                            {
                                label: 'Details Table',
                                fieldname: 'details_table',
                                fieldtype: 'Table',
                                fields: [
                                    {
                                        label: 'Exemption Sub Category',
                                        fieldname: 'exemption_sub_category',
                                        fieldtype: 'Select',
                                        options: sub_category,
                                        in_list_view: 1,
                                        editable: true
                                    },
                                    {
                                        label: 'Employee Tax Exemption Category',
                                        fieldname: 'employee_exemption_category',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Maximum Exempted Amount',
                                        fieldname: 'maximum_amount',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Declared Amount',
                                        fieldname: 'declared_amount',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        editable: true,
                                    },
                                ]
                            },
                            {
                                fieldtype: 'Section Break'
                            },
                            {
                                label: 'Monthly HRA Amount',
                                fieldname: 'hra_amount',
                                fieldtype: 'Currency',
                            },
                            {
                                fieldtype: 'Column Break'
                            },
                            {
                                label: 'Rented in Metro City',
                                fieldname: 'rented_in_metro_city',
                                fieldtype: 'Check',
                            }
                        ],
                        size: 'large',
                        primary_action_label: 'Submit',
                        primary_action(values) {
                            // let total_exe_amount = 0;
                            // $.each(frm.doc.declarations, function(i, k) {
                            //     if (k.exemption_category == "Section 80C") {
                            //         total_exe_amount = k.max_amount - k.amount;
                            //     }
                            // });

                            // let total_80C = 0;
                            // $.each(values.details_table, function(i, m) {
                            //     if (m.employee_exemption_category == "Section 80C") {
                            //         total_80C += parseFloat(m.declared_amount);
                            //     }
                            // });

                            // if (total_80C > total_exe_amount) {
                            //     frappe.msgprint(`You can't enter an amount greater than ${total_exe_amount} for Section 80C.`);
                            // } else {
                                // Add declarations with specific sub-categories to component_array
                                $.each(frm.doc.declarations, function(i, m) {
                                    if (["NPS Contribution by Employer", "Tax on employment (Professional Tax)", "Employee Provident Fund (Auto)","Uniform Allowance"].includes(m.exemption_sub_category)) {
                                        component_array.push({
                                            "sub_category": m.exemption_sub_category,
                                            "category": m.exemption_category,
                                            "max_amount": m.max_amount,
                                            "amount": m.amount
                                        });
                                    }
                                });

                                // Add dialog box values to component_array
                                $.each(values.details_table, function(i, w) {
                                    component_array.push({
                                        "sub_category": w.exemption_sub_category,
                                        "category": w.employee_exemption_category,
                                        "max_amount": w.maximum_amount,
                                        "amount": w.declared_amount
                                    });
                                });

                                console.log(component_array);

                                // Update child table
                                frm.clear_table('declarations');
                                component_array.forEach(row => {
                                    let new_row = frm.add_child('declarations');
                                    new_row.exemption_sub_category = row.sub_category;
                                    new_row.exemption_category = row.category;
                                    new_row.max_amount = row.max_amount;
                                    new_row.amount = row.amount;
                                });


                                frm.set_value("monthly_house_rent", values.hra_amount);
                                frm.set_value("rented_in_metro_city", values.rented_in_metro_city);
                                frm.set_value("custom_posting_date",frappe.datetime.nowdate())
                                frm.refresh_field('declarations');
                                frm.save('Update');
                                d.hide();



                            // }
                        }
                    });

                    d.show();

                    // Update employee_exemption_category when exemption_sub_category changes
                    d.$wrapper.on('change', '[data-fieldname="exemption_sub_category"] select', function() {
                        let selectedValue = $(this).val();
                        let rowIndex = $(this).closest('.grid-row').index();

                        if (selectedValue) {
                            frappe.call({
                                method: 'frappe.client.get',
                                args: {
                                    doctype: "Employee Tax Exemption Sub Category",
                                    name: selectedValue
                                },
                                callback: function(r) {
                                    if (r.message) {
                                        let category = r.message.exemption_category;
                                        let category_max_amount = r.message.max_amount;
                                        d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category = category;
                                        d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount = category_max_amount;
                                        d.fields_dict.details_table.grid.refresh();
                                    }
                                }
                            });
                        }
                    });

                    // Validate declared_amount input
                    // d.$wrapper.on('change', '[data-fieldname="declared_amount"] input', function() {
                    //     let rowIndex = $(this).closest('.grid-row').index();
                    //     let selectedAmount = $(this).val();
                    //     let maxAmount = d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount;
                    //     let component = d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category;

                    //     if (component == "Section 80C") {
                    //         $.each(frm.doc.declarations, function(i, v) {
                    //             if (v.exemption_category == component) {
                    //                 if (v.amount == 150000) {
                    //                     frappe.msgprint("You can't enter the amount here because your Section 80C is at the maximum.");
                    //                     d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.declared_amount = undefined;
                    //                     d.fields_dict.details_table.grid.refresh();
                    //                 } else {
                    //                     let remainingAmount = maxAmount - parseFloat(v.amount);

                    //                     if (selectedAmount > remainingAmount) {
                    //                         frappe.msgprint(`You can't enter an amount greater than ${remainingAmount}.`);
                    //                         d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.declared_amount = undefined;
                    //                         d.fields_dict.details_table.grid.refresh();
                    //                     }
                    //                 }
                    //             }
                    //         });
                    //     } 
                    //     else 
                    //     {

                    //         console.log(selectedAmount,"selectedAmount")
                    //         console.log(maxAmount,"maxAmount")
                    //         if (selectedAmount > maxAmount) {
                    //             frappe.msgprint(`You can't enter an amount greater than ${maxAmount}.`);
                    //             d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.declared_amount = undefined;
                    //             d.fields_dict.details_table.grid.refresh();
                    //         }
                    //     }
                    // });
                } else {
                    frappe.msgprint("You can't Edit the declaration because you are in the New regime.");
                }
            }
        });
    }
}



function edit(frm) {
    var component_array = [];
    var component_array_not_include = [];
    var sub_category = [];

    var component_from_dialogue=[]

    // Collect data from frm.doc.declarations
    $.each(frm.doc.declarations, function(i, m) {
        if (["NPS Contribution by Employer", "Tax on employment (Professional Tax)", "Employee Provident Fund (Auto)"].includes(m.exemption_sub_category)) {
            component_array.push({
                "exemption_sub_category": m.exemption_sub_category,
                "employee_exemption_category": m.exemption_category,
                "maximum_amount": m.max_amount,
                "declared_amount": m.amount
            });
        } else {
            component_array_not_include.push({
                "exemption_sub_category": m.exemption_sub_category,
                "employee_exemption_category": m.exemption_category,
                "maximum_amount": m.max_amount,
                "declared_amount": m.amount
            });
        }
    });

    // Fetch active subcategories
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Employee Tax Exemption Sub Category",
            filters: {
                "is_active": 1,
                "name": ["not in", ["Employee Provident Fund (Auto)", "NPS Contribution by Employer", "Tax on employment (Professional Tax)"]]
            },
            fields: ["name"],
            limit_page_length: 999999999999
        },
        callback: function(subcategory_response) {
            if (subcategory_response.message && subcategory_response.message.length > 0) {
                sub_category = subcategory_response.message.map(v => v.name);

                if (frm.doc.custom_tax_regime === "Old Regime") {
                    let d = new frappe.ui.Dialog({
                        title: 'Declare Your Exemptions',
                        fields: [
                            {
                                label: 'Exemptions Auto Calculated',
                                fieldname: 'details_table',
                                fieldtype: 'Table',
                                cannot_add_rows: 1,
                                cannot_delete_rows: 1,
                                fields: [
                                    {
                                        label: 'Exemption Sub Category',
                                        fieldname: 'exemption_sub_category',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Employee Tax Exemption Category',
                                        fieldname: 'employee_exemption_category',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Maximum Exempted Amount',
                                        fieldname: 'maximum_amount',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Declared Amount',
                                        fieldname: 'declared_amount',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                ]
                            },
                            {
                                fieldtype: 'Section Break'
                            },
                            {
                                label: 'Declare Tax Exemptions',
                                fieldname: 'custom_details_table',
                                fieldtype: 'Table',
                                fields: [
                                    {
                                        label: 'Exemption Sub Category',
                                        fieldname: 'custom_exemption_sub_category',
                                        fieldtype: 'Select',
                                        in_list_view: 1,
                                        options: sub_category.join('\n'),
                                        editable: true
                                    },
                                    {
                                        label: 'Employee Tax Exemption Category',
                                        fieldname: 'custom_employee_exemption_category',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Maximum Exempted Amount',
                                        fieldname: 'custom_maximum_amount',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        label: 'Declared Amount',
                                        fieldname: 'custom_declared_amount',
                                        fieldtype: 'Data',
                                        in_list_view: 1,
                                        editable: true,
                                        reqd:1
                                    },
                                ]
                            },

                            {
                                fieldtype: 'Section Break'
                            },
                            {
                                label: 'Monthly HRA Amount',
                                fieldname: 'hra_amount',
                                fieldtype: 'Int',
                                default:frm.doc.monthly_house_rent,
                            },
                            {
                                fieldtype: 'Column Break'
                            },
                            {
                                label: 'Rented in Metro City',
                                fieldname: 'rented_in_metro_city',
                                fieldtype: 'Check',
                                default:frm.doc.rented_in_metro_city
                            },
                    
                        ],
                        size: 'large',
                        primary_action_label: 'Submit',
                        primary_action(values) {
                            d.hide();

                            // console.log(values)


                            $.each(values.details_table, function(i, w) {
                                component_from_dialogue.push({
                                    "sub_category": w.exemption_sub_category,
                                    "category": w.employee_exemption_category,
                                    "max_amount": w.maximum_amount,
                                    "amount": w.declared_amount
                                });
                            });

                            $.each(values.custom_details_table, function(i, m) {
                                component_from_dialogue.push({
                                    "sub_category": m.custom_exemption_sub_category,
                                    "category": m.custom_employee_exemption_category,
                                    "max_amount": m.custom_maximum_amount,
                                    "amount": m.custom_declared_amount
                                });
                            });

                            frm.clear_table('declarations');
                            component_from_dialogue.forEach(row => {
                                    let new_row = frm.add_child('declarations');
                                    new_row.exemption_sub_category = row.sub_category;
                                    new_row.exemption_category = row.category;
                                    new_row.max_amount = row.max_amount;
                                    new_row.amount = row.amount;
                                });

                                

                                frm.set_value("custom_check",0)
                                frm.set_value("monthly_house_rent", values.hra_amount);
                                frm.set_value("rented_in_metro_city", values.rented_in_metro_city);
                                frm.set_value("custom_posting_date",frappe.datetime.nowdate())
                                frm.refresh_field('declarations');
                                frm.save('Update');
                                d.hide();




                        }
                    });

                    // Populate the dialog's first table
                    let table_field = d.get_field('details_table');
                    if (!table_field.df.data) {
                        table_field.df.data = [];
                    }
                    component_array.forEach(item => {
                        table_field.df.data.push({
                            "exemption_sub_category": item.exemption_sub_category,
                            "employee_exemption_category": item.employee_exemption_category,
                            "maximum_amount": item.maximum_amount,
                            "declared_amount": item.declared_amount
                        });
                    });
                    table_field.grid.refresh();

                    let custom_table_field = d.get_field('custom_details_table');
                    if (!custom_table_field.df.data) {
                        custom_table_field.df.data = [];
                    }
                    component_array_not_include.forEach(item => {
                        custom_table_field.df.data.push({
                            "custom_exemption_sub_category": item.exemption_sub_category,
                            "custom_employee_exemption_category": item.employee_exemption_category,
                            "custom_maximum_amount": item.maximum_amount,
                            "custom_declared_amount": item.declared_amount
                        });
                    });
                    custom_table_field.grid.refresh();

                    d.show();  



                    d.$wrapper.on('change', '[data-fieldname="custom_exemption_sub_category"] select', function() {
                        let selectedValue = $(this).val();
                        let rowIndex = $(this).closest('.grid-row').index();

                        console.log(selectedValue,"7777")

                        if (selectedValue) {
                            frappe.call({
                                method: 'frappe.client.get',
                                args: {
                                    doctype: "Employee Tax Exemption Sub Category",
                                    name: selectedValue
                                },
                                callback: function(r) {
                                    if (r.message) {
                                        let category = r.message.exemption_category;
                                        let category_max_amount = r.message.max_amount;
                                        d.fields_dict.custom_details_table.grid.grid_rows[rowIndex].doc.custom_employee_exemption_category = category;
                                        d.fields_dict.custom_details_table.grid.grid_rows[rowIndex].doc.custom_maximum_amount = category_max_amount;
                                        d.fields_dict.custom_details_table.grid.refresh();
                                    }
                                }
                            });

                            


                        }
                    });

                    d.$wrapper.on('change', '[data-fieldname="custom_declared_amount"] input', function() {
                        let rowIndex = $(this).closest('.grid-row').index();
                        let selectedAmount = $(this).val();
                        
                        let component = d.fields_dict.custom_details_table.grid.grid_rows[rowIndex].doc.custom_exemption_sub_category;

                        if(component=="Uniform Allowance") {
                               

                                frappe.call({
                                    method: "frappe.client.get_list",
                                    args: {
                                        doctype: "Salary Structure Assignment",
                                        filters: { employee: frm.doc.employee, 'docstatus': 1 },
                                        fields: ["*"],
                                        limit: 1,
                                        order_by: "from_date desc"
                                    },
                                    callback: function(res) {
                                        if (res.message && res.message.length > 0) {

                                            if(res.message[0].custom_is_uniform_allowance==0)
                                            {
                                                msgprint("You Are Not Eligible for Uniform Allowance")
                                                d.fields_dict.custom_details_table.grid.grid_rows[rowIndex].doc.custom_declared_amount = 0;
                                                d.fields_dict.custom_details_table.grid.refresh();

                                            }

                                        }
                                    }
                                })



                            }
                        
                    })
                }

                else{
                    msgprint("You Cant Edit Declaration,Because You are in The New Regime")
                }
            }
        }
    });
}

































// frappe.ui.form.on('Employee Tax Exemption Declaration Category', {
//     refresh(frm) {
//         // your code here
//     },
    
//     amount:function(frm,cdt,cdn)
//     {
//         var d=locals[cdt][cdn]
//         // console.log(d,"000")
        
        
//         if(d.amount>d.max_amount)
//         {
//             frappe.model.set_value(cdt, cdn, "amount", 0);
//             msgprint("You Cant Enter Amount Greater than "+d.max_amount)
//         }
//     },

    

//     exemption_sub_category: function(frm, cdt, cdn) {
//         var d = locals[cdt][cdn];

//         console.log(d.exemption_sub_category);

//         frappe.call({
//             method: "frappe.client.get",
//             args: {
//                 doctype: "Employee Tax Exemption Sub Category",
//                 filters: { name: d.exemption_sub_category },
//                 fields: ["*"] 
//             },
//             callback: function(res) {
//                 if (res.message) {

                    
//                     if(res.message.custom_is_nps==1)
//                     {

//                         frappe.call({
//                             "method": "frappe.client.get_list",
//                             args: {
//                                 doctype: "Salary Structure Assignment",
//                                 filters: { employee: frm.doc.employee ,docstatus:1},
//                                 fields: ["*"],
//                                 order_by: "from_date desc",
//                                 limit: 1
//                             },
//                             callback: function(kes) {
//                                 if (kes.message && kes.message.length > 0) {


//                                     if(kes.message[0].custom_is_nps==1)
//                                     {
                                        
//                                         let nps_amount = Math.round((kes.message[0].base/12 * 0.35));
//                                         let nps_percentage=Math.round(nps_amount*kes.message[0].custom_nps_percentage/100);
//                                         let nps_amount_year = Math.round(nps_percentage * 12);
//                                         frappe.model.set_value(cdt, cdn, "max_amount", nps_amount_year);
//                                         frappe.model.set_value(cdt, cdn, "amount", nps_amount_year);



//                                     }
//                                     else{
//                                         frappe.model.set_value(cdt, cdn, "max_amount", 0);
//                                     }



//                                 }
//                             }
//                         })



//                     }


//                     if(res.message.custom_is_epf==1)
//                         {
    
//                             frappe.call({
//                                 "method": "frappe.client.get_list",
//                                 args: {
//                                     doctype: "Salary Structure Assignment",
//                                     filters: { employee: frm.doc.employee ,docstatus:1},
//                                     fields: ["*"],
//                                     order_by: "from_date desc",
//                                     limit: 1
//                                 },
//                                 callback: function(kes) {
//                                     if (kes.message && kes.message.length > 0) {
    
                                        
    
//                                         if(kes.message[0].custom_is_epf==1)
//                                         {
                                            
//                                             let epf_amount = Math.round((kes.message?.at(0).base/12)*0.35);
                                            
//                                             let epf_percentage=Math.round(epf_amount*12/100);
                                            
                                           
//                                             let epf_amount_year = Math.round(epf_percentage * 12);

//                                             if(epf_amount_year>res.message.max_amount)
//                                             {
//                                                 frappe.model.set_value(cdt, cdn, "max_amount", res.message.max_amount);
//                                                 frappe.model.set_value(cdt, cdn, "amount", res.message.max_amount);

                                                
//                                             }

//                                             else
//                                             {
//                                                 frappe.model.set_value(cdt, cdn, "max_amount", epf_amount_year);
//                                                 frappe.model.set_value(cdt, cdn, "amount", epf_amount_year);
//                                             }


                                            
    
    
    
//                                         }
//                                         else{
//                                             frappe.model.set_value(cdt, cdn, "max_amount", 0);
//                                         }
    
    
    
//                                     }
//                                 }
//                             })
    
    
    
//                         }


//                         frappe.model.set_value(cdt, cdn, "max_amount", res.message.max_amount);



                    
//                 } 
                
//             },
           
//         });
//     }
// })






// function edit(frm) 
// {
//     let d = new frappe.ui.Dialog({
//         title: 'Enter details',
//         fields: [
//             {
//                 label: 'Details Table',
//                 fieldname: 'details_table',
//                 fieldtype: 'Table',
//                 fields: [
//                     {
//                         label: 'Exemption Sub Category',
//                         fieldname: 'exemption_sub_category',
//                         fieldtype: 'Link',
//                         options: 'Employee Tax Exemption Sub Category',
//                         in_list_view: 1,
//                         editable: true,
//                         onchange: function() {
//                             console.log(d.get_field('details_table').get_value());
//                         }
//                     },
//                     {
//                         label: 'Employee Tax Exemption Category',
//                         fieldname: 'employee_exemption_category',
//                         fieldtype: 'Link',
//                         options: 'Employee Tax Exemption Category',
//                         in_list_view: 1,
//                         editable: true
//                     },
//                     {
//                         label: 'Maximum Exempted Amount',
//                         fieldname: 'maximum_amount',
//                         fieldtype: 'Currency',
//                         in_list_view: 1
//                     },
//                     {
//                         label: 'Declared Amount',
//                         fieldname: 'declared_amount',
//                         fieldtype: 'Currency',
//                         in_list_view: 1,
//                         editable: true
//                     }
//                 ]
//             }
//         ],
//         size: 'large',
//         primary_action_label: 'Submit',
//         primary_action(values) {
//             frm.clear_table('declarations');

//             var total_amount = 0;
//             values.details_table.forEach(row => {
//                 total_amount += row.declared_amount;
//                 let new_row = frm.add_child('declarations');
//                 new_row.exemption_sub_category = row.exemption_sub_category;
//                 new_row.exemption_category = row.employee_exemption_category;
//                 new_row.max_amount = row.maximum_amount;
//                 new_row.amount = row.declared_amount;
//             });

//             frm.refresh_field('declarations');

//             frm.set_value("total_declared_amount", total_amount);
//             frm.set_value("total_exemption_amount", total_amount);

//             frm.save('Update');

           

//             frappe.db.insert({
//                 "doctype": "Tax Declaration History",
//                 "employee": frm.doc.employee,
//                 "employee_name": frm.doc.employee_name,
//                 "company": frm.doc.company,
//                 "tax_exemption":frm.doc.name,
//                 "income_tax":frm.doc.custom_income_tax,
//                 "posting_date": frappe.datetime.nowdate(),
//                 "payroll_period": frm.doc.payroll_period,
//                 "monthly_house_rent": frm.doc.monthly_house_rent,
//                 "rented_in_metro_city": frm.doc.rented_in_metro_city,
//                 "hra_as_per_salary_structure": frm.doc.hra_as_per_salary_structure,
//                 "total_declared_amount": frm.doc.total_declared_amount,
//                 "annual_hra_exemption": frm.doc.annual_hra_exemption,
//                 "monthly_hra_exemption": frm.doc.monthly_hra_exemption,
//                 "total_exemption_amount": frm.doc.total_exemption_amount,
//                 "declaration_details": values.details_table.map(row => ({
//                     "exemption_sub_category": row.exemption_sub_category,
//                     "exemption_category": row.employee_exemption_category,
//                     "maximum_exempted_amount": row.maximum_amount,
//                     "declared_amount": row.declared_amount
//                 }))
//             })
            
            
            
            

//             d.hide();
//         }
//     });

//     d.show();
// }


// function edit_declaration(frm) {
//     if (frm.doc.employee) {
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Salary Structure Assignment",
//                 filters: { "employee": frm.doc.employee, "docstatus": 1 },
//                 fields: ["*"],
//                 limit: 1,
//                 order_by: "from_date desc",
//             },
//             callback: function(res) {
//                 if (res.message && res.message.length > 0) {
//                     let component_array = [];

//                     if (res.message[0].income_tax_slab === "Old Regime") {
//                         if (res.message[0].custom_is_uniform_allowance == 1) {
//                             let value = res.message[0].custom_uniform_allowance_value;
//                             if (value) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_uniform": 1 },
//                                         fields: ["*"],
//                                     },
//                                     callback: function(response) {
//                                         if (response.message && response.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": response.message[0].name,
//                                                 "category": response.message[0].exemption_category,
//                                                 "max_amount": value,
//                                                 "amount": value
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (res.message[0].custom_is_epf == 1) {
//                             let epf_amount = Math.round((res.message[0].base * 0.35) / 12 * 0.12);
//                             if (epf_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_epf": 1 },
//                                         fields: ["*"],
//                                     },
//                                     callback: function(kes) {
//                                         if (kes.message && kes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": kes.message[0].name,
//                                                 "category": kes.message[0].exemption_category,
//                                                 "max_amount": epf_amount,
//                                                 "amount": epf_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (res.message[0].custom_is_nps == 1) {
//                             let nps_amount = Math.round(((res.message[0].base * 0.35) / 12 * res.message[0].custom_nps_percentage) / 100);
//                             if (nps_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_nps": 1 },
//                                         fields: ["*"],
//                                     },
//                                     callback: function(mes) {
//                                         if (mes.message && mes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": mes.message[0].name,
//                                                 "category": mes.message[0].exemption_category,
//                                                 "max_amount": nps_amount,
//                                                 "amount": nps_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (res.message[0].custom_state) {
//                             frappe.call({
//                                 method: "frappe.client.get_list",
//                                 args: {
//                                     doctype: "Employee Tax Exemption Sub Category",
//                                     filters: { "custom_is_pt": 1 },
//                                     fields: ["*"],
//                                 },
//                                 callback: function(jes) {
//                                     if (jes.message && jes.message.length > 0) {
//                                         component_array.push({
//                                             "sub_category": jes.message[0].name,
//                                             "category": jes.message[0].exemption_category,
//                                             "max_amount": jes.message[0].max_amount,
//                                             "amount": jes.message[0].max_amount
//                                         });
//                                     }
//                                 }
//                             });
//                         }

//                         setTimeout(function() {
                            

//                             let d = new frappe.ui.Dialog({
//                                 title: 'Enter details',
//                                 fields: [
//                                     {
//                                         label: 'Details Table',
//                                         fieldname: 'details_table',
//                                         fieldtype: 'Table',
//                                         fields: [
//                                             {
//                                                 label: 'Exemption Sub Category',
//                                                 fieldname: 'exemption_sub_category',
//                                                 fieldtype: 'Link',
//                                                 options: 'Employee Tax Exemption Sub Category',
//                                                 in_list_view: 1,
//                                                 editable: true,
//                                                 // onchange: function() {
//                                                 //     let table_field = d.fields_dict.details_table;
//                                                 //     let data = table_field.df.data;
                            
//                                                 //     // Access the table data directly
//                                                 //     if (data.length > 0) {
//                                                 //         data.forEach(row => {
//                                                 //             console.log(row.exemption_sub_category);
//                                                 //         });
//                                                 //     } else {
//                                                 //         console.log("No data in table");
//                                                 //     }
//                                                 // }

                                               
//                                             },
//                                             {
//                                                 label: 'Employee Tax Exemption Category',
//                                                 fieldname: 'employee_exemption_category',
//                                                 fieldtype: 'Link',
//                                                 options: 'Employee Tax Exemption Category',
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             },
//                                             {
//                                                 label: 'Maximum Exempted Amount',
//                                                 fieldname: 'maximum_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 read_only:1
//                                             },
//                                             {
//                                                 label: 'Declared Amount',
//                                                 fieldname: 'declared_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             }
//                                         ]
//                                     }
//                                 ],
//                                 size: 'large',
//                                 primary_action_label: 'Submit',
//                                 primary_action(values) {
//                                     frm.clear_table('declarations');
                        
//                                     var total_amount = 0;
//                                     values.details_table.forEach(row => {
//                                         total_amount += row.declared_amount;
//                                         let new_row = frm.add_child('declarations');
//                                         new_row.exemption_sub_category = row.exemption_sub_category;
//                                         new_row.exemption_category = row.employee_exemption_category;
//                                         new_row.max_amount = row.maximum_amount;
//                                         new_row.amount = row.declared_amount;
//                                     });
                        
//                                     frm.refresh_field('declarations');
                        
//                                     frm.set_value("total_declared_amount", total_amount);
//                                     frm.set_value("total_exemption_amount", total_amount);
                        
//                                     frm.save('Update');
                        
                                   
                        
//                                     frappe.db.insert({
//                                         doctype: "Tax Declaration History",
//                                         employee: frm.doc.employee,
//                                         employee_name: frm.doc.employee_name,
//                                         company: frm.doc.company,
//                                         tax_exemption: frm.doc.name,
//                                         income_tax: frm.doc.custom_income_tax,
//                                         posting_date: frappe.datetime.nowdate(),
//                                         payroll_period: frm.doc.payroll_period,
//                                         monthly_house_rent: frm.doc.monthly_house_rent,
//                                         rented_in_metro_city: frm.doc.rented_in_metro_city,
//                                         hra_as_per_salary_structure: frm.doc.salary_structure_hra,
//                                         total_declared_amount: frm.doc.total_declared_amount,
//                                         annual_hra_exemption: frm.doc.annual_hra_exemption,
//                                         monthly_hra_exemption: frm.doc.monthly_hra_exemption,
//                                         total_exemption_amount: frm.doc.total_exemption_amount,
//                                         declaration_details: values.details_table.map(row => ({
//                                             exemption_sub_category: row.exemption_sub_category,
//                                             exemption_category: row.employee_exemption_category,
//                                             maximum_exempted_amount: row.maximum_amount,
//                                             declared_amount: row.declared_amount
//                                         })),
//                                         hra_breakup: frm.doc.custom_hra_breakup.map(row => ({
//                                             month: row.month,
//                                             rent_paid: row.rent_paid,
//                                             earned_basic: row.earned_basic,
//                                             hra_received: row.hra_received,
//                                             excess_of_rent_paid: row.excess_of_rent_paid,
//                                             exemption_amount: row.exemption_amount
//                                         }))
//                                     });
                                    
                                    
                                    
                        
//                                     d.hide();
//                                 }
//                             });

                            
//                             d.fields_dict.details_table.df.data = [];
//                             component_array.forEach(item => {
//                                 d.fields_dict.details_table.df.data.push({
//                                     exemption_sub_category: item.sub_category,
//                                     employee_exemption_category: item.category,
//                                     maximum_amount: item.max_amount,
//                                     declared_amount: item.amount
//                                 });
//                             });
//                             d.fields_dict.details_table.grid.refresh();

//                             d.show();
//                         }, 1000);  
//                     }


//                     if (res.message[0].income_tax_slab === "New Regime") {
                       

//                         if (res.message[0].custom_is_nps == 1) {
//                             let nps_amount = Math.round(((res.message[0].base * 0.35) / 12 * res.message[0].custom_nps_percentage) / 100);
//                             if (nps_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_nps": 1 },
//                                         fields: ["*"],
//                                     },
//                                     callback: function(mes) {
//                                         if (mes.message && mes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": mes.message[0].name,
//                                                 "category": mes.message[0].exemption_category,
//                                                 "max_amount": nps_amount,
//                                                 "amount": nps_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

                       
//                         setTimeout(function() {
                            

//                             let d = new frappe.ui.Dialog({
//                                 title: 'Enter details',
//                                 fields: [
//                                     {
//                                         label: 'Details Table',
//                                         fieldname: 'details_table',
//                                         fieldtype: 'Table',
//                                         fields: [
//                                             {
//                                                 label: 'Exemption Sub Category',
//                                                 fieldname: 'exemption_sub_category',
//                                                 fieldtype: 'Link',
//                                                 options: 'Employee Tax Exemption Sub Category',
//                                                 in_list_view: 1,
//                                                 editable: true,
//                                             },
//                                             {
//                                                 label: 'Employee Tax Exemption Category',
//                                                 fieldname: 'employee_exemption_category',
//                                                 fieldtype: 'Link',
//                                                 options: 'Employee Tax Exemption Category',
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             },
//                                             {
//                                                 label: 'Maximum Exempted Amount',
//                                                 fieldname: 'maximum_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 read_only:1
//                                             },
//                                             {
//                                                 label: 'Declared Amount',
//                                                 fieldname: 'declared_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             }
//                                         ]
//                                     }
//                                 ],
//                                 size: 'large',
//                                 primary_action_label: 'Submit',
//                                 primary_action(values) {
//                                     frm.clear_table('declarations');
                        
//                                     var total_amount = 0;
//                                     values.details_table.forEach(row => {
//                                         total_amount += row.declared_amount;
//                                         let new_row = frm.add_child('declarations');
//                                         new_row.exemption_sub_category = row.exemption_sub_category;
//                                         new_row.exemption_category = row.employee_exemption_category;
//                                         new_row.max_amount = row.maximum_amount;
//                                         new_row.amount = row.declared_amount;
//                                     });
                        
//                                     frm.refresh_field('declarations');
                        
//                                     frm.set_value("total_declared_amount", total_amount);
//                                     frm.set_value("total_exemption_amount", total_amount);
                        
//                                     frm.save('Update');
                        
                                   
                        
//                                     frappe.db.insert({
//                                         doctype: "Tax Declaration History",
//                                         employee: frm.doc.employee,
//                                         employee_name: frm.doc.employee_name,
//                                         company: frm.doc.company,
//                                         tax_exemption: frm.doc.name,
//                                         income_tax: frm.doc.custom_income_tax,
//                                         posting_date: frappe.datetime.nowdate(),
//                                         payroll_period: frm.doc.payroll_period,
//                                         monthly_house_rent: frm.doc.monthly_house_rent,
//                                         rented_in_metro_city: frm.doc.rented_in_metro_city,
//                                         hra_as_per_salary_structure: frm.doc.salary_structure_hra,
//                                         total_declared_amount: frm.doc.total_declared_amount,
//                                         annual_hra_exemption: frm.doc.annual_hra_exemption,
//                                         monthly_hra_exemption: frm.doc.monthly_hra_exemption,
//                                         total_exemption_amount: frm.doc.total_exemption_amount,
//                                         declaration_details: values.details_table.map(row => ({
//                                             exemption_sub_category: row.exemption_sub_category,
//                                             exemption_category: row.employee_exemption_category,
//                                             maximum_exempted_amount: row.maximum_amount,
//                                             declared_amount: row.declared_amount
//                                         })),
                                        
//                                     });
                                    
                                    
                                    
                        
//                                     d.hide();
//                                 }
//                             });

                            
//                             d.fields_dict.details_table.df.data = [];
//                             component_array.forEach(item => {
//                                 d.fields_dict.details_table.df.data.push({
//                                     exemption_sub_category: item.sub_category,
//                                     employee_exemption_category: item.category,
//                                     maximum_amount: item.max_amount,
//                                     declared_amount: item.amount
//                                 });
//                             });
//                             d.fields_dict.details_table.grid.refresh();

//                             d.show();
//                         }, 1000);  
//                     }


//                 }
//             }
//         });
//     }
// }





// function edit_declaration(frm) {
//     if (frm.doc.employee) {
//         var sub_category = [];

//         // Fetch all active Employee Tax Exemption Sub Categories
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Employee Tax Exemption Sub Category",
//                 filters: { "is_active": 1 },
//                 fields: ["*"],
//                 limit_page_length: 999999999999
//             },
//             callback: function(subcategory_response) {
//                 if (subcategory_response.message && subcategory_response.message.length > 0) {
//                     subcategory_response.message.forEach(function(v) {
//                         sub_category.push(v.name);
//                     });
//                 }
//             }
//         });

//         // Fetch the latest Salary Structure Assignment
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Salary Structure Assignment",
//                 filters: { "employee": frm.doc.employee, "docstatus": 1 },
//                 fields: ["*"],
//                 limit: 1,
//                 order_by: "from_date desc"
//             },
//             callback: function(res) {
//                 if (res.message && res.message.length > 0) {
//                     let component_array = [];
//                     let salary_structure = res.message[0];

//                     if (salary_structure.income_tax_slab === "Old Regime") {
//                         if (salary_structure.custom_is_uniform_allowance == 1) {
//                             let value = salary_structure.custom_uniform_allowance_value;
//                             if (value) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_uniform": 1 },
//                                         fields: ["*"]
//                                     },
//                                     callback: function(response) {
//                                         if (response.message && response.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": response.message[0].name,
//                                                 "category": response.message[0].exemption_category,
//                                                 "max_amount": value,
//                                                 "amount": value
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (salary_structure.custom_is_epf == 1) {
//                             let epf_amount = Math.round((salary_structure.base * 0.35) / 12 * 0.12);
//                             if (epf_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_epf": 1 },
//                                         fields: ["*"]
//                                     },
//                                     callback: function(kes) {
//                                         if (kes.message && kes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": kes.message[0].name,
//                                                 "category": kes.message[0].exemption_category,
//                                                 "max_amount": epf_amount,
//                                                 "amount": epf_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (salary_structure.custom_is_nps == 1) {
//                             let nps_amount = Math.round(((salary_structure.base * 0.35) / 12 * salary_structure.custom_nps_percentage) / 100);
//                             if (nps_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_nps": 1 },
//                                         fields: ["*"]
//                                     },
//                                     callback: function(mes) {
//                                         if (mes.message && mes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": mes.message[0].name,
//                                                 "category": mes.message[0].exemption_category,
//                                                 "max_amount": nps_amount,
//                                                 "amount": nps_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (salary_structure.custom_state) {
//                             frappe.call({
//                                 method: "frappe.client.get_list",
//                                 args: {
//                                     doctype: "Employee Tax Exemption Sub Category",
//                                     filters: { "custom_is_pt": 1 },
//                                     fields: ["*"]
//                                 },
//                                 callback: function(jes) {
//                                     if (jes.message && jes.message.length > 0) {
//                                         component_array.push({
//                                             "sub_category": jes.message[0].name,
//                                             "category": jes.message[0].exemption_category,
//                                             "max_amount": jes.message[0].max_amount,
//                                             "amount": jes.message[0].max_amount
//                                         });
//                                     }
//                                 }
//                             });
//                         }

//                         // Delay to ensure all async calls are completed
//                         setTimeout(function() {
//                             let d = new frappe.ui.Dialog({
//                                 title: 'Enter details',
//                                 fields: [
//                                     {
//                                         label: 'Details Table',
//                                         fieldname: 'details_table',
//                                         fieldtype: 'Table',
//                                         fields: [
//                                             {
//                                                 label: 'Exemption Sub Category',
//                                                 fieldname: 'exemption_sub_category',
//                                                 fieldtype: 'Select',
//                                                 options: sub_category,
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             },
//                                             {
//                                                 label: 'Employee Tax Exemption Category',
//                                                 fieldname: 'employee_exemption_category',
//                                                 fieldtype: 'Data',
//                                                 in_list_view: 1,
//                                                 editable: true,
//                                                 read_only: 1
//                                             },
//                                             {
//                                                 label: 'Maximum Exempted Amount',
//                                                 fieldname: 'maximum_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 read_only: 1
//                                             },
//                                             {
//                                                 label: 'Declared Amount',
//                                                 fieldname: 'declared_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             }
//                                         ]
//                                     }
//                                 ],
//                                 size: 'large',
//                                 primary_action_label: 'Submit',
//                                 primary_action(values) {
//                                     frm.clear_table('declarations');

//                                     var total_amount = 0;
//                                     values.details_table.forEach(row => {
//                                         total_amount += row.declared_amount;
//                                         let new_row = frm.add_child('declarations');
//                                         new_row.exemption_sub_category = row.exemption_sub_category;
//                                         new_row.exemption_category = row.employee_exemption_category;
//                                         new_row.max_amount = row.maximum_amount;
//                                         new_row.amount = row.declared_amount;
//                                     });

//                                     frm.refresh_field('declarations');

//                                     frm.set_value("total_declared_amount", total_amount);
//                                     frm.set_value("total_exemption_amount", total_amount);

//                                     frm.save('Update');


//                                 frappe.db.insert({
//                                         doctype: "Tax Declaration History",
//                                         employee: frm.doc.employee,
//                                         employee_name: frm.doc.employee_name,
//                                         company: frm.doc.company,
//                                         tax_exemption: frm.doc.name,
//                                         income_tax: frm.doc.custom_income_tax,
//                                         posting_date: frappe.datetime.nowdate(),
//                                         payroll_period: frm.doc.payroll_period,
//                                         monthly_house_rent: frm.doc.monthly_house_rent,
//                                         rented_in_metro_city: frm.doc.rented_in_metro_city,
//                                         hra_as_per_salary_structure: frm.doc.salary_structure_hra,
//                                         total_declared_amount: frm.doc.total_declared_amount,
//                                         annual_hra_exemption: frm.doc.annual_hra_exemption,
//                                         monthly_hra_exemption: frm.doc.monthly_hra_exemption,
//                                         total_exemption_amount: frm.doc.total_exemption_amount,
//                                         declaration_details: values.details_table.map(row => ({
//                                             exemption_sub_category: row.exemption_sub_category,
//                                             exemption_category: row.employee_exemption_category,
//                                             maximum_exempted_amount: row.maximum_amount,
//                                             declared_amount: row.declared_amount
//                                         })),
//                                         hra_breakup: frm.doc.custom_hra_breakup.map(row => ({
//                                             month: row.month,
//                                             rent_paid: row.rent_paid,
//                                             earned_basic: row.earned_basic,
//                                             hra_received: row.hra_received,
//                                             excess_of_rent_paid: row.excess_of_rent_paid,
//                                             exemption_amount: row.exemption_amount
//                                         }))
//                                     });
                                    
                                    


//                                     d.hide();
//                                 }
//                             });

//                             d.fields_dict.details_table.df.data = [];
//                             component_array.forEach(item => {
//                                 d.fields_dict.details_table.df.data.push({
//                                     exemption_sub_category: item.sub_category,
//                                     employee_exemption_category: item.category,
//                                     maximum_amount: item.max_amount,
//                                     declared_amount: item.amount
//                                 });
//                             });
//                             d.fields_dict.details_table.grid.refresh();

//                             d.show();

//                             // Update employee_exemption_category when exemption_sub_category changes
//                             d.$wrapper.on('change', '[data-fieldname="exemption_sub_category"] select', function() {
//                                 let selectedValue = $(this).val();
//                                 let rowIndex = $(this).closest('.grid-row').index();

//                                 if (selectedValue) {
//                                     frappe.call({
//                                         method: 'frappe.client.get',
//                                         args: {
//                                             doctype: "Employee Tax Exemption Sub Category",
//                                             name: selectedValue
//                                         },
//                                         callback: function(r) {
//                                             if (r.message) {
//                                                 let category = r.message.exemption_category;
//                                                 let category_max_amount=r.message.max_amount;
//                                                 d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category = category;
//                                                 d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount = category_max_amount;
//                                                 d.fields_dict.details_table.grid.refresh();
//                                             }
//                                         }
//                                     });
//                                 }
//                             });

//                             d.$wrapper.on('change', '[data-fieldname="declared_amount"] input', function () {
//                                 let selectedAmount = $(this).val();
//                                 console.log('Selected value in Amount:', selectedAmount);
                                
//                             });

//                         }, 1000);
//                     }
//                 }
//             }
//         });
//     }
// }




// function edit_declaration(frm) {
//     if (frm.doc.employee) {
//         var sub_category = [];

//         // Fetch all active Employee Tax Exemption Sub Categories
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Employee Tax Exemption Sub Category",
//                 filters: { "is_active": 1 },
//                 fields: ["*"],
//                 limit_page_length: 999999999999
//             },
//             callback: function(subcategory_response) {
//                 if (subcategory_response.message && subcategory_response.message.length > 0) {
//                     subcategory_response.message.forEach(function(v) {
//                         sub_category.push(v.name);
//                     });
//                 }
//             }
//         });

//         // Fetch the latest Salary Structure Assignment
//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Salary Structure Assignment",
//                 filters: { "employee": frm.doc.employee, "docstatus": 1 },
//                 fields: ["*"],
//                 limit: 1,
//                 order_by: "from_date desc"
//             },
//             callback: function(res) {
//                 if (res.message && res.message.length > 0) {
//                     let component_array = [];
//                     let salary_structure = res.message[0];

//                     if (salary_structure.income_tax_slab === "Old Regime") {
//                         if (salary_structure.custom_is_uniform_allowance == 1) {
//                             let value = salary_structure.custom_uniform_allowance_value;
//                             if (value) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_uniform": 1 },
//                                         fields: ["*"]
//                                     },
//                                     callback: function(response) {
//                                         if (response.message && response.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": response.message[0].name,
//                                                 "category": response.message[0].exemption_category,
//                                                 "max_amount": value,
//                                                 "amount": value
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (salary_structure.custom_is_epf == 1) {
//                             let epf_amount = Math.round((salary_structure.base * 0.35) / 12 * 0.12);
//                             if (epf_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_epf": 1 },
//                                         fields: ["*"]
//                                     },
//                                     callback: function(kes) {
//                                         if (kes.message && kes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": kes.message[0].name,
//                                                 "category": kes.message[0].exemption_category,
//                                                 "max_amount": epf_amount,
//                                                 "amount": epf_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (salary_structure.custom_is_nps == 1) {
//                             let nps_amount = Math.round(((salary_structure.base * 0.35) / 12 * salary_structure.custom_nps_percentage) / 100);
//                             if (nps_amount) {
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Employee Tax Exemption Sub Category",
//                                         filters: { "custom_is_nps": 1 },
//                                         fields: ["*"]
//                                     },
//                                     callback: function(mes) {
//                                         if (mes.message && mes.message.length > 0) {
//                                             component_array.push({
//                                                 "sub_category": mes.message[0].name,
//                                                 "category": mes.message[0].exemption_category,
//                                                 "max_amount": nps_amount,
//                                                 "amount": nps_amount
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }

//                         if (salary_structure.custom_state) {
//                             frappe.call({
//                                 method: "frappe.client.get_list",
//                                 args: {
//                                     doctype: "Employee Tax Exemption Sub Category",
//                                     filters: { "custom_is_pt": 1 },
//                                     fields: ["*"]
//                                 },
//                                 callback: function(jes) {
//                                     if (jes.message && jes.message.length > 0) {
//                                         component_array.push({
//                                             "sub_category": jes.message[0].name,
//                                             "category": jes.message[0].exemption_category,
//                                             "max_amount": jes.message[0].max_amount,
//                                             "amount": jes.message[0].max_amount
//                                         });
//                                     }
//                                 }
//                             });
//                         }

//                         // Delay to ensure all async calls are completed
//                         setTimeout(function() {
//                             let d = new frappe.ui.Dialog({
//                                 title: 'Enter details',
//                                 fields: [
//                                     {
//                                         label: 'Details Table',
//                                         fieldname: 'details_table',
//                                         fieldtype: 'Table',
//                                         fields: [
//                                             {
//                                                 label: 'Exemption Sub Category',
//                                                 fieldname: 'exemption_sub_category',
//                                                 fieldtype: 'Select',
//                                                 options: sub_category,
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             },
//                                             {
//                                                 label: 'Employee Tax Exemption Category',
//                                                 fieldname: 'employee_exemption_category',
//                                                 fieldtype: 'Data',
//                                                 in_list_view: 1,
//                                                 editable: true,
//                                                 read_only: 1
//                                             },
//                                             {
//                                                 label: 'Maximum Exempted Amount',
//                                                 fieldname: 'maximum_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 read_only: 1
//                                             },
//                                             {
//                                                 label: 'Declared Amount',
//                                                 fieldname: 'declared_amount',
//                                                 fieldtype: 'Currency',
//                                                 in_list_view: 1,
//                                                 editable: true
//                                             }
//                                         ]
//                                     }
//                                 ],
//                                 size: 'large',
//                                 primary_action_label: 'Submit',
//                                 primary_action(values) {
//                                     frm.clear_table('declarations');

//                                     var total_amount = 0;
//                                     values.details_table.forEach(row => {
//                                         total_amount += row.declared_amount;
//                                         let new_row = frm.add_child('declarations');
//                                         new_row.exemption_sub_category = row.exemption_sub_category;
//                                         new_row.exemption_category = row.employee_exemption_category;
//                                         new_row.max_amount = row.maximum_amount;
//                                         new_row.amount = row.declared_amount;
//                                     });

//                                     frm.refresh_field('declarations');

//                                     frm.set_value("total_declared_amount", total_amount);
//                                     frm.set_value("total_exemption_amount", total_amount);

//                                     frm.save('Update');


//                                 frappe.db.insert({
//                                         doctype: "Tax Declaration History",
//                                         employee: frm.doc.employee,
//                                         employee_name: frm.doc.employee_name,
//                                         company: frm.doc.company,
//                                         tax_exemption: frm.doc.name,
//                                         income_tax: frm.doc.custom_income_tax,
//                                         posting_date: frappe.datetime.nowdate(),
//                                         payroll_period: frm.doc.payroll_period,
//                                         monthly_house_rent: frm.doc.monthly_house_rent,
//                                         rented_in_metro_city: frm.doc.rented_in_metro_city,
//                                         hra_as_per_salary_structure: frm.doc.salary_structure_hra,
//                                         total_declared_amount: frm.doc.total_declared_amount,
//                                         annual_hra_exemption: frm.doc.annual_hra_exemption,
//                                         monthly_hra_exemption: frm.doc.monthly_hra_exemption,
//                                         total_exemption_amount: frm.doc.total_exemption_amount,
//                                         declaration_details: values.details_table.map(row => ({
//                                             exemption_sub_category: row.exemption_sub_category,
//                                             exemption_category: row.employee_exemption_category,
//                                             maximum_exempted_amount: row.maximum_amount,
//                                             declared_amount: row.declared_amount
//                                         })),
//                                         hra_breakup: frm.doc.custom_hra_breakup.map(row => ({
//                                             month: row.month,
//                                             rent_paid: row.rent_paid,
//                                             earned_basic: row.earned_basic,
//                                             hra_received: row.hra_received,
//                                             excess_of_rent_paid: row.excess_of_rent_paid,
//                                             exemption_amount: row.exemption_amount
//                                         }))
//                                     });
                                    
                                    


//                                     d.hide();
//                                 }
//                             });

//                             d.fields_dict.details_table.df.data = [];
//                             component_array.forEach(item => {
//                                 d.fields_dict.details_table.df.data.push({
//                                     exemption_sub_category: item.sub_category,
//                                     employee_exemption_category: item.category,
//                                     maximum_amount: item.max_amount,
//                                     declared_amount: item.amount
//                                 });
//                             });
//                             d.fields_dict.details_table.grid.refresh();

//                             d.show();

//                             // Update employee_exemption_category when exemption_sub_category changes
//                             d.$wrapper.on('change', '[data-fieldname="exemption_sub_category"] select', function() {
//                                 let selectedValue = $(this).val();
//                                 let rowIndex = $(this).closest('.grid-row').index();

//                                 if (selectedValue) {
//                                     frappe.call({
//                                         method: 'frappe.client.get',
//                                         args: {
//                                             doctype: "Employee Tax Exemption Sub Category",
//                                             name: selectedValue
//                                         },
//                                         callback: function(r) {
//                                             if (r.message) {
//                                                 let category = r.message.exemption_category;
//                                                 let category_max_amount=r.message.max_amount;
//                                                 d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category = category;
//                                                 d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount = category_max_amount;
//                                                 d.fields_dict.details_table.grid.refresh();
//                                             }
//                                         }
//                                     });
//                                 }
//                             });

//                             d.$wrapper.on('change', '[data-fieldname="declared_amount"] input', function () {
//                                 let selectedAmount = $(this).val();
//                                 console.log('Selected value in Amount:', selectedAmount);
                                
//                             });

//                         }, 1000);
//                     }
//                 }
//             }
//         });
//     }
// }




// function edit_declaration(frm) {
//     if (frm.doc.employee) {
//         var sub_category = [];

//         frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//                 doctype: "Employee Tax Exemption Sub Category",
//                 filters: {
//                     "is_active": 1,
//                     "name": ["not in", ["Employee Provident Fund (Auto)", "NPS Contribution by Employer", "Tax on employment (Professional Tax)"]]
//                 },
//                 fields: ["*"],
//                 limit_page_length: 999999999999
//             },
//             callback: function(subcategory_response) {
//                 if (subcategory_response.message && subcategory_response.message.length > 0) {
//                     subcategory_response.message.forEach(function(v) {
//                         sub_category.push(v.name);
//                     });
//                 }

//                 if (frm.doc.custom_income_tax === "Old Regime") {
//                     let d = new frappe.ui.Dialog({
//                         title: 'Enter details',
//                         fields: [
//                             {
//                                 label: 'Details Table',
//                                 fieldname: 'details_table',
//                                 fieldtype: 'Table',
//                                 fields: [
//                                     {
//                                         label: 'Exemption Sub Category',
//                                         fieldname: 'exemption_sub_category',
//                                         fieldtype: 'Select',
//                                         options: sub_category,
//                                         in_list_view: 1,
//                                         editable: true
//                                     },
//                                     {
//                                         label: 'Employee Tax Exemption Category',
//                                         fieldname: 'employee_exemption_category',
//                                         fieldtype: 'Data',
//                                         in_list_view: 1,
//                                         read_only: 1
//                                     },
//                                     {
//                                         label: 'Maximum Exempted Amount',
//                                         fieldname: 'maximum_amount',
//                                         fieldtype: 'Currency',
//                                         in_list_view: 1,
//                                         read_only: 1
//                                     },
//                                     {
//                                         label: 'Declared Amount',
//                                         fieldname: 'declared_amount',
//                                         fieldtype: 'Currency',
//                                         in_list_view: 1,
//                                         editable: true,
//                                     },
                                    

//                                 ]
//                             },

//                             {
//                                 fieldtype: 'Section Break'
//                             },
//                             {
//                                 label: 'Monthly HRA Amount',
//                                 fieldname: 'hra_amount',
//                                 fieldtype: 'Currency',
                                
//                             },
//                             {
//                                 fieldtype: 'Column Break'
//                             },
//                             {
//                                 label: 'Rented in Metro City',
//                                 fieldname: 'rented_in_metro_city',
//                                 fieldtype: 'Check',
                                
//                             }
//                         ],
//                         size: 'large',
//                         primary_action_label: 'Submit',
//                         primary_action(values) {
//                             let total_exe_amount = 0;
//                             $.each(frm.doc.declarations, function(i, k) {
//                                 if (k.exemption_category == "Section 80C") {
//                                     total_exe_amount = k.max_amount - k.amount;
//                                 }
//                             });

//                             let total_80C = 0;
//                             $.each(values.details_table, function(i, m) {
//                                 if (m.employee_exemption_category == "Section 80C") {
//                                     total_80C += parseFloat(m.declared_amount);
//                                 }
//                             });

//                             if (total_80C > total_exe_amount) {
//                                 frappe.msgprint(`You can't enter an amount greater than ${total_exe_amount} for Section 80C.`);
//                             } else {
//                                 let component_array = [];

//                                 // Fetch Salary Structure and other values
//                                 frappe.call({
//                                     method: "frappe.client.get_list",
//                                     args: {
//                                         doctype: "Salary Structure Assignment",
//                                         filters: { "employee": frm.doc.employee, "docstatus": 1 },
//                                         fields: ["*"],
//                                         limit: 1,
//                                         order_by: "from_date desc"
//                                     },
//                                     callback: function(res) {
//                                         if (res.message && res.message.length > 0) {
//                                             let salary_structure = res.message[0];

//                                             let promises = [];

//                                             if (salary_structure.custom_is_uniform_allowance == 1) {
//                                                 let value = salary_structure.custom_uniform_allowance_value;
//                                                 if (value) {
//                                                     promises.push(frappe.call({
//                                                         method: "frappe.client.get_list",
//                                                         args: {
//                                                             doctype: "Employee Tax Exemption Sub Category",
//                                                             filters: { "custom_salary_component": "Uniform" },
//                                                             fields: ["*"]
//                                                         },
//                                                         callback: function(response) {
//                                                             if (response.message && response.message.length > 0) {
//                                                                 component_array.push({
//                                                                     "sub_category": response.message[0].name,
//                                                                     "category": response.message[0].exemption_category,
//                                                                     "max_amount": value,
//                                                                     "amount": value
//                                                                 });
//                                                             }
//                                                         }
//                                                     }));
//                                                 }
//                                             }

//                                             if (salary_structure.custom_is_epf == 1) {
//                                                 let epf_amount = Math.round((salary_structure.base * 0.35) / 12 * 0.12);
//                                                 let epf_amount_annual=epf_amount*12
//                                                 if (epf_amount) {
//                                                     promises.push(frappe.call({
//                                                         method: "frappe.client.get_list",
//                                                         args: {
//                                                             doctype: "Employee Tax Exemption Sub Category",
//                                                             filters: { "custom_salary_component": "Employee Provident Fund" },
//                                                             fields: ["*"]
//                                                         },
//                                                         callback: function(kes) {
//                                                             if (kes.message && kes.message.length > 0) {
//                                                                 if (epf_amount_annual>150000)
//                                                                 {
//                                                                     component_array.push({
//                                                                         "sub_category": kes.message[0].name,
//                                                                         "category": kes.message[0].exemption_category,
//                                                                         "max_amount": kes.message[0].max_amount,
//                                                                         "amount": 150000
//                                                                     });
//                                                                 }
//                                                                 else{

//                                                                     component_array.push({
//                                                                         "sub_category": kes.message[0].name,
//                                                                         "category": kes.message[0].exemption_category,
//                                                                         "max_amount": kes.message[0].max_amount,
//                                                                         "amount": epf_amount_annual
//                                                                     });

//                                                                 }
//                                                             }
//                                                         }
//                                                     }));
//                                                 }
//                                             }

//                                             if (salary_structure.custom_is_nps == 1) {
//                                                 let nps_amount = Math.round((((salary_structure.base * 0.35) / 12 * salary_structure.custom_nps_percentage) / 100));
//                                                 let nps_amount_annual=nps_amount*12
//                                                 if (nps_amount) {
//                                                     promises.push(frappe.call({
//                                                         method: "frappe.client.get_list",
//                                                         args: {
//                                                             doctype: "Employee Tax Exemption Sub Category",
//                                                             filters: { "custom_salary_component": "NPS" },
//                                                             fields: ["*"]
//                                                         },
//                                                         callback: function(mes) {
//                                                             if (mes.message && mes.message.length > 0) {
//                                                                 component_array.push({
//                                                                     "sub_category": mes.message[0].name,
//                                                                     "category": mes.message[0].exemption_category,
//                                                                     "max_amount": nps_amount_annual,
//                                                                     "amount": nps_amount_annual
//                                                                 });
//                                                             }
//                                                         }
//                                                     }));
//                                                 }
//                                             }

//                                             if (salary_structure.custom_state) {
//                                                 promises.push(frappe.call({
//                                                     method: "frappe.client.get_list",
//                                                     args: {
//                                                         doctype: "Employee Tax Exemption Sub Category",
//                                                         filters: { "custom_salary_component": "Professional Tax (Gujarat)" },
//                                                         fields: ["*"]
//                                                     },
//                                                     callback: function(jes) {
//                                                         if (jes.message && jes.message.length > 0) {
//                                                             component_array.push({
//                                                                 "sub_category": jes.message[0].name,
//                                                                 "category": jes.message[0].exemption_category,
//                                                                 "max_amount": jes.message[0].max_amount,
//                                                                 "amount": jes.message[0].max_amount
//                                                             });
//                                                         }
//                                                     }
//                                                 }));
//                                             }

//                                             // Add dialog box values to component_array
//                                             $.each(values.details_table, function(i, w) {
//                                                 component_array.push({
//                                                     "sub_category": w.exemption_sub_category,
//                                                     "category": w.employee_exemption_category,
//                                                     "max_amount": w.maximum_amount,
//                                                     "amount": w.declared_amount
//                                                 });
//                                             });

//                                             // Wait for all async calls to finish
//                                             Promise.all(promises).then(() => {
//                                                 // Now update the child table
//                                                 frm.clear_table('declarations');
//                                                 frm.refresh_field('declarations');

//                                                 component_array.forEach(row => {
//                                                     let new_row = frm.add_child('declarations');
//                                                     new_row.exemption_sub_category = row.sub_category;
//                                                     new_row.exemption_category = row.category;
//                                                     new_row.max_amount = row.max_amount;
//                                                     new_row.amount = row.amount;
//                                                 });

//                                                 frm.refresh_field('declarations');
//                                                 frm.set_value("monthly_house_rent",values.hra_amount)
//                                                 frm.set_value("rented_in_metro_city",values.rented_in_metro_city)
//                                                 frm.save('Update');
//                                                 d.hide();
//                                             });
//                                         }
//                                     }
//                                 });
//                             }
//                         }
//                     });

//                     d.show();

//                     // Update employee_exemption_category when exemption_sub_category changes
//                     d.$wrapper.on('change', '[data-fieldname="exemption_sub_category"] select', function() {
//                         let selectedValue = $(this).val();
//                         let rowIndex = $(this).closest('.grid-row').index();

//                         if (selectedValue) {
//                             frappe.call({
//                                 method: 'frappe.client.get',
//                                 args: {
//                                     doctype: "Employee Tax Exemption Sub Category",
//                                     name: selectedValue
//                                 },
//                                 callback: function(r) {
//                                     if (r.message) {
//                                         let category = r.message.exemption_category;
//                                         let category_max_amount = r.message.max_amount;
//                                         d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category = category;
//                                         d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount = category_max_amount;
//                                         d.fields_dict.details_table.grid.refresh();
//                                     }
//                                 }
//                             });
//                         }
//                     });

//                     d.$wrapper.on('change', '[data-fieldname="declared_amount"] input', function() {
//                         let rowIndex = $(this).closest('.grid-row').index();
//                         let selectedAmount = parseFloat($(this).val());
//                         let maxAmount = parseFloat(d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.maximum_amount);
//                         let component = d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.employee_exemption_category;

//                         if (component == "Section 80C") {
//                             $.each(frm.doc.declarations, function(i, v) {
//                                 if (v.exemption_category == component) {
//                                     if (v.amount == 150000) {
//                                         frappe.msgprint("You can't enter the amount here because your Section 80C is at the maximum.");
//                                         d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.declared_amount = undefined;
//                                         d.fields_dict.details_table.grid.refresh();
//                                     } else {
//                                         let remainingAmount = maxAmount - parseFloat(v.amount);

//                                         if (selectedAmount > remainingAmount) {
//                                             frappe.msgprint(`You can't enter an amount greater than ${remainingAmount}.`);
//                                             d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.declared_amount = undefined;
//                                             d.fields_dict.details_table.grid.refresh();
//                                         }
//                                     }
//                                 }
//                             });
//                         } else {
//                             if (selectedAmount > maxAmount) {
//                                 frappe.msgprint(`You can't enter an amount greater than ${maxAmount}.`);
//                                 d.fields_dict.details_table.grid.grid_rows[rowIndex].doc.declared_amount = undefined;
//                                 d.fields_dict.details_table.grid.refresh();
//                             }
//                         }
//                     });
//                 } else {
//                     frappe.msgprint("You can't Edit the declaration because you are in the New regime.");
//                 }
//             }
//         });
//     }
// }





