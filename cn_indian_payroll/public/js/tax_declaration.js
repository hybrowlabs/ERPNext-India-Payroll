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
frappe.ui.form.on('Employee Tax Exemption Declaration', {
    refresh:function(frm)
    {
              if (frm.doc.custom_tax_regime === "New Regime") {
                    frm.set_df_property('declarations', 'read_only', 1);
                    frm.set_df_property("custom_declaration_form","hidden",1)
                }

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
                          isUpdating = false;
                      });
                  })
                  .catch((err) => {
                      console.error("Error creating Form.io form:", err);
                  });

                }




        if (!frm.is_new())
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
                    size: 'small',
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
        process_form_data(frm);

      }
    },


});


async function process_form_data(frm) {
  const form_data = JSON.parse(frm.doc.custom_declaration_form_data || '{}');

  if (["Approved", "Pending"].includes(frm.doc.custom_status)) {
      let declarations = [];

      if (frm.doc.custom_tax_regime === "Old Regime") {
          let mediclaim_self_below = parseFloat(form_data["amount"] || 0);
          let mediclaim_self_above = parseFloat(form_data["amount3"] || 0);
          let mediclaim_parent_below = parseFloat(form_data["mpAmount3"] || 0);
          let mediclaim_parent_above = parseFloat(form_data["mpAmount4"] || 0);
          let heal_self = parseFloat(form_data["mp5"] || 0);
          let heal_parent = parseFloat(form_data["mpAmount6"] || 0);

          let limit_self_below = 25000,
              limit_self_above = 50000,
              limit_parent_below = 25000,
              limit_parent_above = 50000,
              limit_health_checkup_total = 5000;

          let eligible_self_below = Math.min(mediclaim_self_below, limit_self_below);
          let eligible_self_above = Math.min(mediclaim_self_above, limit_self_above);
          let eligible_parent_below = Math.min(mediclaim_parent_below, limit_parent_below);
          let eligible_parent_above = Math.min(mediclaim_parent_above, limit_parent_above);

          let eligible_heal_self = Math.min(
              heal_self,
              limit_self_below - eligible_self_below,
              limit_self_above - eligible_self_above
          );
          let eligible_heal_parent = Math.min(
              heal_parent,
              limit_parent_below - eligible_parent_below,
              limit_parent_above - eligible_parent_above
          );

          let total_health_checkup = eligible_heal_self + eligible_heal_parent;
          if (total_health_checkup > limit_health_checkup_total) {
              if (eligible_heal_self >= limit_health_checkup_total) {
                  eligible_heal_self = limit_health_checkup_total;
                  eligible_heal_parent = 0;
              } else {
                  eligible_heal_parent = limit_health_checkup_total - eligible_heal_self;
              }
          }

          form_data["amount"] = eligible_self_below;
          form_data["amount3"] = eligible_self_above;
          form_data["mpAmount3"] = eligible_parent_below;
          form_data["mpAmount4"] = eligible_parent_above;
          form_data["mp5"] = eligible_heal_self;
          form_data["mpAmount6"] = eligible_heal_parent;
      }

      const numbers = frm.doc.custom_tax_regime === "Old Regime" ? [
          { field: "amount", name: "Mediclaim Self, Spouse & Children (Below 60 years)" },
          { field: "amount3", name: "Mediclaim Self (Senior Citizen - 60 years & above)" },
          { field: "mpAmount3", name: "Parents (Below 60 years)" },
          { field: "mpAmount4", name: "Parents (Senior Citizen - 60 years & above)" },
          { field: "mp5", name: "Preventive Checkup (Self + Family)" },
          { field: "mpAmount6", name: "Preventive Checkup (Parents)" },
          { field: "hlAmount", name: "Interest Paid On Home Loan" },
          { field: "pfValue", name: "Investments In PF(Auto)" },
          { field: "aValue2", name: "Pension Scheme Investments & ULIP" },
          { field: "bValue1", name: "Housing Loan Principal Repayment" },
          { field: "amount4", name: "PPF - Public Provident Fund" },
          { field: "dValue1", name: "Home Loan Account Of National Housing Bank" },
          { field: "eValue1", name: "LIC- Life Insurance Premium Directly Paid By Employee" },
          { field: "fValue1", name: "NSC - National Saving Certificate" },
          { field: "gValue1", name: "Mutual Funds - Notified Under Clause 23D Of Section 10" },
          { field: "hValue1", name: "ELSS - Equity Link Saving Scheme Of Mutual Funds" },
          { field: "iValue1", name: "Tuition Fees For Full Time Education" },
          { field: "jValue1", name: "Fixed Deposits In Banks (Period As Per Income Tax Guidelines)" },
          { field: "kValue1", name: "5 Years Term Deposit An Account Under Post Office Term Deposit Rules" },
          { field: "kValue2", name: "Others" },
          { field: "fourValue", name: "(Medical treatment / insurance of handicapped dependant)" },
          { field: "fiveNumber", name: "Medical treatment (specified diseases only)" },
          { field: "sixNumber", name: "Interest repayment of Loan for higher education" },
          { field: "sevenNumber", name: "Deduction for Physically Disabled" },
          { field: "eightNumber", name: "Donation U/S 80G" },
          { field: "nineNumber", name: "NPS Deduction U/S 80CCD(2)(Employer NPS deduction)" },
          { field: "tenNumber", name: "First HSG Loan Interest Ded.(80EE)" },
          { field: "elevenNumber", name: "Contribution in National Pension Scheme" },
          { field: "twelveNumber1", name: "Tax Incentive for Affordable Housing for Ded U/S 80EEA" },
          { field: "fifteenNumber", name: "Tax Incentives for Electric Vehicles for Ded U/S 80EEB" },
          { field: "sixteenNumber", name: "Donations/contribution made to a political party or an electoral trust" },
          { field: "seventeenNumber", name: "Interest on deposits in saving account for Ded U/S 80TTA" },
          { field: "eighteenNumber", name: "Interest on deposits in saving account for Ded U/S 80TTB" },
          { field: "nineteenNumber", name: "P.T. Paid by employee" },
          { field: "twentyNumber", name: "Deduction U/S 80GG" },
          { field: "twentyoneNumber", name: "Rajiv Gandhi Equity Saving Scheme 80CCG" },
          { field: "twentyFour", name: "Uniform Allowance" },
          { field: "thirteen", name: "Education Allowance" },
          { field: "twentysix", name: "Hostel Allowance" },
          { field: "twentyseven", name: "Gratuity" },
          { field: "twentyeight", name: "LTA U/s 10 (5)" },
      ] : [
          { field: "nineNumber", name: "NPS Deduction U/S 80CCD(2)(Employer NPS deduction)" }
      ];

      for (let item of numbers) {
          const value = parseFloat(form_data[item.field] || 0);
          if (value <= 0) continue;

          await frappe.call({
              method: "frappe.client.get_list",
              args: {
                  doctype: "Employee Tax Exemption Sub Category",
                  filters: { is_active: 1, name: item.name },
                  fields: ["name", "exemption_category", "max_amount"]
              },
              async callback(r) {
                  if (r.message && r.message.length > 0) {
                      declarations.push({
                          exemption_sub_category: r.message[0].name,
                          exemption_category: r.message[0].exemption_category,
                          max_amount: r.message[0].max_amount,
                          amount: value
                      });
                  }
              }
          });
      }

      frm.clear_table("declarations");
      declarations.forEach(row => {
          frm.add_child("declarations", row);
      });
      frm.refresh_field("declarations");
  }
}
