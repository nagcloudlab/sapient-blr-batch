package com.example.config;

import javax.sql.DataSource;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;

import com.example.repository.AccountRepository;
import com.example.repository.JdbcAccountRepository;
import com.example.service.TransferService;
import com.example.service.UpiTransferService;
import com.zaxxer.hikari.HikariDataSource;

@Configuration
public class MtsConfiguration {

    
    @Bean
    public DataSource dataSource() {
        // Configure and return the DataSource (e.g., HikariDataSource, BasicDataSource, etc.)
        // For example, using HikariCP:
        HikariDataSource dataSource = new HikariDataSource();
        dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/money_transfer_system_db");
        dataSource.setUsername("root");
        dataSource.setPassword("yourpassword");
        dataSource.setDriverClassName("com.mysql.cj.jdbc.Driver");
        dataSource.setMaximumPoolSize(10);
        return dataSource;
    }

    @Bean
    public JdbcTemplate jdbcTemplate(DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

    @Bean
    public AccountRepository jdbcAccountRepository() {
        return new JdbcAccountRepository(jdbcTemplate(dataSource()));
    }

    @Bean
    public TransferService transferService() {
        return new UpiTransferService(jdbcAccountRepository());
    }
    
}
