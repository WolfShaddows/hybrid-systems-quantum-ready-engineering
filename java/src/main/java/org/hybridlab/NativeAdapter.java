// Purpose: NativeAdapter (java/src/main/java/org/hybridlab/NativeAdapter.java). Expected: validate API input, coordinate decisions and journal, and return a structured response.
package org.hybridlab;

import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.ptr.IntByReference;
import com.sun.jna.ptr.LongByReference;

/** Thin C ABI/JNA boundary. No Rust-owned memory crosses this interface. */
public final class NativeAdapter {
    private interface DecisionLibrary extends Library {
        int hybrid_decide(String account, String operation, long amountCents, long currentBalance,
                          LongByReference outBalance, IntByReference outStatus);
    }
    private static final DecisionLibrary LIBRARY = load();
    private NativeAdapter() {}

    private static DecisionLibrary load() {
        String path=System.getenv("RUST_LIBRARY");
        if(path==null||path.isBlank()) throw new IllegalStateException("RUST_LIBRARY is not set");
        return Native.load(path,DecisionLibrary.class);
    }

    public static String decide(String account,String operation,long amount,long balance) {
        LongByReference outBalance=new LongByReference();
        IntByReference outStatus=new IntByReference();
        int result=LIBRARY.hybrid_decide(account,operation,amount,balance,outBalance,outStatus);
        if(result!=0) throw new IllegalStateException("Rust FFI decision failed: "+result);
        String label=switch(outStatus.getValue()) {
            case 0 -> "POSTED";
            case 1 -> "REJECTED_INSUFFICIENT_FUNDS";
            case 2 -> "REJECTED_BALANCE_OVERFLOW";
            default -> throw new IllegalStateException("Unknown Rust FFI status");
        };
        return label+"|"+String.format("%018d",outBalance.getValue());
    }
}



