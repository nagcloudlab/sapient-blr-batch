package com.example.repository;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

import javax.sql.DataSource;

import com.example.entity.Account;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.jdbc.core.JdbcTemplate;

public class JdbcAccountRepository implements AccountRepository {
    private static final Logger logger = LoggerFactory.getLogger(JdbcAccountRepository.class);
    
    private JdbcTemplate jdbcTemplate;
    
    public JdbcAccountRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
        logger.info("JdbcAccountRepository initialized");
    }

    @Override
    public Account findByAccountNumber(String accountNumber) {
        String sql = "SELECT * FROM accounts WHERE account_number = ?";
        return jdbcTemplate.query(sql, new Object[]{accountNumber}, rs -> {
            if (rs.next()) {
                Account account = new Account();
                account.setAccountNumber(rs.getString("account_number"));
                account.setBalance(rs.getDouble("balance"));
                return account;
            }
            return null;
        });
    }
    public void update(Account account) {
        String sql = "UPDATE accounts SET balance = ? WHERE account_number = ?";
        jdbcTemplate.update(sql, account.getBalance(), account.getAccountNumber());
    }
    
}
