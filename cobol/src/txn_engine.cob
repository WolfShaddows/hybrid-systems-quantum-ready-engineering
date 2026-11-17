       *> Purpose: COBOL transaction-rule engine. Expected: validate one account operation, enforce balance boundaries, and return a machine-readable decision.
       IDENTIFICATION DIVISION.
       PROGRAM-ID. TXN-ENGINE.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 ARG-COUNT PIC 9(4) COMP-5.
       01 ACCOUNT-ID PIC X(32).
       01 OPERATION PIC X(8).
       01 AMOUNT-TEXT PIC X(9).
       01 BALANCE-TEXT PIC X(18).
       01 AMOUNT-CENTS PIC 9(9) COMP-5.
       01 CURRENT-BALANCE PIC 9(18) COMP-5.
       01 NEW-BALANCE PIC 9(18) COMP-5.
       01 MAX-BALANCE PIC 9(18) VALUE 999999999999999999.
       01 DISPLAY-BALANCE PIC 9(18).
       PROCEDURE DIVISION.
           PERFORM MAIN-PROCEDURE
           GOBACK.
       MAIN-PROCEDURE.
           *> Stage 1: read the fixed argument contract supplied by the Rust adapter.
           ACCEPT ARG-COUNT FROM ARGUMENT-NUMBER
           IF ARG-COUNT NOT = 4
               DISPLAY 'ERROR|BAD_ARGUMENT_COUNT'
               MOVE 2 TO RETURN-CODE
               GOBACK
           END-IF
           ACCEPT ACCOUNT-ID FROM ARGUMENT-VALUE
           ACCEPT OPERATION FROM ARGUMENT-VALUE
           ACCEPT AMOUNT-TEXT FROM ARGUMENT-VALUE
           ACCEPT BALANCE-TEXT FROM ARGUMENT-VALUE
           *> Stage 2: reject malformed identifiers and numeric fields before arithmetic.
           IF ACCOUNT-ID = SPACES OR AMOUNT-TEXT IS NOT NUMERIC
               OR BALANCE-TEXT IS NOT NUMERIC
               DISPLAY 'ERROR|BAD_REQUEST'
               MOVE 2 TO RETURN-CODE
               GOBACK
           END-IF
           IF OPERATION NOT = 'CREDIT' AND OPERATION NOT = 'DEBIT'
               DISPLAY 'ERROR|BAD_OPERATION'
               MOVE 2 TO RETURN-CODE
               GOBACK
           END-IF
           MOVE AMOUNT-TEXT TO AMOUNT-CENTS
           MOVE BALANCE-TEXT TO CURRENT-BALANCE
           IF AMOUNT-CENTS = 0
               DISPLAY 'ERROR|BAD_AMOUNT'
               MOVE 2 TO RETURN-CODE
               GOBACK
           END-IF
           *> Stage 3: compute the new balance and guard debit/credit boundaries.
           IF OPERATION = 'DEBIT'
               IF AMOUNT-CENTS > CURRENT-BALANCE
                   MOVE CURRENT-BALANCE TO DISPLAY-BALANCE
                   DISPLAY 'REJECTED_INSUFFICIENT_FUNDS|'
                       DISPLAY-BALANCE
                   MOVE 0 TO RETURN-CODE
                   GOBACK
               END-IF
               COMPUTE NEW-BALANCE = CURRENT-BALANCE - AMOUNT-CENTS
           ELSE
               IF CURRENT-BALANCE > MAX-BALANCE - AMOUNT-CENTS
                   DISPLAY 'REJECTED_BALANCE_OVERFLOW|'
                       CURRENT-BALANCE
                   MOVE 0 TO RETURN-CODE
                   GOBACK
               END-IF
               COMPUTE NEW-BALANCE = CURRENT-BALANCE + AMOUNT-CENTS
           END-IF
           *> Stage 4: emit the machine-readable decision for independent Java validation.
           MOVE NEW-BALANCE TO DISPLAY-BALANCE
           DISPLAY 'POSTED|' DISPLAY-BALANCE
           MOVE 0 TO RETURN-CODE
           GOBACK.






