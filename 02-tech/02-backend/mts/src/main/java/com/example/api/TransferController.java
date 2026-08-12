package com.example.api;

import org.springframework.web.bind.annotation.RestController;

import com.example.dto.TransferRequest;
import com.example.dto.TransferResponse;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;


@RestController
public class TransferController {

    private final com.example.service.TransferService transferService;

    public TransferController(com.example.service.TransferService transferService) {
        this.transferService = transferService;
    }

    @PostMapping(value="/api/v1/transfer",consumes = "application/json", produces = "application/json")
    public TransferResponse transfer(@RequestBody TransferRequest transferRequest) {
        transferService.transfer(transferRequest.getFromAccountNumber(), transferRequest.getToAccountNumber(), transferRequest.getAmount());
        TransferResponse transferResponse = new TransferResponse();
        transferResponse.setTxnId("TXN123456");
        transferResponse.setStatus("SUCCESS");
        transferResponse.setMessage("Transfer successful");
        return transferResponse;
    }
    
    
}
