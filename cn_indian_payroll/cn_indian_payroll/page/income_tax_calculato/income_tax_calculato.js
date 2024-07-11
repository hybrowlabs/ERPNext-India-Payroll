frappe.pages['income-tax-calculato'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Income Tax Calculator',
		single_column: true
	});
	var template_str = frappe.render_template('income_tax_calculator');
	$(".layout-main-section").empty().append(template_str);
	// $("#body").empty().append(template_str);
	$("input[data-type='currency']").on({
		keyup: function() {
		  formatCurrency($(this));
		},
		blur: function() { 
		  formatCurrency($(this), "blur");
		}
	});
	$("#tableblock").hide();
}
// Jquery Dependency




function formatNumber(n) {
  // format number 1000000 to 1,234,567
  return n.replace(/\D/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}


function formatCurrency(input, blur) {
  // appends $ to value, validates decimal side
  // and puts cursor back in right position.
  
  // get input value
  var input_val = input.val();
  
  // don't validate empty input
  if (input_val === "") { return; }
  
  // original length
  var original_len = input_val.length;

  // initial caret position 
  var caret_pos = input.prop("selectionStart");
    
  // check for decimal
  if (input_val.indexOf(".") >= 0) {

    // get position of first decimal
    // this prevents multiple decimals from
    // being entered
    var decimal_pos = input_val.indexOf(".");

    // split number by decimal point
    var left_side = input_val.substring(0, decimal_pos);
    var right_side = input_val.substring(decimal_pos);

    // add commas to left side of number
    left_side = formatNumber(left_side);

    // validate right side
    right_side = formatNumber(right_side);
    
    // On blur make sure 2 numbers after decimal
    if (blur === "blur") {
      right_side += "00";
    }
    
    // Limit decimal to only 2 digits
    right_side = right_side.substring(0, 2);

    // join number by .
    input_val = '₹ '+left_side + "." + right_side;

  } else {
    // no decimal entered
    // add commas to number
    // remove all non-digits
    input_val = formatNumber(input_val);
    input_val = '₹ '+input_val;
    
    // final formatting
    if (blur === "blur") {
      input_val += ".00";
    }
  }
  
  // send updated string to input
  input.val(input_val);

  // put caret back in the right position
  var updated_len = input_val.length;
  caret_pos = updated_len - original_len + caret_pos;
  input[0].setSelectionRange(caret_pos, caret_pos);
}



function calculatetax(){
	$("#tableblock").hide();
	var total_deduction =  (parseInt(document.getElementById('80c').value.replace(/[^0-9.-]+/g,"")) || 0 )+ (parseInt(document.getElementById('nps').value.replace(/[^0-9.-]+/g,"")) || 0)+ (parseInt(document.getElementById('hra').value.replace(/[^0-9.-]+/g,"")) || 0)+( parseInt(document.getElementById('otherdeduction').value.replace(/[^0-9.-]+/g,"")) || 0)+ (parseInt(document.getElementById('80d').value.replace(/[^0-9.-]+/g,"")) || 0)
  	var enteredAmount = total_deduction+parseInt(50000);
  	var rupeesFormat = '₹ ' + enteredAmount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
	$("#totaldeduction").html(rupeesFormat)
	var total_income =  (parseInt(document.getElementById('salaryincome').value.replace(/[^0-9.-]+/g,"")) || 0) +  (parseInt(document.getElementById('otherincome').value.replace(/[^0-9.-]+/g,"")) || 0)
	
	frappe.call({
		method: 'cn_indian_payroll.cn_indian_payroll.tax_utils.income_tax_calculator_template',
		args: {
			'total_income':total_income,
			'deduction':enteredAmount
		},
		callback: function(r) {
			if(r.message=="No Data Found"){
				$(".form-control").val(null);
				$("#totaldeduction").html("0.0");
				$("#totaldeduction").css({
					'color': 'black'
				  });
				$("#calculations").empty().append("<center><h1>"+r.message+"</h1></center>")
			}
			else{
				$("#tableblock").show();
				$("#totaldeduction").css({
					'color': 'red'
				  });
				$("#calculations").empty().append(r.message)
			}
			let table = document.getElementById('calctable');
			let oldregimeCell = table.rows[7].cells[1];
			let newregimeCell = table.rows[7].cells[2];
			let oldtaxableincomeCell = table.rows[4].cells[1];
			let newtaxableincomeCell = table.rows[4].cells[2];
			$("#oldtaxableincome").empty().append('<h5 style="margin-top:10px;margin-left:10px">Taxable Income</h5><p style="text-align:center"><i class="fa fa-inr"></i>'+oldtaxableincomeCell.textContent+'</p>')
			$("#newtaxableincome").empty().append('<h5 style="margin-top:10px;margin-left:10px">Taxable Income</h5><p style="text-align:center"><i class="fa fa-inr"></i>'+newtaxableincomeCell.textContent+'</p>')
			$("#oldtotaltax").empty().append('<h5 style="margin-top:10px;margin-left:10px">Total Tax</h5><p style="text-align:center"><i class="fa fa-inr"></i>'+oldregimeCell.textContent+'</p>')
			$("#newtotaltax").empty().append('<h5 style="margin-top:10px;margin-left:10px">Total Tax</h5><p style="text-align:center"><i class="fa fa-inr"></i>'+newregimeCell.textContent+'</p>')
			
			if(parseInt(oldregimeCell.textContent)>parseInt(newregimeCell.textContent)){
				$("#newtotaltax").css({
					"border-radius": '10px',
					'width':'140px',
					'height': '80px',
					'border-top': '0.5px solid #DF0101',
					'border-right': '0.5px solid #DF0101',
					'border-bottom': '7px solid #DF0101',
					'border-left': '0.5px solid #DF0101',
					'background': 'linear-gradient(180deg, #FFF 0%, #ECAAAA 100%)',
					'box-shadow': '6px 6px 6px 0px rgba(0, 0, 0, 0.25)',
				})
				$("#oldtotaltax").css({
					"border-radius": '10px',
					'width':'140px',
					'height': '80px',
					'border-top': '0.5px solid #53BC5E',
					'border-right': '0.5px solid #53BC5E',
					'border-bottom': '7px solid #53BC5E',
					'border-left': '0.5px solid #53BC5E',
					'background': 'linear-gradient(180deg, #FFF 0%, #D7FDD4 100%)',
					'box-shadow': '6px 6px 6px 0px rgba(0, 0, 0, 0.25)',
				})
			}
			else{
				$("#oldtotaltax").css({
					"border-radius": '10px',
					'width':'140px',
					'height': '80px',
					'border-top': '0.5px solid #DF0101',
					'border-right': '0.5px solid #DF0101',
					'border-bottom': '7px solid #DF0101',
					'border-left': '0.5px solid #DF0101',
					'background': 'linear-gradient(180deg, #FFF 0%, #ECAAAA 100%)',
					'box-shadow': '6px 6px 6px 0px rgba(0, 0, 0, 0.25)',
				})
				$("#newtotaltax").css({
					"border-radius": '10px',
					'width':'140px',
					'height': '80px',
					'border-top': '0.5px solid #53BC5E',
					'border-right': '0.5px solid #53BC5E',
					'border-bottom': '7px solid #53BC5E',
					'border-left': '0.5px solid #53BC5E',
					'background': 'linear-gradient(180deg, #FFF 0%, #D7FDD4 100%)',
					'box-shadow': '6px 6px 6px 0px rgba(0, 0, 0, 0.25)',
				})
			}
		}
	});
}


