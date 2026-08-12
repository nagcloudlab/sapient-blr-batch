package com.example.dto;

import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
public class TransferResponse {

    private String txnId;
    private String status;
    private String message;
    
}
