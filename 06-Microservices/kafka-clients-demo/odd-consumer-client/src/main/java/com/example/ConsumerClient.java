package com.example;

import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.errors.WakeupException;

public class ConsumerClient {
    public static void main(String[] args) {
        java.util.Properties props = new java.util.Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("group.id", "odd-consumer-group");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("auto.offset.reset", "earliest");

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                System.out.println("Shutdown hook triggered. Waking up odd consumer...");
                consumer.wakeup();
            }));

            consumer.subscribe(java.util.List.of("odd-numbers"));

            try {
                while (true) {
                    ConsumerRecords<String, String> records = consumer.poll(java.time.Duration.ofMillis(100));
                    records.forEach(record ->
                            System.out.printf("ODD consumer received number: %s%n", record.value()));
                }
            } catch (WakeupException e) {
                System.out.println("Odd consumer shutdown requested.");
            }
        }
    }
}
