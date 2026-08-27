package com.example;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.util.Properties;

public class ProducerClient {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("acks", "all");
        props.put("retries", Integer.MAX_VALUE);
        props.put("retry.backoff.ms", 100);
        props.put("delivery.timeout.ms", 120000);
        props.put("linger.ms", 0);
        props.put("compression.type", "snappy");
        props.put("buffer.memory", 33554432);
        props.put("max.block.ms", 60000);
        props.put("request.timeout.ms", 30000);

        try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
            String topic = "number-events";

            for (int i = 1; i <= Integer.MAX_VALUE; i++) {
                String value = String.valueOf(i);
                ProducerRecord<String, String> record = new ProducerRecord<>(topic, value, value);
                producer.send(record, (metadata, exception) -> {
                    if (exception != null) {
                        exception.printStackTrace();
                    } else {
                        System.out.printf("Sent number %s to partition %d with offset %d%n",
                                value, metadata.partition(), metadata.offset());
                    }
                });

                try {
                    Thread.sleep(0);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    System.out.println("Producer interrupted while sleeping.");
                    break;
                }
            }
        }
    }
}