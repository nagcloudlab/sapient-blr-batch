package com.example.dto;

import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
public class TransferRequest {

    private String fromAccountNumber;
    private String toAccountNumber;
    private double amount;
    
}
