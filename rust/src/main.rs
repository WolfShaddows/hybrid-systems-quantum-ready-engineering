// Purpose: main (rust/src/main.rs). Expected: validate native inputs, execute the adapter operation, and return a checked result or stable error.
use std::{env, process::ExitCode};
use hybrid_rust_adapter::evaluate;

fn run()->Result<String,&'static str>{
    let args:Vec<String>=env::args().skip(1).collect();
    if args.len()!=4{return Err("expected account_id operation amount_cents balance_cents")}
    let amount=args[2].parse::<u64>().map_err(|_|"amount is not an integer")?;
    let balance=args[3].parse::<u64>().map_err(|_|"balance is not an integer")?;
    let(status,value)=evaluate(&args[0],&args[1],amount,balance)?;
    let label=match status{0=>"POSTED",1=>"REJECTED_INSUFFICIENT_FUNDS",_=>"REJECTED_BALANCE_OVERFLOW"};
    Ok(format!("{label}|{value:018}"))
}
fn main()->ExitCode{match run(){Ok(value)=>{println!("{value}");ExitCode::SUCCESS},Err(e)=>{eprintln!("adapter error: {e}");ExitCode::from(2)}}}



