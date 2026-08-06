package com.example.repository;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import com.example.db.MySqlConnectionFactory;
import com.example.entity.Account;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JdbcAccountRepository implements AccountRepository {
    private static final Logger logger = LoggerFactory.getLogger(JdbcAccountRepository.class);
    
    public JdbcAccountRepository() {
        logger.info("JdbcAccountRepository initialized");
    }

    @Override
    public Account findByAccountNumber(String accountNumber) {
        logFindAction(accountNumber);
        logger.info("Fetching account from DB for accountNumber={}", accountNumber);
        Connection connection=null;
        try{
             connection = MySqlConnectionFactory.getConnection();
            String query = "SELECT * FROM accounts WHERE account_number = ?";
            PreparedStatement preparedStatement = connection.prepareStatement(query);
            preparedStatement.setString(1, accountNumber);
            ResultSet resultSet = preparedStatement.executeQuery();
            if (resultSet.next()) {
                Account account = new Account();
                account.setAccountNumber(resultSet.getString("account_number"));
                account.setBalance(resultSet.getDouble("balance"));
                logger.info("Account found for accountNumber={}", accountNumber);
                return account;
            } else {
                logger.warn("Account not found for accountNumber={}", accountNumber);
                return null; // Account not found
            }
        }catch(Exception e){
            logger.error("Error while finding account by account number={}", accountNumber, e);
            throw new RuntimeException("Error finding account by account number", e);
        }finally{
            if(connection!=null){
                try{
                    connection.close();
                    logger.info("Database connection closed after find action for accountNumber={}", accountNumber);
                }catch(Exception e){
                    logger.error("Error closing database connection after find action", e);
                    throw new RuntimeException("Error closing database connection", e);
                }
            }
        }
    }
    public void update(Account account) {
        logUpdateAction(account);
        logger.info("Updating account balance in DB for accountNumber={} with newBalance={}", account.getAccountNumber(), account.getBalance());
        Connection connection=null;
        try{
             connection = MySqlConnectionFactory.getConnection();
            String query = "UPDATE accounts SET balance = ? WHERE account_number = ?";
            PreparedStatement preparedStatement = connection.prepareStatement(query);
            preparedStatement.setDouble(1, account.getBalance());
            preparedStatement.setString(2, account.getAccountNumber());
            preparedStatement.executeUpdate();
            logger.info("Account update completed for accountNumber={}", account.getAccountNumber());
        }catch(Exception e){
            logger.error("Error updating account for accountNumber={}", account.getAccountNumber(), e);
            throw new RuntimeException("Error updating account", e);
        }finally{
            if(connection!=null){
                try{
                    connection.close();
                    logger.info("Database connection closed after update action for accountNumber={}", account.getAccountNumber());
                }catch(Exception e){
                    logger.error("Error closing database connection after update action", e);
                    throw new RuntimeException("Error closing database connection", e);
                }
            }
        }
    }
    
}
