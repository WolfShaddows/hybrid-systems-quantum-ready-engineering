// Purpose: lib (rust/src/lib.rs). Expected: validate native inputs, execute the adapter operation, and return a checked result or stable error.
use std::{env, ffi::{CStr, c_char}, panic::{AssertUnwindSafe, catch_unwind}, process::Command, ptr};

fn valid_identifier(value: &str, max_len: usize) -> bool {
    !value.is_empty() && value.len() <= max_len && value.bytes().all(|b| b.is_ascii_alphanumeric() || b == b'_' || b == b'-')
}

pub fn evaluate(account: &str, operation: &str, amount: u64, balance: u64) -> Result<(u32, u64), &'static str> {
    if !valid_identifier(account, 32) { return Err("invalid account_id"); }
    if operation != "CREDIT" && operation != "DEBIT" { return Err("invalid operation"); }
    if amount == 0 || amount > 999_999_999 { return Err("amount outside supported range"); }
    if balance > 999_999_999_999_999_999 { return Err("balance outside supported range"); }
    let engine = env::var_os("COBOL_ENGINE").ok_or("COBOL_ENGINE is not set")?;
    let output = Command::new(engine).args([account,operation,&format!("{amount:09}"),&format!("{balance:018}")]).output().map_err(|_| "could not start COBOL engine")?;
    if !output.status.success() { return Err("COBOL engine returned a failure status"); }
    let response=String::from_utf8(output.stdout).map_err(|_| "COBOL output was not UTF-8")?;
    let mut fields=response.trim().split('|');
    let status=fields.next().ok_or("missing COBOL status")?;
    let value=fields.next().ok_or("missing COBOL balance")?;
    if fields.next().is_some()||value.len()!=18||!value.bytes().all(|b|b.is_ascii_digit()){return Err("malformed COBOL response")}
    let balance=value.parse::<u64>().map_err(|_|"invalid COBOL balance")?;
    let code=match status{"POSTED"=>0,"REJECTED_INSUFFICIENT_FUNDS"=>1,"REJECTED_BALANCE_OVERFLOW"=>2,_=>return Err("unrecognized COBOL response")};
    Ok((code,balance))
}

// C ABI used by Java/JNA. Borrowed strings and fixed-width scalars cross the boundary;
// all allocations and COBOL process orchestration remain on the Rust side.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn hybrid_decide(account_ptr:*const c_char,operation_ptr:*const c_char,amount:u64,current_balance:u64,out_balance:*mut u64,out_status:*mut u32)->i32 {
    if account_ptr.is_null()||operation_ptr.is_null()||out_balance.is_null()||out_status.is_null(){return -1;}
    let result=catch_unwind(AssertUnwindSafe(||{
        let account=unsafe{CStr::from_ptr(account_ptr)}.to_str().map_err(|_|"account is not UTF-8")?;
        let operation=unsafe{CStr::from_ptr(operation_ptr)}.to_str().map_err(|_|"operation is not UTF-8")?;
        evaluate(account,operation,amount,current_balance)
    }));
    match result {
        Ok(Ok((status,balance)))=>{unsafe{ptr::write(out_balance,balance);ptr::write(out_status,status);}0}
        _=>-2,
    }
}



