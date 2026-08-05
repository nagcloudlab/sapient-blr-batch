package com.example;

import org.slf4j.Logger;

import com.example.repository.AccountRepository;
import com.example.repository.AccountRepositoryFactory;
import com.example.service.UpiTransferService;

public class MoneyTransferSystemApplication {

    private static Logger logger = org.slf4j.LoggerFactory.getLogger("mts");

    public static void main(String[] args){
        
        //----------------------------------------------
        // phase-1 :  init / bootstrap the application
        //----------------------------------------------
        logger.info("----------------------------------------------------");
        logger.info("Money Transfer System Application is starting...");
        // - create & wire-up all the components (beans) of the application based on the configuration
        AccountRepository sqlAccountRepository = AccountRepositoryFactory.createAccountRepository("SQL");
        UpiTransferService upiTransferService = new UpiTransferService(sqlAccountRepository); // DI
        

        logger.info("Money Transfer System Application has started successfully...");
        logger.info("----------------------------------------------------");
        //----------------------------------------------
        // phase-2 :  run/use the application
        //----------------------------------------------

        upiTransferService.transfer(100.00, "1", "2");
        logger.info("------------------------------");
        upiTransferService.transfer(100.00, "2", "1");


        //----------------------------------------------
        // phase-3 :  shutdown the application
        //----------------------------------------------
        logger.info("----------------------------------------------------");
        // - release all the resources held by the application
        logger.info("----------------------------------------------------");


    }
}
