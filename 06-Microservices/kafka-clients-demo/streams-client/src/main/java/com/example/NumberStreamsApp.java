package com.example;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;

import java.util.Properties;

public class NumberStreamsApp {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "number-splitter-app");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.StringSerde.class);
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.StringSerde.class);

        StreamsBuilder builder = new StreamsBuilder();
        KStream<String, String> source = 
        builder.stream("number-events")
        .peek((key, value) -> System.out.printf("Received number: %s%n", value));

        source.filter((key, value) -> Integer.parseInt(value) % 2 == 0)
                .to("even-numbers");

        source.filter((key, value) -> Integer.parseInt(value) % 2 != 0)
                .to("odd-numbers");

        KafkaStreams streams = new KafkaStreams(builder.build(), props);

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));

        streams.start();
        System.out.println("Number Streams app started. Splitting number-events into odd-numbers and even-numbers.");
    }
}
