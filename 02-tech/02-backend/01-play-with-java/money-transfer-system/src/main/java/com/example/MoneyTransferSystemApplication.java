package com.example;

import com.example.db.MySqlConnectionFactory;
import com.example.repository.AccountRepository;
import com.example.repository.JdbcAccountRepository;
import com.example.service.TransferService;
import com.example.service.UpiTransferService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MoneyTransferSystemApplication {
    private static final Logger logger = LoggerFactory.getLogger(MoneyTransferSystemApplication.class);

    public static void main(String[] args) {
        logger.info("Starting Money Transfer System application");

        //------------------------------------------
        // Init / boot
        //------------------------------------------

        logger.info("Initializing repository and transfer service");
        AccountRepository jdbcAccountRepository = new JdbcAccountRepository();
        TransferService upiTransferService = new UpiTransferService(jdbcAccountRepository);

        //------------------------------------------
        // Use
        //------------------------------------------

        try {
            logger.info("Triggering transfer action: amount={}, from={}, to={}", 100.00, "ACC123", "ACC456");
            upiTransferService.transfer(100.00, "ACC123", "ACC456");
            logger.info("Transfer action completed successfully");
        } catch (RuntimeException e) {
            logger.error("Transfer action failed", e);
            throw e;
        } finally {
            MySqlConnectionFactory.shutdown();
        }


        //------------------------------------------
        // Shutdown / cleanup
        //------------------------------------------
        logger.info("Shutting down Money Transfer System application");

    }
}