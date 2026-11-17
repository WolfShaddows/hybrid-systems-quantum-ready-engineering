// Purpose: TransactionResource (java/src/main/java/org/hybridlab/TransactionResource.java). Expected: validate API input, coordinate decisions and journal, and return a structured response.
package org.hybridlab;

import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

@Path("/")
@Produces(MediaType.APPLICATION_JSON)
public final class TransactionResource {
    @GET
    @Path("health")
    public Response health() {
        return Response.ok("{\"status\":\"ok\",\"ledger\":\"append-only-hash-chain\",\"single_writer_lock\":true,\"decision_adapter\":\"" + (System.getenv("RUST_LIBRARY") == null ? "process" : "native-ffi") + "\"}").build();
    }

    @POST
    @Path("transactions")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response transaction(String body) {
        Main.ApiResponse result = Main.submitJson(body);
        return Response.status(result.status()).entity(result.body()).build();
    }
}




